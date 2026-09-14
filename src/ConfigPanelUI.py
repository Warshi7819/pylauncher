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
from QuestionDialog import QuestionDialog
from InfoDialog import InfoDialog
from OwnConstants import *

class ConfigPanelUI(wx.Panel):
    """
    Class implementing the UI configuration panel
    """
    
    def __init__(self, parent, config, id=-1):
        """
        Class constructor
        Args:
          parent = The parent window
          config = AL's config
          id = The window id, defaults to -1
        """
        wx.Panel.__init__(self, parent, id)


        self.modKeyMap = {"Alt-Key":wx.MOD_ALT,
                          "Control-Key":wx.MOD_CONTROL,
                          "Shift-Key":wx.MOD_SHIFT}
        # Ordered list
        self.modKeys = ["Alt-Key", "Control-Key", "Shift-Key"]

        self.keyMap = {"Space":32,
                       "Enter":13,
                       "Page up":312,
                       "Page down":313,
                       "End":314,
                       "Home":315,
                       "Del":127,
                       "Insert":324,
                       "Esc":27,
                       "0":48,
                       "1":49,
                       "2":50,
                       "3":51,
                       "4":52,
                       "5":53,
                       "6":54,
                       "7":55,
                       "8":56,
                       "9":57,
                       "a":65,
                       "b":66,
                       "c":67,
                       "d":68,
                       "e":69,
                       "f":70,
                       "g":71,
                       "h":72,
                       "i":73,
                       "j":74,
                       "k":75,
                       "l":76,
                       "m":77,
                       "n":78,
                       "o":79,
                       "p":80,
                       "q":81,
                       "r":82,
                       "s":83,
                       "t":84,
                       "u":85,
                       "v":86,
                       "w":87,
                       "x":88,
                       "y":89,
                       "z":90,
                       "F1":342,
                       "F2":343,
                       "F3":344,
                       "F4":345,
                       "F5":346,
                       "F6":347,
                       "F7":348,
                       "F8":349,
                       "F9":350,
                       "F10":351,
                       "F11":352,
                       "F12":353}

        self.keys = ["Space", "Enter", "Page up", "Page down", "End", "Home",
                     "Del", "Insert", "Esc", "0", "1", "2", "3", "4", "5",
                     "6", "7", "8", "9", "a","b", "c", "d", "e", "f", "g",
                     "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                     "s", "t", "u", "v", "w", "x", "y", "z"] #, "F1", "F2",
                     #"F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11",
                     #"F12"
        
        # Hold on to the configuration
        self.config = config

        # Create super sizer
        superSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create staticText with info
        helpText = \
"""
In this section you can enable/disable some of ALs user interface
options. Remember though if you change any of these options you will
have to manually restart the application for the changes to take effect.
"""
        
        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        # Always on top (on/off) default is off
        self.alwaysOnTopCB = wx.CheckBox(self, -1, "Always on top")
        tooltip = "Enabling this will ensure that AL always\nis the topmost window."
        self.alwaysOnTopCB.SetToolTip(wx.ToolTip(tooltip))
        if self.config.config["ontop"]:
            self.alwaysOnTopCB.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.setOnTop, self.alwaysOnTopCB)
        sizer.Add(self.alwaysOnTopCB, 0, wx.ALIGN_LEFT, 1)



        # Always display search window (on/off) default is off
        self.displaySWCB = wx.CheckBox(self, -1, "Always display search window")
        tooltip = "Enabling this will ensure that the search\nresult window always is visible."
        self.displaySWCB.SetToolTip(wx.ToolTip(tooltip))
        if self.config.config["alwaysSearchWindow"]:
            self.displaySWCB.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.setAlwaysDisplayResult, self.displaySWCB)
        sizer.Add(self.displaySWCB, 0, wx.ALIGN_LEFT, 1)
        
        # Configure hotkeys
        # See process and events - keyevents in the wxpython demo
        helpText = \
"""
Here you may configure the hotkeys AL uses. (Hotkeys are the keys you
press each time you want to bring AL up from hiding and ask him a
question)
"""
        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.modKeyChoice = wx.Choice(self, -1,
                                      choices = self.modKeys)
        self.keyChoice = wx.Choice(self, -1, choices = self.keys)
        self.Bind(wx.EVT_CHOICE, self.modKeyChanged, self.modKeyChoice)
        self.Bind(wx.EVT_CHOICE, self.keyChanged, self.keyChoice)
        choiceSizer.Add(self.modKeyChoice, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        choiceSizer.Add(self.keyChoice, 0, wx.ALIGN_CENTER|wx.ALL, 1)


        # Set selected hotkeys
        mkey = self.config.config["hotkeys"][0]
        key = self.config.config["hotkeys"][1]
        
        for keyname in self.modKeys:
            if mkey == self.modKeyMap[keyname]:
                index = self.modKeyChoice.FindString(keyname)
                self.modKeyChoice.SetSelection(index)
                
        for keyname in self.keys:
            if key == self.keyMap[keyname]:
                index = self.keyChoice.FindString(keyname)
                self.keyChoice.SetSelection(index)


        sizer.Add(choiceSizer, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        # Set sizer
        superSizer.Add(sizer)
        self.SetSizer(superSizer)
        self.Fit()



    def setOnTop(self, event):
        """
        Method that handles the toggeling of on top functionality
        Args:
          event = The checkbox event

        Returns: None
        """
        if event.IsChecked():
            self.config.config["ontop"] = True

        else:
            # Disable "always on top"
            self.config.config["ontop"] = False

    
    def setAlwaysDisplayResult(self, event):
        """
        Method that handles the toggeling of always displaying
        search results
        Args:
          event = The checkbox event

        Returns: None
        """
        if event.IsChecked():
            # Enable "always display search results"
            self.config.config["alwaysSearchWindow"] = True

        else:
            # Disable "always display search results"
            self.config.config["alwaysSearchWindow"] = False


    def modKeyChanged(self, event):
        """
        Method to handle a new choice of first hotkey
        Args:
          event = The evt_choice event

        Returns: None
        """
        keyname = event.GetString()
        key = self.modKeyMap[keyname]
        self.config.config["hotkeys"][0] = key


    def keyChanged(self, event):
        """
        Method to handle a new choice of first hotkey
        Args:
          event = The evt_choice event

        Returns: None
        """
        keyname = event.GetString()
        key = self.keyMap[keyname]
        self.config.config["hotkeys"][1] = key
