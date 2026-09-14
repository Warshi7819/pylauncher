###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import os.path

# Import wxpython modules
import wx

# Import own modules
from OwnConstants import *
from ShellFolders import fetchShellFolders
from configparser import ConfigParser
from PickleUtils import loadFromFile, dumpToFile
from FileUtils import copyFile
import os.path
import os

class Config:
    """
    Class implementing the configuration methods
    """

    def __init__(self):
        """
        Class constructor
        """
        shellFolders = fetchShellFolders()
        appDataDir = os.path.join(shellFolders["AppData"][0], "AL")
        self.filename = os.path.join(appDataDir, "config.dat")

        # Figure out the application data directory and create
        # it if it doesn't already exist
        if not os.path.exists(appDataDir):
            os.mkdir(appDataDir)
            # For backwards comptatibility we also copy the current
            # .dat files if they exist
            if os.path.isfile("config.dat"):
                copyFile("config.dat", os.path.join(appDataDir, "config.dat"))

            if os.path.isfile("applist.dat"):
                copyFile("applist.dat",
                         os.path.join(appDataDir, "applist.dat"))

            if os.path.isfile("history.dat"):
                copyFile("history.dat",
                         os.path.join(appDataDir, "history.dat"))

        # Load config
        self.config = self.loadConfig()
        self.config["appDataDir"] = appDataDir
        
        # Hold on to shellfolders
        self.config["shellfolders"] = shellFolders 

        # Ensure backwards compatibility when introducing plugins
        if "plugins" not in self.config:
            self.config["plugins"] = {}
            self.config["plugins"]["index"] = {}
            self.config["plugins"]["search"] = {}

        # Ensure backwards compatibility when introducing APPLIST_VERSION and
        # HISTORY_VERSION
        if not "appListVersion" in self.config:
            self.config["appListVersion"] = None
            
        if not "historyVersion" in self.config:
            self.config["historyVersion"] = None

    def loadConfig(self):
        """
        Method used to load the config
        Args:
          filename = The filename of the config file

        Returns: Dictionary containing the parsed config
        """

        config = loadFromFile(self.filename)
        
        if not config:
            # Failed loading config
            return self.defaultConfig()
        else:
            # Loading of config successfull
            # Now we have to test if it is compatible with
            # the current AL version
            if not "version" in config:
                return self.defaultConfig()

            if not config["version"] == CONFIG_VERSION:
                return self.defaultConfig()

            return config


    def saveConfig(self):
        """
        Method to save current config to file
        Args:
          None

        Returns: None
        """
        dumpToFile(self.config, self.filename)
        

    def getPath(self, key):
        return self.config["directories"][key][0][0]

    def addItem(self, key, path, exts, edit):
        
        if not key:
            return "Please choose a name for this entry"
        if not path:
            return "Please choose a directory"
        if len(exts) == 0:
            return "Please choose file extensions!"
                
        if edit != None:
            # We are editing an existing item.
            # Test if the name has changed
            if key != edit:
                if key in self.config["directories"]:
                    return "The new name of this entry already\n" \
                           + "exists. Please choose a different one"
                else:
                    item = []
                    item.append([path, 1])
                    item.append(self.config["directories"][edit][1])
                    item.append(exts)
                    self.config["directories"][key] = item

                    # Del old entry
                    del self.config["directories"][edit]
                
            else:
                self.config["directories"][key][0][0] = path
                self.config["directories"][key][2] = exts

        else:
            if key in self.config["directories"]:
                return "The name of this entry already exists.\n" \
                       + "Please choose a new name."
            else:
                item = []
                item.append([path, 1])
                item.append(True)
                item.append(exts)
                self.config["directories"][key] = item

        # All ok
        return True


    def defaultConfig(self):
        config = {}
        config["directories"] = {}

        # Append default directories to index. We need to read
        # the registry to figure out the path to e.g start menu,
        # my documents, favorites and so on..
        shellFolders = fetchShellFolders()

        if not shellFolders:
            raise Exception("Failed reading registry... Aborting")

        # Adding directories that should be indexed by default

        config["directories"]["Favorites"] = [shellFolders["Favorites"],
                                              True, ["url"]]
        config["directories"]["Start Menu (user)"] = [shellFolders["Start Menu"],
                                                      True, ["lnk"]]
        config["directories"]["Start Menu (common)"] = [shellFolders["Common Start Menu"],
                                                        True, ["lnk"]]

        # Add quick launch bar to index
        tmp = shellFolders["AppData"]
        tmp[0] = os.path.join(tmp[0], "Microsoft\\Internet Explorer\\Quick Launch")
        config["directories"]["Quick Launch Bar"] = [tmp, True, ["lnk"]]
        
        # Adding directories that has to be enabled before they are indexed
        config["directories"]["My Documents"] = [shellFolders["Personal"],
                                                 False, ["*"]]

        config["ontop"] = False
        config["alwaysSearchWindow"] = False 
        config["hotkeys"] = [wx.MOD_ALT, 32]

        # Show wizard by default
        config["wizard"] = True

        # Set config version
        config["version"] = CONFIG_VERSION

        config["appListVersion"] = APPLIST_VERSION
        config["historyVersion"] = HISTORY_VERSION
        
        # Prepare for plugins
        config["plugins"] = {}
        config["plugins"]["index"] = {}
        config["plugins"]["search"] = {}
 
        return config