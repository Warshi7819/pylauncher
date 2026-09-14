###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Kjetil Jacobsen                   # 
# Date        : 20:10 05.09.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import sys
import os

# Import pywin32 modules
from win32com.shell import shell
import pythoncom

# Import wxpython modules
import wx

# Import own modules
from GuiUtils import openAsBitmap

def convertIconToBitmap(icon):
    try:
        bmp = wx.Bitmap(icon)
    except Exception:
        size = icon.GetSize()
        bmp = wx.Bitmap(size)
        dc = wx.MemoryDC(bmp)
        dc.DrawIcon(icon, 0, 0)
        dc.SelectObject(wx.NullBitmap)
    if bmp.GetWidth() != 16 or bmp.GetHeight() != 16:
        img = bmp.ConvertToImage()
        img.Rescale(16, 16)
        bmp = wx.Bitmap(img)
    return bmp

def getIcon(filename, _seen=None):
    """
    Function to fetch matching icons for files and extensions
    Args:
      extension = A file extension e.g. '.jpg' or a filepath

    Returns: The image as an icon
    """


    # When an exe file does not have an icon the IconFromLocation throws a
    # super ugly log message which is displayed in a pop up box for god knows
    # what reason since it should really suffice to check icon.IsOk() to see
    # if the operation was successfull or not. Therefore directing all log
    # messages to "dev/null"
    nullLog = wx.LogNull()
      
    filename = filename.lower()

    # Guard against infinite recursion
    if _seen is None:
        _seen = set()
    if filename in _seen:
        return wx.Bitmap(16, 16)
    _seen.add(filename)

    # http == .url
    if filename.startswith("http"):
        return getIcon(".url", _seen)
  
    # If it's a lnk file we need to parse it
    if filename.endswith(".lnk"):
        try:
            sh = pythoncom.CoCreateInstance(shell.CLSID_ShellLink,
                                            None, pythoncom.CLSCTX_INPROC_SERVER,
                                            shell.IID_IShellLink)
         
            # Get an IPersist interface
            persist = sh.QueryInterface(pythoncom.IID_IPersistFile)

            persist.Load(filename)
         
            # Get the data
            return getIcon(sh.GetPath(shell.SLGP_RAWPATH)[0], _seen)
        except Exception:
            return wx.Bitmap(16, 16)


    # Can't handle .exe so transforming that one to .com instead..
    if filename == ".exe":
        return getIcon(".com", _seen)

    if filename.endswith(".exe"):
        il = wx.IconLocation(filename, 0)
        icon = wx.Icon(il)
        if icon.IsOk():
            return convertIconToBitmap(icon)
        else:
            return getIcon(".com", _seen)

    r, e = os.path.splitext(filename)
    if e:
        ft =  wx.TheMimeTypesManager.GetFileTypeFromExtension(e)
        if ft: 
            icon = ft.GetIcon()
            if icon != None and icon.IsOk():
                return convertIconToBitmap(icon)

    # Not there yet...
    import mimetypes
    ext = mimetypes.guess_extension(e)
    if ext:
        ft = wx.TheMimeTypesManager.GetFileTypeFromMimeType(ext[0])
        if ft:
            icon = ft.GetIcon()
            if icon.IsOk():
                return convertIconToBitmap(icon)

    return wx.Bitmap(16, 16)


    
