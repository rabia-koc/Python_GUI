import tkinter as tk
from tkinter import ttk 

window = tk.Tk() # high level window

## frame: bir arayüz üzerinde widget'leri organize etmemize ve gruplamamıza olanak sağlayan yapılardır.

#frame_left = tk.Frame(window, width = 540, height = 640,bg = "red")   # window üzerine ekledik.
#frame_left.grid(row = 0, column = 0, padx = 10, pady = 10)
#
#frame_right = tk.Frame(window, width = 540, height = 640, bg = "green")  # window üzerine ekledik.
#frame_right.grid(row = 0, column = 1, padx = 10, pady = 10)
#
#frame1 = tk.LabelFrame(frame_left, text =  "frame1", width = 540, height = 500,bg = "yellow")   # frame1'i frame lefte ekledik.
#frame1.grid(row = 0, column = 0, padx = 10, pady = 10)
#
#frame2 = tk.LabelFrame(frame_left, text =  "frame2", width = 540, height = 140, bg = "yellow")
#frame2.grid(row = 1, column = 0, padx = 10, pady = 10)
#
#label1 = tk.Label(frame2, text="label in frame2")
#label1.grid(row=1, column=0, padx = 10, pady = 10)


# paned window: widgetleri, frameleri ve panelleri organize etmek için kullandığımız yapılardır.
pw = ttk.Panedwindow(window, orient = tk.HORIZONTAL)  # ana paned window, yatay olarak 
pw.pack(fill = tk.BOTH, expand = True)

m2 = ttk.Panedwindow(pw, orient = tk. VERTICAL)    # dikey olarak ana paned window üzerinde olucak.

frame2 = ttk.Frame(pw, width = 720, height = 400, relief = tk.RIDGE)  # en son parametre çerçeve kenarlarının nasıl görüneceği için
frame3 = ttk.Frame(pw, width = 720, height = 240, relief = tk.RAISED) 

m2.add(frame2)  # m2'yi frame2'ye ekliyoruz.
m2.add(frame3)

frame1 = ttk.Frame(pw, width = 360, height = 640, relief = tk.GROOVE)
pw.add(m2)  # pw'ye m2 ekledik.
pw.add(frame1)



window.mainloop()