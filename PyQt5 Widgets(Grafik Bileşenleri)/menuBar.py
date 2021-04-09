# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 15:32:05 2021

@author: casper
"""

from PyQt5.QtWidgets import *
import sys

# window isimli class QMainWindow'dan inherit edilecek yani QMainWindow içerisinde bulunan metotları kullanabilecek.
# çünkü menubar widgeti QMainWindow içerisinden gelen bir widget
class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,520,320) 
        self.setWindowTitle("Menu App")
          
        self.menubar()
        self.show() 
        
    def menubar(self):
        
        bar = self.menuBar()   # bar oluşturduk
        
        file = bar.addMenu("File")    # ilk menü elemanı
        file.addAction("New")         # file içine action ekledik
        
        save = QAction("Save",self)   # save adlı action ekledik
        save.setShortcut("Ctrl+S")    # save bir kısa yol oluşturduk
        file.addAction(save)          # file save ekledik
        
        data = file.addMenu("Data")   # file içine menü oluşturduk.
        data.addAction("Export")      # actionlar ekledik.
        data.addAction("Import")
        
        file.triggered[QAction].connect(self.progressTrig)   # bastığımız yerleri print ettirmek için 
        
        
    def progressTrig(self, q):
        # q: bastığımızı action'u okumamızı sağlayacak parametredir.
        print(q.text())
        
        
app = QApplication(sys.argv)
# window clasına ait bir tane obje oluşturucaz.

window = Window()
window.show()

sys.exit(app.exec())
              
        
        
        
        
        
        









