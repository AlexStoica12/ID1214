from tkinter import *
import tkinter.messagebox

#-----------TODO-------------
# 1. Figure out how to modularly display stock information and be able to resize it easily in the code
# 2. Figure out how to make the different frames resizeable

class Interface:

    def leftClick(self, event):
        print("I LEFT CLICKED!") 

    def rightClick(self, event):
        print("I RIGHT CLICKED!")

    def setStatus(self, newText):
        self.statusBar.config(text = newText)

    def __init__(self):
         # ***** WINDOW ***** 

        window = Tk() #Creates a window
        window.geometry("800x600") #Set window dimensions to be 800x600

        windowTitle = "Stock Assistant" 
        window.title(windowTitle) #Change window title a certain string

        # ***** MENU *****

        menu = Menu(window) #Creates a menu at the top of the window
        window.config(menu = menu) #Configures the window to show the menu

        fileMenu = Menu(menu, tearoff = 0) #Creates a file dropdown (tearoff = 0 removes a dotted line above the first cascade)
        menu.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label = "Exit", command = window.quit) 

        # ***** STATUS BAR *****

        self.statusBar = Label(window, text = "Idle", bd = 1, relief = SUNKEN, anchor = W)
        self.statusBar.pack(side = BOTTOM, fill = X)

        # ***** PANEL FRAME *****

        panelsFrame = Frame(window, bg = "blue") #Creates the frame for displaying stock panels
        panelsFrame.pack(side = LEFT, fill = Y)

        stockPic = PhotoImage(file = "C:\\Users\\Andre\\Desktop\\Programs\\Python Programs\\AI Project\\stocks.png") #Imports image to use for the stock panel title

        panelsTitle = Label(panelsFrame, image = stockPic)
        panelsTitle.pack()

        searchEntry = Entry(panelsFrame, bd = 5) #Creates the entry for entering a stock to search for
        searchEntry.pack(side = LEFT, padx = 10, pady = 10, anchor = N)

        searchButton = Button(panelsFrame, text = "SEARCH", bd = 5, command = lambda : self.setStatus(searchEntry.get())) #Creates the stock search button
        searchButton.pack(side = LEFT, padx = 10, pady = 10, anchor = N)

        # ***** ASSISTANT FRAME *****

        assistantFrame = Frame(window, bg = "red") #Creates the frame for displaying the Stock Assistant
        assistantFrame.pack(side = TOP, fill = X)

        SApic = PhotoImage(file = "C:\\Users\\Andre\\Desktop\\Programs\\Python Programs\\AI Project\\sa.png")

        SATitle = Label(assistantFrame, image = SApic) #Creates the [S]tock [A]ssistant title label
        SATitle.pack() #Fills in the label to the full X

        predictionButton = Button(assistantFrame, text = "Predict a stock for me!", fg = "white", bg = "blue", bd = 5) #Creates the button to ask for a stock value prediction
        predictionButton.pack(padx = 10, pady = 10)

        # ***** PORTFOLIO FRAME *****

        portfolioFrame = Frame(window, bg = "green") #Creates the frame for displaying stock portfolio
        portfolioFrame.pack(side = BOTTOM, fill = BOTH, expand = TRUE)

        portfolioPic = PhotoImage(file = "C:\\Users\\Andre\\Desktop\\Programs\\Python Programs\\AI Project\\portfolio.png")\

        portfolioTitle = Label(portfolioFrame, image = portfolioPic)
        portfolioTitle.pack()

        window.mainloop() #Continuos loop for the window

interface = Interface()