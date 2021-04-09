import tkinter as tk
from tkinter import ttk 

window = tk.Tk()            # top level window
window.geometry("500x450")  # window size x*y

# buton fonksiyonu
def buttonFunction():
    print("here")
    
    # radio buttona bastıktan sonra butona basınca elde ettiğim değerleri elde edebilmem için
    m = method.get()  # variable yi method ile alıcaz.
    # 1 ve 2 deme sebebi: radiobutton da value'lere o değerleri verdik.
    if m =="1":
        print("method1")
    elif m =="2":
        print("method2")
    else:
        print("method1 & method2")
    
    # combobox
    print(problem.get())
    
    # checkButtona bastıktan sonra butona basınca 
    value = save_var.get() 
    if value == 1:
        print("Save__")
    else:
        print("not save")
        
button = tk.Button(window, text = "button", activebackground = "red", bg = "black",
                    fg = "white", activeforeground = "black",
                    height = 15, width = 50, command = buttonFunction)

button.grid(row = 0, column = 0, pady = 15)  # window'a ekledik.

# radio button
method = tk.StringVar()  # radio butona basınca elde edeceğim value tanımlayabilmek için
# value: method1'in 1'i
# variable: buraya bastığım zaman string olarak variable return edecek anlamına geliyor.
tk.Radiobutton(window, text = "method1: ", value = "1", activebackground = "red",
               bg = "green",height = 5, width = 5,borderwidth = 15, variable = method).grid(row=1,column=0)

tk.Radiobutton(window, text = "method2: ", value = "2", variable = method).grid(row=1,column=1, pady=15)

# comboBox
problem = tk.StringVar()  # variable tanımladık.
# problem 1, problem 2, problem 3'lerden seçim yapıcaz.
comboBox = ttk.Combobox(window, textvariable = problem, values = ("1", "2", "3"), state= "readonly")
 
comboBox.grid(row=2, column=0, pady=15)

def checkButtonFunction():
    print("save")

# checkButton
# seçtiğimiz variable'leri kaydetmek için gerekli olan variable oluşturduk.
save_var = tk.IntVar()
save_var.set(0)  # indeks 0'a set ettik.
# checkbutton da bir şey seçtiğim zaman save_var isimli variableye kayıt olucak.
c_button = tk.Checkbutton(window, text = "Save", variable = save_var, font = "Times 25", 
                          activebackground = "green", activeforeground = "white",
                          bg = "yellow", command = checkButtonFunction)

c_button.grid(row=2, column=1, pady=15)



window.mainloop()