# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 18:11:53 2021

@author: casper
"""

import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox

window = tk.Tk()   # pencere oluşturduk.
window.geometry("500x450")  # pencerenin boyutu
window.title("Welcome to first app")

# buton ekliyoruz.
def buttonFunction():
    print("Push button")   # butona basınca konsolda bu yazı yazacak.
    
    # butona basınca labeli değiştirmek için 
    label.config(text = "hello world",
                 fg = "black",
                 bg = "red",
                 font = "Times 25")
    # entry 
    value = entry.get()  # entry içinde yazan değerleri çekiyoruz.
    print(value)
    # yazdığım yazının butona basınca hello world kısmında yazdığımız yazının olması için
    label.configure(text = value)
    entry.configure(state = "disabled") # en sonda entry'in input almasını kapatıyoruz.

# butona basınca ekrana msj çıkması için farklı msj fonksiyonları;
    
#    message_box = messagebox.showinfo(title = "info", message = "information")
#    message_box = messagebox.askretrycancel(title = "info", message = "information")
#    message_box = messagebox.askquestion(title = "info", message = "information")
#    message_box = messagebox.askyesnocancel(title = "info", message = "information")
    message_box = messagebox.showerror(title = "info", message = "information")
    print(message_box)
    
# buttonu window'un üzerine koyacağımız için ilk parametre window
# 2.parametre: buton ismi
# 3.parametrede butona basıldığı zaman rengi kırmızı olacak
# 4.parametre: arka plan rengi
# 5.parametre: yazı rengi
# 6.parametre:butona basmadığımız zaman rengi black
# 7. parametre ve 8.parametre: eni ve boyu
# 9.parametre: butona basıldığında command ile fonksiyona götürecek.
button = tk.Button(window, text = "First button", activebackground = "red",
                   bg = "black", fg = "white", activeforeground = "black",
                   height = 15, width = 50,
                   command = buttonFunction)

button.pack()   # butonu window'a ekledik.

# label oluşturuyoruz. 
# sonucu parametre text uzunluğu 150 pikselden oluşacak.
label = tk.Label(window, text = "Hi World", font = "Times 16", 
                 fg = "white", bg = "black", wraplength = 150)

# 1.parametre: ne tarafta olacağı
# 2.parametre: 25 piksel uzunluğunda sağ taraftan boşluk bıraktı.
label.pack(side = tk.RIGHT, padx = 25)  # window'a yerleştirme 

# entry, size: 50
entry = tk.Entry(window, width = 50)
# bir kere entry'e giriş yapabileceğiz. ilk parametre: place holder ekledik
# 2.parametrede verilen indekse göre entry içerisine bir string entegre etmiş oluyoruz.
entry.insert(string = "write something only one time",index = 0)
entry.pack(side = tk.LEFT, padx = 25)   # entry'i sol tarafa aldık.



# window'un görülebilmesi için 
window.mainloop()