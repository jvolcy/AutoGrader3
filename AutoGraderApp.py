from IAGConstant import IAGConstant
from console import console
# from AutoGrader3 import AutoGrader3
# import GradingEngine


autoGrader =  None
APP_NAME = "Spelman AutoGrader 3"
VERSION = "pre 3.0.0"
COPYRIGHT_TEXT = "copyright 2016-2020"
CREDITS = "J Volcy"
'''
appName = "Spelman AutoGrader 3"
version = "pre 3.0.0"
copyrightText = "copyright 2016-2020"
credits = "J Volcy"
'''

# from tkinter import *
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font

class Controller(IAGConstant):

    # =======================================================================
    # static class of enumerated button image types
    # ======================================================================
    class WIDGET_CLR(object):
        CLEAR = 0
        LIGHT_GRAY = 1
        LIGHT_BLUE = 2
        BLUE_GRAY = 3

    # class constants
    MAIN_WND_MIN_WIDTH = 600
    MAIN_WND_MIN_HEIGHT = 440

    # =======================================================================
    #
    #
    # ======================================================================
    def makeWidgetImage(self, width, height, widgetClr=WIDGET_CLR.CLEAR):
        if widgetClr == self.WIDGET_CLR.LIGHT_GRAY:
            # request for light gray button
            return self.__lightGrayPixelImg.zoom(width, height)
        elif widgetClr == self.WIDGET_CLR.LIGHT_BLUE:
            # request for light blue button
            return self.__lightBluePixelImg.zoom(width, height)
        elif widgetClr == self.WIDGET_CLR.BLUE_GRAY:
            #request for light blue gray
            return self.__blueGrayPixelImg.zoom(width, height)
        else:
            # default: return clear button
            return self.__clearPixelImg.zoom(width, height)


    # =======================================================================
    #
    #
    # ======================================================================
    def __buildMenuFrame(self):
        self.__menubar = Menu(self.__frameMenu)
        self.__filemenu = Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="New", command=None)
        self.__filemenu.add_command(label="Open", command=None)
        self.__filemenu.add_command(label="Save", command=None)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Exit", command=self.mainWindow.quit)
        self.__menubar.add_cascade(label="File", menu=self.__filemenu)

        self.__helpmenu = Menu(self.__menubar, tearoff=0)
        self.__helpmenu.add_command(label="Help Index", command=None)
        self.__helpmenu.add_command(label="About...", command=None)
        self.__menubar.add_cascade(label="Help", menu=self.__helpmenu)

        self.mainWindow.config(menu=self.__menubar)

        self.btnSettings = Button(self.__frameMenu, fg='black', text="0. Settings", image=self.imgBtn_85x30, compound="center", command=self.__btnSettingClick)
        self.btnSettings.pack(side='left')

        self.btnInput = Button(self.__frameMenu, fg='black', text="1. Input/Setup", image=self.imgBtn_100x30, compound="center", command=self.__btnInputClick)
        self.btnInput.pack(side='left')

        self.btnOutput = Button(self.__frameMenu, fg='black', text="2. Output", image=self.imgBtn_76x30, compound="center", command=self.__btnOutputClick)
        self.btnOutput.pack(side='left')

        self.btnConsole = Button(self.__frameMenu, fg='blue', text="Console", image=self.imgBlueBtn_76x30, compound="center")
        self.btnConsole.pack(side='left')

    # =======================================================================
    #
    #
    # ======================================================================
    def __buildMainFrames(self):
        # build Settings frame
        #TEMP self.__buildSettingsFrame()

        # build Input frame
        #TEMP self.__buildInputFrame()

        # build Output frame
        self.__buildOutputFrame()

        # build Console frame
        # build Help frame



    # =======================================================================
    #
    #
    # ======================================================================
    def __buildStatusFrame(self):
        self.imgLblReady = self.makeWidgetImage(100, 27, self.WIDGET_CLR.BLUE_GRAY)
        self.lblReady = Label(self.__frameStatus, fg='black', text='Ready', image=self.imgLblReady, compound='center', borderwidth=0, padx=0, pady=0)
        self.lblReady.pack(side='left')

        self.lblMessage = Label(self.__frameStatus, bg='#e8e8ff', fg='blue', text='AutoGrader 2.X', borderwidth=0, padx=0, pady=0)
        self.lblMessage.pack(fill=X, expand=True, side='left')

        self.imgLblLanguage = self.makeWidgetImage(120, 27, self.WIDGET_CLR.BLUE_GRAY)
        self.lblLanguage = Label(self.__frameStatus, fg='purple', text='Auto', image=self.imgLblLanguage, compound='center', borderwidth=0, padx=0, pady=0)
        self.lblLanguage.pack(side='left')


    # =======================================================================
    # The settings frame consists of 9 sub "entry frames".  Each of these contains
    # a label and some sort of input widget.  The labels are all 240 pixels wide
    #
    # ======================================================================
    def __buildSettingsFrame(self):
        self.__settingsFrame = Frame(self.__frameMain, bg='#f0f0f0')
        self.__settingsFrame.place(x=24, y=0)
        #self.imgEntryLabel = self.makeWidgetImage(240, 27, self.WIDGET_CLR.LIGHT_GRAY)

        settingLabels = ['Language', 'Max Run Time, sec (0 = no limit)', 'Limit output to this many lines:',
                         'Include source listing in output', 'Auto-uncompress zip files',
                         'Process recursively', 'Python 3 interpreter', 'C++ compiler', 'Shell interpreter']

        self.__entryFrames = []    # list to contain entry frames
        for i in range(9):
            self.__entryFrames.append(Frame(self.__settingsFrame, bg='#f0f0f0', width=552, height=27, highlightthickness=1, highlightbackground='lightgray', relief='flat'))
            self.__entryFrames[i].pack(side='top', pady=4, ipady=2)
            #Label(self.__entryFrames[i], text=settingLabels[i], image=self.imgEntryLabel, bg='#f0f0f0', borderwidth=0, compound='center').place(x=0, y=0) #pack(side='left')
            Label(self.__entryFrames[i], text=settingLabels[i], bg='#f0f0f0', borderwidth=0).place(x=0, y=4, width=240) #pack(side='left')


        # now, individually create the different entry widgets

        # 0 'Language'
        self.comboLanguage = ttk.Combobox(self.__entryFrames[0], values=[ "Auto", "Python 3", "C++"])
        self.comboLanguage.place(x=244, y=2, width=200)

        # 1 'Max Run Time, sec (0 = no limit)'
        self.spinMaxRun = Spinbox(self.__entryFrames[1], from_=0, to=1000, highlightthickness=1, highlightbackground='lightgray', relief='flat')
        self.spinMaxRun.place(x=244, y=2, width=200)

        # 2 'Limit output to this many lines:'
        self.spinMaxOutputLines = Spinbox(self.__entryFrames[2], from_=1, to=10000, highlightthickness=1, highlightbackground='lightgray', relief='flat')
        self.spinMaxOutputLines.place(x=244, y=2, width=200)

        # 3 'Include source listing in output'
        self.comboOutputSource = ttk.Combobox(self.__entryFrames[3], values=[ "Yes", "No"])
        self.comboOutputSource.place(x=244, y=2, width=200)

        # 4 'Auto-uncompress zip files'
        self.comboAutoUncompress = ttk.Combobox(self.__entryFrames[4], values=[ "Yes", "No"])
        self.comboAutoUncompress.place(x=244, y=2, width=200)

        # 5 'Process recursively'
        #self.__entryFrames[5].option_add("*TCombobox*Listbox*Background", 'green')
        #self.__entryFrames[5].option_add("*TCombobox*background", 'red')
        self.comboProcessRecursively = ttk.Combobox(self.__entryFrames[5], values=[ "Yes", "No"])
        self.comboProcessRecursively.place(x=244, y=2, width=200)

        # 6 'Python 3 interpreter'
        self.pythonInterpreter = StringVar(self.__entryFrames[6], value='---')
        self.__entryPythonInterpreter =  Entry(self.__entryFrames[6], textvariable=self.pythonInterpreter)
        self.__entryPythonInterpreter.place(x=244, y=0, width=304) #pack(expand=True, fill='both')  # .pack(side='left', expand=False, fill="x")

        # 7 'C++ compiler'
        self.cppCompiler = StringVar(self.__entryFrames[7], value='---')
        self.__entryCppCompiler =  Entry(self.__entryFrames[7], textvariable=self.cppCompiler)
        self.__entryCppCompiler.place(x=244, y=0, width=304) #pack(expand=True, fill='both')  # .pack(side='left', expand=False, fill="x")

        # 8 'Shell interpreter'
        self.shell = StringVar(self.__entryFrames[8], value='---')
        self.__entryShell = Entry(self.__entryFrames[8], textvariable=self.shell)
        self.__entryShell.place(x=244, y=0, width=304) #.pack(side="left",fill="x", expand=False, ipady=3, ipadx=3) #.pack(side='left', expand=False, fill="x")


    # =======================================================================
    #
    #
    # ======================================================================
    def __buildInputFrame(self):
        self.__inputFrame = Frame(self.__frameMain, bg='#f0f0f0')
        self.__inputFrame.pack(expand=True, fill='both') #place(x=0, y=0, width=400)

        self.btnStart = Button(self.__inputFrame, fg='blue', text="Start", image=self.imgBtn_100x50, compound="center", command=None)
        self.btnStart.place(x=454, y=67)

        self.btnSourceDir = Button(self.__inputFrame, fg='black', text="Source Directory", image=self.imgBtn_150x30, compound="center", command=None)
        self.btnSourceDir.place(x=39, y=28)

        self.sourceDir = StringVar(self.__inputFrame, value='---')
        self.__entrysourceDir =  Entry(self.__inputFrame, textvariable=self.sourceDir)
        self.__entrysourceDir.place(x=200, y=31, width=360)

        self.btnTestAdd = Button(self.__inputFrame, fg='black', text="Add", image=self.imgBtn_76x30, compound="center", command=None)
        self.btnTestAdd.place(x=39, y=136)

        self.btnTestRemove = Button(self.__inputFrame, fg='black', text="Remove", image=self.imgBtn_76x30, compound="center", command=None)
        self.btnTestRemove.place(x=39, y=170)

        self.btnDataAdd = Button(self.__inputFrame, fg='black', text="Add", image=self.imgBtn_76x30, compound="center", command=None)
        self.btnDataAdd.place(x=39, y=252)

        self.btnDataRemove = Button(self.__inputFrame, fg='black', text="Remove", image=self.imgBtn_76x30, compound="center", command=None)
        self.btnDataRemove.place(x=39, y=286)

        # Add list boxes
        self.listTestData = Listbox(self.__inputFrame, selectmode=EXTENDED, height=5)
        self.listTestData.place(x=134, y=128, width=420)

        self.listDataFiles = Listbox(self.__inputFrame, selectmode=EXTENDED, height=4)
        self.listDataFiles.place(x=134, y=243, width=420)

        # Add misc anonymous labels
        Label(self.__inputFrame, bg='#f0f0f0', fg='black', text='Test Data', borderwidth=0, padx=0, pady=0, font = ("helvetica", 14, "bold italic")).place(x=42, y=116)
        Label(self.__inputFrame, bg='#f0f0f0', fg='black', text='Data Files', borderwidth=0, padx=0, pady=0, font = ("helvetica", 14, "bold italic")).place(x=39, y=232)
        Label(self.__inputFrame, bg='#f0f0f0', fg='black', text='Test data files substitute for keyboard inputs to the programs under test.', borderwidth=0, padx=0, pady=0, font = ("helvetica", 12, "italic")).place(x=139, y=215)
        Label(self.__inputFrame, bg='#f0f0f0', fg='black', text='Data files are files that may need to be read by the programs under test.', borderwidth=0, padx=0, pady=0, font = ("helvetica", 12, "italic")).place(x=139, y=315)

    # =======================================================================
    #
    #
    # ======================================================================
    def __buildOutputFrame(self):
        self.__outputFrame = Frame(self.__frameMain, bg='#f0f0f0')
        self.__outputFrame.pack(expand=True, fill=BOTH) #place(x=0, y=0, width=400)
        #self.__outputFrame.place(x=0, y=0)

        # ---------- create the main output window frames ----------
        self.__outputFrameTop = Frame(self.__outputFrame, bg='#f0f0f0', height=30, borderwidth=0, relief=None)
        self.__outputFrameMiddle = Frame(self.__outputFrame, bg='#f0f0f0', borderwidth=0, relief='groove')
        self.__outputFrameBottom = Frame(self.__outputFrame,  bg='#f0f0f0', height=30, borderwidth=0, relief=None)

        # Top Frame:  <<Prev / Student Name / Next >>
        self.btnPrev = Button(self.__outputFrameTop, fg='black', text="<< Prev", image=self.imgBtn_100x30, compound="center", command=None)
        self.btnPrev.pack(side=LEFT)

        self.comboStudent = ttk.Combobox(self.__outputFrameTop, values=[], width=30)
        self.comboStudent.pack(side=LEFT)

        self.btnNext = Button(self.__outputFrameTop, fg='black', text="Next >>", image=self.imgBtn_100x30, compound="center", command=None)
        self.btnNext.pack(side=LEFT)

        # Middle Frame (Web View)

        # Bottom Frame:  View Summary/View Report
        self.btnSummaryReport = Button(self.__outputFrameBottom, fg='black', text="View Summary", image=self.imgBtn_150x30, compound="center", command=None)
        self.btnSummaryReport.pack(side=LEFT)



        # ---------- pack in the main window frames ----------
        self.__outputFrameTop.pack(fill=None, expand=False, side=TOP)
        self.__outputFrameMiddle.pack(fill=BOTH, expand=True, side=TOP)
        self.__outputFrameBottom.pack(fill=None, expand=False, side=TOP)

    # =======================================================================
    #
    #
    # ======================================================================
    def __init__(self):
        # ---------- defint pixel images ----------
        # Base64 image encodings from https://www.base64-image.de
        self.__clearPixelData = '''iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAEGWlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPrtzZyMkzlNsNIV0qD8NJQ2TVjShtLp/3d02bpZJNtoi6GT27s6Yyc44M7v9oU9FUHwx6psUxL+3gCAo9Q/bPrQvlQol2tQgKD60+INQ6Ium65k7M5lpurHeZe58853vnnvuuWfvBei5qliWkRQBFpquLRcy4nOHj4g9K5CEh6AXBqFXUR0rXalMAjZPC3e1W99Dwntf2dXd/p+tt0YdFSBxH2Kz5qgLiI8B8KdVy3YBevqRHz/qWh72Yui3MUDEL3q44WPXw3M+fo1pZuQs4tOIBVVTaoiXEI/MxfhGDPsxsNZfoE1q66ro5aJim3XdoLFw72H+n23BaIXzbcOnz5mfPoTvYVz7KzUl5+FRxEuqkp9G/Ajia219thzg25abkRE/BpDc3pqvphHvRFys2weqvp+krbWKIX7nhDbzLOItiM8358pTwdirqpPFnMF2xLc1WvLyOwTAibpbmvHHcvttU57y5+XqNZrLe3lE/Pq8eUj2fXKfOe3pfOjzhJYtB/yll5SDFcSDiH+hRkH25+L+sdxKEAMZahrlSX8ukqMOWy/jXW2m6M9LDBc31B9LFuv6gVKg/0Szi3KAr1kGq1GMjU/aLbnq6/lRxc4XfJ98hTargX++DbMJBSiYMIe9Ck1YAxFkKEAG3xbYaKmDDgYyFK0UGYpfoWYXG+fAPPI6tJnNwb7ClP7IyF+D+bjOtCpkhz6CFrIa/I6sFtNl8auFXGMTP34sNwI/JhkgEtmDz14ySfaRcTIBInmKPE32kxyyE2Tv+thKbEVePDfW/byMM1Kmm0XdObS7oGD/MypMXFPXrCwOtoYjyyn7BV29/MZfsVzpLDdRtuIZnbpXzvlf+ev8MvYr/Gqk4H/kV/G3csdazLuyTMPsbFhzd1UabQbjFvDRmcWJxR3zcfHkVw9GfpbJmeev9F08WW8uDkaslwX6avlWGU6NRKz0g/SHtCy9J30o/ca9zX3Kfc19zn3BXQKRO8ud477hLnAfc1/G9mrzGlrfexZ5GLdn6ZZrrEohI2wVHhZywjbhUWEy8icMCGNCUdiBlq3r+xafL549HQ5jH+an+1y+LlYBifuxAvRN/lVVVOlwlCkdVm9NOL5BE4wkQ2SMlDZU97hX86EilU/lUmkQUztTE6mx1EEPh7OmdqBtAvv8HdWpbrJS6tJj3n0CWdM6busNzRV3S9KTYhqvNiqWmuroiKgYhshMjmhTh9ptWhsF7970j/SbMrsPE1suR5z7DMC+P/Hs+y7ijrQAlhyAgccjbhjPygfeBTjzhNqy28EdkUh8C+DU9+z2v/oyeH791OncxHOs5y2AtTc7nb/f73TWPkD/qwBnjX8BoJ98VQNcC+8AAAALSURBVAgdY2AAAgAABQABjbub8wAAAABJRU5ErkJggg=='''
        self.__lightGrayPixelData = '''iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAEGWlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPrtzZyMkzlNsNIV0qD8NJQ2TVjShtLp/3d02bpZJNtoi6GT27s6Yyc44M7v9oU9FUHwx6psUxL+3gCAo9Q/bPrQvlQol2tQgKD60+INQ6Ium65k7M5lpurHeZe58853vnnvuuWfvBei5qliWkRQBFpquLRcy4nOHj4g9K5CEh6AXBqFXUR0rXalMAjZPC3e1W99Dwntf2dXd/p+tt0YdFSBxH2Kz5qgLiI8B8KdVy3YBevqRHz/qWh72Yui3MUDEL3q44WPXw3M+fo1pZuQs4tOIBVVTaoiXEI/MxfhGDPsxsNZfoE1q66ro5aJim3XdoLFw72H+n23BaIXzbcOnz5mfPoTvYVz7KzUl5+FRxEuqkp9G/Ajia219thzg25abkRE/BpDc3pqvphHvRFys2weqvp+krbWKIX7nhDbzLOItiM8358pTwdirqpPFnMF2xLc1WvLyOwTAibpbmvHHcvttU57y5+XqNZrLe3lE/Pq8eUj2fXKfOe3pfOjzhJYtB/yll5SDFcSDiH+hRkH25+L+sdxKEAMZahrlSX8ukqMOWy/jXW2m6M9LDBc31B9LFuv6gVKg/0Szi3KAr1kGq1GMjU/aLbnq6/lRxc4XfJ98hTargX++DbMJBSiYMIe9Ck1YAxFkKEAG3xbYaKmDDgYyFK0UGYpfoWYXG+fAPPI6tJnNwb7ClP7IyF+D+bjOtCpkhz6CFrIa/I6sFtNl8auFXGMTP34sNwI/JhkgEtmDz14ySfaRcTIBInmKPE32kxyyE2Tv+thKbEVePDfW/byMM1Kmm0XdObS7oGD/MypMXFPXrCwOtoYjyyn7BV29/MZfsVzpLDdRtuIZnbpXzvlf+ev8MvYr/Gqk4H/kV/G3csdazLuyTMPsbFhzd1UabQbjFvDRmcWJxR3zcfHkVw9GfpbJmeev9F08WW8uDkaslwX6avlWGU6NRKz0g/SHtCy9J30o/ca9zX3Kfc19zn3BXQKRO8ud477hLnAfc1/G9mrzGlrfexZ5GLdn6ZZrrEohI2wVHhZywjbhUWEy8icMCGNCUdiBlq3r+xafL549HQ5jH+an+1y+LlYBifuxAvRN/lVVVOlwlCkdVm9NOL5BE4wkQ2SMlDZU97hX86EilU/lUmkQUztTE6mx1EEPh7OmdqBtAvv8HdWpbrJS6tJj3n0CWdM6busNzRV3S9KTYhqvNiqWmuroiKgYhshMjmhTh9ptWhsF7970j/SbMrsPE1suR5z7DMC+P/Hs+y7ijrQAlhyAgccjbhjPygfeBTjzhNqy28EdkUh8C+DU9+z2v/oyeH791OncxHOs5y2AtTc7nb/f73TWPkD/qwBnjX8BoJ98VQNcC+8AAAAKSURBVAgdY3gGAADoAOegvBZqAAAAAElFTkSuQmCC'''
        self.__lightBluePixelData = '''iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAEGWlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPrtzZyMkzlNsNIV0qD8NJQ2TVjShtLp/3d02bpZJNtoi6GT27s6Yyc44M7v9oU9FUHwx6psUxL+3gCAo9Q/bPrQvlQol2tQgKD60+INQ6Ium65k7M5lpurHeZe58853vnnvuuWfvBei5qliWkRQBFpquLRcy4nOHj4g9K5CEh6AXBqFXUR0rXalMAjZPC3e1W99Dwntf2dXd/p+tt0YdFSBxH2Kz5qgLiI8B8KdVy3YBevqRHz/qWh72Yui3MUDEL3q44WPXw3M+fo1pZuQs4tOIBVVTaoiXEI/MxfhGDPsxsNZfoE1q66ro5aJim3XdoLFw72H+n23BaIXzbcOnz5mfPoTvYVz7KzUl5+FRxEuqkp9G/Ajia219thzg25abkRE/BpDc3pqvphHvRFys2weqvp+krbWKIX7nhDbzLOItiM8358pTwdirqpPFnMF2xLc1WvLyOwTAibpbmvHHcvttU57y5+XqNZrLe3lE/Pq8eUj2fXKfOe3pfOjzhJYtB/yll5SDFcSDiH+hRkH25+L+sdxKEAMZahrlSX8ukqMOWy/jXW2m6M9LDBc31B9LFuv6gVKg/0Szi3KAr1kGq1GMjU/aLbnq6/lRxc4XfJ98hTargX++DbMJBSiYMIe9Ck1YAxFkKEAG3xbYaKmDDgYyFK0UGYpfoWYXG+fAPPI6tJnNwb7ClP7IyF+D+bjOtCpkhz6CFrIa/I6sFtNl8auFXGMTP34sNwI/JhkgEtmDz14ySfaRcTIBInmKPE32kxyyE2Tv+thKbEVePDfW/byMM1Kmm0XdObS7oGD/MypMXFPXrCwOtoYjyyn7BV29/MZfsVzpLDdRtuIZnbpXzvlf+ev8MvYr/Gqk4H/kV/G3csdazLuyTMPsbFhzd1UabQbjFvDRmcWJxR3zcfHkVw9GfpbJmeev9F08WW8uDkaslwX6avlWGU6NRKz0g/SHtCy9J30o/ca9zX3Kfc19zn3BXQKRO8ud477hLnAfc1/G9mrzGlrfexZ5GLdn6ZZrrEohI2wVHhZywjbhUWEy8icMCGNCUdiBlq3r+xafL549HQ5jH+an+1y+LlYBifuxAvRN/lVVVOlwlCkdVm9NOL5BE4wkQ2SMlDZU97hX86EilU/lUmkQUztTE6mx1EEPh7OmdqBtAvv8HdWpbrJS6tJj3n0CWdM6busNzRV3S9KTYhqvNiqWmuroiKgYhshMjmhTh9ptWhsF7970j/SbMrsPE1suR5z7DMC+P/Hs+y7ijrQAlhyAgccjbhjPygfeBTjzhNqy28EdkUh8C+DU9+z2v/oyeH791OncxHOs5y2AtTc7nb/f73TWPkD/qwBnjX8BoJ98VQNcC+8AAAAMSURBVAgdY5h08REABD4CRkzI4LsAAAAASUVORK5CYII='''
        self.__blueGrayPixelData = '''iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAEGWlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPrtzZyMkzlNsNIV0qD8NJQ2TVjShtLp/3d02bpZJNtoi6GT27s6Yyc44M7v9oU9FUHwx6psUxL+3gCAo9Q/bPrQvlQol2tQgKD60+INQ6Ium65k7M5lpurHeZe58853vnnvuuWfvBei5qliWkRQBFpquLRcy4nOHj4g9K5CEh6AXBqFXUR0rXalMAjZPC3e1W99Dwntf2dXd/p+tt0YdFSBxH2Kz5qgLiI8B8KdVy3YBevqRHz/qWh72Yui3MUDEL3q44WPXw3M+fo1pZuQs4tOIBVVTaoiXEI/MxfhGDPsxsNZfoE1q66ro5aJim3XdoLFw72H+n23BaIXzbcOnz5mfPoTvYVz7KzUl5+FRxEuqkp9G/Ajia219thzg25abkRE/BpDc3pqvphHvRFys2weqvp+krbWKIX7nhDbzLOItiM8358pTwdirqpPFnMF2xLc1WvLyOwTAibpbmvHHcvttU57y5+XqNZrLe3lE/Pq8eUj2fXKfOe3pfOjzhJYtB/yll5SDFcSDiH+hRkH25+L+sdxKEAMZahrlSX8ukqMOWy/jXW2m6M9LDBc31B9LFuv6gVKg/0Szi3KAr1kGq1GMjU/aLbnq6/lRxc4XfJ98hTargX++DbMJBSiYMIe9Ck1YAxFkKEAG3xbYaKmDDgYyFK0UGYpfoWYXG+fAPPI6tJnNwb7ClP7IyF+D+bjOtCpkhz6CFrIa/I6sFtNl8auFXGMTP34sNwI/JhkgEtmDz14ySfaRcTIBInmKPE32kxyyE2Tv+thKbEVePDfW/byMM1Kmm0XdObS7oGD/MypMXFPXrCwOtoYjyyn7BV29/MZfsVzpLDdRtuIZnbpXzvlf+ev8MvYr/Gqk4H/kV/G3csdazLuyTMPsbFhzd1UabQbjFvDRmcWJxR3zcfHkVw9GfpbJmeev9F08WW8uDkaslwX6avlWGU6NRKz0g/SHtCy9J30o/ca9zX3Kfc19zn3BXQKRO8ud477hLnAfc1/G9mrzGlrfexZ5GLdn6ZZrrEohI2wVHhZywjbhUWEy8icMCGNCUdiBlq3r+xafL549HQ5jH+an+1y+LlYBifuxAvRN/lVVVOlwlCkdVm9NOL5BE4wkQ2SMlDZU97hX86EilU/lUmkQUztTE6mx1EEPh7OmdqBtAvv8HdWpbrJS6tJj3n0CWdM6busNzRV3S9KTYhqvNiqWmuroiKgYhshMjmhTh9ptWhsF7970j/SbMrsPE1suR5z7DMC+P/Hs+y7ijrQAlhyAgccjbhjPygfeBTjzhNqy28EdkUh8C+DU9+z2v/oyeH791OncxHOs5y2AtTc7nb/f73TWPkD/qwBnjX8BoJ98VQNcC+8AAAAMSURBVAgdY3jx4j8ABYsC0GTwZRQAAAAASUVORK5CYII='''
        # ---------- Create the main window & set its minimum dimensions ----------
        self.mainWindow = Tk()
        self.mainWindow.minsize(self.MAIN_WND_MIN_WIDTH, self.MAIN_WND_MIN_HEIGHT)
        self.mainWindow.title('Spelman AutoGrader 2.X')

        # ---------- Set the default fond for the app ----------
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=14, family="Arial")

        # ---------- create pixel images ----------
        self.__clearPixelImg = PhotoImage(data=self.__clearPixelData)
        self.__lightGrayPixelImg = PhotoImage(file='pics/lightGrayPixel.png') #(data=self.__lightGrayPixelData)
        self.__lightBluePixelImg = PhotoImage(data=self.__lightBluePixelData)
        self.__blueGrayPixelImg = PhotoImage(data=self.__blueGrayPixelData)

        # make images for the different buttons
        self.imgBtn_150x30 = self.makeWidgetImage(150, 30)
        self.imgBtn_76x30 = self.makeWidgetImage(76, 30)
        self.imgBtn_100x50 = self.makeWidgetImage(100, 50)
        self.imgBtn_100x30 = self.makeWidgetImage(100, 30)
        self.imgBtn_85x30 = self.makeWidgetImage(100, 30)

        self.imgBlueBtn_76x30 = self.makeWidgetImage(76, 30, self.WIDGET_CLR.LIGHT_BLUE)

        # ---------- create the main window frames ----------
        self.__frameMenu = Frame(self.mainWindow, bg='#e8e8ff', height=40, borderwidth=1, relief='groove')
        self.__frameMain = Frame(self.mainWindow, bg='#f0f0f0', borderwidth=1, relief='groove')
        self.__frameStatus = Frame(self.mainWindow,  bg='#e8e8ff', height=27, borderwidth=1, relief='groove')

        # ---------- create the main frames ----------
        self.__buildMenuFrame()
        self.__buildMainFrames()
        self.__buildStatusFrame()

        # ---------- pack in the main window frames ----------
        self.__frameMenu.pack(fill=X, expand=False, side=TOP)
        self.__frameMain.pack(fill=BOTH, expand=True, side=TOP)
        self.__frameStatus.pack(fill=X, expand=False, side=TOP)

        # Run the mainloop (required)
        self.mainWindow.mainloop()


    def __btnSettingClick(self):
        #self.__settingsFrame.place(x=24, y=0)
        self.__settingsFrame.lift()

    def __btnInputClick(self):
        self.__inputFrame.lift()

    def __btnOutputClick(self):
        self.__outputFrame.lift()

