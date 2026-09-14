###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

class SearchObject:

    def getEnabler(self):
        raise Exception("getEnabler method must be overridden")

    def executeSearch(self, searchString):
        raise Exception("executeSearch method must be overridden")

    def getShortDescription(self):
        return Exception("the getShortDescription method must be overridden")

    def getIcon(self):
        return None