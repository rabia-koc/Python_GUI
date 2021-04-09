
from PyQt5.QtGui import QFont
# bu class QWidgetten inherit edicek yani QWidget clasında bulunan tüm metotları kullanabilir demek

from PyQt5.QtWidgets import *
import sys

class Window(QWidget):
    
    def __int__(self):
        super().__init__()   # bu QWidget clasından inherit edebilmemizi sağlayan kod satırı
        
        self.setGeometry(50, 50, 1080, 640)   
        # pencereinin 50'ye 50'sinden başlasın 1080 piksele 640 piksel boyutu olsun. eni ve boyu demek en son 2 yazdığım satır.
        self.setWindowTitle("PyQt5 App")
        
        self.button()
        self.label()
        self.entry()
        self.messageBox()
        self.font()
        self.show()
        
    # button
    # windowu ifade eden self
    def button(self):
        button = QPushButton("Hello World", self)   # window'un üzerine koymak için self yazdık.
        button.setToolTip("This is a hello world button")   # buton üzerine geldiğimiz zaman yazacak yazı
        button.resize(100, 50)   # buton boyutu
        button.move(50, 50)   # butonun konumu
        
        button.clicked.connect(self.buttonFunction)    # butona tıklandığında bağlantı kur
        # burdaki self window'un içindeki butonFunction
    
    def buttonFunction(self):
        print("hello world")
        
    
     # label
    def label(self):
        
        text1 = QLabel("hello", self)        # window üzerine koymak için self dedik.
        self.text2 = QLabel("world", self)   # başına self koyunca sadece label'e ait olmaz,
        # window clasına ait instance bir variable olmuş olur.
        
        # geometry manager
        text1.move(170, 50) 
        self.text2.move(170, 70)
        
        button1 = QPushButton("Change", self)
        button1.move(170, 100)
        button1.clicked.connect(self.button1Function)

    def button1Function(self):
        self.text2.setText("Hello World")   # text2'yi değiştirmek için 
        self.text2.resize(200, 25)
        self.text2.setFont(QFont("Arial", 25, QFont.Bold))   # kalın yazı yaptık

    def entry(self):
        
        self.textBox = QLineEdit(self)
        self.textBox.setPlaceholderText("place holder")    # entry içinde bu yazı yazar.
        self.textBox.move(300, 50)
        
        button1 = QPushButton("Save", self)    # entry içini kullanabilmek için buton tanımladık.
        button1.move(300, 75)
        button1.clicked.connect(self.saveFunction)
        
    
    def saveFunction(self):
        
        txt = self.textBox.text()   # txt'i oku demek.
        
        # txt boş değilse 
        if txt != "":
            print(txt)
        else:
            print("write something")

    def messageBox(self):
        
        button1 = QPushButton("message", self)
        button1.move(500, 50)
        button1.clicked.connect(self.messageFunction)
        
        button2 = QPushButton("message2",self)
        button2.move(500, 75)
        button2.clicked.connect(self.messageFunction2)

    def messageFunction(self):
        # soru sorduk ve cevapları yazdık.
        m_box = QMessageBox.question(self, "Question", "Did you enjoy the course?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,  QMessageBox.No)  # sonuncu parametre ile butona basınca mavi vurgu olmasını sağladık.
    
        if m_box == QMessageBox.Yes:
            print("yes")
        elif m_box == QMessageBox.No:
            print("no")
        else:
            print("cancel")
            
    # bize bilgi vermesi için;
    def messageFunction2(self):
        m_box = QMessageBox.information(self, "Information", "Enjor your course")

    
    def font(self):
        self.label = QLabel("Hello world", self)
        self.label.move(700, 100)
        
        button2 = QPushButton("choose font", self)
        button2.move(700, 50)
        button2.clicked.connect(self.setfont)  

    def setfont(self):
        font, ok = QFontDialog.getFont()     # font'un yazı tipini değiştirmek için fontdialog'u çağırdık.
        # 2 tane varibale return ediyor. 
        
        # ok seçersek hello world yazısını değiştirebiliriz.
        if ok:
            self.label.setFont(font)    # return edilen fontu kullanıyor.
            self.label.resize(200, 75)

app = QApplication(sys.argv)
# window clasına ait bir tane obje oluşturucaz.

window = Window()
window.show()

sys.exit(app.exec())
        
        