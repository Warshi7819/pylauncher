###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modues
import urllib.parse
import webbrowser

# Import own modules
from . import SearchObject

class WebPlugin(SearchObject.SearchObject):
    """
    The class that implements the WebPlugin which enables the user
    to execute a given url (opening a new browser)
    """

    def __init__(self):
        """
        The class constructor
        Args:
          None
        """
        # This plugin should catch searches that startswith web:
        self.searchEnabler = "web"


    def getShortDescription(self):
        """
        Method to fetch a short description of what this plugin do. To be
        displayed when the mouse is over the icon for the given search plugin
        Args:
          None

        Returns: [STRING] Description
        """

        return "Open given URL in default browser"


    def getEnabler(self):
        """
        Method that returns the search enabler
        Args:
          None

        Returns
        """
        return self.searchEnabler


    def getIcon(self):
        """
        Method to get path to icon
        Args:
          None

        Returns: [STRING] Relative path to icon
        """
        return "icons\\internetIcon.ico"
    

    def executeSearch(self, searchString):
        """
        Method to start up the default web browser with the given url
        Args:
          searchString = The search string the user types in

        Returns: None
        """
        url = searchString[4:]
        encoded = False
        
        for best_enc in ['ascii', 'us-ascii','iso-8859-1','iso-8859-2']:
            try:
                url = url.encode(best_enc)
                encoded = True
            except Exception as e: 
                pass
            else: 
                pass

        if not encoded:
            return
        
        url = url.strip()
        if not url.lower().startswith("ww"):
            if not url.lower().startswith("http"):
                url = "http://%s" % url
                
        webbrowser.open(url,new=0)