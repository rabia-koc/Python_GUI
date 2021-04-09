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
    print("Clicked: ", item)

treeview = ttk.Treeview(frame1)
treeview.grid(row=0, column=1, padx=25, pady=25)

treeview.insert("", "0", "Major", text="Major")
treeview.insert("Major", "1", "EUR/USD", text="EUR/USD")
treeview.insert("", "2", "Minor", text="Minor")
treeview.insert("Minor", "3", "EUR/GBR", text="EUR/GBR")

treeview.bind("<Double-1>", callback)

def openTrade():
    print("openTrade")

open_button = tk.Button(frame1, text="Open Trading", command=openTrade)
open_button.grid(row=2, column=1, padx=5, pady=5)

# frame3: text editor(fundamental analysis), scroll bar
textBox = tk.Text(frame3, width=70, height=10, wrap="word")  # içine kelimeleri aldı.
textBox.grid(row=0, column=0, padx=25, pady=25)

# dikey olucak, fonskiyon olarak textbox'ın yview'ını kullanıcaz.
scroll = tk.Scrollbar(frame3, orient=tk.VERTICAL, command=textBox.yview())
scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10)  # bunu bir yere yapıştırmamız gerekiyor.(sticky)
textBox.config(yscrollcommand=scroll.set)  # yani textbox'ım ile scrollbar'ımı kullanmak istiyorum demek istiyor.

# frame2: tab view, radio button, result(labelframe), plot
tabs = ttk.Notebook(frame2, width=540, height=300)
tabs.place(x=25, y=25)

tab1 = ttk.Frame(tabs, width=50, height=50)
tab2 = ttk.Frame(tabs)

tabs.add(tab1, text="line")
tabs.add(tab2, text="Scatter", compound=tk.LEFT)    # compound parametresi bize bunu sola yaslamamızı sağlıyor.

# radio button
method = tk.StringVar()  # radio button da bulunan değerleri okuyabilmek için variable oluşturuyoruz.
tk.Radiobutton(frame2, text="m1: ", value="m1", variable=method).place(x=580, y=100)  # bunlara bastığımız zaman elde edeceğimiz variable'rı method'a kaydedicez.
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


