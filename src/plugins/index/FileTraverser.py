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
import os
import re


class FileTraverser:
    """
    Class that implements the filetraverser
    """
    
    def __init__(self):
        """
        Class constructor
        Args:
          None
        """
        pass


    def traverse(self, directory, filterSpec):
        """
        Method that traverses the disk and fetches
        the applications that matches the filter
        Args:
          directory = The path where we should start traversing
          filterSpec = The file filter

        Returns: [LIST] List of matches
        """

        filter = FileFilter(filterSpec)
        
        filelist = []
                
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                if not filter.filter(name):
                    # Add file to applicationList
                    fullPath = os.path.join(root, name)
                    filelist.append((name, fullPath))

        return filelist

        
class FileFilter:
    """
    Filter away files that don't match the regexp
    """
    
    def __init__(self, fileExtensionList):
        """
        Class constructor
        Args:
          fileExtensionList = The list of file extensions of the files
                              we don't want to filter away
        """
        expression = r".*\.("
        first = True
        all = False
        
        for ext in fileExtensionList:
            if first:
                first = False
                expression = "%s%s" % (expression, ext)
            else:
                expression = "%s|%s" % (expression, ext)


            if ext == "*":
                all = True
                break

        if all:
            expression = r".*\.*"
        else:
            expression = "%s)$" % expression

        self.exp = re.compile(expression)


    def filter(self, fileName):
        """
        Method to filteraway files that we should not include
        Args:
          filename = The filename we want to test

        Returns: [BOOLEAN] False if the file matches the filter, that is do not filter
                 this file. True if the file does not match
        """

        if self.exp.match(fileName):
            return False
        else:
            return True

    