###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import pickle
import os

def loadFromFile(filename):
    """
    Function to load pickled data from file
    Args:
    filename = the file containing the marshalled data
    
    Returns: unmarshalled object or None on error
    """
    if os.path.isfile(filename):
        try:
            fp = open(filename, "rb")
            data = pickle.loads(fp.read())
            fp.close()
        except Exception as e:
            return None
        
        return data
    else:
        return None


def dumpToFile(data, filename):
    """
    Function to marshall an object to file
    Args:
    data = The object/data to marshall
    filename = Where we should store the data
    
    Returns: None
    """
    fp = open(filename, "wb")
    try:
        fp.write(pickle.dumps(data))
    except Exception as e:
        pass

    fp.close()