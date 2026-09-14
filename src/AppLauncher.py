###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import win32api
import os
import threading

class AppLauncher(threading.Thread):
    """
    Class implementing a thread that will launch and forget
    a given program
    """
    
    def __init__(self, command):
        """
        Class constructor
        Args:
          command = The command to be executed by the main thread
        """
        threading.Thread.__init__(self)
        self.command = command[0]
        self.alias = command[1]


    def run(self):
        """
        Thread body that executes the program. Using a thread so
        that the main application (GUI) will not be unresponsive
        while we execute a program.
        Args:
          None

        Returns: None
        """

        if self.command:
            if not self.alias:
                # Execute file
                try:
                    os.startfile(self.command)
                except UnicodeEncodeError as e:
                    # Guess encoding from defined list
                    for best_enc in ['us-ascii','iso-8859-1','iso-8859-2']:
                        try:
                            tmp = self.command.encode(best_enc)
                            os.startfile(tmp)
                            break
                        except Exception as e: 
                            # Failed encoding or failed starting with that encoding
                            # Try next if any
                            pass

            else:
                # use win32api on aliases since we have experienced some
                # strange stuff trying to execute url's with startfile
                command = self.command[0]
                args = self.command[1]
                win32api.ShellExecute(0, "open", command, args, ".", 1)
                
 

        



        
       