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

# Import own modules
from . import IndexerObject
from .Aliases import Aliases

class AliasPlugin(IndexerObject.IndexerObject):
    """
    Class that implements the extraction aliases from the aliases.txt file
    """
    
    def __init__(self, config, indexer):
        """
        Class constructor
        Args:
          None
        """
        self.config = config
        self.indexer = indexer
        self.aliasesFile = os.path.join(self.config.config["appDataDir"], "aliases.txt")

    def fetchApps(self):
        """
        Method to fetch aliases from aliases.txt file
        Args:
          None

        Returns: list of aliases
        """

        appList = []
        aliases = Aliases(self.aliasesFile)
        data = aliases.loadAliases()

        for alias in data:
            appList.append([alias[0], alias[1:], True])
        
        return appList

    def default(self):
        """
        Method that overides default behaviour. This plugin
        should be loaded by default
        Args:
          None

        Returns: True
        """
        return True


    def getDescription(self):
        """
        Method that returns a short descriptive string
        Args:
          None

        Returns: A string describing the plugin
        """
        return "When activated this plugin will index\n" \
               + "the aliases.txt file present on the system."