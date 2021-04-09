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
    #print("Clicked: ", item)

treeview = ttk.Treeview(frame1)
treeview.grid(row=0, column=1, padx=25, pady=25)

treeview.insert("", "0", "Major", text="Major")
treeview.insert("Major", "1", "EUR/USD", text="EUR/USD")
treeview.insert("", "2", "Minor", text="Minor")
treeview.insert("Minor", "3", "EUR/GBR", text="EUR/GBR")

treeview.bind("<Double-1>", callback)

def readNews(item):
    if item == "EUR/USD":
        news = pd.read_csv("news_EURUSD.txt")
    elif item == "EUR/GBR":
        news = pd.read_csv("news_EURGBR.txt")
    textBox.insert(tk.INSERT, news)  # textbox'ta görselleştirmek için.

# arayüzde tradingin başlaması için major ya da minorün içinden birisini seçmemiz gerekiyor.
# biz 2 kere tıkladığımızda örneğin EUR/USD'nı item kısmında yazdırıyorduk.
# item global bir variable olduğu için bu item'ı openTrade metodu içerisinde kullanabilirim.
def openTrade():
    global data, future, line, canvas, data_close_array, future_array, ax1, line2, canvas2, ax2, line3, canvas3, ax3, line4, canvas4, ax4
    print("openTrade")
    # item eşit değildir boş bir stringe yani doluysa
    if item != "":
        print("Chosen item: ", item)

        if item == "EUR/USD":

            # button setting
            # eğer tradingi open yaptıysam openTrade button'nını kapatıp start button'ı aktif etmem gerek.
            open_button.config(state="disabled")
            start_button.config(state="normal")

            # read data
            # neyi open edicem? open etmem gereken şey ne?
            # benim seçtiğim currency pair'ime göre bir data yüklemem gerekiyor.
            data = pd.read_csv("eurusd.csv")

            # split data
            # veri akışını simüle edebilmemiz için
            future = data[-1000:]   # data'mın 1000 tane verisini ayırıyoruz.
            data = data[: len(data)-1000]
            data_close_array = data.close1.values  # kapanış değerlerini yani close1 değerlerini array haline getirdi.
            future_array = list(future.close1.values)  # en sonda bir liste haline getiriyoruz.

            # line
            fig1 = plt.Figure(figsize=(5, 4), dpi=100)
            ax1 = fig1.add_subplot(111)
            line, = ax1.plot(range(len(data)), data.close1, color="blue")  # x eksenim data'mın uzunluğu kadar olucak. y değerim: 2. parametre
            # elimde bir figür var figürün üzerine bir line plot çizdirdim ve bu line plotun da verisi data.close1'den geliyor.
            # bunu bir canvasa eklemem gerekiyor.
            canvas = FigureCanvasTkAgg(fig1, master=tab1)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)   # her yeri doldursun BOTH ile

            # scatter
            fig2 = plt.Figure(figsize=(5, 4), dpi=100)
            ax2 = fig2.add_subplot(111)
            line2 = ax2.scatter(range(len(data)), data.close1, s=1, alpha=0.5, color="blue")    # size=1 aldık
            canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # read news
            readNews(item)

        elif item == "EUR/GBR":
            # button setting
            # eğer tradingi open yaptıysam openTrade button'nını kapatıp start button'ı aktif etmem gerek.
            open_button.config(state="disabled")
            start_button.config(state="normal")

            # read data
            # neyi open edicem? open etmem gereken şey ne?
            # benim seçtiğim currency pair'ime göre bir data yüklemem gerekiyor.
            data = pd.read_csv("eurgbr.csv")

            # split data
            # veri akışını simüle edebilmemiz için
            future = data[-1000:]  # data'mın 1000 tane verisini ayırıyoruz.
            data = data[: len(data) - 1000]
            data_close_array = data.close1.values  # kapanış değerlerini yani close1 değerlerini array haline getirdi.
            future_array = list(future.close1.values)  # en sonda bir liste haline getiriyoruz.

            # line
            fig3 = plt.Figure(figsize=(5, 4), dpi=100)
            ax3 = fig3.add_subplot(111)
            line3, = ax3.plot(range(len(data)), data.close1, color="blue")  # x eksenim data'mın uzunluğu kadar olucak. y değerim: 2. parametre
            # elimde bir figür var figürün üzerine bir line plot çizdirdim ve bu line plotun da verisi data.close1'den geliyor.
            # bunu bir canvasa eklemem gerekiyor.
            canvas3 = FigureCanvasTkAgg(fig3, master=tab1)
            canvas3.draw()
            canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  # her yeri doldursun BOTH ile

            # scatter
            fig4 = plt.Figure(figsize=(5, 4), dpi=100)
            ax4 = fig4.add_subplot(111)
            line4 = ax4.scatter(range(len(data)), data.close1, s=1, alpha=0.5, color="blue")  # size=1 aldık
            canvas4 = FigureCanvasTkAgg(fig4, master=tab2)
            canvas4.draw()
            canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # read news
            readNews(item)

        else:
            messagebox.showinfo(title="Warning", message="Double click to chose currency pair")

    else:
        messagebox.showinfo(title="Warning", message="Double click to chose currency pair")

