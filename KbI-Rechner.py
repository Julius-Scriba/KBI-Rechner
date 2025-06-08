import customtkinter as ctk
import threading
import os
from datetime import datetime
import random
from typing import Optional
import psutil
import re
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import schedule
"""Kassenbestands-Ist-Rechner"""

# Logger debug mode
debugMode = bool(False)
class Logger:
    def __init__(self, path, file_name=None, debug_mode=False):
        self.path = path
        self.file_name = file_name if file_name else 'log.txt'
        self.time = datetime.now().time().strftime('%H:%M:%S')
        self.date = datetime.now().date().strftime('%Y-%m-%d')
        self.debug_mode = debug_mode
        if file_name is None: file_name = 'log.txt'
    
    def updateLog():
        startDate = datetime.now().date().strftime('%Y-%m-%d')
        with open() as file:
            pass
    
    def log(self, mode: Optional[str] = 'standart', type: Optional[str] = 'Info', orgin: Optional[str] = None, operation: Optional[str] = None, status: Optional[str] = None):
        import inspect
        self.time = datetime.now().time().strftime('%H:%M:%S')
        self.date = datetime.now().date().strftime('%Y-%m-%d')
        """
        Parameters:
            mode: Debug, Standart
            type: Info, Warning, Error
        
        Format:
            [date time] [type] {orgin} {operation} {status}
            
            orgin:
                function name
                program name
            
            operation:

            
            status: 
                successful : failed
                true       : false
        """
        if self.debug_mode == False and mode.lower() == 'debug': return
        if orgin == None:
            orgin = f'{inspect.stack()[1].function} |'
            if mode.lower() == 'debug':
                print(f'[{self.date} {self.time}] [Warning] Logger.log orgin variable none')
        if operation == None:
            operation = '\\{\\operation\\}\\'
            if mode.lower() == 'debug':
                print(f'[{self.date} {self.time}] [Warning] Logger.log operation variable none')
        if status == None:
            status = ''
            if mode.lower() == 'debug':
                print(f'[{self.date} {self.time}] [Warning] Logger.log status variable none')
        try:
            if type == 'Info/addedValue':
                log_str = f'[{self.date} {self.time}] [Info] {operation}'
            else:
                log_str = f'[{self.date} {self.time}] [{type}] {orgin} {operation} {status}'
            if mode.lower() == 'debug':
                print(f'[{self.date} {self.time}] [Info] log_str creation successfull')
            with open(f'{self.path}\\{self.file_name}', 'a') as log_file:
                if mode.lower() == 'debug':
                    print(f'[{self.date} {self.time}] [Info] file creation successful')
                print(log_str)
                log_file.write(log_str+'\n')
                log_file.close()
                return
        except Exception as e:
            print(f'[{self.date} {self.time}] [Error] Logger.log function failed: {str(e)}')
            return


logger = Logger(path='C:\\Users\\Jack Nores Smith\\Downloads', debug_mode=debugMode)

app = ctk.CTk() 
logger.log(type='Info', orgin='program', operation='started', status='successfully')
app.title('KbI-Zähler')
app.attributes('-topmost', True)
app.resizable(width=False, height=False)
#ctk.set_widget_scaling(1.2)
#app.geometry('180x230')
#ctk.set_window_scaling(0.5)

operands = ctk.StringVar()
overallResult = ctk.DoubleVar()

current_value = ctk.DoubleVar()
current_count = ctk.IntVar()
current_Cvalue = ctk.DoubleVar(value=0.00)

valuesList = list()
currentListPos = None

coinValues = ['2.00', '1.00', '0.50', '0.20', '0.10', '0.05', '0.02', '0.01']

standardChange = ctk.DoubleVar(value=450)

# Coin & Bill Log
coin_2_00_count = (2.00, 0) # Format: (CoinValue, Count)
coin_1_00_count = (1.00, 0)
coin_0_50_count = (0.50, 0)
coin_0_20_count = (0.20, 0)
coin_0_10_count = (0.10, 0)
coin_0_05_count = (0.05, 0)
coin_0_02_count = (0.02, 0)
coin_0_01_count = (0.01, 0)

coin_2_00_value = ctk.DoubleVar(value=0)
coin_1_00_value = ctk.DoubleVar(value=0)
coin_0_50_value = ctk.DoubleVar(value=0)
coin_0_20_value = ctk.DoubleVar(value=0)
coin_0_10_value = ctk.DoubleVar(value=0)
coin_0_05_value = ctk.DoubleVar(value=0)
coin_0_02_value = ctk.DoubleVar(value=0)
coin_0_01_value = ctk.DoubleVar(value=0)

bill_500_count = (500, 0)
bill_200_count = (200, 0)
bill_100_count = (100, 0)
bill_050_count = (50, 0)
bill_020_count = (20, 0)
bill_010_count = (10, 0)
bill_005_count = (5, 0)

bill_500_value = ctk.DoubleVar(value=0)
bill_200_value = ctk.DoubleVar(value=0)
bill_100_value = ctk.DoubleVar(value=0)
bill_050_value = ctk.DoubleVar(value=0)
bill_020_value = ctk.DoubleVar(value=0)
bill_010_value = ctk.DoubleVar(value=0)
bill_005_value = ctk.DoubleVar(value=0)

coin_Counts = [coin_2_00_count, coin_1_00_count, coin_0_50_count, 
              coin_0_20_count, coin_0_10_count, coin_0_05_count, 
              coin_0_02_count, coin_0_01_count]
bill_Counts = [bill_500_count, bill_200_count, bill_100_count, 
              bill_050_count, bill_020_count, bill_010_count, 
              bill_005_count]

total_counts = [
    bill_500_count,
    bill_200_count, 
    bill_100_count, 
    bill_050_count, 
    bill_020_count, 
    bill_010_count, 
    bill_005_count,
    coin_2_00_count, 
    coin_1_00_count, 
    coin_0_50_count, 
    coin_0_20_count, 
    coin_0_10_count, 
    coin_0_05_count, 
    coin_0_02_count, 
    coin_0_01_count
]

def getTotal():
    totalvalue = 0
    for count in total_counts:
        totalvalue += (count[0]*count[1])
    totalvalue = round(totalvalue, 2)
    return totalvalue

total_Counts = (bill_Counts, coin_Counts)
    
global remained
global withdrawable

# Settings
automatic_switching = ctk.BooleanVar(value=True)    # By default True/On
nonReset = ctk.BooleanVar(value=False)      # By default False/Off
extraWeight = ctk.IntVar(value=34)  # By default 0

show_powerbar = ctk.BooleanVar(value=True)
show_procentages = ctk.BooleanVar(value=False)
show_remainingTime = ctk.BooleanVar(value=True)

focusMode_onStart = ctk.BooleanVar(value=True)  # By default True/On
autoReportEmail_onExit = ctk.BooleanVar(value=True) # By default True/On
autoShutdown_onExit = ctk.BooleanVar(value=False)   # By default False/Off
autoSave = ctk.BooleanVar(value=True)
easyUse = ctk.BooleanVar(value=True)

