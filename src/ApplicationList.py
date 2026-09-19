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
from GuiUtils import openAsBitmap


class ApplicationList(wx.Frame):
    """Frame that displays the list of applications matching the search."""

    def __init__(self, parent, config):
        """
        Class constructor
        Args:
          parent = The parent window
        """
        self.parent = parent
        self.config = config
        
        windowStyle = wx.FRAME_SHAPED | wx.SIMPLE_BORDER
        if self.config.config["ontop"]:
            windowStyle = windowStyle | wx.STAY_ON_TOP
        
        wx.Frame.__init__(self, self.parent, -1, "ApplicationList",
                          style = windowStyle)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        # Fix shaped window
        self.hasShape = False
        img_path = "images\\background-minimal-blue-results.bmp"
        self.background = openAsBitmap(img_path)
        w, h = self.background.GetWidth(), self.background.GetHeight()
        self.SetClientSize((w, h))

        if wx.Platform == "__WXGTK__":
            # wxGTK requires that the window be created before you can
            # set its shape, so delay the call to SetWindowShape until
            # this event.
            self.Bind(wx.EVT_WINDOW_CREATE, self.setWindowShape)
        else:
            # On wxMSW and wxMac the window has already been created,
            # so go for it.
            self.setWindowShape()
            
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.background, 0,0, True)


        self.appList = wx.ListCtrl(self, -1, size = (237,185),
                                   pos = (7,7),
                                   style=wx.LC_REPORT \
                                   | wx.BORDER_NONE \
                                   | wx.LC_SINGLE_SEL)

        self.appList.InsertColumn(0, "")
        self.appList.SetColumnWidth(0, 235)

        # Bind list events
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.parent.executeProgram,
                  self.appList)
        
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.onColBeginDrag,
                  self.appList)

        # Bind key down/up events so that I can trap the tab key event
        # and the esc key
        self.appList.Bind(wx.EVT_KEY_DOWN, self.parent.changeFocus)
        self.appList.Bind(wx.EVT_KEY_UP, self.parent.onKeyUp)
        self.Bind(wx.EVT_KEY_DOWN, self.parent.onKeyUp)
        self.Bind(wx.EVT_KEY_UP, self.parent.onKeyDown)

        # Center window on screen
        self.CentreOnParent(wx.BOTH)
        
        pos = self.GetPosition()
        self.SetPosition((pos[0], pos[1]+90))


    def onColBeginDrag(self, event):
        """
        Method that prevents resizing of columns
        Args:
          event = The column drag event

        Returns: None
        """
        # Do not allow resizing colum
        if event.GetColumn() == 0:
            event.Veto()


    def setWindowShape(self, *evt):
        """
        Method to set the window shape
        Args:
          evt = The event

        Returns: None
        """
        
        # Use the bitmap's mask to determine the region
        r = wx.Region(self.background)
        self.hasShape = self.SetShape(r)


    def onPaint(self, evt):
        """
        Method to handle paint event
        Args:
          evt = The paint event

        Returns: None
        """
        
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.background, 0,0, True)


    def toggleWindow(self, visible):
        """
        Method to toggle window on off
        Args:
          visible = If True show window. Otherwise hide it

        Returns: None
        """
        if visible:
            self.Show()
        else:
            self.Hide()