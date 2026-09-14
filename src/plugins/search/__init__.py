###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Define which plugins that should be loaded
from .GooglePlugin import GooglePlugin
from .GoogleGroupsPlugin import GoogleGroupsPlugin
from .DictionaryPlugin import DictionaryPlugin
from .WikipediaPlugin import WikipediaPlugin
from .MailPlugin import MailPlugin
from .WebPlugin import WebPlugin
from .ImdbPlugin import ImdbPlugin

# List of available plugins
searchPlugins = ["GooglePlugin",
                 "GoogleGroupsPlugin",
                 "DictionaryPlugin",
                 "WikipediaPlugin",
                 "MailPlugin",
                 "WebPlugin",
                 "ImdbPlugin"]