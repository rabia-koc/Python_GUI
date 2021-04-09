import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("Geometry Manager")


## pack kullanımı
#red = tk.Button(window, text = "Red",fg= "red")
#red.pack(side = tk.LEFT)  # sola yasladık.
#
#green = tk.Button(window, text = "green",fg= "green")
#green.pack(side = tk.LEFT)   
#
#blue = tk.Button(window, text = "blue",fg= "blue")
#blue.pack(side = tk.LEFT)
#
#black = tk.Button(window, text = "black",fg= "black")
#black.pack(side = tk.BOTTOM)   # window üzerinde ortalanır.
#
#brown = tk.Button(window, text = "brown",fg= "brown")
#brown.pack(side = tk.BOTTOM)
#
#cyan = tk.Button(window, text = "cyan",fg= "cyan")
#cyan.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
# TOP: en üste, BOTH: yatay eksende tamamen doldur, expand ile buton genişlemiş oluyor.

## grid manager kullanımı
# 5 tane row
#for r in range(5):
    # 5 tane column
#    for c in range(5):
#        label = tk.Label(window, text = 'R%s/C%s'%(r, c), borderwidth = 2)  # row ve column indekslerimi yazacak orada 
#        label.grid(row = r, column = c, padx = 3, pady = 3)  # birbirine geçmemesi için padx ve pady ekledik.


# place kullanımı
label1 = tk.Label(window, text = "place1")
label1.place(x = 15, y = 15)  # x ve y ekseninde pikseller belirledik.

label2 = tk.Label(window, text = "place2")
label2.place(x = 30, y = 30)

label3 = tk.Label(window, text = "place3")
label3.place(x = 45, y = 45)

label4 = tk.Label(window, text = "place4")
label4.place(relx = 0, rely = 0)  # oranlamış olduk, sol üst köşeye denk geldi.





window.mainloop()












