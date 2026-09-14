###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################


# Import own modules
from . import IndexerObject
from .FileTraverser import FileTraverser
from Logger import Logger
from DirectoryWatcher import DirectoryWatcher

class DirectoryPlugin(IndexerObject.IndexerObject):
    """
    Class that implements the directory plugin
    """

    def __init__(self, config, indexer):
        """
        Class constructor
        """
        
        self.config = config
        self.indexer = indexer
        self.log = Logger()
        self.watcher = None
        
        # Initialize the watcher
        self.reinitializeWatcher()
        

    def reinitializeWatcher(self):
        """
        Method to reinitialize the watcher
        Args:
          None
          
        Returns: None
        """
        
        self.log.info("Reinitializing watchers")
        if self.watcher != None:
            # Stopping current watcher
            self.log.info("Stopping current watcher")
            self.watcher.stop()
            self.watcher.closeListeners()
            self.log.info("Stopped")
                        
        self.watcher = DirectoryWatcher(self.dirChanged)
        self.watcher.start()
       
        directories = self.config.config["directories"]
        for watchDir in directories:
            path = directories[watchDir][0][0]
            self.watcher.addListener(watchDir, path)
        
        self.log.info("Done reinitializing watchers")


    def dirChanged(self):
        """
        Method to handle call backs from the directory watcher
        Args:
          None
          
        Returns: None
        """
        
        self.log.info("Dir changed, request reindex")
        # Request idle reindex
        self.indexer.reindex(False)


    def fetchApps(self):
        """
        Method to fetch apps from the directories given
        Args:
          directories = The list of directories we want to index

        Returns: None
        """
        
        directories = self.config.config["directories"]

        appList = []
        
        # traverse disk
        filetraverser = FileTraverser()
        for dir in directories:
            if directories[dir][1]:
                path = directories[dir][0][0]
                filterSpec = directories[dir][2]
                apps = filetraverser.traverse(path, filterSpec)
                for app in apps:
                    appList.append([app[0], app[1], False])

        self.reinitializeWatcher()
        return appList
    
    
    def stop(self):
        """
        Method to stop the directory watcher thread
        Args:
          None
          
        Returns: None
        """
        
        self.watcher.stop()
        self.watcher.closeListeners()