import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
# file dialog'dan import edeceğimiz şey olarak resim seçicez.
# bu resmi import edip ayrıca kullanıcı arayüzünde görselleştiricez.

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

window = tk.Tk()
window.geometry("500x800") 


# file dialog
def openFile():
    file_name = filedialog.askopenfilename(initialdir = "D:\Python-GUİ\3.Bölüm-Tkinter Widgets(Grafik Bileşenleri)", title = "select a file...")
    # bu method bize bir string return edecek.
    print(file_name)
    img = Image.open(file_name) # resmi açmak için
    img = ImageTk.PhotoImage(img)  # açılan resmi arayüze eklemek için
    
    label = tk.Label(window, image = img)  # labele img ekledik.
    label.image = img
    label.pack(padx = 15, pady = 15)
    
button = tk.Button(window, text = "open file", command = openFile)
button.pack()

# plot
fig = Figure(figsize = (5, 4), dpi = 50)   # yani 250x200 piksel elde etmiş oluruz.
data = np.arange(0, 3, 0.1) 
fig.add_subplot(111).plot(data, data*2+10)  # x ve y ekseni tanımladık

canvas = FigureCanvasTkAgg(fig, master = window)
canvas.draw()
canvas.get_tk_widget().pack()

# mouse event
def leftClick(event):
    tk.Label(window, text = "left").pack()
    
def middleClick(event):
    tk.Label(window, text = "middle").pack()

def rightClick(event):
    tk.Label(window, text = "right").pack()


window.bind("<Button-1>", leftClick)    # tek sol click
window.bind("<Button-2>", middleClick)  # tek click orta
window.bind("<Button-3>", rightClick)   # tek click sağ




window.mainloop()