###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import queue
import time
import threading 

# Import wxpython modules
import wx

# Import own methods
from SuffixTree import Tree
from OwnConstants import *
from AppList import AppList
from ReindexerThread import ReindexerThread
from Logger import Logger

class Indexer(threading.Thread):
    """
    Class that handles the indexing, and search requests
    """

    def __init__(self, parent, queryQueue, config):
        """
        The class constructor
        Args:
          parent = The parent window
          queryQueue = The query queue
          config = The Al configuration
        """
        
        # Create and populate tree
        threading.Thread.__init__(self)
        self.parent = parent
        self.READY = False
        self.RUNNING = True
        self.STOPPED = False
        self.queryQueue = queryQueue
        self.matches = []
        self.mapping = {}
        self.config = config
        self.log = Logger()
        
        # Start reindexer thread
        self.reindexerThread = ReindexerThread(self)
        self.reindexerThread.start()


    def run(self):
        """
        The thread body
        Args:
          None

        Returns: None
        """

        # Load application list
        self.appList = AppList(self.config, self)

        # Create case insensitive suffix tree
        # and populate it
        self.tree = Tree(False)
        self.populate()

        
        while(self.RUNNING):
            # Search thread
            try:
                searchString = self.queryQueue.get(True, 0.5)
            except queue.Empty as e:
                continue

            if searchString.find(":") > 0:
                # Special plugin search, aborting
                evt = InsertApplication(item=[None, searchString, None],
                                        key=-2)
                wx.PostEvent(self.parent, evt)
                continue
            
            # Clear list by passing it the key -1
            self.mapping = {}
            evt = InsertApplication(item=[0, 0, 0], key=-1)
            wx.PostEvent(self.parent, evt)
                        
            # Test that index is ready to receive search
            if self.isReady:
                # Perform search
                result = self.tree.search(searchString)
                startChar = searchString[0:1]
                self.matches = self.appList.rank(result, startChar)

                # Start populating list in GUI
                for i in range(0, len(self.matches)):
                    # Ensure that this query is not overridden by
                    # a newer one and that the app is still running
                    if self.queryQueue.empty() and self.RUNNING:
                        # Send update event to the GUI
                        realKey = int(self.matches[i])
                        self.mapping[i] = realKey
                        app = self.appList.appList[realKey]
                        
                        evt = InsertApplication(item = app,
                                                key = i)
                        wx.PostEvent(self.parent, evt)
                    else:
                        break

                    # Reduce the speed we send events
                    # based on how many items we already have
                    # sent to the Gui. This is done since the loading
                    # of the icons would overwhelm the app if no throtteling
                    # is done..
                    if i > 10:
                        # Delay half a second before sending new event
                        if i > 40:
                            # If we have already sent over 40 events
                            # for this query deleay 1 second before
                            # sending the next event
                            if self.queryQueue.empty():
                                time.sleep(0.5)
                        if self.queryQueue.empty():
                            time.sleep(0.5)
            else:
                pass

        self.STOPPED = True


    def reindex(self, force=False):
        """
        Method to schedule a reindex of the data. If force is true we will
        schedule a forced reindex. That means that we should not wait until
        the system is idle
        
        Args:
          force [BOOLEAN]: Wheter or not we should force a immidiate reindex or
                           if we should wait until the system is idle before
                           we trigger one

        Returns: None
        """
        self.log.info("Requesting reindex. Using force: %s" % force)
        self.reindexerThread.requestReindex(force)
        

    def isReady(self):
        """
        Method to test if indexing is finished and we are able to
        perform a search through all applications
        Args:
          None

        Returns: True if index is ready, False otherwise
        """
        if self.READY:
            return True
        else:
            return False


    def populate(self):
        """
        Method to populate tree
        Args:
          None
          
        Returns: None
        """
        for i in range(0, len(self.appList.appList)):
            # Index app name into suffix tree
            appName = self.appList.appList[i][0]
            self.tree.addString(appName, "%s" % i)

            # We also split the app name into words
            # and index first char in each word.
            # E.g. "microsoft word" becomes: "mw"
            words = appName.strip().strip("\n").split()
            if len(words)>1:
                initials = ""
                for word in words:
                    initials += word[0]

                self.tree.addString(initials, "%s" % i)


        # The index is now ready to be used
        self.READY = True

    def getExecutionString(self, index, startChar=""):
        """
        Method to get the string to execute given an indes
        Args:
          index = The index of the program in the applist

        Returns: The command to execute (string)
        """
        # Map from list to correct application
        key = self.mapping[index]
        if self.appList.appList[key][2]:
            execString = " ".join(self.appList.appList[key][1])
        else:
            execString = self.appList.appList[key][1]

        # Update execution history
        if not execString in self.appList.history:
            self.appList.history[execString] = {}

        if not startChar in self.appList.history[execString]:
            self.appList.history[execString][startChar] = 1
        else:
            self.appList.history[execString][startChar] += 1

        
        return (self.appList.appList[key][1],
                self.appList.appList[key][2])
    
    def stop(self):
        """
        Method to stop the indexer and reindexer-thread. The method bussy waits
        until the indexer has shutdown completely
        Args:
          None

        Returns: None
        """
        self.log.info("Stopping indexer")
        self.RUNNING = False

        self.log.info("Stopping indexer plugins")
        self.appList.stopIndexerPlugins()

        self.log.info("Stopping reindexing thread")
        self.reindexerThread.stop()
        while self.reindexerThread.isRunning():
            time.sleep(0.5)
        
        # Wait until the current indexing is done so that we save
        # the correct applist
        self.log.info("Waiting until ongoing reindex has finished.")
        while(not self.READY):
            time.sleep(0.2)

        self.log.info("Saving application list and history")
        self.appList.saveAppList()
        self.appList.saveHistory()

        while(not self.STOPPED):
            time.sleep(0.5)

        self.log.info("Indexer has been stopped")




    