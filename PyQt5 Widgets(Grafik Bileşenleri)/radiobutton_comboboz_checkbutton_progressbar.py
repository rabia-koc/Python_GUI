# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 16:25:11 2021

@author: casper
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import sys

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(50, 50, 1080, 640)
        self.setWindowTitle("PYQT5 App")
        
        self.radioButton()
        self.comboBox()
        self.checkBox()
        self.progressBar()
        self.show()
        
    def radioButton(self):
        
        self.method1 = QRadioButton("method1", self)
        self.method2 = QRadioButton("method2", self)
        self.method3 = QRadioButton("method3", self)
        
        self.method1.move(50, 40)
        self.method2.move(50, 60)
        self.method3.move(50, 80)
        
        self.method1.setChecked(True)   # default olarak seçili yaptık
        
        button = QPushButton("Radio Button", self)
        button.move(50, 100)
        button.clicked.connect(self.radioButtonFunction)  # butona tıklandığı zaman fonksiyonu çağırması için

    def radioButtonFunction(self):
         # isChecked metodu ile kontrol ediyoruz.
        if self.method1.isChecked():
            print("method1")
        elif self.method2.isChecked():
            print("method2")
        elif self.method3.isChecked():
            print("method3")
        else:
            print("choose")

    def comboBox(self):
        
        self.combo = QComboBox(self)
        self.combo.move(150, 40)  
        self.combo.addItem("method1")   # combo'ya metodları ekledik. buraya int ya da floatta ekleyebiliriz ama string yaparak.
        self.combo.addItem("method2")
        self.combo.addItems(["method3","method4"])   # tek tek eklemek yerine toplu bir şekilde ekledik.
        
        button = QPushButton("Combo Box", self)
        button.move(150, 70)
        button.clicked.connect(self.comboFunction)   # combobox seçimi yaptıktan sonra buton ile basmak için
        
    def comboFunction(self):
        print(self.combo.currentText())   
        # combobox'ta seçilen metotlardan birini yani şuanki seçili olanı yazar.
    

    def checkBox(self):
        self.save = QCheckBox("Save", self)   # kaydetmek için
        self.save.move(250, 40)
        
        button = QPushButton("Save", self)
        button.move(250, 70)
        button.clicked.connect(self.checkFunction)
      
    # save butonuna basınca seçili ise kayıt değilse no kayıt.
    def checkFunction(self):
        if self.save.isChecked():
            print("save")
        else:
            print("not save")
    
    def progressBar(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(400, 40, 200, 25)   # ilk 2 parametre x ve y, son 2 parametre eni ve boyu
        self.pbar.setValue(0)    # yani 0'dan başlasın demek
    
        self.timer = QTimer()    # belirli bir periyotta sayaç yapmak için 
        self.timer.timeout.connect(self.handleTimer)   # bir saniyede bir yani orda belirlediğim periyot doldukça connect gerçekleştir.
        self.timer.start(500)   # periyodu belirledik. yani timer ne kadar sürede başlıcak  
        # 0.5 ms de bir başa dönecek, timeout yapıcak, timeout yaptıkça da handleTimer fonksiyonu ile bu metodu çağırıcak.
    
    # pbar'ın dolabilmesi için gerekli olan işlemler
    def handleTimer(self):
        value = self.pbar.value()  
        step = 5  
        # değerim 100'den küçükse 5'er 5'er adımlarla ilerlemiş oluyor.        
        if value < 100:
            value = value + step
            self.pbar.setValue(value)   # value'yi input olarak veriyoruz.
        else:
            self.timer.stop()



app = QApplication(sys.argv)
# window clasına ait bir tane obje oluşturucaz.

window = Window()
window.show()

sys.exit(app.exec())
        
