###################################################
# Application : pyMP                              #
#  * Asynchronous event based music player        #
#  * utilizing the powers of pymedia and wxPython #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 14:37 05.09.2004                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import wxpython modules
import wx
import wx.adv

# Import own modules
from GuiUtils import bitmapType, openAsBitmap

class AlSplashScreen(wx.adv.SplashScreen):
    """
    Class that implements the splash screen
    """
    
    def __init__(self, parent):
        """
        Class constructor
        Args:
          parent = The parent frame
        """
        bmp = openAsBitmap("images\\al-logo.png")
        wx.adv.SplashScreen.__init__(self, bmp,
                                 wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                 3000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnClose(self, event):
        """
        Called when the splash-timeout fires
        Args:
          event = The close event

        Returns: None
        """
        
        event.Skip()
        self.Hide()
        
   