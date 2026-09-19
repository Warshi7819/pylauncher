###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# This project depends on the following
# pip install pywin32
# pip install wxpython

# change directory to AL's directory so that relative
# paths work
import sys, os
al_dir = sys.argv[0]
if al_dir.rfind('\\') != -1:
    al_dir = al_dir[:al_dir.rfind('\\')]
    os.chdir(al_dir)

# So that plugins are able to load
# modules in src.
sys.path.append(os.getcwd())

# Import standard modules
import time
import queue
import os.path

# Import wxpython modules
import wx
from wx.lib.stattext import GenStaticText

# Import own modules
from Logger import Logger
from OwnConstants import *
from plugins.search import *
from GuiUtils import openAsBitmap, getSelected, rescaleBitmap
from Curry import curry
from Indexer import Indexer
from AppLauncher import AppLauncher
from AboutDialog import AboutDialog
from ConfigFrame import ConfigFrame
from Config import Config
from AlSplashScreen import AlSplashScreen
from IconExtractor import getIcon
from ApplicationList import ApplicationList
from Wizard import ALWizard
from ShellFolders import fetchShellFolders



class AlFrame(wx.Frame):
    """
    The Application Launcher AL
    """

    def __init__(self, parent):
        """
        Class constructor
        Args:
          parent = The parent window
        """
        
        # Load config
        self.logger = Logger()
        self.logger.info("Loading config")
        self.config = Config()
        
        # Initialize logger
        logFileName = os.path.join(self.config.config["appDataDir"], "al-log.dat")
        
        windowStyle = wx.FRAME_SHAPED | wx.SIMPLE_BORDER \
                      | wx.FRAME_NO_TASKBAR

        # Enable window on top?
        if self.config.config["ontop"]:
            windowStyle = windowStyle | wx.STAY_ON_TOP
            
        # Init frame
        wx.Frame.__init__(self, parent, -1, "Al 0.1", style = windowStyle)

        # Initializing the indexer
        self.queryQueue = queue.Queue(100)        
        self.indexer = Indexer(self, self.queryQueue, self.config)

        # Fire it up
        self.indexer.start()

        # Show splash screen
        splash = AlSplashScreen(self)

        # Load search plugins
        self.plugins = {}
        self.pluginMap = {}
        for plugin in searchPlugins:
            
            self.plugins[plugin] = eval("%s()" % plugin)
            self.pluginMap[self.plugins[plugin].getEnabler()] = plugin



        # Register hotkey
        self.RegisterHotKey(DISPLAY, self.config.config["hotkeys"][0],
                            self.config.config["hotkeys"][1])
        self.Bind(wx.EVT_HOTKEY, self.onHotKeyfunction, id=DISPLAY)

        # Bind needed events
        self.Bind(wx.EVT_PAINT,           self.onPaint)
        self.Bind(wx.EVT_CLOSE,           self.onCloseWindow)
        self.Bind(EVT_INSERT_APPLICATION, self.insertItem)

        
        # Center window on screen
        self.Move((0,0))
        self.Centre(wx.HORIZONTAL)

        # Set background image
        self.hasShape = False
        img_path = "images\\background-minimal-blue.bmp"
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

        # Set icon
        icon = getIcon(".exe")
        self.appIcon = wx.StaticBitmap(self, -1, icon, (8, 55),
                        (icon.GetWidth(), icon.GetHeight()))

        self.appIcon.SetBackgroundColour("#DDF2FF")
        self.appIcon.SetForegroundColour("#DDF2FF")
        
        self.label = GenStaticText(self, -1, '', wx.Point(28, 55),
                                   (180, 15), wx.ST_NO_AUTORESIZE)
        self.label.SetBackgroundColour("#DDF2FF")
        self.label.SetForegroundColour("#000000")
        self.label.SetLabel(" ...")
        
        # Create cursor to be used by all buttons
        cursor = wx.Cursor(wx.CURSOR_HAND)

        # Add about button
        aboutBmp = openAsBitmap("icons\\information.png")

        self.aboutButton = wx.BitmapButton(self, -1, aboutBmp, (220, 8),
                                            (aboutBmp.GetWidth(),
                                             aboutBmp.GetHeight()),
                                           wx.BU_EXACTFIT | wx.BORDER_NONE)
        self.aboutButton.SetToolTip("About AL")
        self.aboutButton.SetInitialSize(self.aboutButton.GetBestSize())
        self.aboutButton.SetBitmapFocus(aboutBmp)
        self.aboutButton.SetBitmapPressed(aboutBmp)
        self.aboutButton.SetBitmapDisabled(aboutBmp)
        self.aboutButton.SetCursor(cursor)
        self.aboutButton.SetBackgroundColour("#DDF2FF")
        self.Bind(wx.EVT_BUTTON, self.onShowAbout, self.aboutButton)

        
        # Add config button
        configBmp = openAsBitmap("icons/cog.png")
        configDownBmp = openAsBitmap("icons/cog.png")

        self.configButton = wx.BitmapButton(self, -1, configBmp, (8, 8),
                                            (configBmp.GetWidth(),
                                             configBmp.GetHeight()),
                                            wx.BU_EXACTFIT | wx.BORDER_NONE)
        
        self.configButton.SetToolTip("Configure AL")
        self.configButton.SetInitialSize(self.configButton.GetBestSize())
        self.configButton.SetBitmapFocus(configBmp)
        self.configButton.SetBitmapPressed(configBmp)
        self.configButton.SetBitmapDisabled(configBmp)
        self.configButton.SetCursor(cursor)
        self.configButton.SetBackgroundColour("#DDF2FF")
        self.Bind(wx.EVT_BUTTON, self.onShowConfig, self.configButton)



        # Add exit button
        exitBmp = openAsBitmap("icons/exit.png")
        exitDownBmp = openAsBitmap("icons/exit_down.png")

        self.exitButton = wx.BitmapButton(self, -1, exitBmp, (220, 49),
                                          (exitBmp.GetWidth(),
                                           exitBmp.GetHeight()),
                                          wx.BU_EXACTFIT | wx.BORDER_NONE)
        
        self.exitButton.SetToolTip("Quit AL")
        self.exitButton.SetInitialSize(self.exitButton.GetBestSize())
        self.exitButton.SetBitmapFocus(exitBmp)
        self.exitButton.SetBitmapPressed(exitDownBmp)
        self.exitButton.SetBitmapDisabled(exitBmp)
        self.exitButton.SetCursor(cursor)
        self.exitButton.SetBackgroundColour("#DDF2FF")
        self.Bind(wx.EVT_BUTTON, self.onCloseWindow, self.exitButton)

        # Set icon to be used by sub-dialogs and frames
        self.icon = wx.Icon("images\\al_icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        
        # Create the search TextCtrl
        self.inputField = wx.TextCtrl(self, -1, "",
                                      size=(125, -1),
                                      pos=(60, 27),
                                       style=wx.WANTS_CHARS | wx.TE_PROCESS_ENTER)
        
        wx.CallAfter(self.inputField.SetInsertionPoint, 0)
        # Bind key down events so that I can trap the tab key event
        self.inputField.Bind(wx.EVT_KEY_DOWN, self.changeFocus)

        # Bind key up events because we want to catch the esc key when
        # it's pressed
        self.inputField.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        
        # Bind EVT_TEXT and perform search on every character entered
        self.Bind(wx.EVT_TEXT, self.performSearch, self.inputField)
        # Bind enter button to execute program
        self.inputField.Bind(wx.EVT_TEXT_ENTER, self.executeProgram)

        # Create the application list
        self.applicationList = ApplicationList(self, self.config)

        
        # Display wizard if the config says so
        if self.config.config["wizard"]:
            wizard = ALWizard(self)
            wizard.runWizard()
            # Do not display wizard in the future
            self.config.config["wizard"] = False

    def changeFocus(self, event=None):
        """
        Method to control keyboard focus
        Args:
          event = key event
          
        Returns: None
        """

        # if the TAB key has been pressed, change focus
        # of if the up/down key is pressed change focus
        # to appList if the input field has focus
        keyCode = event.GetKeyCode()
        if keyCode in [9, 317, 319]:
            widget = self.FindFocus()
            if widget == None:
                self.inputField.SetFocus()
                # Hide application list?
                if not self.config.config["alwaysSearchWindow"]:
                    self.applicationList.toggleWindow(False)
                
            elif widget == self.applicationList.appList:
                if not keyCode in [317, 319]:
                    self.inputField.SetFocus()
                    # Hide application list
                    if not self.config.config["alwaysSearchWindow"]:
                        self.applicationList.toggleWindow(False)
                else:
                    event.Skip()
            else:
                # Show application list
                self.applicationList.appList.SetFocus()
                if not self.config.config["alwaysSearchWindow"]:
                    self.applicationList.toggleWindow(True)
                    
        elif keyCode == 27:
            # Catch esc key down and do nothing
            pass
        else:
            event.Skip()


    def onKeyDown(self, event):
        """
        Method to catch the esc key when it's pressed and skip it
        Args:
          event = The key event

        Returns: None
        """
        if event.GetKeyCode() == 27:
            # Catch esc key down and do nothing
            pass
        else:
            event.Skip()

    def onKeyUp(self, event):
        """
        Method to catch when the esc key is released and hide AL
        Args:
          event = The key event

        Returns: None
        """
        if event.GetKeyCode() == 27:
            # Catch esc key
            self.applicationList.toggleWindow(False)
            self.toggleWindow()
        else:
            event.Skip()

            
    def executeProgram(self, event):
        """
        Method to execute the currently seledted item
        Args:
          event = The key event

        Returns: None
        """
        selected = getSelected(self.applicationList.appList)
        searchString = self.inputField.GetLabel().lower()
        
        if selected:
            try:
                searchChar = searchString[0:1]
                key = int(selected[0])
                command = self.indexer.getExecutionString(key, searchChar)
                appLaunch = AppLauncher(command)
                appLaunch.start()

            except Exception as e:
                pass

        else:
            self.executeSearchPlugin(searchString)

        self.applicationList.toggleWindow(False)
        self.toggleWindow()



    def executeSearchPlugin(self, searchString):
        """
        Method to match search towards available search plugins
        Args:
          searchString = The search string supplied by the user

        Returns: None
        """

        searchString = searchString.strip()
        index = searchString.find(":")
        if index > 0:
            searchEnabler = searchString[:index]
            if searchEnabler in self.pluginMap:
                self.plugins[self.pluginMap[searchEnabler]].executeSearch(searchString)
                
    
    def insertItem(self, event):
        """
        Method to insert an item into the application list
        Args:
          item = The string to insert
          key = The position

        Returns: None
        """
        item, execString, alias = event.item
        key = event.key

        if key == -1:
            # Clear list
            self.applicationList.appList.ClearAll()
            self.applicationList.appList.InsertColumn(0, "")
            self.applicationList.appList.SetColumnWidth(0, 235)
            self.appIcon.SetBitmap(getIcon(".exe"))
            self.appIcon.SetToolTip(wx.ToolTip(""))
            self.label.SetLabel(" ...")

        elif key == -2:
            # This is a query that probably matches a search plugin
            # Clear app list
            self.applicationList.appList.ClearAll()
            self.applicationList.appList.InsertColumn(0, "")
            self.applicationList.appList.SetColumnWidth(0, 235)
            # Display correct icon and label text
            self.matchSearchPlugin(execString)
            
        else:
            li = wx.ListItem()
            li.SetText(item)
            li.SetId(self.applicationList.appList.GetItemCount())
            index = self.applicationList.appList.InsertItem(li)
            self.applicationList.appList.SetItem(index, 0, item)
            self.applicationList.appList.SetItemData(index, key)
            
            if key == 0:
                # Default select topmost item
                self.applicationList.appList.Select(0)
                if alias:
                    self.appIcon.SetBitmap(getIcon(".exe"))
                    tooltip = wx.ToolTip("execute: %s" % " ".join(execString))
                    self.appIcon.SetToolTip(tooltip)
                else:
                    self.appIcon.SetBitmap(getIcon(execString))
                    tooltip = wx.ToolTip("execute: %s" % execString)
                    self.appIcon.SetToolTip(tooltip)

                self.label.SetLabel(item)


    def performSearch(self, event):
        """
        Method to perform search and populate applicationList
        Also test if it matches one of the searchPlugins. If it does no
        matches will be returned from our suffixtree so display the
        given searhplugin icon and the text as you write it
        Args:
          event =

        Returns: None
        """
        self.queryQueue.put(event.GetString())


    def matchSearchPlugin(self, searchString):
        """
        If this search triggers a search plugin display the
        icon associated to that search plugin and the text
        already typed in by the user
        Args:
          searchString = The query the user has entered

        Returns: None
        """
        
        searchString = searchString.strip()
        index = searchString.find(":")
        
        if index > 0:
            # Find the search enabler
            searchEnabler = searchString[:index]
            if searchEnabler in self.pluginMap:
                iconPath = self.plugins[self.pluginMap[searchEnabler]].getIcon()
                if iconPath != None:
                    # display icon
                    icon = openAsBitmap(iconPath)
                    icon = rescaleBitmap(icon)
                    self.appIcon.SetBitmap(icon)
                    self.appIcon.SetToolTip(wx.ToolTip(self.plugins[self.pluginMap[searchEnabler]].getShortDescription()))
                    
                # Display written text, but not the search plugin enabler.
                self.label.SetLabel(searchString[index+1:])

        
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


    def toggleWindow(self, event=None):
        """
        Method to toggel parent visibility
        Args:
          event = (opt) wxPython event
        """
        
        if self.IsShown():
            self.Hide()
            self.applicationList.toggleWindow(False)
            self.inputField.Clear()
        else:
            self.Show()
            self.Raise()
            self.inputField.SetFocus()
            

    def onHotKeyfunction(self, event):
        """
        Method to handle hotkey events
        Args:
          event = wxPython hotkey event

        Returns: None
        """

        id = event.GetId()
        
        if id == DISPLAY:
            # Figure out if resultlist should be shown
            if self.config.config["alwaysSearchWindow"]:
                if self.IsShown():
                    self.applicationList.toggleWindow(False)
                else:
                    self.applicationList.toggleWindow(True)
            # Show AL
            self.toggleWindow()

            
    def onShowAbout(self, event):
        """
        Method called when the about button is pressed
        Args:
          event = The button event

        Returns: None
        """
        dlg = AboutDialog(self, -1, "About AL %s" % APP_VERSION,
                          size=(350, 200),
                          style = wx.DEFAULT_DIALOG_STYLE)
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        dlg.Destroy()
        

    def onShowConfig(self, event):
        """
        Method called when the configuration button is pressed
        Args:
          event = The button event

        Returns: None
        """
        confW = ConfigFrame(self)


    def onCloseWindow(self, event):
        """
        Method called when exiting application. Time to tidy up
        some loose ends.
        Args:
          event = The

        Returns: None
        """
        self.logger.info("Shutting down..")
        
        busy = wx.BusyInfo("Shutting down AL..")
        wx.Yield()

        self.indexer.stop()
        self.config.saveConfig()
        
        self.Destroy()


class Al(wx.App):
    """Main wxPython application class for AL."""

    def __init__(self, redirect=False, filename=None):
        """
        Initialize the application.
        Args:
          redirect = Redirect stdout/stderr to file
          filename = The filename to redirect to
        """
        wx.App.__init__(self, redirect, filename)
        
    
    def OnInit(self):
        """
        Called on application initialization.
        Args: None

        Returns: [BOOLEAN] True if initialization succeeded
        """
        frame = AlFrame(None)
        return True


if __name__ == "__main__":
    # Start an instance of AL only if none
    # already exists. 
    appName = "AL - Application Launcher"

    # Using username in name so different user may
    # run AL on the same machine. If it's defined that is..
    if "USERNAME" in os.environ:
        appName += " user: %s" % os.environ["USERNAME"] 
    
    singleInstanceChecker = wx.SingleInstanceChecker(appName)
    if not singleInstanceChecker.IsAnotherRunning():
        # Figure out where the appdata dir is
        shellFolders = fetchShellFolders()
        logFile = os.path.join(shellFolders["AppData"][0],
                               "AL_log.txt")
        
        app = Al(redirect=False)
        app.MainLoop()
    else:
        print("Another instance of this program is already running. Aborting..")