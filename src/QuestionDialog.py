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


class QuestionDialog(wx.Dialog):
    """Dialog that displays a question and waits for user confirmation."""

    def __init__(self, parent, ID, title, question,size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):
        """
        Initialize the question dialog.
        Args:
          parent = The parent window
          ID = The dialog ID
          title = The dialog title
          question = The question to display
          size = The dialog size
          pos = The dialog position
          style = The dialog style
        """
        
        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)

        # Fill in content
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, question)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)