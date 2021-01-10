from tkinter import *
import tkinter.messagebox
import datetime as dt
import yfinance as yf
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

#Import all the stocks that will be available to the user
stocks = ['MSFT', 'AAPL' , 'TSLA' , 'FB' , 'AMZN' , 'NVDA' , 'AMD' , 'MA', 'PYPL' , 'GOOG' , 'V' , 'CRM' , 'NFLX', 'AXP']

#Date initialization and alteration
today = dt.date.today()
first = today.replace(day = 1)
lastMonth = first - dt.timedelta(days=(32 - today.day))

#Figure initialization for plotting the graphs
searchFig = Figure(figsize = (3, 1), dpi = 100, facecolor="purple")
fig1 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")
fig2 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")
fig3 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")
fig4 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")

#Empty array to store stock symbols of each canvas (plot) for easy searching (index 1 = plot 1, index 2 = plot 2, etc.)
panelStocks = ['', '', '', '', '', '']

#Plot the searching graph (functions differently from the other four)
dfSearch = yf.download('AAPL', start = lastMonth, end = today)
a_search = searchFig.add_subplot(111)
a_search.plot(dfSearch)

#Datafeeds downloaded from yfinance directly for each of the four base plots
df1 = yf.download('MSFT', start = lastMonth, end = today)
df2 = yf.download('TSLA', start = lastMonth, end = today)
df3 = yf.download('NFLX', start = lastMonth, end = today)
df4 = yf.download('AMZN', start = lastMonth, end = today)

#Default initialization for all five of the plots
panelStocks[1] = 'AAPL'
panelStocks[2] = 'MSFT'
panelStocks[3] = 'TSLA'
panelStocks[4] = 'NFLX'
panelStocks[5] = 'AMZN'

#Stores which stocks the user owns in a string array
ownedStocks = []

#Four subplot initializations for each of the graphs
a1 = fig1.add_subplot(111)
a2 = fig2.add_subplot(111)
a3 = fig3.add_subplot(111)
a4 = fig4.add_subplot(111)

#Plots the four different graphs
a1.plot(df1)
a2.plot(df2)
a3.plot(df3)
a4.plot(df4)

#Creates a window
window = Tk()

#Portfolio value initialization
pValue = 0

#Change the status bar text (displayed in bottom left corner)
def setStatus(newText):
    statusBar.config(text = newText)

#Search for a stock
def search(text):
    print(text)
    if text in stocks:
        setStatus('Searching...')
        panelStocks[1] = text #Update stock symbol
        global dfSearch
        dfSearch = yf.download(text, start = lastMonth, end = today) #Get new stock data
        searchFig.clear() #Clear previous figure
        a_search = searchFig.add_subplot(111) #Create new subplot
        a_search.plot(dfSearch) #Plot the new data
        print(getCurrentPrice(text))
    else:
        tkinter.messagebox.showerror('Search Error', 'Sorry! Our database does not hold any information for \"' +text+ '\".')

#Returns current stock price (Function content taken from stackoverflow)
def getCurrentPrice(stock):
    stockTicker = yf.Ticker(stock)
    data = stockTicker.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    return round(last_quote, 2)

#Update the value of the portfolio
def updatePortfolioValue():
    global pValue
    pValue = 0 #Reset portfolio value
    for s in ownedStocks: 
        pValue += getCurrentPrice(s) #For every owned stock, add to the porfolio value by its price     

#Buy a new stock
def buyStock(stock):
    setStatus('Buying stock...')
    print("Bought: " +stock)
    ownedStocks.append(stock)
    updatePortfolioValue()

#Sell a stock
def sellStock(stock):
    setStatus('Selling stock...')
    print("Sold: " +stock)
    if stock in ownedStocks:
        ownedStocks.remove(stock)
    else:
        tkinter.messagebox.showerror('Cannot Sell Stock', 'You do not own any ' +stock+ ' stock!')
    updatePortfolioValue()

#Create a new window when the user wants a prediction
def createPredictionWindow():
    predictionWindow = Toplevel(window)
    predictionWindow.geometry("800x600")
    predictionWindow.resizable(False, False)
    predictionWindow.title("Stock Prediction")

    mainFrame = Frame(predictionWindow, bg = "midnight blue")
    mainFrame.pack(fill = BOTH)

    chooseLabel = Label(mainFrame, text = 'Choose Stock: ', font = fontStyle, bg = 'midnight blue', fg = 'white')
    chooseLabel.pack(side = LEFT)

    stockOptions = StringVar(predictionWindow)
    stockOptions.set(stocks[0])

    options = OptionMenu(mainFrame, stockOptions, *stocks)
    options.pack(side = LEFT)

    confirmButton = Button(mainFrame, text = "Predict!", fg = "white", bg = "blue", bd = 5, font = fontStyleSmall)
    confirmButton.pack(side = LEFT, padx = 10)

    predictionCanvas = FigureCanvasTkAgg(plt, mainFrame)
    predictionCanvas.get_tk_widget().pack(side = BOTTOM)

