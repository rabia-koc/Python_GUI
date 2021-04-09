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


window.mainloop()


