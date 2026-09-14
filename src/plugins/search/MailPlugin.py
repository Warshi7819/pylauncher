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

class MailPlugin(SearchObject.SearchObject):
    """
    The class that implements the mail search plugin
    """

    def __init__(self):
        """
        The class constructor
        Args:
          None
        """
        # This plugin should catch searches that startswith mailto:
        self.searchEnabler = "mailto"


    def getShortDescription(self):
        """
        Method to fetch a short description of what this plugin do. To be
        displayed when the mouse is over the icon for the given search plugin
        Args:
          None

        Returns: [STRING] Description
        """

        return "Send mail to the person specified"


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
        return "icons\\email.png"
    

    def executeSearch(self, searchString):
        """
        Method to start up default mail client when a search
        matches this plugin
        Args:
          searchString = The search string the user types in

        Returns: None
        """
        encoded = False
        
        for best_enc in ['ascii', 'us-ascii','iso-8859-1','iso-8859-2']:
            try:
                searchString = searchString.encode(best_enc)
                encoded = True
            except Exception as e: 
                pass
            else: 
                pass

        if not encoded:
            print("encoding failed")
            return
        
        url = "mailto:" + urllib.parse.quote(searchString[7:],"@@,")
        webbrowser.open(url,new=1)