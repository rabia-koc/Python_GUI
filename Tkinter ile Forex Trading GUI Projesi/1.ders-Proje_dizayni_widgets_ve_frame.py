"""
forex: global pazar demektir. Dünya çapında bir markettir.
Para ticareti yapılıyor. Foreign Exchange: Yabancı paraların birbirine çevrilmesi.
"""
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

window.mainloop()
