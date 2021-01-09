from tkinter import *
import tkinter.messagebox
import datetime as dt
import yfinance as yf
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

search = 'AAPL'

stocks = ['MSFT', 'AAPl' , 'TSLA' , 'FB' , 'AMZN' , 'NVDA' , 'AMD' , 'MA', 'PYPL' , 'GOOG' , 'V' , 'CRM' , 'NFLX']
today = dt.date.today()
first = today.replace(day = 1)
lastMonth = first - dt.timedelta(days=(32 - today.day))

searchFig = Figure(figsize = (3, 1), dpi = 100, facecolor="purple")
fig1 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")
fig2 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")
fig3 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")
fig4 = Figure(figsize = (3, 1), dpi = 100, facecolor="lightskyblue")

panelStocks = ['', '', '', '', '', '']

dfSearch = yf.download('AAPL', start = lastMonth, end = today)
a_search = searchFig.add_subplot(111)
a_search.plot(dfSearch)

df1 = yf.download('MSFT', start = lastMonth, end = today)
df2 = yf.download('TSLA', start = lastMonth, end = today)
df3 = yf.download('NFLX', start = lastMonth, end = today)
df4 = yf.download('AMZN', start = lastMonth, end = today)

panelStocks[1] = 'AAPL'
panelStocks[2] = 'MSFT'
panelStocks[3] = 'TSLA'
panelStocks[4] = 'NFLX'
panelStocks[5] = 'AMZN'

ownedStocks = []

a1 = fig1.add_subplot(111)
a2 = fig2.add_subplot(111)
a3 = fig3.add_subplot(111)
a4 = fig4.add_subplot(111)

a1.plot(df1)
a2.plot(df2)
a3.plot(df3)
a4.plot(df4)

window = Tk() #Creates a window

pValue = 0

def setStatus(newText):
    statusBar.config(text = newText)

def search(text):
    print(text)
    if text in stocks:
        panelStocks[1] = text
        dfSearch = yf.download(text, start = lastMonth, end = today)
        a_search.clear()
        print(getCurrentPrice(text))
    else:
        tkinter.messagebox.showerror('Search Error', 'Sorry! Our database does not hold any information for \"' +text+ '\".')

    a_search     

def getCurrentPrice(stock):
    stockTicker = yf.Ticker(stock)
    data = stockTicker.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    return round(last_quote, 2)

def updatePortfolioValue():
    global pValue
    pValue = 0
    for s in ownedStocks:
        pValue += getCurrentPrice(s)      

def buyStock(stock):
    print("Bought: " +stock)
    ownedStocks.append(stock)
    updatePortfolioValue()

def sellStock(stock):
    print("Sold: " +stock)
    if stock in ownedStocks:
        ownedStocks.remove(stock)
    else:
        tkinter.messagebox.showerror('Cannot Sell Stock', 'You do not own any ' +stock+ ' stock!')
    updatePortfolioValue()

def resetSearchPlot():
    searchFig.clf()  


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

stockPic = PhotoImage(file = "C:\\Users\\Andre\\Desktop\\Programs\\Python Programs\\AI Project\\stocks.png") #Imports image to use for the stock panel title
panelCanvas.create_image(275, 50, image=stockPic) #Sets the image to be the background of the canvas

searchEntry = Entry(panelsFrame, bd = 5, width = 50) #Creates the entry for entering a stock to search for
searchEntry.grid(row = 1, column = 0, padx = 10, pady = 10)

searchButton = Button(panelsFrame, text = "SEARCH", bd = 5, font = fontStyleSmall, command = lambda : search(searchEntry.get())) #Creates the stock search button
searchButton.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = W)

label1 = Label(panelsFrame, text = panelStocks[1]+ '\n Value: $' +str(getCurrentPrice(panelStocks[1])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label1.grid(row = 2, column = 2)
canvas1 = FigureCanvasTkAgg(searchFig, panelsFrame)
canvas1.get_tk_widget().grid(row = 2, padx = 10, pady = 5)
buyButton1 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[1]))
buyButton1.grid(row = 2, column = 1, sticky = NW, pady = 20)
sellButton1 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[1]))
sellButton1.grid(row = 2, column = 1, sticky = SW, pady = 20)

