###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
from urllib.parse import urlencode

# Import own modules
from . import SearchObject
from AppLauncher import AppLauncher

class GoogleGroupsPlugin(SearchObject.SearchObject):
    """
    The class that implements the google groups search plugin
    """

    def __init__(self):
        """
        The class constructor
        Args:
          None
        """
        # This plugin should catch searches that startswith gg:
        self.searchEnabler = "gg"

    def getShortDescription(self):
        """
        Method to fetch a short description of what this plugin do. To be
        displayed when the mouse is over the icon for the given search plugin
        Args:
          None

        Returns: [STRING] Description
        """

        return "Search Google Groups"

    def getEnabler(self):
        """
        Method that returns the search enabler
        Args: None

        Returns: [STRING] The search enabler prefix
        """
        return self.searchEnabler


    def getIcon(self):
        """
        Method that returns the path of the icon to use when this
        search plugin matches a query
        Args:
          None

        Returns: [STRING] Relative path to the icon
        """
        return "icons\\googleIcon.ico"

    def executeSearch(self, searchString):
        """
        Method to fire off a search on google groups
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
        
        # Build the query url
        address = "http://groups.google.com/groups?lnk=hpsg&hl=en&%s"
        query = urlencode({"q":searchString[3:]})
        address = address % query
        # Execute it
        command = (address, False)
        appLaunch = AppLauncher(command)
        appLaunch.start()