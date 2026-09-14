###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import wxpython modules
import wx.lib.newevent

# Application version
APP_VERSION = "1.0.7"

# Internal versions
CONFIG_VERSION = "0.0.3"
APPLIST_VERSION = "0.0.1"
HISTORY_VERSION = "0.0.1"

DEBUG = False
DISPLAY = 101

NO_NAME = 1000
NO_PATH = 1001
NO_EXTS = 1002
NAME_CONFLICT = 1003

# Define the InsertApplication event
(InsertApplication, EVT_INSERT_APPLICATION) = wx.lib.newevent.NewEvent()
