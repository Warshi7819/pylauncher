###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import os

# Import wxpython modules
import wx
from wx.lib.stattext import GenStaticText

# Import own modules
from OwnConstants import *
from InfoDialog import InfoDialog


class AddAliasesFrame(wx.Frame):
    """
    Class that implements the configuration GUI
    """

    def __init__(self, parent, edit = None, index = None):
        """
        Class constructor
        Args:
          parent = The parent frame
          edit = The key of the element we want to edit
                 None if this is a new element
          index = The index of the alias being edited
        """


        # Hold on to some variables
        self.edit = edit
        self.aliases = parent.aliases
        self.parent = parent
        self.index = index

        if self.edit != None:
            frameName = "Edit item"
        else:
            frameName = "Add item"

            
        wx.Frame.__init__(self, parent, -1, frameName)
        self.SetBackgroundColour("#FFFFFF")
        self.Bind(wx.EVT_CLOSE, self.close)

        # Fetch icon
        self.icon = wx.Icon("images\\al_icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        # Create super sizer
        superSizer = wx.BoxSizer(wx.VERTICAL)

        # Create sizer
        sizer = wx.BoxSizer(wx.VERTICAL)


        # Create staticText with info
        helpText = \
"""
 Give the alias an unique name that identifies it:
"""

        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_LEFT, 1)

        # Create the name textctrl
        if self.edit != None:
            # Fetch current name
            self.name = self.aliases[self.index][0]
            self.path = self.aliases[self.index][1]
        else:
            self.name = "New alias"
            self.path = ""

        self.nameCtrl = wx.TextCtrl(self, -1, self.name,
                                    size=(125, -1),
                                    style=wx.WANTS_CHARS)
        
        sizer.Add(self.nameCtrl, 0, wx.ALIGN_LEFT, 1)


        # Create staticText with info
        helpText = \
"""
 The string/program to execute:
"""

        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_LEFT, 1)

        # Horizontal sizer for choose program or write exec string
        execStringSizer = wx.BoxSizer(wx.HORIZONTAL)

        # ExecString ctrl
        self.progText = wx.TextCtrl(self, -1, self.name,
                                    size=(125, -1),
                                    style=wx.WANTS_CHARS)

        execStringSizer.Add(self.progText, 2, wx.EXPAND)

        # Select program button
        self.addButton = wx.Button(self, -1, "Select Program", (310, 430))
        self.Bind(wx.EVT_BUTTON, self.onAddProgram, self.addButton)
        execStringSizer.Add(self.addButton, 2, wx.EXPAND)

        # Add the execStringSizer to main sizer
        sizer.Add(execStringSizer, 0, wx.ALIGN_LEFT, 1)

        # Set current exec string if any
        self.setProgText(self.path)
        
        
        # Create staticText with info
        helpText = \
"""
 Program arguments if any:
"""

        label = wx.StaticText(self, -1, helpText)
        sizer.Add(label, 0, wx.ALIGN_LEFT, 1)

        # Create the extension textctrl
        if self.edit != None:
            # Fetch current extension
            args = self.aliases[index][2]
        else:
            args = ""

        self.arguments = wx.TextCtrl(self, -1, args,
                                      size=(125, -1),
                                      style=wx.WANTS_CHARS)
        
        sizer.Add(self.arguments, 0, wx.ALIGN_LEFT, 1)
        
        self.doneButton = wx.Button(self, -1, "Add Alias", (310, 430))
        self.Bind(wx.EVT_BUTTON, self.addAndClose, self.doneButton)
        sizer.Add(self.doneButton, 0, wx.ALIGN_RIGHT, 1)

         # Set sizer
        superSizer.Add(sizer, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        self.SetSizer(superSizer)
        self.Fit()
        
        # Center the config window
        self.Center(wx.BOTH)
        # Going modal
        self.Show()


    def onAddProgram(self, event):
        """
        Method to add/edit the program associated with an alias
        Args:
          event = The button event

        Returns: None
        """

        fileFilter = "All files (*.*)|*.*"
        
        dlg = wx.FileDialog(self, message="Choose a program",
                            defaultDir=os.getcwd(), 
                            defaultFile="", wildcard=fileFilter,
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR)


        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
            self.setProgText(self.path)

        # Only destroy a dialog after you're done with it.
        dlg.Destroy()


    def setProgText(self, text):
        """
        Method to set the execution string
        Only show the last 29 chars.
        Args:
          text [STRING] = The path to the program or
                          string to be executed

        Returns: None
        """
                    
        self.progText.SetValue(text)
        

    def addAndClose(self, event=None):
        """
        Method to close config window
        Args:
          event = The close event

        Returns: None
        """
        
        # Fetch name
        name = self.nameCtrl.GetValue().strip()

        # The name has to be something..
        if len(name) == 0:
            dlg = InfoDialog(self, -1, "Add/Edit failed",
                             "Please supply a name for the alias.",
                             size=(350, 200),
                             style = wx.DEFAULT_DIALOG_STYLE)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            dlg.Destroy()
            # Don't exit
            return
            
        # Fetch exec string
        execString = self.progText.GetValue().strip()
        
        # Fetch arguments
        arguments = self.arguments.GetValue().strip()
        
        # Update alias
        if self.index != None:
            # we are editing an iem
            self.parent.aliases[self.index] = [name, execString,
                                            arguments]
        else:
            # A new alias
            self.parent.aliases.append([name, execString, arguments])

        # Save aliases
        self.parent.saveAliases()
        
        # Re-populate parent listctrl
        self.parent.populate()
        self.close()


    def close(self, event=None):
        """
        Method to close the dialog
        Args:
          event [OBJ] = The close event

        Returns: None
        """
        self.Destroy()