changers_color = ctk.Variable(value=['#F9F9FA', '#343638'])

# Non Necessary
next_state = ctk.DoubleVar(value=2.00)
currentState_ExtraWeight = ctk.DoubleVar(value=None)

def fill_debug_values():
    global coin_2_00_count, coin_1_00_count, coin_0_50_count, coin_0_20_count, coin_0_10_count, coin_0_05_count, coin_0_02_count, coin_0_01_count
    global coin_2_00_value, coin_1_00_value, coin_0_50_value, coin_0_20_value, coin_0_10_value, coin_0_05_value, coin_0_02_value, coin_0_01_value
    global bill_500_count, bill_200_count, bill_100_count, bill_050_count, bill_020_count, bill_010_count, bill_005_count
    global bill_500_value, bill_200_value, bill_100_value, bill_050_value, bill_020_value, bill_010_value, bill_005_value

    # Assigning debug counts
    coin_2_00_count = (2.00, 23)
    coin_1_00_count = (1.00, 15)
    coin_0_50_count = (0.50, 35)
    coin_0_20_count = (0.20, 24)
    coin_0_10_count = (0.10, 30)
    coin_0_05_count = (0.05, 40)
    coin_0_02_count = (0.02, 50)
    coin_0_01_count = (0.01, 112)

    coin_2_00_value.set(coin_2_00_count[0] * coin_2_00_count[1])
    coin_1_00_value.set(coin_1_00_count[0] * coin_1_00_count[1])
    coin_0_50_value.set(coin_0_50_count[0] * coin_0_50_count[1])
    coin_0_20_value.set(coin_0_20_count[0] * coin_0_20_count[1])
    coin_0_10_value.set(coin_0_10_count[0] * coin_0_10_count[1])
    coin_0_05_value.set(coin_0_05_count[0] * coin_0_05_count[1])
    coin_0_02_value.set(coin_0_02_count[0] * coin_0_02_count[1])
    coin_0_01_value.set(coin_0_01_count[0] * coin_0_01_count[1])

    bill_500_count = (500, 0)
    bill_200_count = (200, 0)
    bill_100_count = (100, 2)
    bill_050_count = (50, 7)
    bill_020_count = (20, 10)
    bill_010_count = (10, 19)
    bill_005_count = (5, 25)

    bill_500_value.set(bill_500_count[0] * bill_500_count[1])
    bill_200_value.set(bill_200_count[0] * bill_200_count[1])
    bill_100_value.set(bill_100_count[0] * bill_100_count[1])
    bill_050_value.set(bill_050_count[0] * bill_050_count[1])
    bill_020_value.set(bill_020_count[0] * bill_020_count[1])
    bill_010_value.set(bill_010_count[0] * bill_010_count[1])
    bill_005_value.set(bill_005_count[0] * bill_005_count[1])
    
    global total_Counts, coin_Counts, bill_Counts, totalValue
    
    value_vars = [
        [bill_500_value, bill_200_value, bill_100_value, bill_050_value, bill_020_value, bill_010_value, bill_005_value],
        [coin_2_00_value, coin_1_00_value, coin_0_50_value, coin_0_20_value, coin_0_10_value, coin_0_05_value, coin_0_02_value, coin_0_01_value]
    ]

    totalValue = 0
    for item in value_vars:
        for value in item:
            totalValue += round(value.get(), 2)
    totalValue = round(totalValue, 2)
    print(totalValue, '€')
    
    coin_Counts = [coin_2_00_count, coin_1_00_count, coin_0_50_count, 
              coin_0_20_count, coin_0_10_count, coin_0_05_count, 
              coin_0_02_count, coin_0_01_count]
    bill_Counts = [bill_500_count, bill_200_count, bill_100_count, 
                bill_050_count, bill_020_count, bill_010_count, 
                bill_005_count]

    total_Counts = (bill_Counts, coin_Counts)
    
    global total_counts
    total_counts = [
        bill_500_count,
        bill_200_count, 
        bill_100_count, 
        bill_050_count, 
        bill_020_count, 
        bill_010_count, 
        bill_005_count,
        coin_2_00_count, 
        coin_1_00_count, 
        coin_0_50_count, 
        coin_0_20_count, 
        coin_0_10_count, 
        coin_0_05_count, 
        coin_0_02_count, 
        coin_0_01_count
    ]
    
    results = list()
    
    for value in bill_Counts:
        bill_value = value[0]
        bill_count = value[1]
        res = bill_count * bill_value
        results.append(res)
    
    for value in coin_Counts:
        coin_value = value[0]
        coin_count = value[1]
        res = coin_count * coin_value
        results.append(res)
    
    final_result = 0
    for res in results:
        final_result += res
    
    overallResult.set(value=float(round(final_result, 2)))
        

def getValue():
    logger.log(mode='Debug', type='Info', orgin='getValue', operation='called', status='successfull')
    CoinValue = menuCoinValue.get()
    currentCount = 0
    for currency in total_counts:
        currency_value = currency[0]
        currency_count = currency[1]
        if currency_value == CoinValue:
            currentCount = currency_count
            break
    gramm = int(entryWeight.get())
    extraWeight = int(entryExtraWeight.get())
    if CoinValue == '2.00':
        StGeMü = 8.5
    elif CoinValue == '1.00':
        StGeMü = 7.5
    elif CoinValue == '0.50':
        StGeMü = 7.8
    elif CoinValue == '0.20':
        StGeMü = 5.74
    elif CoinValue == '0.10':
        StGeMü = 4.1
    elif CoinValue == '0.05':
        StGeMü = 3.92
    elif CoinValue == '0.02':
        StGeMü = 3.06
    elif CoinValue == '0.01':
        StGeMü = 2.3
    else:
        if easyUse.get() == True:
            menuCoinValue.set('2.00')
            CoinValue = '2.00'
            StGeMü = 8.5
        else:
            print('Please choose a Coin Value!')
            return 0
    totalValue = ((gramm-extraWeight)/StGeMü)*float(CoinValue)
    amountOfCoins = round(((gramm-extraWeight)/StGeMü))
    totalValue = round(float(totalValue), 3)
    totalValue = (amountOfCoins*float(CoinValue))
    
    amountText = ('Amount:  '+str(amountOfCoins)+' Coins')
    labelAmount.configure(text=amountText)
    
    totalValueText = ('Total Value:  '+str(round(totalValue, 2))+' €')
    labelValue.configure(text=totalValueText)
    entryWeight.delete(0, ctk.END)
    if nonReset.get() == True:
        pass
    elif automatic_switching.get() == True:
        switchValue(to='Low')
    else:
        menuCoinValue.set('Coin Value')
    
    current_value.set(float(round(totalValue, 2)))
    
    current_count.set(amountOfCoins)
    
    addButton.configure(state='normal')
    
    current_Cvalue.set(CoinValue)

    app.update()
    logger.log(mode='Debug', type='Info', orgin='getValue', operation='executed', status='successfull')
    global coinWeight
    coinWeight = gramm-extraWeight
    return 0

