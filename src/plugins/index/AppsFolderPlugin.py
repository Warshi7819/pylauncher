###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 09.29.2026                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import ctypes
import ctypes.wintypes as wintypes
import os
import glob
import re
import xml.etree.ElementTree as ET

# Import 3rdparty modules
import wx
import win32com.client

# Import own modules
from . import IndexerObject
from Logger import Logger

# shell:AppsFolder prefix for launching UWP apps
APPS_FOLDER_PREFIX = "shell:AppsFolder\\"

# Module-level icon cache for UWP apps, keyed by exec path
appsFolderIconCache = {}

# Package lookup cache: family_name -> package_path
_packagePathCache = {}

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

_kernel32.GetPackagesByPackageFamily.argtypes = [
    wintypes.LPCWSTR,
    ctypes.POINTER(wintypes.UINT),
    ctypes.POINTER(wintypes.LPWSTR),
    ctypes.POINTER(wintypes.UINT),
    wintypes.LPWSTR
]
_kernel32.GetPackagesByPackageFamily.restype = wintypes.LONG

_kernel32.GetPackagePathByFullName.argtypes = [
    wintypes.LPCWSTR,
    ctypes.POINTER(wintypes.UINT),
    wintypes.LPWSTR
]
_kernel32.GetPackagePathByFullName.restype = wintypes.LONG

ERROR_INSUFFICIENT_BUFFER = 0x7A
ERROR_SUCCESS = 0x0

TARGETSIZE_REGEX = re.compile(r'targetsize-([0-9]+)')


