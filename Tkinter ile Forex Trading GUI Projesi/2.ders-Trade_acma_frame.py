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

"""
frame1'in içine widgetleri eklicez. 2 tane widget olucak.
1.si: treeview, 2.si: open trading yapan bir button olucak.
button ile simülate ettiğim tradingi gerçekleştirmiş olacağım. Yani tradingi başlatmış olcağım.
Treeview içinde minor ve major olmak üzere 2 tane kavram var.
Major içinde EUR/USD
Minor içinde EUR/ GBR 
"""

item = ""   # item boş bir string tanımladık.
# Şuan için boş daha sonra item'ı callback fonksiyonuyla burda seçtiğim zaman bu item variable başka bir yerde kullanacağım.
def callback(event):
    global item   # global yaptık çünkü daha sonra item variable'nı bu metot dışarısında başka yerlerde kullanmak için.
    item = treeview.identify("item", event.x, event.y)
    print("Clicked: ", item)

# frame1: treeview, open trade button
treeview = ttk.Treeview(frame1)
treeview.grid(row=0, column=1, padx=25, pady=25)
# treeview içinde 4 tane şey eklicez. 1.si major ekliyoruz.
# Major hiçbir şeyin altına gelmeyeck. O nedenle boş olucak.
# kendisi 0. indexte bulunucak. İsmi major olucak. Görünen ismi Major olucak.
treeview.insert("", "0", "Major", text="Major")
# Major altına
treeview.insert("Major", "1", "EUR/USD", text="EUR/USD")

treeview.insert("", "2", "Minor", text="Minor")
treeview.insert("Minor", "3", "EUR/GBR", text="EUR/GBR")

# major ve minor nasıl seçeciğimiz ve seçtikten sonra nasıl aktif hale getiricez?
# mouse'nin sol click tuşuyla ve 2 kez tıklamamız gereksin
treeview.bind("<Double-1>", callback)


# button frame1'in altında olucak ve openTrade fonksiyonunu çağıracak.
def openTrade():
    print("openTrade")

open_button = tk.Button(frame1, text="Open Trading", command=openTrade)
open_button.grid(row=2, column=1, padx=5, pady=5)
window.mainloop()