def addOperand(operand, case, count):
    currentTime = datetime.now().time().strftime("%H:%M:%S")
    current_OResult = overallResult.get()
    result = round(current_OResult+operand, 2)
    overallResult.set(value=float(result))
    textResult = ('= '+str(overallResult.get())+' €')
    labelResult.configure(text=textResult)
    valuesList.append(result)
    if case == 1:
        insertText = (' + '+str(operand))
    elif case == 2:
        insertText = (' + '+str(operand)+' €, '+str(count)+' Stk, '+ f'(CV: {current_Cvalue.get()} €) | {currentTime}')
    if bool(textboxOperands.get(0.0, ctk.END)) == True:
        insertText = (insertText + '\n')
    textboxOperands.configure(state='normal')
    textboxOperands.insert(ctk.END, text=insertText)
    textboxOperands.configure(state='disabled')
    addButton.configure(state='disabled')
    app.update()
    for item in coin_Counts:
        indexInLs = coin_Counts.index(item)
        value = item[0]
        available = item[1]
        if value == current_Cvalue.get():
            available += count
            coin_Counts[indexInLs] = (value, available)
    print('Coin Counts: ', coin_Counts)
    print('Total Count: ', total_counts)
    insertText = insertText[:-12]+f', (CW: {coinWeight} g)'
    logger.log(type='Info/addedValue', operation=insertText)
    return

def reset_TextboxValue(func):
    if func == '1':
        overallResult.set(value=0)
        textboxOperands.configure(state='normal')
        textboxOperands.tag_add("stike", "0.0", "end")
        textboxOperands.tag_config("strike", overstrike=True)
        textboxOperands.configure(state='disabled')
        textboxOperands.update()
        labelResult.configure(text='= 0.00 €')
    else:
        None
    frameMverification.place_forget()
    app.update()

def updateImportedFiles():
    return
       