open_button  = tk.Button(frame1, text="Open Trading", command=openTrade)
open_button.grid(row=2, column=1, padx=5, pady=5)

# frame3: text editor(fundamental analysis), scroll bar
textBox = tk.Text(frame3, width=70, height=10, wrap="word")
textBox.grid(row=0, column=0, padx=25, pady=25)

scroll = tk.Scrollbar(frame3, orient=tk.VERTICAL, command=textBox.yview())
scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10)
textBox.config(yscrollcommand=scroll.set)

# frame2: tab view, radio button, result(labelframe), plot
tabs = ttk.Notebook(frame2, width=540, height=300)
tabs.place(x=25, y=25)

tab1 = ttk.Frame(tabs, width=50, height=50)
tab2 = ttk.Frame(tabs)

tabs.add(tab1, text="line")
tabs.add(tab2, text="Scatter", compound=tk.LEFT)

# radio button
method = tk.StringVar()
tk.Radiobutton(frame2, text="m1: ", value="m1", variable=method).place(x=580, y=100)
tk.Radiobutton(frame2, text="m2: ", value="m2", variable=method).place(x=580, y=125)

# label frame: result
label_frame = tk.LabelFrame(frame2, text="Result", width=100, height=150)
label_frame.place(x=580, y=25)

tk.Label(label_frame, text="Buy: ", bd=3).grid(row=0, column=0)
tk.Label(label_frame, text="Sell: ", bd=3).grid(row=1, column=0)

# buy sell labels
buy_value = tk.Label(label_frame, text="1", bd=3)
buy_value.grid(row=0, column=1)
sell_value = tk.Label(label_frame, text="0", bd=3)
sell_value.grid(row=1, column=1)
# buy ve sell değerleri bizim plotumuz update edildikçe güncellenecek değerlerdir.

def moving_average(a, n=50):
    ret = np.cumsum(a, dtype=float)   # a daki tüm değerleri topladık.
    ret[n:] = ret[n:] - ret[:-n]
    # elde ettiğim array'in 50. indexten sonraki değerlerinden, n. indexe kadar olan değerlerini çıkartıyorum.
    # n. indexten sonraki değerlerine eşitliyorum
    return ret[n-1:]/n  # n-1. indexten sonuna kadar git bunu n'e böl yani average kısmını yapmış olduk.