label2 = Label(panelsFrame, text = panelStocks[2]+ '\n Value: $' +str(getCurrentPrice(panelStocks[2])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label2.grid(row = 3, column = 2)
canvas2 = FigureCanvasTkAgg(fig1, panelsFrame)
canvas2.get_tk_widget().grid(row = 3, padx = 10, pady = 5)
buyButton2 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[2]))
buyButton2.grid(row = 3, column = 1, sticky = NW, pady = 20)
sellButton2 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[2]))
sellButton2.grid(row = 3, column = 1, sticky = SW, pady = 20)

label3 = Label(panelsFrame, text = panelStocks[3]+ '\n Value: $' +str(getCurrentPrice(panelStocks[3])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label3.grid(row = 4, column = 2)
canvas3 = FigureCanvasTkAgg(fig2, panelsFrame)
canvas3.get_tk_widget().grid(row = 4, padx = 10, pady = 5)
buyButton3 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[3]))
buyButton3.grid(row = 4, column = 1, sticky = NW, pady = 20)
sellButton3 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[3]))
sellButton3.grid(row = 4, column = 1, sticky = SW, pady = 20)

label4 = Label(panelsFrame, text = panelStocks[4]+ '\n Value: $' +str(getCurrentPrice(panelStocks[4])), font = fontStyleSmall, bg = 'midnight blue', fg = 'white')
label4.grid(row = 5, column = 2)
canvas4 = FigureCanvasTkAgg(fig3, panelsFrame)
canvas4.get_tk_widget().grid(row = 5, padx = 10, pady = 5)
buyButton4 = Button(panelsFrame, text = "Buy", font = fontStyleSmall, width = 10, command = lambda : buyStock(panelStocks[4]))
buyButton4.grid(row = 5, column = 1, sticky = NW, pady = 20)
sellButton4 = Button(panelsFrame, text = "Sell", font = fontStyleSmall, width = 10, command = lambda : sellStock(panelStocks[4]))
sellButton4.grid(row = 5, column = 1, sticky = SW, pady = 20)

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

SApic = PhotoImage(file = "C:\\Users\\Andre\\Desktop\\Programs\\Python Programs\\AI Project\\sa.png")
assistantCanvas.create_image(320, 53, image = SApic) #Sets the image to be the background of the canvas

predictionButton = Button(assistantFrame, text = "Predict a stock for me!", fg = "white", bg = "blue", bd = 5, font = fontStyleSmall) #Creates the button to ask for a stock value prediction
predictionButton.grid(padx = 10, pady = 10)

# ***** PORTFOLIO FRAME *****

portfolioFrame = Frame(window, bg = "slate blue") #Creates the frame for displaying stock portfolio
portfolioFrame.grid(row = 1, column = 1, sticky = 'NSE')
portfolioFrame.grid_columnconfigure(0, weight = 1)

portfolioCanvas = Canvas(portfolioFrame, bg = "slate blue", width = 640, height = 100, highlightthickness = 0) #Creates a canvas to display the title image
portfolioCanvas.grid(row = 0, column = 0, columnspan = 2)

portfolioPic = PhotoImage(file = "C:\\Users\\Andre\\Desktop\\Programs\\Python Programs\\AI Project\\portfolio.png")
portfolioCanvas.create_image(320, 50, image = portfolioPic) #Sets the image to be the background of the canvas

portfolioValue = Label(portfolioFrame, text = ("Current Value: $" + str(round(pValue, 2))), bg = "slate blue", fg = "white", font = fontStyle)
portfolioValue.grid(row = 1, column = 0, pady = 20)

portfolioStocks = Label(portfolioFrame, text = ("Current Stocks: " + str(ownedStocks)), bg = "slate blue", fg = "white", font = fontStyle)
portfolioStocks.grid(row = 2, column = 0, pady = 20)

def update():
    print('I UPDATED!')
    updatePortfolioValue()
    print(pValue)
    label1.configure(text = panelStocks[1]+ '\n Value: $' +str(getCurrentPrice(panelStocks[1])))
    label2.configure(text = panelStocks[2]+ '\n Value: $' +str(getCurrentPrice(panelStocks[2])))
    label3.configure(text = panelStocks[3]+ '\n Value: $' +str(getCurrentPrice(panelStocks[3])))
    label4.configure(text = panelStocks[4]+ '\n Value: $' +str(getCurrentPrice(panelStocks[4])))
    label5.configure(text = panelStocks[5]+ '\n Value: $' +str(getCurrentPrice(panelStocks[5])))
    portfolioValue.configure(text = "Current Value: $" + str(round(pValue, 2)))
    portfolioStocks.configure(text = "Current Stocks: " + str(ownedStocks))
    window.after(3000, update)

update()

window.mainloop() #Continuos loop for the window