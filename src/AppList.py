###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Standard modules
from os.path import join

# Own modules
from PickleUtils import loadFromFile, dumpToFile
from plugins.index import *
from GuessEncoding import GuessEncoding
from OwnConstants import *
from Logger import Logger

class AppList:
    """
    Class that implements the methods to save, load
    and modify the application list
    """
    
    def __init__(self, config, indexer):
        """
        Class constructor
        Args:
          config = AL's config
          indexer = The indexer object
        """
        # Hold on to config
        self.config = config
        self.logger = Logger()
        self.guessEnc = GuessEncoding()

        # Load all indexer plugins
        self.plugins = {}
        for plugin in indexerPlugins:
            self.plugins[plugin] = eval("%s(self.config, indexer)" % plugin)
        
        # List holding available applications
        # App = [indexString, What to execute(path)]
        self.appList = None
        self.loadAppList()
        
        # dictionary that holds the execution history
        # This is used for ranking results
        self.history = self.loadHistory()


    def stopIndexerPlugins(self):
        """
        Method to stop all indexer plugins
        Args:
          None
          
        Returns: None
        """
        for plugin in self.plugins.keys():
            self.plugins[plugin].stop()


    def repopulate(self):
        """
        Method to repopulate the application list from
        both directories, alias.txt file and plugins
        Args: None

        Returns: None
        """
        # Clear application list

        appList = []

        for plugin in self.plugins.keys():
            # Load data from plugins that are enabled except for
            # the special DirectoryPlugin
            if plugin != "DirectoryPlugin":
                # Test if plugin is known to config, if not figure out
                # if this should be loaded by default or not
                if plugin not in self.config.config["plugins"]["index"]:
                    if self.plugins[plugin].default():
                        self.config.config["plugins"]["index"][plugin] = True
                    else:
                        self.config.config["plugins"]["index"][plugin] = False
                        
                # If plugin is enabled, load data from it
                if self.config.config["plugins"]["index"][plugin]:
                    # load the data
                    appList.extend(self.plugins[plugin].fetchApps())


        # Load directories
        appList.extend(self.plugins["DirectoryPlugin"].fetchApps())
        
        # Traverse through results and ensure that none of them uses the reserved
        # keyword ":". Also convert the app "path" to unicode
        newList = []
        for i in range(0, len(appList)):
            try:
                appList[i][0] = appList[i][0].replace(":", ">")
                appList[i][0] = self.guessEnc.convertToUnicode(appList[i][0])
            except Exception as e:
                self.logger.warning("Application skipped because of unicode convert error:")
                self.logger.warning(appList[i][0])
                continue
            
            newList.append(appList[i])

        self.appList = newList

    def loadAppList(self):
        """
        Method to load the application list from file
        Args:
          None

        Returns: [LIST] The loaded data or an empty list if it fails
        """
        tmp = loadFromFile(join(self.config.config["appDataDir"], "applist.dat"))
        
        # Test version
        if tmp == None:
            # No data, force repopulate
            self.repopulate()
        else:
            if self.config.config["appListVersion"] == None or self.config.config["appListVersion"] != APPLIST_VERSION:
                # New config version, repopulate and save new version
                self.logger.info("New applist version. Repopulate the applist ")
                self.repopulate()
                self.config.config["appListVersion"] = APPLIST_VERSION
            else:
                self.appList = tmp


    def saveAppList(self):
        """
        Method to dump the application list to file
        Args:
          None

        Returns: None
        """
        dumpToFile(self.appList, join(self.config.config["appDataDir"], "applist.dat"))


    def loadHistory(self):
        """
        Method to load execution history from file
        Args:
          None

        Returns: [DICT] The loaded information or an empty dictionary if an
                 error occures
        """
        tmp = loadFromFile(join(self.config.config["appDataDir"], "history.dat"))
        if tmp == None:
            return {}
        else:
            if self.config.config["historyVersion"] == None or self.config.config["historyVersion"] != HISTORY_VERSION:
                self.logger.info("New history version, nuke old history..")
                self.config.config["historyVersion"] = HISTORY_VERSION
                return {}
            return tmp


    def saveHistory(self):
        """
        Method to save execution history to file
        Args:
          None

        Returns: None
        """
        dumpToFile(self.history, join(self.config.config["appDataDir"], "history.dat"))


    def rank(self, resultSet, startChar = ""):
        """
        Method to extract results from index based on list indexes.
        Also sort the applications extracted based on how many
        times they have been executed (rank)
        Args:
          resultSet = The initial resultset from the suffix tree
                      search
          startChar = The starting character of the search

        Returns: [LIST] A subset of the appIndex that matches the original
                 search term. And that also is sorted based on
                 the execution history of each application
        """

        rankDict = {}
        for key in resultSet:
            if self.appList[int(key)][2]:
                execString = " ".join(self.appList[int(key)][1])
            else:
                execString = self.appList[int(key)][1]
                
            if execString not in self.history:
                rank = 0
            else:
                if startChar not in self.history[execString]:
                    rank = 0
                else:
                    rank = self.history[execString][startChar]

            if rank not in rankDict:
                rankDict[rank] = []

            rankDict[rank].append(key)

            
        rankDictKeys = sorted(rankDict.keys(), reverse=True)

        resultSet = []
        for rankKey in rankDictKeys:
            resultSet.extend(rankDict[rankKey])

        del rankDict
        del rankDictKeys
        return resultSet