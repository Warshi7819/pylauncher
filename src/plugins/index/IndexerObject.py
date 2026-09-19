###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

class IndexerObject:
    """Base class for all indexer plugins."""

    def fetchApps(self, args=None):
        raise Exception("fetchApps method must be overridden")


    def startMonitor(self, callbackFunction):
        pass

    def stopMonitor(self):
        return True

    def default(self):
        return False

    def getDescription(self):
        raise Exception("getDescription method must be overridden")

    def stop(self):
        return