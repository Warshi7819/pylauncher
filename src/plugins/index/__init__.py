###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Define which plugins that should be loaded
from .DirectoryPlugin import DirectoryPlugin
from .FirefoxPlugin import FirefoxPlugin
from .AliasPlugin import AliasPlugin

# List of available plugins
indexerPlugins = ["DirectoryPlugin", "FirefoxPlugin", "AliasPlugin"]