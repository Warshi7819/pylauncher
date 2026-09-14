###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import threading
import queue

# Import own methods
from SuffixTree import Tree
from Logger import Logger
from DetectIdleTime import DetectIdleTime

REINDEX_IDLE = 1
REINDEX_NOW = 0

class ReindexerThread(threading.Thread):
    """
    Class that implements the reindexing thread
    """
    
    def __init__(self, parent):
        """
        Class constructor
        Args:
          parent = The indexer itself
        """
        threading.Thread.__init__(self)
        self.indexer = parent
        self.RUNNING = True
        self.STOP = False
        self.log = Logger()
        self.queue = queue.Queue(10)
                
        
    def requestReindex(self, force=False):
        """
        Method to request reindex
        Args:
          force [BOOLEAN]: Wheter or not if we should force an immediat 
                           reindex or wait until the machine is IDLE
        
        Returns: [Queue] The queue
        """
        if(force):
            self.queue.put(REINDEX_NOW)
        else:
            self.queue.put(REINDEX_IDLE)
    
        
    def run(self):
        """
        The body of the reindexer thread
        Args:
          None

        Returns: None
        """
        
        idleReindex = False
        forceReindex = False
        
        try:
            
            while not self.STOP:
            
                # Fetch queue event, timeout after one sec
                try:
                    reindexRequest = self.queue.get(True, 1)
                except queue.Empty as e:
                    # No reindex request available
                    reindexRequest = None
    
                
                if reindexRequest == REINDEX_IDLE:
                    idleReindex = True
                elif reindexRequest == REINDEX_NOW:
                    forceReindex = True
    
                
                # Test if we should execute a force index or a idle index
                if forceReindex:
                    if self.__reindex():
                        forceReindex = False
                elif idleReindex:
                    if self.__machineIsIdle():
                        if self.__reindex():
                            idleReindex = False

        except Exception as e:
            self.log.warning("Reindexer Thread crashed: %s" % e)


        self.RUNNING = False
            
          
    def __reindex(self):
        """
        Method that reindexes the suffix tree if no currently indexer is ready
        that is..
        Args: 
          None
          
        Returns [BOOLEAN]: True if new index was made False otherwise
        """
        try:
            if self.indexer.isReady():
                self.log.info("Starting reindex..")
                # Repopulate appList from disk and alias list
                self.indexer.appList.repopulate()
                    
                # Create new case insensitive suffix tree
                # and populate it
                self.indexer.tree = Tree(False)
                self.indexer.populate()
                self.log.info("Reindex completed.")
                return True
            
            else:
                return False    
        except Exception as e:
            self.log.error("Exception while reindexing: %s" % e)
        
        return False
    
    
    def __machineIsIdle(self):
        """
        Method to test if the machine has been idle for 10 minutes
        If so we can run reindex
        Args:
          None
          
        Returns: True if machine has been idle for 10 minutes, False otherwise
        """
        
        timeToBeat = 10*60
        
        detectIdle = DetectIdleTime()
        currentIdleTime = detectIdle.getIdleTime()
        
        try:
            if int(currentIdleTime) >= timeToBeat:
                return True
        except Exception as e:
            self.log.error("Exception while casting idle time to int: %s" % e)
        
            
    def stop(self):
        """
        Method used to signal thread to stop
        Args:
          None
          
        Returns: None
        """
        self.STOP = True
    
    
    def isRunning(self):
        """
        Method that returns the running state of the thread
        Args: 
          None
          
        Returns: [BOOLEAN] True or False to answer the question
        """
        return self.RUNNING