# =======================================================================
# public static void main(String[] args)
# Entry point into the application.
# ======================================================================
def main():
    global autoGrader
    console("main...")

    #console('%d, %f', 3, 4.3)
    # TEMP  autoGrader = AutoGrader3()

    controller = Controller()



    # ** THIS IS WHERE WE GATHER THE INFORMATION NORMALLY GATHERED THROUGH THE GUI.
    # THEN, EXECUTE THE GRADING ENGINE

        
    #---------- Commit the AG options to the JSON file ----------
    # TEMP autoGrader.saveConfiguration()
    console("Exiting main()...")

main()

# =======================================================================
# Help HTML string
# ======================================================================
HELP_HTML = "<!DOCTYPE html PUBLIC \"-#W3C#DTD XHTML 1.0 Strict#EN\" \"http:#www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">" + \
    "<html xmlns=\"http:#www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">" + \
    "<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />" + \
    "<title>AutoGrader 2 Help</title></head>" + \
    "<body style=\"background: white; font-family: Cambria\">" + \
    "<div class=\"WordSection1\">" + \
    "<div style=\"text-align: center;\"><b>" + \
    "<span style=\"font-size: 18pt; color: rgb(0, 112, 192)\">Spelman AutoGrader 2</span></b><br>" + \
    "</div>&nbsp;<br>" + \
    "<span style=\"font-size: 14pt; color: rgb(0, 112, 192)\"><big>Introduction</big> </span><br>" + \
    "The Spelman AutoGrader 2 program is designed to help grade " + \
    "Python and C++ programs submitted through Moodle.&nbsp; The program runs on macOS and Linux systems only.  " + \
    "It is not Windows compatible.  To use the program, " + \
    "perform a “download all submissions” of the target assignment from " + \
    "Moodle. &nbsp;Extract " + \
    "the downloaded zip file.&nbsp; This will create a directory on disk that holds " + \
    "all student submissions.&nbsp; We will call this our “top-level " + \
    "directory” (TLD).&nbsp; The TLD should contain as many sub-directories as there " + \
    "are submitted assignments.&nbsp; The names of these sub-directories should be " + \
    "formatted as “student name_assignment”.&nbsp; If your TLD does not contain " + \
    "sub-directories, please see the section on&nbsp; " + \
    "<a href=\"#moodle_download_settings\">Moodle Download Settings</a>.<br>&nbsp;<br>" + \
    "The individual student directories may contain program files " + \
    "(*.cpp, *.h, *.py, etc) zip files (*.zip) or subdirectories.&nbsp; The " + \
    "AutoGrader first searches for zip files.&nbsp; If any are found and the " + \
    "auto-uncompress option is selected, these are uncompressed into subdirectories " + \
    "with the same names as the zip files.&nbsp; The AutoGrader next " + \
    "searches for programming files.&nbsp; For each student submission, this " + \
    "search begins in the individual submission directory and continues recursively " + \
    "through sub-directories until a programming file is found.&nbsp; If a " + \
    "programming language is specified, the AutoGrader looks for programming files " + \
    "for that language only.&nbsp; If the programming language is set to “Auto” " + \
    "(recommended), the AutoGrader searches for any programming files and attempts " + \
    "to classify the submission as a Python or C++ program.<br>&nbsp;<br>" + \
    "For C++, one (and only one) of the multiple source files " + \
    "should contain a main().&nbsp; For Python, the top-level module must be identified " + \
    "among the multiple .py files.&nbsp; By default, AutoGrader assumes that " + \
    "top-level Python modules are named “main.py”.&nbsp; For this reason, it is " + \
    "advisable to instruct students to name their top-level Python modules “main.py” " + \
    "when submitting multi-file projects.&nbsp; If multiple Python files are " + \
    "found and none are named “main.py”, the AutoGrader will prompt you to " + \
    "select which of the multiple files is the top level file.<br>" + \
    "<span style=\"font-size: 14pt; color: rgb(0, 112, 192)\"></span><br>The " + \
    "AutoGrader UI is organized by a set of numbered buttons at the top of " + \
    "the screen.&nbsp; The buttons are labeled “0-Settings”, “1-Input/Setup” " + \
    "and “2-Output”.&nbsp; A 4th button labeled “Console” is for process " + \
    "tracking and debugging grading mishaps.&nbsp; The numbered buttons " + \
    "suggest the order of operations.&nbsp; On startup, you will be on the " + \
    "“1 - Input/Setup” screen corresponding to Button 1.&nbsp; You will " + \
    "probably need to use Button 0, “Settings”, only once, the first time " + \
    "you launch AutoGrader 2 to configure the program.&nbsp; The " + \
    "configuration options are described in the " + \
    "“<a href=\"#configuration_options\">Configuration Options</a>” section. <br><br><br>" + \
    "<span style=\"font-size: 14pt; color: rgb(0, 112, 192)\">" + \
    "<a name=\"configuration_options\"></a><big>“0 - Settings” Screen</big><br>" + \
    "</span>The first time you run AutoGrader 2, you will likely want to " + \
    "customize the program.&nbsp; Below is a description of the different " + \
    "configuration options." + \
    "<br><br><span style=\"font-size: 14pt; color: rgb(0, 112, 192)\">Configuration" + \
    "Options</span>" + \
    "<ul><li><span style=\"font-weight: bold;\">Language</span> - The AutoGrader can grade&nbsp; Python and C++ " + \
    "code.&nbsp; You may specify the language for the programs under test or " + \
    "you may let the AutoGrader automatically detect the language by " + \
    "selecting “Auto”.&nbsp; This&nbsp; is the recommended setting.&nbsp; In " + \
    "“Auto” mode, it is possible to have mixed-language submissions, meaning " + \
    "that some students may submit their assignment in Python while others " + \
    "do so in C++.</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">Max Run Time </span>- You may specify the maximum run-time for each " + \
    "submission.&nbsp; This is a safeguard against rogue programs that run " + \
    "an infinite loop, for example.&nbsp; The AutoGrader will kill any " + \
    "program that runs beyond the specified max run time.&nbsp; Setting this " + \
    "value to 0 disables the max run time check.&nbsp; This is not " + \
    "recommended.</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">Limit Output Lines</span> - You may limit the maximum number of output " + \
    "lines included in the final report for each program under test.&nbsp;" + \
    "This is a safeguard against runaway programs that generate mass output " + \
    "in an infinite loop.</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">Include Source Listing in Output </span>- Specify whether or not a " + \
    "listing of each source program file should be included in the final " + \
    "report.</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">Auto Uncompress</span> - Specify whether or not the AutoGrader should " + \
    "uncompress zip files.&nbsp; When multiple programming files are " + \
    "involved, they may be submitted as a compressed zip file. The&nbsp;" + \
    "AutoGrader can automatically uncompress these.&nbsp; If unsure, select " + \
    "“Yes”.</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">Process Recursively</span> - When compressed submissions are " + \
    "uncompressed, the program files may be located in a " + \
    "sub-directory.&nbsp; The AutoGrader can automatically search these " + \
    "subdirectories until a program file is found.&nbsp; If unsure, select " + \
    "“Yes”.</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">Python 3 Interpreter</span> - " + \
    "When first run, the AutoGrader wil attempt " + \
    "to automatically detect a suitable python 3 interpreter.&nbsp; If none " + \
    "is found, you will have to manually enter the path to the interpreter " + \
    "here.&nbsp; Also, if you have multiple Python interpreters installed, " + \
    "the default interpreter is randomly selected among the possible options.&nbsp; You may " + \
    "change the default interpreter here.<br>" + \
    "</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">C++ compiler </span>- When " + \
    "first run, the AutoGrader will attempt to" + \
    "automatically detect a suitable c++ compiler.&nbsp; If none is " + \
    "found, you will have to manually enter the path to a compiler " + \
    "here.&nbsp; If you do not have a c++ compiler installed and do not " + \
    "intend to grade c++ programs, you may leave this field blank.<br>" + \
    "</li></ul>" + \
    "<ul><li><span style=\"font-weight: bold;\">Shell Interpreter " + \
    "</span>- Programs are tested in a “sandbox” shell. &nbsp; By default, the shell /bin/bash is used.&nbsp; You may " + \
    "specify a different shell here." + \
    "</li></ul><br><br>" + \
    "<span style=\"font-size: 14pt; color: rgb(0, 112, 192)\"><big>“1 - Input/Setup” Screen</big><br></span>Under " + \
    "normal operations, you will spend your time on the “1 - Input/Setup” " + \
    "and “2-Output” screens only.&nbsp; Starting with the “1 - Input/Setup” " + \
    "screen, you must specify the TLD (top-level directory) of the " + \
    "uncompressed zip file downloaded from Moodle.&nbsp; This is the minimum " + \
    "requirement.&nbsp; Most likely, you will want to specify test data " + \
    "files and possibly data files.&nbsp; Once these are specified, click " + \
    "the “Start” button to begin autograding.&nbsp; Once the grading is " + \
    "completed, you will be automatically switched to the “<a \"href=#output_screen\">2 - Output</a>” screen.<br><br>" + \
    "<span style=\"font-size: 14pt; color: rgb(0, 112, 192)\">Test Data</span><br>" + \
    "For programs that require keyboard input, you must specify the inputs " + \
    "in a test data file.&nbsp; This file contains one line for each " + \
    "required input.&nbsp; So, if a program requies the user to enter 3 " + \
    "integers, your test data file should contain 3 lines, each containing 1 " + \
    "integer.<br>" + \
    "You may include multiple test cases in a single test data file by " + \
    "separating test cases with a double @&nbsp; (“@@”)&nbsp; line.&nbsp;" + \
    "Using the example of a program that requires the user to enter 3 " + \
    "integers, a test data file with the following contents would test the " + \
    "program using two different data sets:<br><br>" + \
    "<span style=\"font-style: italic; color: rgb(102, 102, 0)\">" + \
    "12<br>" + \
    "72<br>" + \
    "2<br>" + \
    "@@<br>" + \
    "103<br>" + \
    "-3<br>" + \
    "44</span>" + \
    "<br><br>Note that in the case above, the program would be executed twice, once for each test case." + \
    "<br><br>You may add comments at the end " + \
    "of the file beyond the expected keyboard inputs.&nbsp; In our example, " + \
    "anything beyond the 3rd integer should be ignored by the program under " + \
    "test .&nbsp; However, be mindful that an ill-behaved program could interpret this as " + \
    "user input.&nbsp; For a well-behaved program, the following is an " + \
    "equivalent test data file:<br><br>" + \
    "<span style=\"font-style: italic; color: rgb(102, 102, 0)\">" + \
    "12<br>" + \
    "72<br>" + \
    "2<br>This is a comment.&nbsp; It should have no effect on " + \
    "a program that reads only 3 integers." + \
    "<br><br>" + \
    "@@<br>103<br>" + \
    "-3<br>44<br>" + \
    "This is another comment." + \
    "</span><br><br>" + \
    "Note that specifying test data is optional.&nbsp; Some programs do not " + \
    "require user input.&nbsp; When test data is required, but not " + \
    "specified, the likely outcome is a “max execution time exceeded” error for each " + \
    "submission.<br><br>" + \
    "<span style=\"font-size: 14pt; color: rgb(0, 112, 192)\">Data Files</span><br>" + \
    "Some programs need access to data files.&nbsp; In such cases, the " + \
    "data files should be specified here.&nbsp; Each data file will be " + \
    "copied to the working directory of each program when the program is " + \
    "executed.&nbsp; Note that the AutoGrader assumes that the data files to " + \
    "be accessed are in the same directory as the program under test.&nbsp;" + \
    "It is important that submitted programs make the same assumption unless " + \
    "the submitted program includes its own data files.<br><br><br>" + \
    "<span style=\"font-size: 14pt; color: rgb(0, 112, 192)\"><big>" + \
    "<a name=\"output_screen\"></a>“2 - Output” Screen</big><br>" + \
    "</span>Upon completion of the autograding process, you will be switched " + \
    "to the “2 - Output” screen.&nbsp; The main part of the screen will " + \
    "display the results of the grading process.&nbsp; You can add a grade " + \
    "and a comment to each submission.&nbsp; At the top of the screen, there " + \
    "is a navigation bar to help with navigating to a particular student's " + \
    "submission.&nbsp; At the bottom of the screen, is a button to save the " + \
    "grading results as well as the instructor comments to a file.&nbsp; " + \
    "AutoGrader 2 files have a “.ag2” extension.&nbsp; You may also export the " + \
    "report to an HTML file.&nbsp; This is recommended as it allows you to " + \
    "review the grading using any web browser.&nbsp; You cannot update the " + \
    "grade in the exported HTML.&nbsp; A third button switches the main " + \
    "window to display a summary of student grades and instructor " + \
    "comments.&nbsp; Use this view to help with the transfer of grades back " + \
    "to Moodle.<br><br><br>" + \
    "<big><span style=\"font-size: 14pt; color: rgb(0, 112, 192)\">" + \
    "<a name=\"moodle_download_settings\"></a><big>Moodle Download " + \
    "Settings</big></span>" + \
    "</big><br>If the downloaded student submissions are not in individual " + \
    "folders under the top-level directory, follow the instructions below " + \
    "<br><ol><li>Verify that you are using Moodle 3.1 or later</li>" + \
    "<li>Go to the assignment and click on “View/grade all submissions”</li>" + \
    "<li>Scroll to the very bottom of the page and verify that the “Download " + \
    "submissions in folders” option is checked.&nbsp; You will only need to do " + \
    "this once.&nbsp;" + \
    "Moodle will remember your choice.</li>" + \
    "<li>Now, under “Grading action” select “Download all submissions”.</li></ol>" + \
    "<br><br><big><span style=\"font-size: 14pt; color: rgb(0, 112, 192)\">" + \
    "<a name=\"acknowledgments\"></a><big>Acknowledgments</big></span>" + \
    "</big><br>" + \
    "<u>AutoGrader 2</u><br>" + \
    "Copyright (c) 2016-2018 Jerry Volcy<br>" + \
    "Department of Computer Science, Spelman College<br><br>" + \
    "<u>SyntaxHighlighter 3.0.83</u><br>" + \
    "Copyright (C) 2004-2010 Alex Gorbatchev<br>" + \
    "http:#alexgorbatchev.com/SyntaxHighlighter<br>" + \
    "used under dual MIT and GPL licenses<br><br>" + \
    "</div>" + \
    "</body></html>";






# =======================================================================
# To Do
# Auto version incrementing
# copy data files to submission folders
# make a subdirectory in the TLD for extracted test files
# clean up data files and extracted test files
# ======================================================================


# =======================================================================
# xxx
# ======================================================================

#----------  ----------
#----------  ----------
#----------  ----------
#----------  ----------