def predict():
    hello



# ***** WINDOW ***** 
window.geometry("1280x720") #Set window dimensions to be 1280x720
window.resizable(False, False)

fontStyle = tkFont.Font(family = "Palatino Linotype", size = 16)
fontStyleSmall = tkFont.Font(family = "Palatino Linotype", size = 10, weight = "bold")

windowTitle = "Stock Assistant" 
window.title(windowTitle) #Change window title a certain string

# ***** MENU *****

menu = Menu(window) #Creates a menu at the top of the window
window.config(menu = menu) #Configures the window to show the menu

fileMenu = Menu(menu, tearoff = 0) #Creates a file dropdown (tearoff = 0 removes a dotted line above the first cascade)
menu.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "Exit", command = window.quit) 

# ***** STATUS BAR *****

statusBar = Label(window, text = "Idle", bd = 1, relief = SUNKEN)
statusBar.grid(row = 10, sticky = W)

# ***** PANEL FRAME *****

panelsFrame = Frame(window, bg = "midnight blue") #Creates the frame for displaying stock panels
panelsFrame.grid(sticky = N, rowspan = 2, row = 0, column = 0)

panelCanvas = Canvas(panelsFrame, bg = "midnight blue", width = 550, height = 100, highlightthickness = 0) #Creates a canvas to display the title image
panelCanvas.grid(row = 0, column = 0, columnspan = 2)

stockPic = PhotoImage(file = "C:\\Users\\andre\\Desktop\\Python Workspace\\AI Project\\stocks.png") #Imports image to use for the stock panel title
panelCanvas.create_image(275, 50, image=stockPic) #Sets the image to be the background of the canvas

searchEntry = Entry(panelsFrame, bd = 5, width = 50) #Creates the entry for entering a stock to search for
searchEntry.grid(row = 1, column = 0, padx = 10, pady = 5)

searchButton = Button(panelsFrame, text = "SEARCH", bd = 5, font = fontStyleSmall, command = lambda : search(searchEntry.get())) #Creates the stock search button
searchButton.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = W)

#Search plot
label1 = Label(panelsFrame, text = panelStocks[1]+ '\n Value: $' +str(getCurrentPrice(panelStocks[1])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label1.grid(row = 2, column = 2)
canvas1 = FigureCanvasTkAgg(searchFig, panelsFrame)
canvas1.get_tk_widget().grid(row = 2, padx = 10, pady = 5)
buyButton1 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[1]))
buyButton1.grid(row = 2, column = 1, sticky = NW, pady = 20)
sellButton1 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[1]))
sellButton1.grid(row = 2, column = 1, sticky = SW, pady = 20)

#Static plot 1
label2 = Label(panelsFrame, text = panelStocks[2]+ '\n Value: $' +str(getCurrentPrice(panelStocks[2])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label2.grid(row = 3, column = 2)
canvas2 = FigureCanvasTkAgg(fig1, panelsFrame)
canvas2.get_tk_widget().grid(row = 3, padx = 10, pady = 5)
buyButton2 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[2]))
buyButton2.grid(row = 3, column = 1, sticky = NW, pady = 20)
sellButton2 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[2]))
sellButton2.grid(row = 3, column = 1, sticky = SW, pady = 20)

#Static plot 2
label3 = Label(panelsFrame, text = panelStocks[3]+ '\n Value: $' +str(getCurrentPrice(panelStocks[3])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label3.grid(row = 4, column = 2)
canvas3 = FigureCanvasTkAgg(fig2, panelsFrame)
canvas3.get_tk_widget().grid(row = 4, padx = 10, pady = 5)
buyButton3 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[3]))
buyButton3.grid(row = 4, column = 1, sticky = NW, pady = 20)
sellButton3 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[3]))
sellButton3.grid(row = 4, column = 1, sticky = SW, pady = 20)

