import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

window = tk.Tk()   # ana penceremiz
window.geometry("1080x640")
window.title("Trading")

# ana window'un içinde bulunacak panedwindow için;
# neden horizontol seçtik?
# widget2 ve frame1 yatay bir şekilde sıralandığı için
pw = ttk.Panedwindow(window, orient=tk.HORIZONTAL)
pw.pack(fill=tk.BOTH, expand=True)   #

w2 = ttk.Panedwindow(pw, orient=tk.VERTICAL)
# Widget2'nin içindeki frame2 ve frame3 dikey bir şekilde sıralanmış.

frame1 = ttk.Frame(pw, width = 360, height = 640, relief = tk.SUNKEN)
# relief: frame'in kenarlarının nasıl gözükeceği
frame2 = ttk.Frame(pw, width = 720, height = 400, relief = tk.SUNKEN)
frame3 = ttk.Frame(pw, width = 720, height = 640, relief = tk.SUNKEN)

# frame2 ve frame3'ü window2'ye eklememiz gerekiyor.
w2.add(frame2)
w2.add(frame3)

# frame1 ve window2'yi pw'ye ekliyeceğiz.
pw.add(w2)
pw.add(frame1)


item = ""
def callback(event):
    global item
    item = treeview.identify("item", event.x, event.y)
    #print("Clicked: ", item)

treeview = ttk.Treeview(frame1)
treeview.grid(row=0, column=1, padx=25, pady=25)

treeview.insert("", "0", "Major", text="Major")
treeview.insert("Major", "1", "EUR/USD", text="EUR/USD")
treeview.insert("", "2", "Minor", text="Minor")
treeview.insert("Minor", "3", "EUR/GBR", text="EUR/GBR")

treeview.bind("<Double-1>", callback)

# arayüzde tradingin başlaması için major ya da minorün içinden birisini seçmemiz gerekiyor.
# biz 2 kere tıkladığımızda örneğin EUR/USD'nı item kısmında yazdırıyorduk.
# item global bir variable olduğu için bu item'ı openTrade metodu içerisinde kullanabilirim.
def openTrade():
    print("openTrade")
    # item eşit değildir boş bir stringe yani doluysa
    if item != "":
        print("Chosen item: ", item)

        if item == "EUR/USD":

            # button setting
            # eğer tradingi open yaptıysam openTrade button'nını kapatıp start button'ı aktif etmem gerek.
            open_button.config(state="disabled")
            start_button.config(state="normal")

            # read data
            # neyi open edicem? open etmem gereken şey ne?
            # benim seçtiğim currency pair'ime göre bir data yüklemem gerekiyor.
            data = pd.read_csv("eurusd.csv")

            # split data
            # veri akışını simüle edebilmemiz için
            future = data[-1000:]   # data'mın 1000 tane verisini ayırıyoruz.
            data = data[: len(data)-1000]
            data_close_array = data.close1.values  # kapanış değerlerini yani close1 değerlerini array haline getirdi.
            future_array = list(future.close1.values)  # en sonda bir liste haline getiriyoruz.

            # line
            fig1 = plt.Figure(figsize=(5, 4), dpi=100)
            ax1 = fig1.add_subplot(111)
            line, = ax1.plot(range(len(data)), data.close1, color="blue")  # x eksenim data'mın uzunluğu kadar olucak. y değerim: 2. parametre
            # elimde bir figür var figürün üzerine bir line plot çizdirdim ve bu line plotun da verisi data.close1'den geliyor.
            # bunu bir canvasa eklemem gerekiyor.
            canvas = FigureCanvasTkAgg(fig1, master=tab1)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)   # her yeri doldursun BOTH ile

            # scatter
            fig2 = plt.Figure(figsize=(5, 4), dpi=100)
            ax2 = fig2.add_subplot(111)
            line2 = ax2.scatter(range(len(data)), data.close1, s=1, alpha=0.5, color="blue")    # size=1 aldık
            canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        elif item == "EUR/GBR":
            # button setting
            # eğer tradingi open yaptıysam openTrade button'nını kapatıp start button'ı aktif etmem gerek.
            open_button.config(state="disabled")
            start_button.config(state="normal")

            # read data
            # neyi open edicem? open etmem gereken şey ne?
            # benim seçtiğim currency pair'ime göre bir data yüklemem gerekiyor.
            data = pd.read_csv("eurgbr.csv")

            # split data
            # veri akışını simüle edebilmemiz için
            future = data[-1000:]  # data'mın 1000 tane verisini ayırıyoruz.
            data = data[: len(data) - 1000]
            data_close_array = data.close1.values  # kapanış değerlerini yani close1 değerlerini array haline getirdi.
            future_array = list(future.close1.values)  # en sonda bir liste haline getiriyoruz.

            # line
            fig3 = plt.Figure(figsize=(5, 4), dpi=100)
            ax3 = fig3.add_subplot(111)
            line3, = ax3.plot(range(len(data)), data.close1, color="blue")  # x eksenim data'mın uzunluğu kadar olucak. y değerim: 2. parametre
            # elimde bir figür var figürün üzerine bir line plot çizdirdim ve bu line plotun da verisi data.close1'den geliyor.
            # bunu bir canvasa eklemem gerekiyor.
            canvas3 = FigureCanvasTkAgg(fig3, master=tab1)
            canvas3.draw()
            canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  # her yeri doldursun BOTH ile

            # scatter
            fig4 = plt.Figure(figsize=(5, 4), dpi=100)
            ax4 = fig4.add_subplot(111)
            line4 = ax4.scatter(range(len(data)), data.close1, s=1, alpha=0.5, color="blue")  # size=1 aldık
            canvas4 = FigureCanvasTkAgg(fig4, master=tab2)
            canvas4.draw()
            canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        else:
            messagebox.showinfo(title="Warning", message="Double click to chose currency pair")

    else:
        messagebox.showinfo(title="Warning", message="Double click to chose currency pair")

