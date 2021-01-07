from tkinter import *
import tkinter.messagebox
import matplotlib.pyplot as plt
import yfinance as yf

def leftClick(event):
    print("I LEFT CLICKED!") 

def rightClick(event):
    print("I RIGHT CLICKED!")

def setStatus(newText):
    statusBar.config(text = newText)

# ***** WINDOW ***** 

window = Tk() #Creates a window
window.geometry("1280x720") #Set window dimensions to be 800x600

windowTitle = "Stock Assistant" 
window.title(windowTitle) #Change window title a certain string

# ***** MENU *****

menu = Menu(window) #Creates a menu at the top of the window
window.config(menu = menu) #Configures the window to show the menu

fileMenu = Menu(menu, tearoff = 0) #Creates a file dropdown (tearoff = 0 removes a dotted line above the first cascade)
menu.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "Exit", command = window.quit) 

# ***** STATUS BAR *****

statusBar = Label(window, text = "Idle", bd = 1, relief = SUNKEN, anchor = W)
statusBar.pack(side = BOTTOM, fill = X)

# ***** PANEL FRAME *****

panelsFrame = Frame(window, bg = "magenta4") #Creates the frame for displaying stock panels
panelsFrame.pack(side = LEFT, fill = Y)

panelCanvas = Canvas(panelsFrame, bg = "gray15", width = 400, height = 100, highlightthickness = 0) #Creates a canvas to display the title image
panelCanvas.pack()

stockPic = PhotoImage(file = "C:\\Users\\andre\\Desktop\\Python Workspace\\AI Project\\stocks.png") #Imports image to use for the stock panel title
panelCanvas.create_image(200, 50, image=stockPic) #Sets the image to be the background of the canvas

searchEntry = Entry(panelsFrame, bd = 5) #Creates the entry for entering a stock to search for
searchEntry.pack(side = LEFT, padx = 10, pady = 10, anchor = N)

searchButton = Button(panelsFrame, text = "SEARCH", bd = 5, command = lambda : setStatus(searchEntry.get())) #Creates the stock search button
searchButton.pack(side = LEFT, padx = 10, pady = 10, anchor = N)

# ***** ASSISTANT FRAME *****

assistantFrame = Frame(window, bg = "gray25") #Creates the frame for displaying the Stock Assistant
assistantFrame.pack(side = TOP, fill = X)

assistantCanvas = Canvas(assistantFrame, bg = "gray25", width = 200, height = 100, highlightthickness = 0) #Creates the canvas for displaying the title image
assistantCanvas.pack()

SApic = PhotoImage(file = "C:\\Users\\andre\\Desktop\\Python Workspace\\AI Project\\sa.png")
assistantCanvas.create_image(102, 53, image = SApic) #Sets the image to be the background of the canvas

predictionButton = Button(assistantFrame, text = "Predict a stock for me!", fg = "white", bg = "blue", bd = 5) #Creates the button to ask for a stock value prediction
predictionButton.pack(padx = 10, pady = 10)

# ***** PORTFOLIO FRAME *****

portfolioFrame = Frame(window, bg = "gray28") #Creates the frame for displaying stock portfolio
portfolioFrame.pack(side = BOTTOM, fill = BOTH, expand = TRUE)

portfolioCanvas = Canvas(portfolioFrame, bg = "gray28", width = 200, height = 100, highlightthickness = 0) #Creates a canvas to display the title image
portfolioCanvas.pack()

portfolioPic = PhotoImage(file = "C:\\Users\\andre\\Desktop\\Python Workspace\\AI Project\\portfolio.png")
portfolioCanvas.create_image(100, 50, image = portfolioPic) #Sets the image to be the background of the canvas

window.mainloop() #Continuos loop for the window