#Static plot 3
label4 = Label(panelsFrame, text = panelStocks[4]+ '\n Value: $' +str(getCurrentPrice(panelStocks[4])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label4.grid(row = 5, column = 2)
canvas4 = FigureCanvasTkAgg(fig3, panelsFrame)
canvas4.get_tk_widget().grid(row = 5, padx = 10, pady = 5)
buyButton4 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[4]))
buyButton4.grid(row = 5, column = 1, sticky = NW, pady = 20)
sellButton4 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[4]))
sellButton4.grid(row = 5, column = 1, sticky = SW, pady = 20)

#Static plot 4
label5 = Label(panelsFrame, text = panelStocks[5]+ '\n Value: $' +str(getCurrentPrice(panelStocks[5])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label5.grid(row = 6, column = 2)
canvas5 = FigureCanvasTkAgg(fig4, panelsFrame)
canvas5.get_tk_widget().grid(row = 6, padx = 10, pady = 5)
buyButton5 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[5]))
buyButton5.grid(row = 6, column = 1, sticky = NW, pady = 20)
sellButton5 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[5]))
sellButton5.grid(row = 6, column = 1, sticky = SW, pady = 20)

# ***** ASSISTANT FRAME *****

assistantFrame = Frame(window, bg = "dark slate blue") #Creates the frame for displaying the Stock Assistant
assistantFrame.grid(sticky = 'NSEW', row = 0, column = 1)

assistantCanvas = Canvas(assistantFrame, bg = "dark slate blue", width = 640, height = 100, highlightthickness = 0) #Creates the canvas for displaying the title image
assistantCanvas.grid(sticky = 'NSEW')

SApic = PhotoImage(file = "C:\\Users\\andre\\Desktop\\Python Workspace\\AI Project\\sa.png")
assistantCanvas.create_image(320, 53, image = SApic) #Sets the image to be the background of the canvas

predictionButton = Button(assistantFrame, text = "Predict a stock for me!", fg = "white", bg = "blue", bd = 5, font = fontStyleSmall, command = lambda : createPredictionWindow()) #Creates the button to ask for a stock value prediction
predictionButton.grid(padx = 10, pady = 10)

# ***** PORTFOLIO FRAME *****

portfolioFrame = Frame(window, bg = "slate blue") #Creates the frame for displaying stock portfolio
portfolioFrame.grid(row = 1, column = 1, sticky = 'NSE')
portfolioFrame.grid_columnconfigure(0, weight = 1)

portfolioCanvas = Canvas(portfolioFrame, bg = "slate blue", width = 640, height = 100, highlightthickness = 0) #Creates a canvas to display the title image
portfolioCanvas.grid(row = 0, column = 0)

portfolioPic = PhotoImage(file = "C:\\Users\\andre\\Desktop\\Python Workspace\\AI Project\\portfolio.png")
portfolioCanvas.create_image(320, 50, image = portfolioPic) #Sets the image to be the background of the canvas

portfolioValue = Label(portfolioFrame, text = ("Current Value: $" + str(round(pValue, 2))), bg = "slate blue", fg = "white", font = fontStyle) #Label to display portfolio value
portfolioValue.grid(row = 1, pady = 20)

portfolioStocks = Label(portfolioFrame, text = ("Current Stocks: " + str(ownedStocks)), bg = "slate blue", fg = "white", font = fontStyle) #Label to display owned stocks
portfolioStocks.grid(row = 2, pady = 20)

#Function for updating all the information on in the window (very important!)
def update():
    setStatus('Updating...')
    print('I UPDATED!')
    updatePortfolioValue()
    print(pValue)
    #Update all the label values to the proper variable value
    label1.configure(text = panelStocks[1]+ '\n Value: $' +str(getCurrentPrice(panelStocks[1])))
    label2.configure(text = panelStocks[2]+ '\n Value: $' +str(getCurrentPrice(panelStocks[2])))
    label3.configure(text = panelStocks[3]+ '\n Value: $' +str(getCurrentPrice(panelStocks[3])))
    label4.configure(text = panelStocks[4]+ '\n Value: $' +str(getCurrentPrice(panelStocks[4])))
    label5.configure(text = panelStocks[5]+ '\n Value: $' +str(getCurrentPrice(panelStocks[5])))
    portfolioValue.configure(text = "Current Value: $" + str(round(pValue, 2)))
    portfolioStocks.configure(text = "Current Stocks: " + str(ownedStocks))
    #Perform update every 3 seconds (3000 milliseconds), running off window.mainloop()
    window.after(3000, update)
    #Redraw search canvas (keeps it updated for when a new stock is searched)
    canvas1.draw()
    setStatus('Idle')

update()

window.mainloop() #Continuos loop for the window