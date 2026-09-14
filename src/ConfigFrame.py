###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import wxpython modules
import wx

# Import own modules
from OwnConstants import *
from ConfigPanelIndexer import ConfigPanelIndexer
from ConfigPanelUI import ConfigPanelUI
from ConfigPanelAddons import ConfigPanelAddons
from ConfigPanelAliases import ConfigPanelAliases

class ConfigNotebook(wx.Notebook):
    """
    Class implementing the config notebook
    """
    
    def __init__(self, parent, config, indexer, id=-1):
        """
        Class constructor
        Args:
          parent = The parent window
          config = AL's config
          indexer = The indexer object
          id = The window id, defaults to -1
        """
        wx.Notebook.__init__(self, parent, id)
        
        win = ConfigPanelIndexer(self, config, indexer)
        self.AddPage(win, "Indexer")

        win = ConfigPanelAddons(self, config)
        self.AddPage(win, "Addons")

        win = ConfigPanelUI(self, config)
        self.AddPage(win, "UI")

        win = ConfigPanelAliases(self, config)
        self.AddPage(win, "Aliases")
        
        self.Fit()
                
        

class ConfigFrame(wx.Frame):
    """
    Class implementing the config frame
    """
    
    def __init__(self, parent):
        """
        Class constructor
        Args:
          parent = The parent frame

        Returns: None
        """
        wx.Frame.__init__(self, parent, -1, "Configure AL")
        self.SetBackgroundColour("#FFFFFF")
        self.Bind(wx.EVT_CLOSE, self.close)

        self.parent = parent
        self.config = self.parent.config
        self.indexer = self.parent.indexer

        self.configNotebook = ConfigNotebook(self, self.config, self.indexer)
        self.Fit()

        # Fetch icon
        self.icon = wx.Icon("images\\al_icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        
        self.Center(wx.BOTH)
        # Show the thingy
        self.Show()
        

    def close(self, evt=None):
        """
        Method to close config window
        Args:
          evt = The close event

        Returns: None
        """
        self.Destroy()