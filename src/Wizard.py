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
from wx.adv import WizardPageSimple, Wizard
import wx.lib.agw.hyperlink as hl

# Import own modules
from OwnConstants import *
from GuiUtils import openAsBitmap


class TitledPage(WizardPageSimple):
    """
    Class that implements a simple titled wizard page
    """
    
    def __init__(self, parent, title):
        """
        Class constructor
        Args:
          parent = The parent window
          title = The title of the page
        """
        WizardPageSimple.__init__(self, parent)
        self.sizer = self.makePageTitle(self, title)

    def makePageTitle(self, wizPg, title):
        """
        Method to create the titled page
        Args:
          wizPg = The wizard page
          title = The title of the page

        Returns: [SIZER] The page sizer
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        wizPg.SetSizer(sizer)
        title = wx.StaticText(wizPg, -1, title)
        title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
        return sizer
    

class ALWizard:
    """
    Class implementing the AL wizard
    """
    
    def __init__(self, parent):
        """
        Class constructor
        Args:
          parent = The parent window
        """
        self.parent = parent



    def runWizard(self):
        """
        Method to run the AL wizard
        Args:
          None

        Returns: None
        """

        bmp = openAsBitmap("images\\wizard.bmp")

        wizard = Wizard(self.parent, -1, "AL Wizard", bmp)
        page1 = TitledPage(wizard, "Usage")
        page2 = TitledPage(wizard, "Searching")
        page3 = TitledPage(wizard, "Summary")
        page4 = TitledPage(wizard, "Configuration")
        page5 = TitledPage(wizard, "Credits")
        self.page1 = page1

        # PAGE 1 USAGE
        page1.sizer.Add(wx.StaticText(page1, -1, """
This wizard will show you how to use AL. Let's start by bringing
AL out of hiding. Hold down the 'alt' key and gently tap the space
key. To hide AL again follow the same procedure or press the esc key.
Next page will instruct you how to search for and execute the desired
application"""))
        wizard.FitToPage(page1)

        # PAGE 2 SEARCHING
        page2.sizer.Add(wx.StaticText(page2, -1, """
We will use the power of a simple example to train you in using AL.
In this example we will fire up Microsofts number one editor namely
Wordpad. Bring AL out from hiding and start by typing the character w.
AL will now fetch all applications available that contains an w
character in its name. Press the tab key to view all results. There
probably are quite a few results displayed. Press the tab key again so
that ALs main window again gains focus. Continue slowly typing the
remaining charcters of the application name namely ordpad. AL will
narrow down the search as you type. The first hit on the list is always
displayed in the lower left corner of the main window. To start the
first hit just press enter. If the first hit is not the correct one
press the tab key to display all results. Select the correct application
and press enter to start it."""))
        wizard.FitToPage(page2)

        # PAGE 3 SUMMARY
        page3.sizer.Add(wx.StaticText(page3, -1, """
Now you have learnd enough to start using AL. Here is a quick
summary:

1) Hold down the alt key and tap space to show/hide AL
2) When AL is shown just start typing the name of the application
   you want to start.
3) Use the tab key to show all results if the fist hit shown in the
   lower left corner of the main window is not the correct one
4) Press enter to execute the selected application

For your convinience AL learns, so the more you use it the more precise
the search results will be.

"""))
        wizard.FitToPage(page3)

        # PAGE 4 CONFIGURATION
        page4.sizer.Add(wx.StaticText(page4, -1, """
To configure AL press the cog icon in the upper left corner. Here you
can configure the data that should be searchable and some of ALs
user interface options like always ontop and the hotkeys used (default
'alt' 'space'). For updates please visit our project which is hosted
at SourceForge:
"""))


        link = self.createHyperlink(page4, "AL at SourceForge",
                                    "http://sourceforge.net/projects/launcher")

        page4.sizer.Add(link, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        wizard.FitToPage(page4)

        # PAGE 5 CREDITS
        label = """
Developers:
  - Rune Devik
  - Kjetil Jacobsen

Logo, Splashscreen:"""
        
        page5.sizer.Add(wx.StaticText(page5, -1, label))

        link = self.createHyperlink(page5, "  - Geekcorp Software",
                                    "http://www.geekcorp.com")
        page5.sizer.Add(link)

        label = """
Front panel Icons:"""
        page5.sizer.Add(wx.StaticText(page5, -1, label))
        link = self.createHyperlink(page5, "  - FAM FAM FAM",
                                    "http://www.famfamfam.com/lab/icons/silk")
        page5.sizer.Add(link)
        
        label = """
Testers:
  - Vegar     - Sveinar 
  - Jorgen    - Stig Petter
"""

        page5.sizer.Add(wx.StaticText(page5, -1, label))



        # Use the Chain function to connect the pages
        page1.Chain(page2).Chain(page3).Chain(page4).Chain(page5)

        # Run the wizard
        wizard.RunWizard(page1)


    def createHyperlink(self, window, title, url):
        """
        Method to create a hyperlink
        Args:
          window = The parent window
          title = The title of the url
          url = The url itself

        Returns: [HYPERLINK] The hyperlink created
        """
        # Draw hyperlink to sourceforge
        link = hl.HyperLinkCtrl(window, wx.ID_ANY,
                                title,
                                URL=url)
        
        link.SetColours("BLUE", "BLUE", "BLUE")
        link.EnableRollover(True)
        link.SetUnderlines(False, False, True)
        link.SetBold(True)
        link.UpdateLink()

        return link