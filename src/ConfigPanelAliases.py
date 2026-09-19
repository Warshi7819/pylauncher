###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import os.path

# Import wxpython modules
import wx

# Import own modules
from QuestionDialog import QuestionDialog
from InfoDialog import InfoDialog
from AddAliasesFrame import AddAliasesFrame
from plugins.index import Aliases
from OwnConstants import *


class ConfigPanelAliases(wx.Panel):
    """
    Class implementing the config panel for the aliases plugin
    """
    
    def __init__(self, parent, config, id=-1):
        """
        Class constructor
        Args:
          parent = The parent window
          config = AL's config
        """
        wx.Panel.__init__(self, parent, id)

        # hold on to config
        self.config = config

        # Figure out where the aliases file is located
        self.aliasesFile = os.path.join(self.config.config["appDataDir"], "aliases.txt")

        # load aliases
        self.aliasesObj = Aliases.Aliases(self.aliasesFile)
        self.aliases = self.aliasesObj.loadAliases()
        
        # Create super sizer
        superSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create staticText with info
        helpText = \
"""
By adding/deleting entries in the list below you will control the aliases
being indexed by AL. Double clicking an existing item will bring up a
advanced dialogbox which will let you decide the name of the alias,
which program to associate with the alias and the program's arguments if
any. Press the \"Create Alias\" button to create a new alias.
Note: If you make any changes you will have to trigger a reindex before
these changes take affect. More info under the \"Indexer\" config tab.
"""
        
        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        # Create checklistbox
        self.lb = wx.ListBox(self, -1, size=(300,200))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.evtListBox, self.lb)
        sizer.Add(self.lb, 0, wx.ALIGN_CENTRE|wx.ALL, 3)
        self.populate()

        # Adding delete and add button
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.deleteButton = wx.Button(self, -1, "Delete selected")
        self.Bind(wx.EVT_BUTTON, self.onDeleteButton, self.deleteButton)
        buttonSizer.Add(self.deleteButton, 2, wx.EXPAND)

        self.createButton = wx.Button(self, -1, "Create Alias")
        self.Bind(wx.EVT_BUTTON, self.onCreateButton, self.createButton)
        buttonSizer.Add(self.createButton, 2, wx.EXPAND)
        sizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)


        # Set sizer
        superSizer.Add(sizer)
        self.SetSizer(superSizer)
        self.Fit()


    def populate(self):
        """
        Method to populate list with aliases
        Args:
          None

        Returns: None
        """
        # Populate checklistbox
        
        self.lb.Clear()
        i = 0
        for i in range(0, len(self.aliases)):
            self.lb.Insert(self.aliases[i][0], i)
            i += 1


    def saveAliases(self):
        """
        Method to save the aliases
        Args:
          None

        Returns: None
        """

        self.aliasesObj.saveAliases(self.aliases)
        
        

    def evtListBox(self, event):
        """
        Method that handles when an item in the check
        list box has been double clicked.
        Args:
          event = The button event

        Returns: None
        """
        index = event.GetInt()
        name = self.lb.GetString(index)
        addAliasesFrame = AddAliasesFrame(self, name, index)


    def onCreateButton(self, event):
        """
        Method that handles when the add directory
        button is pressed
        Args:
          event = The button event

        Returns: None
        """

        addAliasesFrame = AddAliasesFrame(self)


    def onDeleteButton(self, event):
        """
        Method that handles when the delete button is
        pressed
        Args:
          event = The button event

        Returns: None
        """
        index = self.lb.GetSelection()
        if index != -1:
            name = self.lb.GetString(index)

            question = "Do you really want to delete:" \
                       + "\n'%s'\nfrom the Alias list?" % name
            dlg = QuestionDialog(self, -1, "Confirm delete",
                                 question, size=(350, 200),
                                 style = wx.DEFAULT_DIALOG_STYLE)
            dlg.CenterOnScreen()

            # this does not return until the dialog is closed.
            val = dlg.ShowModal()
    
            if val == wx.ID_OK:
                # Delete from config
                del self.aliases[index]
                # Delete from list
                self.lb.Delete(index)

                self.saveAliases()
                
            dlg.Destroy()


    def close(self, event=None):
        """
        Method to close the aliases config panel
        Args:
          event = The close event

        Returns: None
        """
        if event:
            event.Skip()