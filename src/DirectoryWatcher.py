###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Kjetil Jacobsen                   # 
# Date        : 20:10 05.09.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import threading
import os.path
import time

# Import win32 modules
import win32con
import win32event
import win32file

# Import own modules
from Logger import Logger


class DirectoryWatcher(threading.Thread):
    """
    Class that implements the functinality needed to listen for file changes
    in the given set of directories.
    """
    
    def __init__(self, callBackMethod):
        """
        Class constructor
        Args:
          None
        """
        
        threading.Thread.__init__(self)
        self.directories = {}
        self.listeners = {}
        self.reload = True
        self.pause = False
        self.paused = False
        self.running = True
        self.terminated = False
        
        self.callBackMethod = callBackMethod
        
        self.log = Logger()


    def addListener(self, name, directory, recursive=True):
        """
        Method to add a listener to a given directory
        Args:
          name [STRING] = The name of this listener
          directory [STRING] = The relative or absolute path to the dir
                               we want to watch
          recursive [BOOLEAN] = If we should watch sub dirs or not..

        Returns: None
        """
        
        fullPath = os.path.abspath(directory)
        watchSubDirs = 0
        
        if name not in self.listeners:
            if recursive:
                watchSubDirs = 1

            
            # Setup a change handle
            changeHandle = win32file.FindFirstChangeNotification(fullPath,
                                                                 watchSubDirs,
                                                                 win32con.FILE_NOTIFY_CHANGE_FILE_NAME
                                                                 )
            # Pause watcher while we update
            self.pauseWatcher()
            # update
            self.listeners[name] = changeHandle
            self.reload = True
            # unpause watcher thread 
            self.unpauseWatcher()
            
        else:
            self.log.warning("A directory listener with the name: %s is already registered.. Dropping this one." % name)
        

    def pauseWatcher(self):
        """
        Method to pause the watcher while we update its config
        Args:
          None

        Returns: None
        """
        self.pause = True
        while True:
            if self.paused:
                break

            time.sleep(0.500)


    def unpauseWatcher(self):
        """
        Method to unpause the watcher when the config is updated
        Args:
          None

        Returns: None
        """
        
        self.reload = True
        self.paused = False
        self.pause = False


    def stop(self):
        """
        Method to stop watchig dirs. Called when preparing for shutdown.
        Args:
          None

        Returns: None
        """
        
        self.running = False
        while not self.terminated:
            time.sleep(.200)


    def closeListeners(self):
        """
        Method to close the current open handels. Called when shutting down.
        Args:
          None

        Returns: None
        """
        
        listeners = self.listeners.keys()
        for key in listeners:
            win32file.FindCloseChangeNotification(self.listeners[key])


    def run(self):
        """
        The body of the thread that "polls" the handels for directory changes
        Args:
          None

        Returns: None
        """
        
        watchlist = []
        
        
        while self.running:
            if self.pause:
                self.paused=True
                time.sleep(0.200)
                continue
            
            if self.reload:
                watchlist = list(self.listeners.keys())
                self.reload = False
                if len(watchlist) > 0:
                    print(self.listeners[watchlist[0]])

            for directory in watchlist:
                result = win32event.WaitForSingleObject(self.listeners[directory], 10)
                if result == win32con.WAIT_OBJECT_0:

                    # Trigger callback, directory has changed
                    if self.callBackMethod:
                        # Avoid callbacks when shuting down
                        if self.running:
                            self.callBackMethod()
                    else:
                        print("dir changed")
                    win32file.FindNextChangeNotification(self.listeners[directory])


        self.terminated = True


# Implemented main method for testing..
if __name__ == "__main__":
    watcher = DirectoryWatcher(None)
    watcher.start()
    watcher.addListener("listen", "c:\\Users\\Rune\\workspace")
    
    time.sleep(20)

    watcher.stop()
    watcher.closeListeners()