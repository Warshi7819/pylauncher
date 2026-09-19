###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
from winreg import *

def fetchShellFolders():
    """
    Function to fetch shell folders. Used to figure out the path
    to e.g. the Start menu, My Documents and Favorites..
    Args:
      None

    Returns: [DICT] A dictionary with all the shell folder names and their
             respective path
    """
    
    # Dictionary to hold our findings
    shellFolderDict = {}

    # The key name
    keyname = "Software\\Microsoft\\Windows\\CurrentVersion" \
              + "\\Explorer\\Shell Folders"
    
    # Read data for current user    
    kkey = OpenKey(HKEY_CURRENT_USER, keyname)
    kinfo = QueryInfoKey(kkey)
    for x in range(0, kinfo[1]):
        try:
            (name, value, ttype) = EnumValue(kkey, x)
            shellFolderDict[name] = [value, ttype]
        except EnvironmentError:
            return {}
    kkey.Close()

    # Find data for all users
    kkey = OpenKey(HKEY_LOCAL_MACHINE, keyname)
    kinfo = QueryInfoKey(kkey)
    for x in range(0, kinfo[1]):
        try:
            (name, value, ttype) = EnumValue(kkey, x)
            shellFolderDict[name] = [value, ttype]
        except EnvironmentError:
            return {}
    kkey.Close()

    return shellFolderDict

if __name__ == "__main__":
   dict = fetchShellFolders()
   fp = open("debug.txt", "w")
   for name in dict:
       fp.write("%s:\n" % name)
       fp.write("%s\n" % dict[name])

   fp.close()