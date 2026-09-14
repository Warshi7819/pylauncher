###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

def copyFile(source, dest):
    """
    Method to copy a file from source to dest
    Args:
      source = The source file to copy
      dest = The destination filename

    Returns: None when done
    """
    # Read complete file into memory
    # Not usefull for large files!!
    fp = open(source, "rb")
    data = fp.read()
    fp.close()
    
    fp = open(dest, "wb")
    fp.write(data)
    fp.close()