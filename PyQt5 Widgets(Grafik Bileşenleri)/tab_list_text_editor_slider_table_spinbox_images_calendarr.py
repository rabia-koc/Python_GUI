# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 15:29:44 2021

@author: casper
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
import numpy as np
from datetime import datetime
import calendar
import sys

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(50, 50, 1080, 640)
        self.setWindowTitle("PYQT5 App")
        
#        self.tabs()
#        self.listW()
#        self.textEditor()
#        self.slider()
#        self.table()
#        self.spinbox()
#        self.image()
        self.calendar()
        self.show()
       
    def tabs(self):
        
        mainLayout = QVBoxLayout()    # vertical layout
        # bunun altına tab oluşturduk
        self.tab = QTabWidget()
        # tabin altına 3 tane tab oluşturduk
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        
        # tab1'in altına vertical, diğerlerine horizontol layout oluşturduk.
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        
        # layoutların altına yerleştirmek için 3 tane buton oluşturduk.
        self.button1 = QPushButton("First tab")
        self.button2 = QPushButton("Second tab")
        self.button3 = QPushButton("Third tab")
        
        vbox.addWidget(self.button1)   # buton1' vertical layouta ekledik
        hbox.addWidget(self.button2)
        hbox2.addWidget(self.button3)
        
        # layoutları tablara sırasıyla ekledik.
        self.tab1.setLayout(vbox)
        self.tab2.setLayout(hbox)
        self.tab3.setLayout(hbox2)
        
        # bulunan tabları Qtabwidgetse ekledik
        self.tab.addTab(self.tab1, "First")   # içine isimlerini de yazdık.
        self.tab.addTab(self.tab2, "Second")
        self.tab.addTab(self.tab3, "Third")
        
        mainLayout.addWidget(self.tab)    # tabı mainlayouta eklemek için. mainlayout başına self eklemiyoruz çünkü window clası içine mainlayot variable tanımlamadık 
        # mainlayoutu sadece tab içinde bir variable olarak tanımladık.
        
        self.setLayout(mainLayout)        # mainlayoutu görselleştirilmesi için
     
    def listW(self):
        
        self.list = QListWidget(self)   # içine self aldı çünkü window da durucak
        
        c = 2019    
        # 2019'dan geriye sayarak 10 sayı yazdırdık.
        for i in range(10):
            self.list.addItem(str(c-i))    # sırasıyla 0-1-2.. diye çıkartıcak.
            # listenin içine bir item eklerken onu string olarak eklemeliyiz.

    def textEditor(self):
        
        self.editor = QTextEdit(self)   # bir variable oluşturduk
        self.editor.move(50, 50)
        
        button = QPushButton("Text Editor",self)   # buton oluşturduk, texteditordeki orada yazan yazıları print etmesi için 
        button.move(50, 25)
        button.clicked.connect(self.textEditorFunction)   # tıklandığında connect yapması için

    def textEditorFunction(self):
        text = self.editor.toPlainText()      # editorda yazan texti al
        print(text)


    def slider(self):
        
        vbox = QVBoxLayout()   # slider içine vertical layout oluşturduk.
        
        self.slider = QSlider(Qt.Horizontal)   # slider: bir tane horizontol olabilir ya da vertical olabilir.
        self.slider.setMinimum(0)           # 0'dan başlasın
        self.slider.setMaximum(100)         # 100' kadar 
        self.slider.setTickInterval(10)     # 10'ar 10'ar gidicek.
        self.slider.setTickPosition(QSlider.TicksBelow)   # çizgileri aşağıda olması için: tickbelow
        
        self.slider.valueChanged.connect(self.sliderFunction)   
        # slider da meydana gelen değişikleri gözlemleyebilmek için 
        # eğer bu slider da bir değişiklik varsa bir valuechange varsa  sliderfunctionla connect yapıcak
        
        vbox.addWidget(self.slider)    # slideri verticale ekledik.
        vbox.addStretch()              # sağ taraftan sıkıştırma
        self.setLayout(vbox)    
        
    def sliderFunction(self):
        print(self.slider.value())            # sliderdeki değerleri al yazdır. 
        
    def table(self):
        
        vbox = QVBoxLayout()     # table kullanacağımız layout oluşturduk,verticalbox kullandık
        
        self.table = QTableWidget()   # table oluşturduk
        self.table.setRowCount(2)     # 2 satır
        self.table.setColumnCount(2)  # 2 sütun
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("method1"))   # 0. indekse sahip olan column ismini oluşturduk
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("method2"))   
        
        # table doldurmak için
        arr = np.array([[1, 2], [3, 4]])    
        # arr'yin shapenin satır sayısı 2 oldu
        for r in range(arr.shape[0]): 
            # sütun sayısı da 2 oldu
            for c in range(arr.shape[1]):
                # table için satır, sütun, item ekledik ve intleri string yaptık
                self.table.setItem(r, c, QTableWidgetItem(str(arr[r, c])))
         
        # table üzerinde değerleri seçmek için buton oluşturduk
        button = QPushButton("Table")
        button.clicked.connect(self.getValue)  # bağlantı sağlamak için fonksiyon kullandık

        vbox.addWidget(self.table)    # table'yi verticalboxa ekledik
        vbox.addWidget(button)        # verticalboxa butonu ekledik.
        self.setLayout(vbox)          # verticalboxun gözükmesi için

    def getValue(self):
        for item in self.table.selectedItems():
            # 1'den fazla seçili item olabilir onun için bu metodu kullandık.
            print("Value: {}, row: {}, column: {}".format(item.text(),item.row(),item.column()))

    def spinbox(self):
        
        self.spinbox = QSpinBox(self)        # spinbox oluşturduk
        self.spinbox.move(50, 50)
        self.spinbox.setRange(30, 40)         # spinbox aralığı
        self.spinbox.setSingleStep(1)        # 1'er adımlarla
        self.spinbox.setSuffix(" $")         # dolar işareti koymak için
            
        button = QPushButton("spin button", self)   # değerleri almak için buton oluşturduk
        button.move(50, 25)
        button.clicked.connect(self.spinFunction)

    def spinFunction(self):
        print(self.spinbox.value())

     # resim eklemek için 
    def image(self):
        
        self.image = QLabel(self)          # window üzerinde bulunacak
        self.image.setPixmap(QPixmap("icon1.png"))   # Qlabel üzerine bir tane resim koyduk
        self.image.move(50, 50) 

    def calendar(self):
        
        self.calendar = QCalendarWidget(self)      
        self.calendar.move(20, 20)
        self.calendar.setGridVisible(True)    # calendar da bulunan değerler günler arasında çizgiler oluşturuyor yani gridler oluşturuyor
        
        self.calendar.clicked.connect(self.printDateInfo)   # calendar üzerinde bulunan günleri nasıl alıcağımız için

    # qDate parametresi ile takvimimden gün ay ve yılı çekmek için
    def printDateInfo(self, qDate):
        print("{}/{}/{}".format(qDate.month(), qDate.day(), qDate.year()))


app = QApplication(sys.argv)
# window clasına ait bir tane obje oluşturucaz.

window = Window()
window.show()

sys.exit(app.exec())
        