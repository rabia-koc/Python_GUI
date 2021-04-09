import tkinter as tk
from tkinter import ttk  

window = tk.Tk()
window.geometry("800x600")


# menu 
def fileFunction():
    print("here")

menubar = tk.Menu(window)  # menubar oluşturduk.
window.config(menu = menubar)  # menubarı window menusune ekledik.

file = tk.Menu(menubar)  # file menüsü
edit = tk.Menu(menubar)  # edit menüsü

menubar.add_cascade(label = "file", menu = file)  # menubar üzerine ekledik
menubar.add_cascade(label = "edit", menu = edit)

# file ve editin içini doldurduk.
file.add_command(label = "new file", command =fileFunction )
edit.add_command(label = "undo", command =fileFunction )


# tabs
tabs = ttk.Notebook(window, width = 540, height = 300)  # window üzerinde bir tab oluşturduk.
tabs.place(x = 25, y = 25)

# tabs'a tabları ekledik.
tab1 = ttk.Frame(tabs, width = 50, height = 50)
tab2 = ttk.Frame(tabs, width = 50, height = 50)
tab3 = ttk.Frame(tabs, width = 50, height = 50)

tk.Label(tab1, text = "tab1").pack()
tk.Label(tab2, text = "tab2").pack()
tk.Label(tab3, text = "tab3").grid()

# ana taba tabları ekledik.
tabs.add(tab1, text = "treeview")
tabs.add(tab2, text = "list box")
tabs.add(tab3, text = "text editor")

# tree view
treeview = ttk.Treeview(tab1)
treeview.place(x = 5, y = 5)

treeview.insert("", "0", "item1", text = "Spain")
treeview.insert("item1", "1", "item2", text = "Madrid")  # spain altına eklemek için item 1 dedik.
treeview.insert("", "2", "item3", text = "France")  # hiçbir şeyin altında olmadığı için ilk parametre boş
treeview.insert("item3", "3", "item4", text = "Paris")  # France altına ekledik.

# window da herhangi bir hareket yağtığım zaman event farkına varicak bu hareketi return edecek.
def callback(event):
    item = treeview.identify("item", event.x, event.y)
    # treeview üzerine geldiğim zaman bir item seçtiğim zaman x ve y'ye göre bu item'ın hangisi olduğunu 
    # item variable üzerine yazdırabiliyoruz.
    print(item)

# treeview üzerinde mouse ile bir çift tıklama gerçekleştiğinde callback fonksiyonunu çağır.
treeview.bind("<Double-1>",callback)

# listbox: farklı farklı item'leri depolamak için kullandığımız listelerdir.
listBox = tk.Listbox(tab2, selectmode = tk.MULTIPLE)  # tab2 de bulunacak. 2.parametre ile birden fazla dosya seçebiliyorum.
listBox.insert(0,"Spain")
listBox.insert(1,"France")
listBox.insert(2,"China")

listBox.place(x = 5, y = 5)

def getItem():
    index_list = listBox.curselection()   # önce listboxa erişiyoruz, curselection ile item'ın indeksini alıyoruz.
    print(index_list)
    for each in index_list:
        # birden fazla seçersek sırayla print etmesi için
        print(listBox.get(each))

# listbox içindeki item'lere erişmek için buton oluşturduk.
button = tk.Button(tab2, text = "button", command = getItem)
button.place(x = 150, y = 5)

# text editor
textEditor = tk.Text(tab3, width = 25, height = 25, wrap = tk.WORD)  # son parametre: kelimelerle işlem yapacağımız anlamına geliyor.
textEditor.grid(row = 0, column = 0, padx = 10, pady = 10)

def textFunction():
    print(textEditor.get(1.0, tk.END))   # yazdığım her şeyi kayıt etmesi için böyle yazdık.

# yazdığımız texti kaydetmek için buton oluşturduk.
button = tk.Button(tab3, text = "save", command = textFunction)
button.grid(row = 0, column = 2, padx = 10, pady = 10)


# scroll
scroll = tk.Scrollbar(tab3, orient = tk.VERTICAL, command = textEditor.yview)
# 2.parametre: dikey olması için,
# 3.parametre: textEditorunun y ekseninde olacak.
scroll.grid(row = 0, column = 1, sticky = tk.N + tk.S)  # kuzeye ve güneye bağladık.
textEditor.config(yscrollcomman = scroll.set)   # set ile oluşturduğum scrollbar textEditore set edilmiş oluyor. 


window.mainloop()













