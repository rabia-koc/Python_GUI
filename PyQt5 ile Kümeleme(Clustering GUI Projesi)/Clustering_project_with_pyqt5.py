import warnings
warnings.filterwarnings("ignore")  # hata olmayan uyarıları filtreliyor konsol kısmında gözükmesini engelliyor

from PyQt5.QtWidgets import *

import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()   # QMainWindow'dan inherit edicek yani QMainWindow'da bulunan metotların hepsini kullanmak için
        
        # window'un nereden açılacağı
        self.left = 50
        self.top = 50
        self.width = 1080   # eni
        self.height = 6403   # boyu
        self.title = "Clustering"
        
        # bunların görülebilmesi için 
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top ,self.width, self.height )
        
        self.k = 1    # k'yı min değere eşitledik, k'yı seçtikten sonra clustering metodu içinde kullanmak için k'yı bir clas parametresi yapıyoruz.
        self.save_txt = ""  # başlangıçta boş bir string olsun, bunu neden yaptık? save_txt olması için bir tane variable tanımlamamız gerekiyor.
        
        self.widgets()
        self.tabWidget()
        self.layouts()
        self.prepareData()
        
        self.show()    
        
    def tabWidget(self):
        self.tabs = QTabWidget()   # 1 tane tab oluşturduk.
        self.setCentralWidget(self.tabs)   # tabs'ı central widegts yaptık
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Main")
        
        # widegt'leri eklemek için
    def widgets(self):
        
        # plot
        self.p = PlotCanvas(self, width = 5, height = 5)
    
        # label K
        # k sayısını seç diye uyarı veren label
        self.k_number_text = QLabel("Choose K:")
        
        # spin box
        self.k_number = QSpinBox(self)    
        self.k_number.setMinimum(1)   
        self.k_number.setMaximum(9)
        self.k_number.setSingleStep(1)     # 1'er adımlarla
        self.k_number.valueChanged.connect(self.k_numberFunction)    # k_number'de valueChanged varsa numberFunction ile connect kur
        
        # radio button
        self.text_save = QRadioButton("Save text", self)
        self.plot_save = QRadioButton("Save plot", self)
        self.text_plot_save = QRadioButton("Save text and plot", self)
        self.text_plot_save.setChecked(True)    # kullanıcı arayüzünü açtığım zaman burda save seçili olur otomatikman
        
        # button
        self.cluster = QPushButton("Cluster", self)
        self.cluster.clicked.connect(self.clusterFunction)   # butona bastığımız zaman fonksiyonla bağlantı kurucak
    
        # list
        self.result_list = QListWidget(self)
    
    def prepareData(self):
        
        self.p.clear()     # eğer plotta bir veri varsa temizlemek için
        
        data = pd.read_csv("data.csv")   # datayı okuma işlemi yaptık.
        
        self.f1 = data.iloc[:,3].values     # annual income, values ile np.array'e çeviriyoruz
        self.f2 = data.iloc[:,4].values     # spending score
        
        X = np.array(list(zip(self.f1, self.f2)))    # array içinde bir liste halinde birleştirmek için
        
        # random bir şekilde centroid oluşturuyoruz
        self.C_x = np.random.randint(0, np.max(X) - 20, size = self.k)   # centroid'deki x eksenindeki değerleri al demek
        self.C_y = np.random.randint(0, np.max(X) - 20, size = self.k)   # y ekseni için
        
        # görselleştirmek için
        self.p.plot(self.f1, self.f2, "black", 7)    # size: 7
        self.p.plot(self.C_x, self.C_y, "red", 200, "*")
    
    def k_numberFunction(self):
        self.k = self.k_number.value()    # k değerini seçmek için  
        self.prepareData()                # spinbox ile k değerini değiştirirken aynı zamanda plotun güncellenmesi için
    
    # a ve b arasındaki mesafeyi bulucaz.
    def dist(self, a, b):
        #  a ve b arasındaki mesafeyi bulabilmek için euclidean distance bulabilmek için 
        # a ve b noktaları arasındaki mesafeyi return ediyor.
        return np.linalg.norm(a - b, axis = 1)
    
    def kMeansClustering(self, f1, f2, C_x, C_y, k):
        # np.array kullanma sebebi: distance bulmak için matematiksel işlemler olucak ve np.array kolay bir şekilde yapmasını sağlıyor.
        X = np.array(list(zip(f1, f2)))
        
        C = np.array(list(zip(C_x, C_y)))
        
        # verimin hangi kümeye ait olduğunu saklayabilmek için bir tane array oluşturmamız gerekiyor, cluster arrayi oluşturmak gerekiyor.
        # çünkü grafikteki mavi noktanın centrod 0'a mı centroid 1'e mi yakın olduğuna bakıcaz ve bunun kümesine 0 numaralı küme diyeceğiz.
        # boş bir array oluşturmak gerekiyor.
        # array uzunluğu kaç tane veri varsa o kadar olacak yani X kadar 
        clusters = np.zeros(len(X))
        
        # kümeleme işlemini 10 kere yapsın yani 10 kere centroidleri tanımla
        for z in range(10):
            # en yakın noktaları bulacağımız for döngüsü
            for i in range(len(X)):
                # centroidler ile veri arasındaki mesafeyi bulucaz, tek tek bulucaz
                distances = self.dist(X[i], C)   # X'in indeks i deki verisine bak ve centroid ile karşılaştır.
                # bu distance fonksiyonu veriyle centroidler arasındaki mesafeyi bulucak yani euclidean distance bulucak.
                # bu dist fonksiyonunu tanımlamamız gerekiyor çünkü otomatik bir şekilde gelen fonksiyon değil
                
                cluster = np.argmin(distances) # uzaklıkların min değerinin indeksini bulmamız gerekiyor
                # çünkü array içindeki min değerin indeksini aldığımız zaman o indeks değerine karşılık gelen şey hangi cluster olduğudur.
                
                clusters[i] = cluster  # clusters'ın i.indeksine bu clusteri depola
            
            # mean recompute yapmak için  
            for i in range(k):
                
                # clusters'ların indeksi 0 ve 1 olucak çünkü k:2
                # noktaları belirliyoruz ve eğer clusters array'in içindeki bir değer örneğin 0.clustere eşitse burdaki pointleri points isimli listeye atıyoruz. 
                points = [ X[j] for j in range(len(X)) if clusters[j] == i]
                
                # yeni bir centrodi belirlemek için bunların ortalamasını almak gerekiyor ve zaten daha önceden bir centroidimiz vardı yani C array'dir, bunlar 2 tane 
                C[i] = np.mean(points, axis = 0)
        
        # max cluster sayısı 9 olacağı için 9 farklı kümeleme işlemi gerçekleştirebiliriz onun için 9 farklı renge ihtiyacımız var.
        colors = ['black', 'red', 'cyan','magenta', 'blue', 'yellow',"darkgreen","silver","indigo","maroon"]
        # görselleştirmek için 
        for i in range(k):
            # bir tane clustere ait noktaları aldık ve bu for döngüsü döndükçe tüm clusterlara ait noktalar farklı renklerde olucak.
            points = np.array([ X[j] for j in range(len(X)) if clusters[j] == i])
            self.p.plot(points[:,0], points[:,1], colors[i], 7)   # pointler x ve y indeksleri, i.rengi seçicek, size:7
            self.p.plot(C[:,0], C[:,1], "red", 200, "*")           # centroidler için    
            
            # result kısmında görselleştirmek için;
            # 2.parametre cluster'ın hangi cluster olduğu ve cluster 1,2,3,4,5 gitsin diye 1 ekledik
            result_txt = "Cluster" + str(i+1) + ": " + str(len(points)) + " (" + colors[i] + ")"
            self.result_list.addItems([result_txt])  # arayüzde göstermek için
            
            # save_txt'yi çıkan sonuçlar ile doldurucaz ve birden fazla cluster olduğu için araya -- koyduk.
            self.save_txt = self.save_txt + result_txt + " -- "
            
    def clusterFunction(self):
        
        # cluster butonuna tekrar tekrar basınca list kısmını ve plotu temizlemek gerekiyor
        self.result_list.clear()   
        self.p.clear()
        
        # önce datayı yolluyoruz. 
        self.kMeansClustering(self.f1, self.f2, self.C_x, self.C_y, self.k)
        
        # radio buttonları kullanarak save_txt yapma;
        # eğer text_save radiobutton seçili ise 
        if self.text_save.isChecked():
            path_name = "cluster_result.txt"   # sonuçları buraya kaydedecek.
            text_file = open(path_name,"w")    # text dosyasını açıyoruz write etmek için
            text_file.write(self.save_txt)     # save_txt'yi write edicez
            text_file.close()
            
        if self.plot_save.isChecked():
            self.p.fig.savefig("cluster_figure.jpg")   # arayüzde bulunan figure kaydetmek için
            
        # bu seçili ise her ikisini de yap
        if self.text_plot_save.isChecked():
            path_name = "cluster_result.txt"
            text_file = open(path_name,"w")
            text_file.write(self.save_txt)
            text_file.close()  
            
            self.p.fig.savefig("cluster_figure.jpg")
 
    # sayfa düzeni için
    def layouts(self):
        
        # layout
        self.mainlayout = QHBoxLayout()   # horizontal 
        self.leftlayout = QFormLayout()
        self.middlelayout = QFormLayout()
        self.rightlayout = QFormLayout()
        
        # left
        self.leftlayoutGroupBox = QGroupBox("Plot")   # 
        self.leftlayout.addRow(self.p)     # p widegt'i içinde olucak
        self.leftlayoutGroupBox.setLayout(self.leftlayout)   # groupbox içine leftlayout ekledik
        
        # middle
        self.middlelayoutGroupBox = QGroupBox("Clustering")
        self.middlelayout.addRow(self.k_number_text)
        self.middlelayout.addRow(self.k_number)    # spinbox ekledik
        # radiobuttonları ekledik
        self.middlelayout.addRow(self.text_save)
        self.middlelayout.addRow(self.plot_save)
        self.middlelayout.addRow(self.text_plot_save)
        self.middlelayout.addRow(self.cluster)   # butonu ekledik
        self.middlelayoutGroupBox.setLayout(self.middlelayout)
        
        # right
        self.rightlayoutGroupBox = QGroupBox("Result")
        self.rightlayout.addRow(self.result_list)
        self.rightlayoutGroupBox.setLayout(self.rightlayout)
        
        # main -> tab 
        # mainlayout'a groupbox'ların hepsini ekliyoruz.
        self.mainlayout.addWidget(self.leftlayoutGroupBox, 50)   # ne kadar oranlar yer kaplıcaklarını yüzdelik olarak en son parametrede belirttik.
        self.mainlayout.addWidget(self.middlelayoutGroupBox, 25)
        self.mainlayout.addWidget(self.rightlayoutGroupBox, 25)
        self.tab1.setLayout(self.mainlayout)   # mainlayout'u tab1'e ekledik.
        
        # FigureCanvas'tan inherit edecek 
class PlotCanvas(FigureCanvas):
    
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        
        self.fig = Figure(figsize=(width,height), dpi = dpi)
        
        # figure'yi figurecanvasa yolladık böylece FigureCanvastan inherit etmiş oluyoruz.
        FigureCanvas.__init__(self,self.fig)
        
        # c: color, s: size, m: plotu nasıl göstereceğim yani plot üzerindeki şekil
    def plot(self, x,y,c,s, m = "."):
        
        self.ax = self.figure.add_subplot(111)
        self.ax.scatter(x,y,c = c, s = s, marker = m)
        self.ax.set_title("K-Means Clustering")
        self.ax.set_xlabel("Income")   # gelir demek
        self.ax.set_ylabel("Number of Transaction") # harcama demek
        self.draw()    # plotu çizdirmek içim
        
        # fugure'yi temizlemek için
    def clear(self):
        self.fig.clf()


app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())
               












