# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 16:51:18 2021

@author: casper
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys

# layout: sayfa düzeni yani bir sayfadaki görsel ögelerin düzenlenmesiyle ilgilenen grafik tasarımının bir parçası yani bir grafik bileşeni demek.
# 2 tane layout var birisi horizontol diğeri vertical
# horizontol: yatay ve vertical: dikey anlamına gelen layout

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(50, 50, 1080, 640)
        self.setWindowTitle("PYQT5 App")
        
 #       self.horizontal()
 #       self.vertical()
        self.verticalAndHorizontal()
 #       self.formlayout()
 #       self.qsplitter()
  #      self.gridLayout()
        self.show()
        
    def horizontal(self):
        
        hbox = QHBoxLayout()   # self yazmıyoruz çünkü en sonda window içine ekleme yapıyoruz.
        
        # widgets
        button1 = QPushButton("yes", self)
        text1 = QLabel("hello", self)
        button2 = QPushButton("no", self)
        text2 = QLabel("world", self)
        button3 = QPushButton("1", self)
        text3 = QLabel("2", self)
        
        # add widgets into hbox
        hbox.addStretch()   # soldan sıkıştırma
        hbox.addWidget(button1)
        hbox.addWidget(text1)
        hbox.addWidget(button2)
        hbox.addWidget(text2)
        hbox.addWidget(button3)
        hbox.addWidget(text3)
        hbox.addStretch()     # en sondan yani sağdan sıkıştırmış oluyoruz, sola yaslamış olduk 
        
        self.setLayout(hbox)
    
    def vertical(self):
        
        vbox = QVBoxLayout()
        
        # widgets
        button1 = QPushButton("yes", self)
        text1 = QLabel("hello", self)
        button2 = QPushButton("no", self)
        text2 = QLabel("world", self)
        button3 = QPushButton("1", self)
        text3 = QLabel("2", self)
        
        # add widgets into hbox
#        vbox.addStretch()     # yukardan sıkıştırma
        vbox.addWidget(button1)
        vbox.addWidget(text1)
        vbox.addWidget(button2)
        vbox.addWidget(text2)
        vbox.addWidget(button3)
        vbox.addWidget(text3)
        vbox.addStretch()    # aşağıdan sıkıştırma
        
        self.setLayout(vbox)
        
        # vertical ve horizontol beraber kullanmak için
    def verticalAndHorizontal(self):
        
        mainlayout = QHBoxLayout()   
        # bir tane horizontol yaptık
        # iiçine 3 tane vertical koyduk
        leftlayout = QVBoxLayout()
        midlayout = QVBoxLayout()
        rightlayout = QVBoxLayout()
        
        # layoutları mainlayouta ekledik.
        mainlayout.addLayout(leftlayout)
        mainlayout.addLayout(midlayout)
        mainlayout.addLayout(rightlayout)
        
        # widgets
        button1 = QPushButton("left")
        button2 = QPushButton("mid")
        button3 = QPushButton("r1")
        button4 = QPushButton("r2")
        
        leftlayout.addWidget(button1)  
        
        midlayout.addWidget(button2)

        rightlayout.addStretch()     # yukarıdan sıkıştırma
        rightlayout.addWidget(button3)
        rightlayout.addWidget(button4)
        rightlayout.addStretch()     # aşağıdan sıkıştıma
        
        self.setLayout(mainlayout)   # windowda belirtilmesi için

# formlayout: label ve layoutları bir araya getirir.
    def formlayout(self):
        
        hbox1= QHBoxLayout()   # horizontol oluşturduk.
        
        hbox1.addWidget(QPushButton("1"))
        hbox1.addWidget(QPushButton("2"))
        hbox1.addStretch()     # sağdan sıkıştırma
        
        formLayout = QFormLayout()   # formlayout oluşturduk.
        formLayout.addRow(QLabel("Push 1 or 2"), hbox1)   # formlayouta label ve horizontol ekledik.
        
        self.setLayout(formLayout)
        
# qsplitter: frameleri ayırmaya yarayan yatay ve dikey çizgilerdir.
# topleft ve topright splitter1 de birleşiyor.
# buttom frame: splitter2'nin alt kısmı yani sağ tarafında, sol tarafında yani yukarıda bunlar birbirine splitter1 ile bağlı
# splitter2 oluşturuken yukardaki splitter1 ve aşağıdaki buttom frame birleştirip oluşturucaz.
# splitter2 üzerinde görünmeyen horizontol layout var üzerinde birleşmiş oluyorlar.
# layoutta window'un bir alt bileşenidir.
    def qsplitter(self):
        
        hbox = QHBoxLayout(self)   # horizontol layout
        
        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)   # frame şeklini dikdörtgen belirledik.
        
        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)
        
        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)
        
        splitter1 = QSplitter(Qt.Horizontal)    # topleft ve topright bir araya getirmek için horizontol yaptık çünkü yatay bir şekilde frameleri diziyor.
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)
        
        splitter2 = QSplitter(Qt.Vertical)      # splitter1 ve bottom'u bir araya getirecek splitter2 oluşturduk. splitter2 yukarıyı ve aşağıyı bir araya getiriyor yani dikey horizontol.
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        
        hbox.addWidget(splitter2)   # splitter2' yi horizontola ekledik
        self.setLayout(hbox)        # horizontolun gözükmesi için
        
# groupbox: widgetleri gruplayan bir kutu
    def createButton(self):
        
        groupBox = QGroupBox("Buttons")
        button1 = QPushButton("1")
        button2 = QPushButton("2")
        button3 = QPushButton("3")
        
        vbox = QVBoxLayout()    #butonları verticalbox'a ekledik, butonlar dikey sıralanacak.
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)
        vbox.addStretch()   # aşağıdan sıkıştırdık yani hepsi yukarda toplansın
        
        groupBox.setLayout(vbox)   # verticalbox'u groupbox içine ekledik
        
        return groupBox   # neden return ettik? çünkü gridlayout metodu içinden birden fazla kullanıcaz.
        
    def gridLayout(self):
        
        grid = QGridLayout()
        
        grid.addWidget(self.createButton(), 0, 0)     # window clasına ait bir metod olduğu için self ile çağırdık.
        # çağırınca bir groupbox return edecek, son 2 parametre yerleşeceği yer.(0.satır, 0.sütun)
        grid.addWidget(self.createButton(), 1, 0)
        
        
        self.setLayout(grid)    # window'a eklemek için
        
        
        
        
app = QApplication(sys.argv)
# window clasına ait bir tane obje oluşturucaz.

window = Window()
window.show()

sys.exit(app.exec())
               
        