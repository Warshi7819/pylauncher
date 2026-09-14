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
from AddDirFrame import AddDirFrame
from OwnConstants import *


class ConfigPanelIndexer(wx.Panel):
    """
    Class implementing the config panel for the indexer
    """
    
    def __init__(self, parent, config, indexer, id=-1):
        """
        Class constructor
        Args:
          parent = The parent window
          config = AL's config
          indexer = The indexer object
          id = The panel id, defaults to -1
        """
        wx.Panel.__init__(self, parent, id)

        self.indexer = indexer
        self.config = config
        
        # Create super sizer
        superSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create staticText with info
        helpText = \
"""
By adding/deleting directories to the list below you will control the
content that is being indexed (and thus searchable). Double clicking an
item will bring up a advanced dialogbox which will let you decide which
filetypes to include.
"""
        
        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        # Create checklistbox
        self.lb = wx.CheckListBox(self, -1, size=(300,200))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.evtListBox, self.lb)
        self.Bind(wx.EVT_CHECKLISTBOX, self.evtCheckListBox, self.lb)
        sizer.Add(self.lb, 0, wx.ALIGN_CENTRE|wx.ALL, 3)
        self.populate()

        # Adding delete and add button
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.deleteButton = wx.Button(self, -1, "Delete selected")
        self.Bind(wx.EVT_BUTTON, self.onDeleteButton, self.deleteButton)
        buttonSizer.Add(self.deleteButton, 2, wx.EXPAND)

        self.addButton = wx.Button(self, -1, "Add directory")
        self.Bind(wx.EVT_BUTTON, self.onAddButton, self.addButton)
        buttonSizer.Add(self.addButton, 2, wx.EXPAND)
        sizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        # Create staticText with info
        helpText = \
"""
If you make any changes you will have to trigger a reindex before these
changes take affect. That basically means that AL will traverse the
directories selected and make the programs that matches searchable.
Note:
 This operation is time consuming and I/O intensive. Therefore a reindex
 should not be performed unless it's needed.
"""
        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        # Create reindex button
        self.reindexButton = wx.Button(self, -1, "Reindex", (20, 410))
        self.Bind(wx.EVT_BUTTON, self.onReindexButton, self.reindexButton)
        sizer.Add(self.reindexButton, 0, wx.ALIGN_LEFT, 1)

                
        # Set sizer
        superSizer.Add(sizer)
        self.SetSizer(superSizer)
        self.Fit()


    def populate(self):
        """
        Method to populate list
        Args:
          None

        Returns: None
        """
        # Populate checklistbox
        self.lb.Clear()
        i = 0
        for dir in self.config.config["directories"]:
            self.lb.Insert(dir, i)
            if self.config.config["directories"][dir][1]:
                self.lb.Check(i)
            i += 1


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
        addDirFrame = AddDirFrame(self, name)


    def evtCheckListBox(self, event):
        """
        Method that handles when an item in the check
        list box is being checked/unchecked
        Args:
          event = The evtCheckListBox

        Returns: None
        """

        index = event.GetInt()
        name = self.lb.GetString(index)

        if self.lb.IsChecked(index):
            self.config.config["directories"][name][1] = True
        else:
            self.config.config["directories"][name][1] = False


    def onAddButton(self, event):
        """
        Method that handles when the add directory
        button is pressed
        Args:
          event = The button event

        Returns: None
        """

        addDirFrame = AddDirFrame(self)


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
                       + "\n'%s'\nfrom the index?" % name
            dlg = QuestionDialog(self, -1, "Confirm delete",
                                 question, size=(350, 200),
                                 style = wx.DEFAULT_DIALOG_STYLE)
            dlg.CenterOnScreen()

            # this does not return until the dialog is closed.
            val = dlg.ShowModal()
    
            if val == wx.ID_OK:
                # Delete from config
                del self.config.config["directories"][name]
                # Delete from list
                self.lb.Delete(index)
                
                # TODO: Request idleReindex


            dlg.Destroy()


    def onReindexButton(self, event):
        """
        Method that handles when the reindex button is
        pressed
        Args:
          event = The button event

        Returns: None
        """

        question = "Do you really want to force a reindex?"
        dlg = QuestionDialog(self, -1, "Confirm reindex", question, size=(350, 200),
                             style = wx.DEFAULT_DIALOG_STYLE)
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
            dlg.Destroy()
            self.indexer.reindex(True)
            
            info = "Forced reindex has been scheduled."
            dlg = InfoDialog(self, -1, "Status", info,
                             size=(350, 200),
                            style = wx.DEFAULT_DIALOG_STYLE)
            
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            dlg.Destroy()
            self.close()
            
        else:
            dlg.Destroy()

    def close(self, event=None):
        if event:
            event.Skip()