def update():
    global data_close_array, ax1, ax2, ax3, ax4
    # değeri kafadan attık, buy value ve sell value farklı olması adına atadğımız bir değer.
    spread = 0.0002
    # data_close_array'inin sadece sonuncu elemanını alıyor
    # yuvarladık virgülden sonra beş basamak göster demek.
    buy_value.config(text=str((data_close_array[-1]-spread).round(5)))
    sell_value.config(text=str((data_close_array[-1]+spread).round(5)))

    window.after(500, update)

    # future_array'ın ilk elemanını alıp data_close_array'ın en sonuna ekliyoruz.
    # böylece her 500ms de bir data_close_array güncellenmiş oluyor. Yeni bir eleman eklenmiş oluyor.
    # data_close_array'ın en sonuncu elemanını label de görselleştirdiğim zaman start trading butonuna basınca buy ve sell değerleri güncelleniyor.
    data_close_array = np.append(data_close_array, future_array.pop(0))

    # method 1 i seçersem.
    if method.get() == "m1":
        if item == "EUR/USD":
            # line
            # EUR/USD pair'ım ax1 ve ax2 de mevcut. Bu nedenle ax1'i ve ax2'yi güncellemem gerekiyor.
            # veri ekleyeceğim için önce xlim'i genişletmem gerekiyor. Eğer genişletmezsem eklediğim veriyi göremem
            # data_close_array'inin uzunluğu kadar artı 10 birim genişlikte genişlettik.
            ax1.set_xlim(0, len(data_close_array) + 10)
            line.set_ydata(data_close_array)  # bunu da güncelledik.
            line.set_xdata(range(len(data_close_array)))

            # scatter
            ax2.set_xlim(0, len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s=1, alpha=0.5, color="blue")

            # moving average
            n = 50  # orta seviye bir windowing
            mid_rolling = moving_average(data_close_array, n)  # n sayısını kendisine input parametresi olarak alıcak.
            ax1.plot(range(n-1, len(data_close_array)), mid_rolling, linestyle="--", color="red")
            ax2.plot(range(n-1, len(data_close_array)), mid_rolling, linestyle="--", color="red")

            canvas.draw()
            canvas2.draw()

        elif item == "EUR/GBR":
            # line
            # EUR/USD pair'ım ax1 ve ax2 de mevcut. Bu nedenle ax1'i ve ax2'yi güncellemem gerekiyor.
            # veri ekleyeceğim için önce xlim'i genişletmem gerekiyor. Eğer genişletmezsem eklediğim veriyi göremem
            # data_close_array'inin uzunluğu kadar artı 10 birim genişilikte genişlettik.
            ax3.set_xlim(0, len(data_close_array) + 10)
            line3.set_ydata(data_close_array)  # bunu da güncelledik.
            line3.set_xdata(range(len(data_close_array)))

            # scatter
            ax4.set_xlim(0, len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s=1, alpha=0.5, color="blue")

            # moving average
            n = 50  # orta seviye bir windowing
            mid_rolling = moving_average(data_close_array, n)  # n sayısını kendisine input parametresi olarak alıcak.
            ax3.plot(range(n-1, len(data_close_array)), mid_rolling, linestyle="--", color="red")
            ax4.plot(range(n-1, len(data_close_array)), mid_rolling, linestyle="--", color="red")

            canvas3.draw()
            canvas4.draw()

    elif method.get() == "m2":
        if item == "EUR/USD":
            # line
            # EUR/USD pair'ım ax1 ve ax2 de mevcut. Bu nedenle ax1'i ve ax2'yi güncellemem gerekiyor.
            # veri ekleyeceğim için önce xlim'i genişletmem gerekiyor. Eğer genişletmezsem eklediğim veriyi göremem
            # data_close_array'inin uzunluğu kadar artı 10 birim genişilikte genişlettik.
            ax1.set_xlim(0, len(data_close_array) + 10)
            line.set_ydata(data_close_array)  # bunu da güncelledik.
            line.set_xdata(range(len(data_close_array)))

            # scatter
            ax2.set_xlim(0, len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s=1, alpha=0.5, color="blue")

            # moving average
            n = 200  # orta seviye bir windowing
            long_rolling = moving_average(data_close_array, n)  # n sayısını kendisine input parametresi olarak alıcak.
            ax1.plot(range(n-1, len(data_close_array)), long_rolling, linestyle="--", color="red")
            ax2.plot(range(n - 1, len(data_close_array)), long_rolling, linestyle="--", color="red")

            canvas.draw()
            canvas2.draw()

        elif item == "EUR/GBR":
            # line
            # EUR/USD pair'ım ax1 ve ax2 de mevcut. Bu nedenle ax1'i ve ax2'yi güncellemem gerekiyor.
            # veri ekleyeceğim için önce xlim'i genişletmem gerekiyor. Eğer genişletmezsem eklediğim veriyi göremem
            # data_close_array'inin uzunluğu kadar artı 10 birim genişilikte genişlettik.
            ax3.set_xlim(0, len(data_close_array) + 10)
            line3.set_ydata(data_close_array)  # bunu da güncelledik.
            line3.set_xdata(range(len(data_close_array)))

            # scatter
            ax4.set_xlim(0, len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s=1, alpha=0.5, color="blue")

            # moving average
            n = 200  # orta seviye bir windowing
            long_rolling = moving_average(data_close_array, n)  # n sayısını kendisine input parametresi olarak alıcak.
            ax3.plot(range(n-1, len(data_close_array)), long_rolling, linestyle="--", color="green")
            ax4.plot(range(n - 1, len(data_close_array)), long_rolling, linestyle="--", color="green")

            canvas3.draw()
            canvas4.draw()
    else:
        if item == "EUR/USD":
            # line
            # EUR/USD pair'ım ax1 ve ax2 de mevcut. Bu nedenle ax1'i ve ax2'yi güncellemem gerekiyor.
            # veri ekleyeceğim için önce xlim'i genişletmem gerekiyor. Eğer genişletmezsem eklediğim veriyi göremem
            # data_close_array'inin uzunluğu kadar artı 10 birim genişilikte genişlettik.
            ax1.set_xlim(0, len(data_close_array) + 10)
            line.set_ydata(data_close_array)  # bunu da güncelledik.
            line.set_xdata(range(len(data_close_array)))

            # scatter
            ax2.set_xlim(0, len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s=1, alpha=0.5, color="blue")

            canvas.draw()
            canvas2.draw()

        elif item == "EUR/GBR":
            # line
            # EUR/USD pair'ım ax1 ve ax2 de mevcut. Bu nedenle ax1'i ve ax2'yi güncellemem gerekiyor.
            # veri ekleyeceğim için önce xlim'i genişletmem gerekiyor. Eğer genişletmezsem eklediğim veriyi göremem
            # data_close_array'inin uzunluğu kadar artı 10 birim genişilikte genişlettik.
            ax3.set_xlim(0, len(data_close_array) + 10)
            line3.set_ydata(data_close_array)  # bunu da güncelledik.
            line3.set_xdata(range(len(data_close_array)))

            # scatter
            ax4.set_xlim(0, len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s=1, alpha=0.5, color="blue")

            canvas3.draw()
            canvas4.draw()

# button
def startTrading():
    # windowu güncellemek için gerekli olan fonksiyonu çağırıyoruz.
    window.after(0, update)   # 0 demek direk başlar başlamaz. yani start butonuna basılır basılmaz update metoduna git demek.
    print("startTrading")

start_button = tk.Button(frame2, text="Start Trading", command=startTrading)
start_button.place(x=580, y=150)

start_button.config(state="disabled")

window.mainloop()

# start tradinge basınca line ve scatterde belirli bir veri akışı olmasını sağlıcaz.
# m1, m2 metotlarına görede plotumuzu güncellicez.