open_button  = tk.Button(frame1, text="Open Trading", command=openTrade)
open_button.grid(row=2, column=1, padx=5, pady=5)

# frame3: text editor(fundamental analysis), scroll bar
textBox = tk.Text(frame3, width=70, height=10, wrap="word")
textBox.grid(row=0, column=0, padx=25, pady=25)

scroll = tk.Scrollbar(frame3, orient=tk.VERTICAL, command=textBox.yview())
scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10)
textBox.config(yscrollcommand=scroll.set)

# frame2: tab view, radio button, result(labelframe), plot
tabs = ttk.Notebook(frame2, width=540, height=300)
tabs.place(x=25, y=25)

tab1 = ttk.Frame(tabs, width=50, height=50)
tab2 = ttk.Frame(tabs)

tabs.add(tab1, text="line")
tabs.add(tab2, text="Scatter", compound=tk.LEFT)

# radio button
method = tk.StringVar()
tk.Radiobutton(frame2, text="m1: ", value="m1", variable=method).place(x=580, y=100)
tk.Radiobutton(frame2, text="m2: ", value="m2", variable=method).place(x=580, y=125)

# label frame: result
label_frame = tk.LabelFrame(frame2, text="Result", width=100, height=150)
label_frame.place(x=580, y=25)

tk.Label(label_frame, text="Buy: ", bd=3).grid(row=0, column=0)
tk.Label(label_frame, text="Sell: ", bd=3).grid(row=1, column=0)

# button
def startTrading():
    print("startTrading")

start_button = tk.Button(frame2, text="Start Trading", command=startTrading)
start_button.place(x=580, y=150)
# ilerleyen zamanlarda open trading butonuna bastığımız zaman start button'ı tekrar aktif hale getiricez.
start_button.config(state="disabled")

window.mainloop()


