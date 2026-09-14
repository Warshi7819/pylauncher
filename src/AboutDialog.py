###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules

# Import wxpython modules
import wx
import wx.lib.agw.hyperlink as hl

# Import own modules
from Wizard import ALWizard


class AboutDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)

        # Fill in content
        sizer = wx.BoxSizer(wx.VERTICAL)
        aboutString = \
        """
        AL is an application distributed under the GPL license.
        It's main task is to help the user find and execute
        his/her applications more easily by suffix search rather     
        than manually browsing through the Start menu. Please
        visit our website for further information and updates:"""
        label = wx.StaticText(self, -1, aboutString)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        # Draw hyperlink at the bottom
        link = hl.HyperLinkCtrl(self, wx.ID_ANY,
                                "www.garageinnovation.org/AL",
                                URL="http://www.garageinnovation.org/AL")
        
        link.SetColours("BLUE", "BLUE", "BLUE")
        link.EnableRollover(True)
        link.SetUnderlines(False, False, True)
        link.SetBold(True)
        link.UpdateLink()

        sizer.Add(link, 0, wx.ALIGN_CENTRE, 5)
        
        # Add an empty string as a divider between the text
        # and the comming button
        aboutString = ""
        label = wx.StaticText(self, -1, aboutString)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        

        # Add wizard button
        wizButton = wx.Button(self, -1, "View ALs wizard")
        self.Bind(wx.EVT_BUTTON, self.onWizButton, wizButton)
        sizer.Add(wizButton, 0, wx.ALIGN_LEFT, 5)


        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


    def onWizButton(self, event):
        """
        Method to handle when the wiz button is pressed
        Args:
          event = The button event

        Retruns: None
        """
        wizard = ALWizard(self)
        wizard.runWizard()