def centerProgram(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

def step_Back():
    if len(valuesList) < 2:
        print('Step Back is not possible. Only one Value available!')
        return
    else:
        pass
    lastResult = valuesList[len(valuesList)-1]
    print(len(valuesList))
    labelResult.configure(text=lastResult)
    app.update()

def switchValue(to):
    current_value = menuCoinValue.get()
    if current_value == 'Coin Value':
        if to == 'High':
            menuCoinValue.set(value='0.01')
        elif to == 'Low':
            menuCoinValue.set(value='2.00')
        return
    coinC = coinValues.index(current_value)
    if to == 'High':
        next_value = coinC-1
    elif to == 'Low':
        next_value = coinC+1
        if next_value == 8:
            next_value = 0
    menuCoinValue.set(value=coinValues[next_value])

def addAdditionalValue():
    currentTime = datetime.now().time().strftime("%H:%M:%S")
    txt = additionalValueEntry.get()
    if txt == '/settings':
        additionalValueEntry.delete(0, ctk.END)
        mainFrame.pack_forget()
        settingsFrame.pack()
        global threadSettingsFrame
        threadSettingsFrame = threading.Thread(target=check_state)
        threadSettingsFrame.start()
        app.update()
        return threadSettingsFrame
    elif txt == '/shutdown':
        shutdown(True, True)
        return
    elif txt == '/save':
        save_log()
        return
    elif txt.lower() == '/sre' or txt.lower() == '/sendReportEmail':
        prepHTMLEmail()
        return
    elif txt.startswith('/seller '):
        startPos = len("/seller ")
        endPos = len(txt)
        newUser = txt[startPos:endPos].strip()
        h1.configure(text=newUser)
        app.update()
        print(f'Log:    {newUser} has logged in!')
        additionalValueEntry.delete(0, ctk.END)
        return
    elif txt == "cw()":
        calcWithdrawal(total=overallResult.get(), change=standardChange.get())
        return
    elif txt == "/print_tc":
        print(total_counts)
        return
    elif txt == '/exit':
        try:
            fullscreen.destroy()
            reportWindow.destroy()
            pass
        except:
            pass
        app.destroy()
        print('Log:    User closed App!')
        return
    elif txt == '/focus':
        logger.log(orgin='command promt', operation='start focus mode')
        focusWindow()
        return
    elif txt.startswith('/report'):
        if txt.lower() == '/report a':
            updateReport()
            reportWindowFunc(mode='all')
        elif txt.lower() == '/report b':
            updateReport()
            reportWindowFunc(mode='onlyChange')
        return
    elif txt == '/debug':
        global debugMode
        if debugMode == False:
            debugMode = True
            logger.log(operation='debug-mode=', status='true')
        else:
            debugMode = False
            logger.log(operation='debug-mode=', status='false')
        additionalValueEntry.delete(0, ctk.END)
        return
    listed = txt.split(', ')
    additionalValue = int(listed[0])
    logger.log(operation=f'additionalValue= {additionalValue}')
    billValue = int(listed[1])
    billCount = int(additionalValue/billValue)
    insertStr = f' + {additionalValue} €, {billCount} Stk, (BV: {billValue} €) | {currentTime}\n'
    current_OResult = overallResult.get()
    next_OResult = current_OResult + additionalValue
    overallResult.set(value=next_OResult)
    labelResult.configure(text=f'= {overallResult.get()} €')
    textboxOperands.configure(state='normal')
    textboxOperands.insert(index=ctk.END, text=insertStr)
    textboxOperands.configure(state='disabled')
    additionalValueEntry.delete(0, ctk.END)
    for item in bill_Counts:
        indexInLs = bill_Counts.index(item)
        value = item[0]
        available = item[1]
        if value == billValue:
            available += billCount
            bill_Counts[indexInLs] = (value, available)
            logger.log(mode='debug', type='Info/addedValue', operation=f'bills_Counts: {bill_Counts}')
    insertStr = insertStr[:-12]
    logger.log(type='Info/addedValue', operation=insertStr)
    app.update()

def focusWindow():
    centerProgram(app)
    global fullscreen
    try:
        if fullscreen.winfo_exists():
            fullscreen.destroy()
            additionalValueEntry.delete(0, ctk.END)
            return
    except:
        fullscreen = ctk.CTk()
        fullscreen.attributes('-fullscreen', True)
        fullscreen.overrideredirect(True)
        if (additionalValueEntry and additionalValueEntry.get().strip()):
            additionalValueEntry.delete(0, ctk.END)
        exitButton = ctk.CTkButton(master=fullscreen, text='X', command=lambda: fullscreen.destroy(),
                                       fg_color='darkred', hover_color='red', width=50, height=50, font=('Helvetica', 20))
        exitButton.pack(side='top', anchor='ne', padx=(20, 0))
        
        reportEmailBtn = ctk.CTkButton(fullscreen, text='Report Email', font=('Helvetica', 20),
                                       height=50, fg_color="darkgreen", hover_color="green", command=prepHTMLEmail)
        reportEmailBtn.place(x=10, y=10)
        
        fullscreen.mainloop()
        return

def quitSettingsFrame():
    settingsFrame.pack_forget()
    mainFrame.pack()
    entryExtraWeight.configure(text=extraWeight.get())

def change_state(func):
    if func == 'automatic_switching':
        if automatic_switching.get() == False:
            nonReset.set(value=False)
            automatic_switching.set(value=True)
        else:
            automatic_switching.set(value=False)
    elif func == 'nonReset':
        if nonReset.get() == False:
            automatic_switching.set(value=False)
            nonReset.set(value=True)
        else:
            nonReset.set(value=False)

def check_state():
    print('run check_state')
    while settingsFrame.winfo_viewable():
        if extraWeightSetEntry.get() != currentState_ExtraWeight.get():
            print('checks state')
            currentState_ExtraWeight.set(value=extraWeightSetEntry.get())
            if autoSave.get() is True:
                extraWeight.set(currentState_ExtraWeight)
                print(extraWeight.get())
            continue
        else:
            continue

def save_log():
    log_txt = textboxOperands.get('0.0', 'end').replace('\n', '\n'+(' '*4))
    log_txt = (' '*3)+log_txt
    if log_txt is None:
        return
    with open("KbI-Rechner-Log.txt", "a") as file:
        file.write(f'New LogNote:  {datetime.now().date().strftime("%d-%m-%Y")} ; {datetime.now().time().strftime("%H:%M:%S")}\n')
        file.write(log_txt)
        file.close()
    


def save_settings():
    extraWeight.set(value=extraWeightSetEntry.get())
    entryExtraWeight.insert(index=1, string=extraWeight.get())

def color_chooser():
    pass

def saveCurrentSession():
    log_text = textboxOperands.get('0.0', ctk.END)
    with open() as file:
        file.write('\n')
        for line in log_text:
            file.write(line)
        file.close()

def displayCurrentTime():
    currentTime = datetime.now().time().strftime("%H:%M:%S")
    timeDisplay.configure(text=currentTime)
    app.update()
    if currentTime == "00:00:01":
        newDate = datetime.now().date().strftime("%d-%m-%Y")
        dateDisplay.configure(text=newDate)
        print(f"Log:    Updated Date to {newDate}")
    app.after(1000, displayCurrentTime)

def powerWarning(percent):
    if percent <= 10:
        if powerbar.cget('progress_color') == 'red':
            powerbar.configure(progress_color='grey')
        else:
            powerbar.configure(progress_color='red')
        app.update_idletasks()
        app.after(500, powerWarning, percent)
    else:
        return

def updatePowerbar():
    battery = psutil.sensors_battery()
    if battery is not None:
        global percent
        percent = battery.percent
        plugged = battery.power_plugged
        remainingTimeMin = int(round(battery.secsleft / 60, 2))
        endStr = ' m'
        # if remainingTimeMin >= 60:
        #     endStr = ' h'
        #     remainingTimeMin = round(battery.secsleft / 3600, 2) # Hours
        if plugged:
            pluggedString = ' plugged'
            remainingTimeHour = pluggedString
            remainingTimeSec = pluggedString
            endStr = None
        formated_percent = percent/100
        powerbar.set(value=formated_percent)
        if endStr is not None:
            remainingTimeLabel.configure(text=str(remainingTimeMin)+ endStr)
        else:
            remainingTimeLabel.configure(text='plugged')
        logger.log(mode='debug', operation='read battery-status', status='sucessful')
        logger.log(mode='debug', operation=f'battery-status: {percent}')
        if percent < 20:
            powerbar.configure(progress_color='red')
            if percent <= 10:
                powerWarning(percent)
        elif percent < 50:
            powerbar.configure(progress_color='orange')
        else:
            powerbar.configure(progress_color='green')
    else:
        logger.log(mode='debug', operation='read battery-status', status='failed')
        pass
    app.update_idletasks()
    app.after(10000, updatePowerbar)

def getWithdrawable(currency_list, change):
    # define total
    total = 0
    for currency in currency_list:
        total += (currency[1]*currency[0])
    total = round(total, 2)
    
    # define withdraw values
    withdrawValue = round(total-change, 2)
    withdrawList = []
    
    changeList = []
    
    for currency in currency_list:
        currency_value = currency[0]
        currency_count = currency[1]
        if currency_value <= withdrawValue:
            maxQuotient = round(withdrawValue // currency_value)
            if maxQuotient <= currency_count:
                withdraw_count = int(maxQuotient)
                currency_count -= maxQuotient
            else:
                withdraw_count = int(currency_count)
                currency_count = 0
        else:
            withdraw_count = 0
        withdrawValue -= withdraw_count*currency_value
        withdrawValue = round(withdrawValue, 2)
        currency_count = int(currency_count)
        withdrawList.append([currency_value, withdraw_count])
        changeList.append([currency_value, currency_count])
    withdrawValue = round(total-change, 2)
    return withdrawValue, withdrawList, changeList

def calcWithdrawal(total, change, returnAll=True):
    try:
        remained = round(total-change, 2)
        logger.log(mode='debug', operation=f'Remained: {remained}')
        print(remained) # currently editing !!!
    except Exception as error:
        logger.log(mode='debug', operation='get remained', status=f'failed with: {error}')
        # remained = total
        return 0
    if remained <= 0:
        return 0
    global currencyValues
    currencyValues = list() # Es darf nur das verwendet werden, von dem auch etwas verfügbar ist.
    for bill in bill_Counts:
        billValue = bill[0]
        billCount = bill[1]
        if billCount != 0:
            currencyValues.append((billValue, billCount))
    for coin in coin_Counts:
        coinValue = coin[0]
        coinCount = coin[1]
        if coinCount != 0:
            currencyValues.append((coinValue, coinCount))
    if not currencyValues:
        return 0
    print(f'currencyValues: {currencyValues}')
    withdrawable = {}   # bills & coins to withdraw
    while remained != 0:
        for item in currencyValues:
            logger.log(mode='debug', type='Info', operation=f'{item}')
            value = item[0]
            available = item[1]
            if remained == 0:
                break
            if value <= remained:
                quotient = int(remained // value)
                if quotient <= available:
                    deductionValue = quotient*value
                    remainCount = available-deductionValue
                    if remainCount < 0:
                        remainCount = 0
                else:
                    deductionValue = available*value
                    remainCount = 0
                """                                                 # Chaning values only locally
                if value <= 2:
                    index = coin_Counts.index(item)
                    coin_Counts[index] = (value, remainCount)
                elif value >= 5:
                    index = bill_Counts.index(item)
                    bill_Counts[index] = (value, remainCount)
                """
                index = currencyValues.index(item)
                currencyValues[index] = (value, remainCount)
                remained = round(remained-deductionValue, 2)
                print(f'{round(remained, 2)} -= ({value} x {quotient}) : {round(remained, 2)}')
                withdrawable[value] = quotient
            else:
                continue
    logger.log(operation=f'remained: {remained}')       # sollte nach der implementierung in die gui in debug mode gesetzt werden!
    print('Remained Type:', type(remained), 'Remained:', remained)
    logger.log(operation=f'withdraw: {withdrawable}')
    print('Withdrawable Type:', type(withdrawable), 'Withdrawable:', withdrawable)
    return withdrawable

def updateReport(reportTxt=False):
    withdrawable = calcWithdrawal(total=overallResult.get(), change=standardChange.get())
    logger.log(mode='debug', type='Info/addedValue', operation=f'bills: {bill_Counts}')
    logger.log(mode='debug', type='Info/addedValue', operation=f'coins: {coin_Counts}')
    logger.log(mode='debug', type='Info/addedValue', operation=f'withdrawable: {withdrawable}')
    if reportTxt == True:
        for item in bill_Counts:
            value = item[0]
            count = item[1]
            lineLenght = 20
            sideString = str(int(lineLenght/2)*' ')
            txt = (sideString+str(value)+sideString+sideString+str(count))
            print(txt)
    return

def sendEmail(subject, message, receiver):
    sender = 'reportSystemMHS@gmail.com'
    password = 'jvsq dgxv fgkh sdmr'

    receiver = receiver if receiver else 'jacknoressmith@web.de'
    subject = subject if subject else f'Report KbI-Rechner Fehlgeschlagen'
    message = message if message else 'Die Nachricht konnte nicht ordnungsgemäß versendet werden! Senden sie nochmals eine Anfrage.'
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receiver, msg.as_string())
        logger.log(operation='email send', status='successfuly')
    except Exception as error:
        logger.log(operation=f'error has ocurred: {error}')

def sendHTMLReportEmail(subjec, message, receiver):
    pass

def sendReportEmail():  # Bericht via Email
    # totalValue, withdraw, change = generateReport()
    currentHour = int(datetime.now().strftime("%H"))
    if currentHour <= 11:
        daytime = 'Morgens'
    elif currentHour > 12 and currentHour < 14:
        daytime = 'Mittags'
    elif currentHour > 14:
        daytime = 'Abends'
    else:
        daytime = 'Day'
    subject = f'KbI-Rechner Report | {daytime}'
    message = str('')
    # gesamt
    message += 'Gesamt:\n'
    for list in total_Counts:
        for item in list:
            value = item[0]
            count = item[1]
            string = f'{value}, {count}'
            print(string)
            message += ('\n'+string)
    withdrawable = calcWithdrawal(total=overallResult.get(), change=standardChange.get())
    message += '\n\nWithdrawed:\n'
    if type(withdrawable) != int:
        for item in withdrawable:
            message += ('\n'+item)
    else:
        message += '\nNothing to Withdraw!'
    print('Report Email Message: ', message)
    # message.join(f'\nTotal Value: {totalValue}')
    # if withdraw != None:
    #     message += ('\nWithdraw:')
    #     tabSpace = ' '*4
    #     for item in withdraw:
    #         value = item[0]
    #         count = item[1]
    #         if value < 5:
    #             typ = 'Münze'
    #         else:
    #             typ = 'Schein'
    #         message += ('\n'+tabSpace+f'{value} {typ}, {count} Stk')
    # message += (f'\nChange: {change}')
    receiver = 'Juliuslianscriba@gmail.com'
    sendEmail(subject=subject, message=message, receiver=receiver)

def sendHTMLEmail(subject, message_html, message_plain=None, receiver=None):
    sender = 'reportSystemMHS@gmail.com'
    password = 'jvsq dgxv fgkh sdmr'

    receiver = receiver if receiver else 'jacknoressmith@web.de'
    subject = subject if subject else f'Report KbI-Rechner Fehlgeschlagen'
    message_html = message_html if message_html else None
    message_plain = message_plain if message_plain else None
    
    msg = MIMEText(message_html, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receiver, msg.as_string())
        logger.log(operation='email sended', status='successfull')
    except Exception as error:
        print(f'error has occurred: {error}')
        


def prepHTMLEmail():
    try:
        receiver = 'juliuslianscriba@gmail.com'
        with open('C:\\Users\\Jack Nores Smith\\Downloads\\KbI-Rechner-SW\\emailLayout.html', 'r') as file:
            message = file.read()
            file.close()
        date = datetime.now().date().strftime('%d/%m/%Y')
        time = datetime.now().time().strftime('%H:%M:%S')
        if time <= '11:30':
            daytimezone = 'Morgens'
        elif time >= '11:30' and time <= '15:30':
            daytimezone = 'Mittags'
        elif time > '15:30':
            daytimezone = 'Abends'
        seller = 'Julius'
        worktime = '7h'
        shift = '1'
        wv, wl, cl = getWithdrawable(currency_list=total_counts, change=standardChange.get())
        total = getTotal()
        withdraw = []
        change = []
        totalValues = [withdraw, change]
        for varLs in totalValues:
            totalValue_bill = 0
            totalValue_coin = 0
            curr_ls = 'bill'
            for currency in wl:
                currency_value = currency[0]
                currency_count = currency[1]
                res = currency_count*currency_value
                if currency_value >= 5.00:
                    totalValue_bill += round(res, 2)
                elif currency_value <= 2.00:
                    totalValue_coin += round(res, 2)
            varLs.append(round(totalValue_bill, 2))
            varLs.append(round(totalValue_coin, 2))
                    
        replacements_dict = {
            "{date_str}": date.replace("/", "."),
            "{time_str}": time,
            "{seller_str}": seller,
            "{worktime_str}": worktime,
            "{shift_str}": shift,
            
            "500_count_withdrawed": str(wl[0][1]),
            "500_value_withdrawed": str(wl[0][0]*wl[0][1]),
            "200_count_withdrawed": str(wl[1][1]),
            "200_value_withdrawed": str(wl[1][0]*wl[1][1]),
            "100_count_withdrawed": str(wl[2][1]),
            "100_value_withdrawed": str(wl[2][0]*wl[2][1]),
            "050_count_withdrawed": str(wl[3][1]),
            "050_value_withdrawed": str(wl[3][0]*wl[3][1]),
            "020_count_withdrawed": str(wl[4][1]),
            "020_value_withdrawed": str(wl[4][0]*wl[4][1]),
            "010_count_withdrawed": str(wl[5][1]),
            "010_value_withdrawed": str(wl[5][0]*wl[5][1]),
            "005_count_withdrawed": str(wl[6][1]),
            "005_value_withdrawed": str(wl[6][0]*wl[6][1]),
            
            "total_bill_value_withdrawed": str(withdraw[0]),
            
            "2.00_count_withdrawed": str(wl[7][1]),
            "2.00_value_withdrawed": str(wl[7][0]*wl[7][1]),
            "1.00_count_withdrawed": str(wl[8][1]),
            "1.00_value_withdrawed": str(wl[8][0]*wl[8][1]),
            "0.50_count_withdrawed": str(wl[9][1]),
            "0.50_value_withdrawed": str(wl[9][0]*wl[9][1]),
            "0.20_count_withdrawed": str(wl[10][1]),
            "0.20_value_withdrawed": str(wl[10][0]*wl[10][1]),
            "0.10_count_withdrawed": str(wl[11][1]),
            "0.10_value_withdrawed": str(wl[11][0]*wl[11][1]),
            "0.05_count_withdrawed": str(wl[12][1]),
            "0.05_value_withdrawed": str(wl[12][0]*wl[12][1]),
            "0.02_count_withdrawed": str(wl[13][1]),
            "0.02_value_withdrawed": str(wl[13][0]*wl[13][1]),
            "0.01_count_withdrawed": str(wl[14][1]),
            "0.01_value_withdrawed": str(wl[14][0]*wl[14][1]),
            
            "total_coin_value_withdrawed": str(withdraw[1]),
            "total_value_withdrawed": str(wv),


            "500_count_change": str(cl[0][1]),
            "500_value_change": str(cl[0][0]*cl[0][1]),
            "200_count_change": str(cl[1][1]),
            "200_value_change": str(cl[1][0]*cl[1][1]),
            "100_count_change": str(cl[2][1]),
            "100_value_change": str(cl[2][0]*cl[2][1]),
            "50_count_change": str(cl[3][1]),
            "50_value_change": str(cl[3][0]*cl[3][1]),
            "20_count_change": str(cl[4][1]),
            "20_value_change": str(cl[4][0]*cl[4][1]),
            "10_count_change": str(cl[5][1]),
            "10_value_change": str(cl[5][0]*cl[5][1]),
            "5_count_change": str(cl[6][1]),
            "5_value_change": str(cl[6][0]*cl[6][1]),
            
            "total_bill_value_change": str(change[0]),
            
            "2.00_count_change": str(cl[7][1]),
            "2.00_value_change": str(cl[7][0]*cl[7][1]),
            "1.00_count_change": str(cl[8][1]),
            "1.00_value_change": str(cl[8][0]*cl[8][1]),
            "0.50_count_change": str(cl[9][1]),
            "0.50_value_change": str(cl[9][0]*cl[9][1]),
            "0.20_count_change": str(cl[10][1]),
            "0.20_value_change": str(cl[10][0]*cl[10][1]),
            "0.10_count_change": str(cl[11][1]),
            "0.10_value_change": str(cl[11][0]*cl[11][1]),
            "0.05_count_change": str(cl[12][1]),
            "0.05_value_change": str(cl[12][0]*cl[12][1]),
            "0.02_count_change": str(cl[13][1]),
            "0.02_value_change": str(cl[13][0]*cl[13][1]),
            "0.01_count_change": str(cl[14][1]),
            "0.01_value_change": str(cl[14][0]*cl[14][1]),
            
            "total_coin_value_change": str(change[1]),
            "total_value_change": str()
        }
        for placeholder, replacement in replacements_dict.items():
            message = message.replace(placeholder, replacement)
        subject = f'Kassenbericht am {date.replace("/", ".")} | {daytimezone}'
        sendHTMLEmail(message_html=message, subject=subject, receiver=receiver)
    except Exception as error:
        print(f'error has occured: {error}')

def reportWindowFunc(mode):
    if mode is None:
        mode = 'all'
    global reportWindow
    try:
        additionalValueEntry.delete(0, 'end')
        if reportWindow.winfo_exists():
            reportWindow.destroy()
            return
    except:
        reportWindow = ctk.CTk()
        reportWindow.title(string='Report')
        reportWindow.attributes('-topmost', True)
        reportWindow.resizable(width=False, height=False)

        rW_mainFrame = ctk.CTkFrame(master=reportWindow, fg_color='transparent')
        rW_mainFrame.pack(expand=True, fill='both')  

        rW_valuesFrame = ctk.CTkFrame(master=rW_mainFrame, fg_color='darkorange', corner_radius=0)  
        rW_valuesFrame.pack(expand=True, fill='both')  

        rW_billValueLabel = ctk.CTkLabel(master=rW_valuesFrame, text='Bill Value')  
        rW_billValueLabel.grid(row=0, column=0, padx=5, pady=5)  
        rW_billCountLabel = ctk.CTkLabel(master=rW_valuesFrame, text='Count')  
        rW_billCountLabel.grid(row=0, column=1, padx=5, pady=5)  
        rW_billValueLabel = ctk.CTkLabel(master=rW_valuesFrame, text='Value')  
        rW_billValueLabel.grid(row=0, column=2, padx=5, pady=5)
        
        coins_data = []
        coins_total = float()
        bills_data = []
        bills_total = int()
        if mode == 'all':
            for item in bill_Counts:
                bill = item[0]
                count = item[1]
                value = round(count*bill, 2)
                bills_data.append((bill, count, value))
                bills_total += value
        elif mode == 'onlyChange':
            for item in currencyValues:
                currency = item[0]
                count = item[1]
                value = round(count*currency, 2)
                if currency < 5:
                    coins_data.append((currency, count, value))
                    coins_total += value
                elif currency >= 5:
                    bills_data.append((currency, count, value))
                    bills_total += value

        for i, (bill, count, value) in enumerate(bills_data):
            i+=1
            rW_bill_label = ctk.CTkLabel(master=rW_valuesFrame, text=bill)  
            rW_bill_label.grid(row=i, column=0, padx=5, pady=5)
            rW_bill_count = ctk.CTkLabel(master=rW_valuesFrame, text=count)  
            rW_bill_count.grid(row=i, column=1, padx=5, pady=5)
            rW_bill_value = ctk.CTkLabel(master=rW_valuesFrame, text=value)  
            rW_bill_value.grid(row=i, column=2, padx=5, pady=5)

        rW_totalBillsFrame = ctk.CTkFrame(master=rW_mainFrame, fg_color='grey', corner_radius=0)  
        rW_totalBillsFrame.pack(expand=True, fill='both', padx=0, pady=0)  

        rW_totalBillsLabel = ctk.CTkLabel(master=rW_totalBillsFrame, text='Total Bills Value:')  
        rW_totalBillsLabel.grid(row=0, column=0, padx=5, pady=5)  
        rW_totalBillsValue = ctk.CTkLabel(master=rW_totalBillsFrame, text=f'{bills_total} €', anchor='e')  
        rW_totalBillsValue.grid(row=0, column=1, padx=5, pady=5)

        rW_valuesFrame2 = ctk.CTkFrame(master=rW_mainFrame, fg_color='darkorange', corner_radius=0)  
        rW_valuesFrame2.pack(expand=True, fill='both')
        
        rW_coinValueLabel = ctk.CTkLabel(master=rW_valuesFrame2, text='Coin Value')  
        rW_coinValueLabel.grid(row=0, column=0, padx=5, pady=5)  
        rW_coinCountLabel = ctk.CTkLabel(master=rW_valuesFrame2, text='Count')  
        rW_coinCountLabel.grid(row=0, column=1, padx=5, pady=5, sticky='ew')  
        rW_coinValueLabel = ctk.CTkLabel(master=rW_valuesFrame2, text='Value')  
        rW_coinValueLabel.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        if mode == 'all':
            for item in coin_Counts:
                coin = item[0]
                count = item[1]
                value = round(count*coin, 2)
                coins_data.append((coin, count, value))
                coins_total += value

        for i, (coin, count, value) in enumerate(coins_data):
            i+=1
            rW_coin_label = ctk.CTkLabel(master=rW_valuesFrame2, text=coin)  
            rW_coin_label.grid(row=i, column=0, padx=5, pady=5)
            rW_coin_count = ctk.CTkLabel(master=rW_valuesFrame2, text=count)  
            rW_coin_count.grid(row=i, column=1, padx=5, pady=5)
            rW_coin_value = ctk.CTkLabel(master=rW_valuesFrame2, text=value)  
            rW_coin_value.grid(row=i, column=2, padx=5, pady=5)

        rW_totalCoinsFrame = ctk.CTkFrame(master=rW_mainFrame, fg_color='gray', corner_radius=0)
        rW_totalCoinsFrame.pack(expand=True, fill='both', padx=0, pady=0)
        
        rW_totalCoinsLabel = ctk.CTkLabel(master=rW_totalCoinsFrame, text='Total Coins Value:')  
        rW_totalCoinsLabel.grid(row=(i+1), columnspan=2, column=0, padx=5, pady=5, sticky='ew')  
        rW_totalCoinsValue = ctk.CTkLabel(master=rW_totalCoinsFrame, text=f'{coins_total} €', anchor='e')  
        rW_totalCoinsValue.grid(row=(i+1), column=2, padx=5, pady=5, sticky='ew')
        
        #style = ttk.Style()
        #style.configure("CustomSeperator.TSeperator", background='black')
        
        #rW_seperator = ttk.Separator(master=rW_mainFrame, orient='horizontal', style="CustomSeperator.TSeperator")
        #rW_seperator.pack(expand=True, fill='x', padx=0, pady=0)
        
        rW_totalAllLabel = ctk.CTkLabel(master=rW_mainFrame, text='Total Value for all Bills and Coins:', anchor='e')  
        rW_totalAllLabel.pack(expand=True, fill='both', padx=5, pady=5)  
        rW_totalAllValue = ctk.CTkLabel(master=rW_mainFrame, text=f'{round(bills_total+coins_total, 2)} €', anchor='e')
        rW_totalAllValue.pack(expand=True, fill='both', padx=5, pady=5)
        
        reportWindow.mainloop()
        return

global generateReport
def generateReport(change=standardChange.get()):
    if change == None:
        change = 0
    totalValue = list()
    widthdrawValues = calcWithdrawal(total=overallResult.get(), change=change)
    for item in bill_Counts:
        totalValue.append(item)
    for item in coin_Counts:
        totalValue.append(item)
    totalValueSave = totalValue
    if widthdrawValues != (None or 0):
        for item in widthdrawValues:
            print('\ngenerateReport() => item: ', item, '\n')
            currency = item[0]
            count = item[1]
            index = totalValue.index(item[0])
            available = totalValue[index]
            available -= count
            totalValue[index] = (currency, available)
    return totalValueSave, widthdrawValues, change

def debug_test():
    print('Debug Test Started!')
    fill_debug_values()
    prepHTMLEmail()
    print('Debug Test Ended!')

# debug_test()

def shutdown(email_stat=False, shutdown_stat=False):
    if (autoReportEmail_onExit.get() == True) or (email_stat == True):
        # sendReportEmail()
        prepHTMLEmail()
    if (autoShutdown_onExit.get() == True) or (shutdown_stat == True):
        os.system('shutdown /s /f /t 0')
        

def submit_entry(event, function):
    entry_text = event.widget.get()
    if entry_text and entry_text.strip():
        if (isinstance(function, tuple) == True):
            functions = function
            for single_function in functions:
                single_function()
        else:
            function()
    else:
        return

settingsFrame = ctk.CTkFrame(master=app)

quitFrame = ctk.CTkButton(master=settingsFrame, text='<--', command=quitSettingsFrame, width=15,
                          fg_color=['#F9F9FA', '#343638'])
quitFrame.place(x=5, y=5)

automaticSwitchingSw = ctk.CTkSwitch(master=settingsFrame, text='Automatic CV Switching', variable=automatic_switching)
automaticSwitchingSw.grid(row=0, column=0, padx=5, pady=(35, 5), sticky='ew')

nonResetSw = ctk.CTkSwitch(master=settingsFrame, text='Non CV Reset', variable=nonReset)
nonResetSw.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

extraWeightSetEntry = ctk.CTkEntry(master=settingsFrame, placeholder_text='Set Extra Weight')
extraWeightSetEntry.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

saveSettingsBut = ctk.CTkButton(master=settingsFrame, text='Save Settings', command=save_settings)
saveSettingsBut.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

saveLog_to_File = ctk.CTkButton(master=settingsFrame, text='Save current Session Log', command=saveCurrentSession)
saveLog_to_File.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

# <header>
header = ctk.CTkFrame(master=app, corner_radius=0)
header.pack(expand=True, fill='x')

header.columnconfigure(0, weight=1)
header.columnconfigure(1, weight=1)
header.columnconfigure(2, weight=1)

h1 = ctk.CTkLabel(master=header, text='Julius', font=('Helvetica', 20))
#h1.pack(side='top', anchor='w')
h1.grid(row=0, column=0, padx=5, pady=5, sticky='w')

dateDisplay = ctk.CTkLabel(master=header, text=(datetime.now().date().strftime("%d-%m-%Y")), 
                           font=('Helvetica', 20))
#dateDisplay.pack(side='top', anchor='center')
dateDisplay.grid(row=0, column=1, padx=5, pady=5)

timeDisplay = ctk.CTkLabel(master=header, text='hh:mm:ss', font=('Helvetica', 20))
#timeDisplay.pack(side='top', anchor='e')
timeDisplay.grid(row=0, column=2, padx=5, pady=5, sticky='e')

if show_powerbar.get() == True:
    powerbarFrame = ctk.CTkFrame(master=header, fg_color='transparent')
    powerbarFrame.grid(row=0, column=3, padx=5, pady=5, sticky='e')
    
    powerbar = ctk.CTkProgressBar(master=powerbarFrame, width=50, height=20, progress_color='green',
                                  corner_radius=0, mode='determinate')
    powerbar.grid(row=0, column=0, padx=0, pady=0)
    
    if show_procentages.get() == True:
        percentagesLabel = ctk.CTkLabel(master=powerbarFrame, text='100%', bg_color='transparent')
        percentagesLabel.grid(row=0, column=0, padx=0, pady=0)
        try:
            percentagesLabel.configure(bg_color='rgba(255, 255, 255, 0.5)')
        except Exception as errorName:
            print(errorName)
        #percentagesLabel.wm_attributes('-transparentcolor', '#ab23ff')
    if show_remainingTime.get() == True:
        remainingTimeLabel = ctk.CTkLabel(master=powerbarFrame, text='remaining_time', bg_color='transparent')
        remainingTimeLabel.grid(row=0, column=1, padx=(5, 0), pady=0)

# </header>

mainFrame = ctk.CTkFrame(master=app)
mainFrame.pack()

leftFrame = ctk.CTkFrame(master=mainFrame, corner_radius=0)
leftFrame.grid(row=0, column=0, sticky='nesw')

coinValueFrame = ctk.CTkFrame(master=leftFrame, bg_color='transparent', fg_color=leftFrame.cget('fg_color'), corner_radius=0)
coinValueFrame.grid(row=0, column=0, columnspan=2)

leftChanger = ctk.CTkButton(master=coinValueFrame, text='<', command=lambda: switchValue(to='High'), width=60,
                            fg_color=changers_color.get(), hover_color='purple')
leftChanger.grid(row=0, column=0, padx=5, pady=5)

menuCoinValue = ctk.CTkComboBox(master=coinValueFrame, values=coinValues, state='readonly')
menuCoinValue.set(value='Coin Value')
menuCoinValue.grid(row=0, column=1, padx=5, pady=5)

rightChanger = ctk.CTkButton(master=coinValueFrame, text='>', command=lambda: switchValue(to='Low'), width=60,
                             fg_color=changers_color.get(), hover_color='purple')
rightChanger.grid(row=0, column=2, padx=5, pady=5)


entryExtraWeight = ctk.CTkEntry(master=leftFrame, placeholder_text='Extra Weight (g)')
entryExtraWeight.grid(row=1, column=1, padx=5, pady=5)

if extraWeight.get() != 0:
    entryExtraWeight.insert(index=0, string=extraWeight.get())

entryWeight = ctk.CTkEntry(master=leftFrame, placeholder_text='Weight (g)')
entryWeight.grid(row=1, column=0, padx=5, pady=5)

def submit_entryWeight(event):
    submit_entry(event=event, function=(getValue,lambda: addOperand(operand=current_value.get(), case=2, count=current_count.get())))
entryWeight.bind('<Return>', submit_entryWeight)

labelValue = ctk.CTkLabel(master=leftFrame, text='0.00 €')
labelValue.grid(row=3, column=0, padx=5, pady=5)

labelAmount = ctk.CTkLabel(master=leftFrame, text='Amount:    0 Coins')
labelAmount.grid(row=3, column=1, padx=5, pady=5)

submitButton = ctk.CTkButton(master=leftFrame, text='Get Value', command=getValue)
submitButton.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

addButton = ctk.CTkButton(master=leftFrame, text='Add Value to Calculation', command=lambda: addOperand(operand=current_value.get(), case=2, count=current_count.get()))
addButton.configure(state='disabled')
addButton.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

additionalValueEntry = ctk.CTkEntry(master=leftFrame, placeholder_text='Additional Value')
additionalValueEntry.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

def submit_additionalValueEntry(event):
    submit_entry(event=event, function=addAdditionalValue)
additionalValueEntry.bind('<Return>', submit_additionalValueEntry)

addAdditionalValueButton = ctk.CTkButton(master=leftFrame, text='Add Additional Value to Calculation', command=addAdditionalValue)
addAdditionalValueButton.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

rightFrame = ctk.CTkFrame(master=mainFrame, corner_radius=0)
rightFrame.grid(row=0, column=1, sticky='nesw')

textboxOperands = ctk.CTkTextbox(master=rightFrame, state='disabled')
textboxOperands.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nesw')

labelResult = ctk.CTkLabel(master=rightFrame, text='= 0.00 €', font=('Arial Bold', 25))
labelResult.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nesw')

buttonReset = ctk.CTkButton(master=rightFrame, text='Reset', command=lambda: frameMverification.place(x=150, y=80),
                            fg_color='darkred', hover_color='grey')
buttonReset.grid(row=2, column=0, padx=5, pady=5)

buttonStepBack = ctk.CTkButton(master=rightFrame, text='Step Back', command=step_Back)
buttonStepBack.grid(row=2, column=1, padx=5, pady=5)

frameMverification = ctk.CTkFrame(master=app, border_width=2, border_color='black')

labelVerification = ctk.CTkLabel(master=frameMverification, text='Are you sure you want to reset?')
labelVerification.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

buttonCancel = ctk.CTkButton(master=frameMverification, text='Cancel', command=lambda: reset_TextboxValue(func='2'))
buttonCancel.grid(row=1, column=0, padx=5, pady=5)

buttonSubmit = ctk.CTkButton(master=frameMverification, text='Submit', command=lambda: reset_TextboxValue(func='1'))
buttonSubmit.grid(row=1, column=1, padx=5, pady=5)

displayCurrentTime()
updatePowerbar()
def focusMode_check_onStart():
    if (focusMode_onStart.get()):
        focusWindow()
app.after(100, focusMode_check_onStart)

app.mainloop()
logger.log(type='Info', orgin='program', operation='exited', status='successfull')
shutdown()
# def save_values(insertValues):
#     with open() as file:
#         fileContent = file.readlines()
#         file.close()
#         for item in insertValues:
#             Pos = (fileContent.find('{item} =')-any)


# savingProcess = threading.Thread(target=save_values)
# savingProcess.start()




"""
Voice-commands:
    - befehle werden in bearbeitungs-warteschleife gesetzt
    - schnitt-takt festlegen
    - bestätigungs ton

Weitere Funktionen:
    - Reset / Löschen
            - Alte Werte sind durchgestrichen (strikethrough)
            - Werden von der Calculation Entfernt
    - Operanten können wie in HTML via kreuz entfernt werden.
            - Ermöglicht es einzelne Werte ohne besonderen Aufwand aus der Berechnung präzise zu entfernen.
    - Speicherung der Werte (Manuell sowie Automatisch)
            - Log Datei
                    - Auflistung von ausgeführten Funktionen und Änderungen von Variablen 
                      und sonstigen Werten (start und end-zeit der gui)
    - Focus Screen wird immer automatisch auf dem hauptbildschirm gestartet und nicht wie es eigentlich besser ist, auf dem bildschirm, wo sich grade die app befindet.
    - Akku Anzeige (Optional)
        Aufbau:
            - Befindet sich in dem Akku Anzeige Frame
            - Als erste Schicht kommt die Progressbar
            - Zweite Schicht ist das Label für die Prozent anzeige (Optional)
        Funktionen:
            - Wie lange hält der Akku bei gleichbleibenden Verbrauch (Uhrzeit: Bis wann, Zeit: Wieviel Stunden)
            - Aktueller Akkustand
    - Niedriger Akku Warnton
    - Teilen Funktion (WhatsApp und/oder Email)
        - Bericht (Kasseninhalt: Berechnet automatisch, was herrausgenommen werden muss, 
          sodass genau das Wechselgeld übrig bleibt. Sodass automatisch mit einmal rechnen der Wechselgeld-Bericht erstellt werden kann.)
"""