class AppsFolderPlugin(IndexerObject.IndexerObject):
    """
    Class that indexes apps from the Windows shell AppsFolder.
    This includes UWP/Store apps like Windows Terminal, Calculator, etc.
    """

    def __init__(self, config, indexer):
        """
        Class constructor.
        Args:
          config = The application config
          indexer = The indexer object
        """
        self.config = config
        self.indexer = indexer
        self.log = Logger()

    def fetchApps(self):
        """
        Method to fetch apps from shell:AppsFolder.
        Args: None

        Returns: [LIST] List of applications found
        """
        import traceback
        try:
            return self.enumerateAppsFolder()
        except Exception as e:
            self.log.warning("AppsFolder enumeration failed: %s" % str(e))
            traceback.print_exc()
            return []

    def default(self):
        """
        Method that overrides default behaviour. This plugin
        should be loaded by default.
        Args:
          None

        Returns: [BOOLEAN] True
        """
        return True

    def getDescription(self):
        """
        Method that returns a short descriptive string
        about the plugin.
        Args:
          None

        Returns: [STRING] A string describing the plugin
        """
        return "When activated this plugin will index all\n" \
               + "installed apps from the Windows AppsFolder\n" \
               + "including UWP/Store apps like Terminal"

    def enumerateAppsFolder(self):
        """
        Method to enumerate all apps from shell:AppsFolder
        using Shell.Application COM automation.
        Args: None

        Returns: [LIST] List of [name, path, isAlias] entries
        """
        apps = []
        skipped = 0

        import pythoncom
        pythoncom.CoInitialize()

        shellApp = win32com.client.Dispatch("Shell.Application")
        folder = shellApp.NameSpace("shell:AppsFolder")
        items = folder.Items()
        total = items.Count

        for i in range(total):
            item = items.Item(i)
            if item == None:
                continue

            name = item.Name
            path = item.Path

            # Filter out web shortcuts
            skip = path.startswith("http://") \
                or path.startswith("https://") \
                or path.lower().endswith(".html") \
                or path.lower().endswith(".htm")

            if skip:
                skipped += 1
            elif name == "":
                skipped += 1
            elif path == "":
                skipped += 1
            else:
                # Build the exec path
                # For UWP apps path is an AppUserModelID (no backslash)
                # For regular apps path is a full file path
                if '\\' in path:
                    execPath = path
                else:
                    execPath = "%s%s" % (APPS_FOLDER_PREFIX, path)

                # Extract icon
                iconBitmap = self.__extractIcon(path)
                if iconBitmap != None:
                    appsFolderIconCache[execPath.lower()] = iconBitmap

                apps.append([name, execPath, False])

        self.log.info("AppsFolder indexed %d applications, skipped %d" % (len(apps), skipped))
        return apps

    def __extractIcon(self, path):
        """
        Method to extract an icon for an app.
        For regular apps (file paths), uses SHGetFileInfo on the exe.
        For UWP apps (AppUserModelID), parses AppXManifest.xml for the
        logo file (approach from amnweb/icon-extractor).
        Args:
          path = The item path (file path or AppUserModelID)

        Returns: [BITMAP] The icon as a bitmap, or None
        """
        try:
            nullLog = wx.LogNull()

            # Regular apps: extract icon from the exe
            if '\\' in path:
                return self.__getIconFromExe(path)

            # UWP apps: get icon from AppXManifest.xml
            return self.__getIconFromManifest(path)

        except Exception:
            return None

    def __getIconFromExe(self, exePath):
        """
        Method to extract an icon from an exe file.
        Args:
          exePath = The full path to the exe

        Returns: [BITMAP] The icon as a bitmap, or None
        """
        try:
            shell32 = ctypes.windll.shell32
            user32 = ctypes.windll.user32

            class _SHFILEINFO(ctypes.Structure):
                _fields_ = [
                    ("hIcon", wintypes.HANDLE),
                    ("iIcon", ctypes.c_int),
                    ("dwAttributes", wintypes.DWORD),
                    ("szDisplayName", ctypes.c_wchar * 260),
                    ("szTypeName", ctypes.c_wchar * 80),
                ]

            shell32.SHGetFileInfoW.argtypes = [ctypes.c_void_p, wintypes.DWORD,
                                                ctypes.POINTER(_SHFILEINFO), wintypes.UINT,
                                                wintypes.UINT]
            shell32.SHGetFileInfoW.restype = wintypes.UINT

            info = _SHFILEINFO()
            flags = 0x100  # SHGFI_ICON
            shell32.SHGetFileInfoW(exePath, 0x80, ctypes.byref(info),
                                    ctypes.sizeof(info), flags)

            if info.hIcon == None or info.hIcon == 0:
                return None

            icon = wx.Icon()
            icon.CreateFromHICON(info.hIcon)

            if icon.IsOk():
                bmp = wx.Bitmap(32, 32)
                dc = wx.MemoryDC(bmp)
                dc.DrawIcon(icon, 0, 0)
                dc.SelectObject(wx.NullBitmap)
                user32.DestroyIcon(info.hIcon)

                if bmp.IsOk():
                    if bmp.GetWidth() != 16 or bmp.GetHeight() != 16:
                        img = bmp.ConvertToImage()
                        img.Rescale(16, 16)
                        bmp = wx.Bitmap(img)
                    return bmp

            user32.DestroyIcon(info.hIcon)
            return None

        except Exception:
            return None

    def __getIconFromManifest(self, appId):
        """
        Method to extract an icon for a UWP app by parsing its
        AppXManifest.xml for the logo file. (Approach from
        amnweb/icon-extractor.)
        Args:
          appId = The AppUserModelID (e.g. Microsoft.WindowsTerminal_8wekyb3d8bbwe!App)

        Returns: [BITMAP] The icon as a bitmap, or None
        """
        try:
            # Get family name from AppUserModelID
            # Format: PackageFamilyName!EntryPoint
            familyName = appId.split("!")[0]

            # Get package path
            packagePath = self.__getPackagePath(familyName)
            if packagePath == None:
                return None

            # Parse AppXManifest.xml for the logo
            iconPath = self.__getIconPathFromManifest(packagePath)
            if iconPath == None:
                return None

            # Load the image
            bmp = wx.Bitmap(iconPath, wx.BITMAP_TYPE_ANY)
            if bmp.IsOk():
                if bmp.GetWidth() != 16 or bmp.GetHeight() != 16:
                    img = bmp.ConvertToImage()
                    img.Rescale(16, 16)
                    bmp = wx.Bitmap(img)
                return bmp

            return None

        except Exception:
            return None

    def __getPackagePath(self, familyName):
        """
        Method to find the package install path for a UWP app family.
        Args:
          familyName = The package family name

        Returns: [STRING] The package path, or None
        """
        if familyName in _packagePathCache:
            return _packagePathCache[familyName]

        try:
            # GetPackagesByPackageFamily to find full names
            count = wintypes.UINT(0)
            bufferLength = wintypes.UINT(0)
            ret = _kernel32.GetPackagesByPackageFamily(
                familyName, ctypes.byref(count), None,
                ctypes.byref(bufferLength), None)

            if ret != ERROR_INSUFFICIENT_BUFFER or count.value == 0:
                _packagePathCache[familyName] = None
                return None

            fullNames = (wintypes.LPWSTR * count.value)()
            buffer = ctypes.create_unicode_buffer(bufferLength.value)

            ret = _kernel32.GetPackagesByPackageFamily(
                familyName, ctypes.byref(count), fullNames,
                ctypes.byref(bufferLength), buffer)

            if ret != ERROR_SUCCESS or count.value == 0:
                _packagePathCache[familyName] = None
                return None

            # Use the first full name
            fullName = fullNames[0]
            if fullName == None:
                _packagePathCache[familyName] = None
                return None

            # GetPackagePathByFullName
            length = wintypes.UINT(0)
            ret = _kernel32.GetPackagePathByFullName(
                fullName, ctypes.byref(length), None)
            if ret != ERROR_INSUFFICIENT_BUFFER:
                _packagePathCache[familyName] = None
                return None

            path = ctypes.create_unicode_buffer(length.value)
            ret = _kernel32.GetPackagePathByFullName(
                fullName, ctypes.byref(length), path)
            if ret != ERROR_SUCCESS:
                _packagePathCache[familyName] = None
                return None

            _packagePathCache[familyName] = path.value
            return path.value

        except Exception:
            _packagePathCache[familyName] = None
            return None

    def __getIconPathFromManifest(self, packagePath):
        """
        Method to find the icon file path from a UWP package's
        AppXManifest.xml. Looks for Square44x44Logo and picks the
        best targetsize variant.
        Args:
          packagePath = The package install path

        Returns: [STRING] The icon file path, or None
        """
        manifestPath = os.path.join(packagePath, "AppXManifest.xml")
        if not os.path.exists(manifestPath):
            return None

        root = ET.parse(manifestPath)
        velement = root.find(".//VisualElements")
        if velement == None:
            velement = root.find(
                ".//{http://schemas.microsoft.com/appx/manifest/uap/windows10}VisualElements")
        if velement == None:
            return None

        if "Square44x44Logo" not in velement.attrib:
            return None

        logoFile = velement.attrib["Square44x44Logo"]

        # Glob for the actual image file (with targetsize-* qualifiers)
        logofileStem = os.path.splitext(os.path.basename(logoFile))[0]
        logofileExt = os.path.splitext(logoFile)[1]
        logofileDir = os.path.dirname(logoFile)

        logopattern = os.path.join(logofileDir, "**",
                                    logofileStem + "*" + logofileExt)
        logofiles = glob.glob(logopattern, recursive=True,
                              root_dir=packagePath)
        logofiles = [x.lower() for x in logofiles]

        if len(logofiles) == 0:
            return None

        # Sort by target size: prefer 48 or closest bigger
        def targetSizeSort(s):
            m = TARGETSIZE_REGEX.search(s)
            if m:
                size = int(m.group(1))
                if size < 48:
                    return 5000 - size
                return size - 48
            return 10000

        logofiles.sort(key=targetSizeSort)
        return os.path.join(packagePath, logofiles[0])
