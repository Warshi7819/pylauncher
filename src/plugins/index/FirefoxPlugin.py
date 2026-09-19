###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import os
import os.path

# Import own modules
from . import IndexerObject

class FirefoxPlugin(IndexerObject.IndexerObject):
    """
    Class that implements the extraction of firefox bookmarks
    if firefox exists on the system
    """
    
    def __init__(self, config, indexer):
        """
        Class constructor
        Args:
          config = The application config
          indexer = The indexer object
        """
        self.config = config
        self.indexer = indexer
        self.firefoxDir = self.config.config["shellfolders"]["AppData"][0]
        self.firefoxDir = os.path.join(self.firefoxDir, "Mozilla", "Firefox",
                                       "Profiles")

    def fetchApps(self):
        """
        Method to parse Firefox's bookmarks.html file and
        return bookmarks
        Args:
          None

        Returns: [LIST] a list of link names and adresses
        """
        bookmarks = {}

        # Figure out the placement for the bookmarks.html file
        # if mozilla firefox indeed is installed that is
        if not os.path.isdir(self.firefoxDir):
            # Return empty list, dir does not exist
            return []
            
        else:
            # Find the bookmarks.html file. Gee I would be happy if
            # there was some way other than searching to find the
            # path to the profile directory
            bookmarkFiles = []
            dirs = os.listdir(self.firefoxDir)
            
            for dir in dirs:
                tmp = os.path.join(self.firefoxDir, dir)
                if os.path.isdir(tmp):
                    tmp = os.path.join(tmp, "bookmarks.html")
                    if os.path.isfile(tmp):
                        bookmarkFiles.append(tmp)

            # In the case that we find more than one profile
            # directory containing a bookmarks.html file we cannot
            # say which one is the current one. Therefore we traverse
            # them all
            for file in bookmarkFiles:
                fp = open(file, "r")
                lines = fp.readlines()

                # Extract anchors from file
                for line in lines:
                    line = line.strip().strip("\n").lower()
                    if line.find("href=") != -1:
                        startAddress = line.find("href=")+6
                        endAddress = line[startAddress:].find("\"") + startAddress
                        address = line[startAddress:endAddress]
                        endName = line.find("</a>")
                        startName = line[:endName].rfind(">")+1
                        linkName = line[startName:endName]
                        
                        # Filter out duplicates
                        if not address in bookmarks:
                            bookmarks[address]=linkName
                fp.close()


            appList = []
            for path in bookmarks.keys():
                name = bookmarks[path]
                appList.append([name, path, False])
                
            # Return extracted data
            return appList

    def default(self):
        """
        Method that overides default behaviour. This plugin
        should be loaded by default
        Args:
          None

        Returns: [BOOLEAN] True
        """
        return True

    def getDescription(self):
        """
        Method that returns a short descriptive string
        Args:
          None

        Returns: [STRING] A string describing the plugin
        """
        return "When activated this plugin will index\n" \
               + "the bookmarks firefox has if firefox is\n" \
               + "present on the system"