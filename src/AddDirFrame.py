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
from wx.lib.stattext import GenStaticText

# Import own modules
from OwnConstants import *
from InfoDialog import InfoDialog


class AddDirFrame(wx.Frame):
    """
    Class that implements the configuration GUI
    """

    def __init__(self, parent, edit = None):
        """
        Class constructor
        Args:
          parent = The parent frame
          edit = The key of the element we want to edit
                 None if this is a new element
        """
        
        # Hold on to some variables
        self.edit = edit
        self.config = parent.config
        self.indexer = parent.indexer
        self.parent = parent

        if self.edit != None:
            frameName = "Edit item"
            self.path = self.config.getPath(self.edit)
        else:
            frameName = "Add item"
            self.path = ""
            
        wx.Frame.__init__(self, parent, -1, frameName)
        self.SetBackgroundColour("#FFFFFF")
        self.Bind(wx.EVT_CLOSE, self.close)

        # Fetch icon
        self.icon = wx.Icon("images\\al_icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        # Create sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create staticText with info
        helpText = \
"""
 Please add/edit chosen directory by browsing. All sub-directories will
 automatically be traversed and added when reindex is triggered.
"""
        
        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_LEFT, 1)

        self.addButton = wx.Button(self, -1, "Select Directory", (310, 430))
        self.Bind(wx.EVT_BUTTON, self.onAddDir, self.addButton)
        sizer.Add(self.addButton, 0, wx.ALIGN_LEFT|wx.ALL, 1)

        self.dirLabel = GenStaticText(self, -1, "", size=(200, 15),
                                      style=wx.ST_NO_AUTORESIZE)
        sizer.Add(self.dirLabel, 0, wx.ALIGN_LEFT|wx.ALL, 1)

        self.setDirLabelText(self.path)

        # Create staticText with info
        helpText = \
"""
 Give this item an unique name that identifies it.
"""

        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_LEFT, 1)

        # Create the extension textctrl
        if self.edit != None:
            # Fetch current extension
            self.name = self.edit
        else:
            self.name = "NEW ITEM"

        self.nameCtrl = wx.TextCtrl(self, -1, self.name,
                                    size=(125, -1),
                                    style=wx.WANTS_CHARS)
        
        sizer.Add(self.nameCtrl, 0, wx.ALIGN_LEFT|wx.ALL, 1)

        
        # Create staticText with info
        helpText = \
"""
 Chose the extensions that should be added. e.g. doc,pdf,exe,lnk,url
 or any other filetype you want to include.
"""

        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_LEFT, 1)

        # Create the extension textctrl
        if self.edit != None:
            # Fetch current extension
            exts = ",".join(self.config.config["directories"][self.edit][2])
        else:
            exts = "exe,lnk,url"

        self.extensions = wx.TextCtrl(self, -1, exts,
                                      size=(125, -1),
                                      style=wx.WANTS_CHARS)
        
        sizer.Add(self.extensions, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        self.doneButton = wx.Button(self, -1, "Add", (310, 430))
        self.Bind(wx.EVT_BUTTON, self.addAndClose, self.doneButton)
        sizer.Add(self.doneButton, 0, wx.ALIGN_RIGHT|wx.ALL, 1)
        
        # Set/fit sizer
        self.SetSizer(sizer)
        sizer.Fit(self)

        self.Center(wx.BOTH)
        # Show the thingy
        self.Show()



    def setDirLabelText(self, text):
        """
        Method to set the text of the directory label
        Only show the last 29 chars.
        Args:
          text [STRING] = The path to the directory

        Returns: None
        """
        if len(text) > 30:
            labelText = " ...%s" % text[-29:]
        else:
            labelText = text
            
        self.dirLabel.SetLabel(labelText)

        
    def onAddDir(self, event):
        """
        Method to add/edit a directory to this item
        Args:
          event = The button event

        Returns: None
        """
        
        if self.edit != None:
            dlg = wx.DirDialog(self, "Choose a directory:", self.path,
                               style=wx.DD_DEFAULT_STYLE)
        else:
            dlg = wx.DirDialog(self, "Choose a directory:",
                               style=wx.DD_DEFAULT_STYLE)


        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
            self.setDirLabelText(self.path)

        # Only destroy a dialog after you're done with it.
        dlg.Destroy()
        

    def addAndClose(self, event=None):
        """
        Method to close config window
        Args:
          evt = The close event

        Returns: None
        """
        # Fetch extensions
        tmp = self.extensions.GetLabel().split(",")
        exts = []
        
        for ext in tmp:
            ext = ext.strip().lower()
            if ext:
                exts.append(ext)

        name = self.nameCtrl.GetLabel().strip()

        ret = self.config.addItem(name, self.path,
                                  exts, self.edit)

        if ret != True:
            dlg = InfoDialog(self, -1, "Add/Edit failed", ret,
                             size=(350, 200),
                             style = wx.DEFAULT_DIALOG_STYLE)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            dlg.Destroy()

        else:
            # all well. Populate the parents listctrl
            self.parent.populate()
            
            # TODO: request idle reindex 
            
            # close
            self.close()

    def close(self, event=None):
        self.Destroy()