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
from plugins.index import *
from Curry import curry

class ConfigPanelAddons(wx.Panel):
    """
    Class implementing the Addons configuration panel
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

        # Hold on to the configuration
        self.config = config


        # Create super sizer
        superSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create staticText with info
        helpText = \
"""
In this section you can enable/disable some of AL's addon functionality.
Note: A reindex is needed for the changed to be visible!
"""
        
        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        # Hold dictionaries of checkboxes
        self.CBList = {}

        # Toggle addons on or of. Fetch all available indexer plugins
        # and let this panel toggel their state
        for pluginName in self.config.config["plugins"]["index"]:
            # Fetch current status
            toggled = self.config.config["plugins"]["index"][pluginName]
            # Fetch tooltip
            plugin = eval("%s(self.config, None)" % pluginName)
            tooltip = plugin.getDescription()
            
            # Create the new checkbox
            self.CBList[pluginName] = wx.CheckBox(self, -1, pluginName)
            self.CBList[pluginName].SetToolTip(wx.ToolTip(tooltip))
            self.Bind(wx.EVT_CHECKBOX, curry(self.toggelPlugin, pluginName),
                      self.CBList[pluginName])
            # Toggle it if the plugin is activated
            if toggled:
                self.CBList[pluginName].SetValue(True)

            # Add it to sizer
            sizer.Add(self.CBList[pluginName], 0,
                      wx.ALIGN_LEFT, 1)

        # Set sizer
        superSizer.Add(sizer)
        self.SetSizer(superSizer)
        self.Fit()

        
    def toggelPlugin(self, pluginName, event):
        """
        Method to toggle plugin on off
        Args:
          pluginName = The name of the plugin being toggled
          event = The checkbox event

        Returns: None
        """
        if event.IsChecked():
            # The plugin is checked
            self.config.config["plugins"]["index"][pluginName] = True
        else:
            # Plugin is disabled
            self.config.config["plugins"]["index"][pluginName] = False