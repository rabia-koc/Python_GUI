# libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter, QPen # icon and load image
from PyQt5.QtCore import Qt, QPoint
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # load image

import cv2 # open-cv use for image resize

## Convolutional Neural Network
import keras
from keras.datasets import mnist    # keras kütüphanesi içinde bulunan mnist veri setini kullanmak için
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D    # CNN için
#%% preprocess

(x_train, y_train),(x_test, y_test) = mnist.load_data()    # veri setini yüklüyoruz. 2 tane tupple ve içinde 2'şer tane variable return edecek.

# x_train: 60 bin tane resim var, x_train data setini kullanarak CNN eğiticez
# x_test data seti ile bunu test edicez. x_test: 10 bin tane resim var.
# test ederken daha önce göstermediğim resimlerle test ediyoruz.
# x_train ve x_test resimlerinin img'larının label'leri neler? yani hangi sınıfa ait olduğu bilgisi nerede saklanıyor?
# y_train ve y_test array'lerinde saklanıyor.
plt.figure()
i = 55
plt.imshow(x_train[i], cmap = "gray")   # x_train datasının 55. indeksine bakıyor, resmi gri bir hale getiriyor.
print("Label: ",y_train[i])        
plt.axis("off")    # resim göstereceğimiz için eksenleri kapatıyoruz.
plt.grid(False)    # plot üzerindeki gridleri kaldırdı.
# 8 sayısı karşımıza çıkıyor.
# bu resimler 0-9 sayılarından oluşuyor

# bu veriyi nöral networkte kullanılabilir hale getiricez.
# yani keras kütüphanesinin input olarak aldığı belli kurallar var
# size: 60000,28,28, 1 tane de chanel istiyor. Chanel: resmin RGB mi yoksa tek renk siyah beyaz mı olduğu
# bu veri setinin size'ni 60000,28,28,  1 şeklinde ayarlamamız gerekiyor.
img_rows = 28
img_cols = 28
# 60 bin alabilmek için x_train.shape'nin 0.indeksini alıyoruz, sonra 28,28,1 olarak devam ediyoruz.
x_train = x_train.reshape( x_train.shape[0],img_rows,img_cols,1)  
x_test = x_test.reshape( x_test.shape[0],img_rows,img_cols,1)  # x_testide böyle yapıyoruz
input_shape = (img_rows,img_cols,1)    # input shape de chanel değeri ekledik çünkü keras böyle kabul ediyor.

# normalization:
# her bir inputun benzer dağılıma sahip olmasını sağlayan önemli bir adımdır.
# input dediğimiz şeyler resmimizin her bir pikseli yani 28x28'lik matrisin her bir değeri demek.
# normalization işleminden sonra nöral network'ün eğitimi daha hızlı tamamlanır.
# bir resim nasıl normalization edilir?
# resimlerde normalization işlemi gerçekleştirmek için 255 değerine bölmemiz yeterlidir.
# normalization işlemi benim verimi 0 ve 1 arasına sıkıştırmak demektir, 255 bölmek bu işlemi gerçekleştirir. 
x_train = x_train.astype("float32")   # bilgi kaybetmemek adına bu çevirmeyi yaptık
x_test = x_test.astype("float32")

x_train /= 255 # x_train = x_train/255
x_test /= 255

# Bunların içinde labelleri içeren array'ler var, bu array'leri eğitebilmek için categorical hale getirmem gerekiyor
# aslında binary görünümlü hale getirmek demek
num_classes = 10
y_train = keras.utils.to_categorical(y_train, num_classes)  # 10 tane sınıfım var
y_test = keras.utils.to_categorical(y_test, num_classes)

# %% CNN

model_list = []  # modelimi depolucam
score_list = []  # soore depolucam

batch_size = 256
epochs = 5

# 2 tane modeli aynı anda eğitmek için bir for döngüsü çeviricem,
# for döngüsü çevirmeden önce bu 2 model arasındaki farklılık: modellerimizdeki hidden layer'larda bulunan nöron sayısıydı.
# bunun için bir array oluşturuyoruz.
filter_numbers = np.array([[16,32,64], [8,16,32]])  # model1 ve model2 deki nöron sayıları
# 2 dedik çünkü 2 modelimiz var
for i in range(2):
    
    print(filter_numbers[i])   # hangi nöronları kullanacağımızı print ettirdik.
    model = Sequential()       # sequential bir dizi oluşturduk. 
    # kaç tane nöron olucak? filter'ın i.indeksinin 0.indeksi kadar yani 16 tane nöronum olucak 
    model.add(Conv2D(filter_numbers[i,0], kernel_size = (3,3), activation = "relu", input_shape = input_shape))
    model.add(Conv2D(filter_numbers[i,1], kernel_size = (3,3), activation = "relu"))   # 1.indeks için
    # burda tekrardan input_shape gerek yok çünkü bunlar sequential olduğu için ilk oluşturduğumuz Conv2D outputu bir sonraki gelenin inputu oluyor.
    # bunlar birbirinin outputunu ve inputunu biliyorlar.
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Dropout(0.25))# %25 oranında drop yapacağı anlamına geliyor.
    # diyelim ki 8 tane nöronum var, %25'i 2 yapıyor.
    # her seferinde bu 8 tane nörondan 2'sini drop yapıcam yani söndürücem sanki bunlar kapalıymış orda yokmuş gibi davranıcam.
    # future extraction kısmı tamamlandı şimdi classification kısmına başlıyoruz
    model.add(Flatten()) # matrisleri düzleştiriyoruz.
    model.add(Dense(filter_numbers[i,2], activation = "relu"))  # 2.indekste bulunan nöron sayısını kullanarak yeni bir hidden layer oluşturabiliriz.
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation = "softmax"))  # bu output layer olucak.
    # softmax fonksiyonu: class sayısı 2'den fazlaysa kullanılan bir yöntemdir.
    # artık output layerdeki nöron sayısı num_classes'a eşit yani 10'a eşit.
    
    # nöral network'ü eğitmek için kullanacağımız fonksiyonları ve sonucu parametrede de değerlendirme için kullanacağımız metrik in ne olduğunu belirliyeceğiz.
    model.compile(loss = keras.losses.categorical_crossentropy, optimizer = keras.optimizers.Adadelta(),
                  metrics = ["accuracy"])
    # loss fonksiyonu: keras kütüphanesinin losslarının içerisinde bulunan categorical_crossentropy olucak.
    
    # model eğitim aşaması:
    # x_train ve y_train ile eğitim başlıyacak
    # verbose = 1: 0 ve 1 değerlerini alıyor. 1 yaptığım zaman modelim eğitilirken konsol kısmında eğitim sonuçlarını aynı anda bana göstermesini sağlıyor.
    history = model.fit(x_train, y_train, batch_size = batch_size, epochs = epochs, verbose = 1, validation_data = (x_test, y_test))
    
    # test işlemi için:
    score = model.evaluate(x_test, y_test, verbose = 0)
    print("Model {} Test Loss: {}".format(i+1, score[0]))  # i 0 olsun, i+1: 1 olur, model1'im  yani burda score içinde indeksi o olan yerdeki değer
    print("Model {} Test Accuracy: {}".format(i+1, score[1]))
    model_list.append(model)  # modeli deopladık.
    score_list.append(score)  # score'leri depoladık.
    
    model.save("model" + str(i+1) + ".h5")  # modeli kaydetme işlemi 

# model1: 3 layer=> 16, 32, 64 tane nöron
# model2: 3 layer=> 8, 16, 32 tane nöron
# %% modelleri yükleme işlemi
model1 = load_model("model1.h5")
model2 = load_model("model2.h5")
#%% Canvas
# sınıflandırmak istediğimiz sayıyı draw canvas methodunu kullanarak arayüze çizmiş olucaz.
class Canvas(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        self.width = 400
        self.height = 400
        self.setWindowTitle("Draw Digit App")
        self.setGeometry(50, 100, self.width, self.height)
        
        # çizilebilir hale gelmesi için QImage ekledik.
        self.image = QImage(self.size(),QImage.Format_RGB32)  # self.size: 400'e 400 return eden bir method.
        # yani bir window'um var bu window içerisine image classını kullanarak bir tane resim eklemiş oluyorum.
        
        self.image.fill(Qt.black)   # yani ekranı siyah yap demek.
        
        self.lastPoint = QPoint()
        self.drawing = False   # başlangıçta false olucak çünkü çizmiyorum
        
        # image_array
        self.im_np = np.zeros([self.width, self.height])   # bir array oluşturduk.
        
        # resmi çizdikten sonra kaydetmek için buton oluşturduk.
        button1 = QPushButton("Ok!", self)
        button1.move(2, 2)
        button1.clicked.connect(self.enterFunction)
        
        self.show()
        
    # image çağırmak için;
    def paintEvent(self, event):
        canvasPainter = QPainter(self)   # image boyamak için kullanacağımız bir yapı
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())  # nasıl bir image çizeceğimizi ayarlıyoruz.
        
    # bir tane pointer oluşturuyoruz.
    def enterFunction(self):
        ptr = self.image.constBits()    # bize pointer return ediyor.
        ptr.setsize(self.image.byteCount())   # image'nin byte sayısına kadar boyutunu belirlemiş oluyoruz.
        
        # image'min üzerine bir şey çizicem bu 400x400'lük matrisin içini çizdiğim şey ile doldurmam lazım.
        # örneğin; arka plan siyah olduğu için matrisimin büyük çoğunluğu black yani 0 değerine sahip olacak.
        # ama ben buraya bir şey çizdiğim zaman beyazla çizicem ve bu çizdiğim yerlerde 1 değerine sahip olacaklar.
        self.im_np = np.array(ptr).reshape(self.width, self.height,4)   # bir tane matris belirliyoruz.
        # self.im_np edebilmek için yukarda define etmem lazım.
        self.im_np = self.im_np[:,:,0]  # RGB renklerden sadece bir tanesini aldık
        self.im_np = self.im_np/255.0   
        # normalization ediyoruz. siyahlar 0 dı beyazlar 1 di 
        # ama bu normalde RGB olacağı için normalde siyaha yaklaştıkça renkler 0'a, beyaza yaklaştıkça RGB renklerin karışımı 255 olmak zorunda
        # bir resmi normalization yapmak için onu 255 bölmek yeterli. doğru tahminler yapabilmek için bu işlemi yaptık.
        
        # enter fonksiyonuna basınca ne olacağını yazıyoruz.
        # her yer siyahsa toplamı da 0 olacaktır. yani buraya hiç bir çizmemişim demektir.
        if np.sum(self.im_np) ==0:
            print("Please write a digit")
        # eğer bir şeyler çizdiysem
        else:
            plt.figure(figsize = (1, 1), dpi = 200)  
            plt.imshow(self.im_np, cmap = "gray")
            plt.axis("off")
            plt.grid(False)
            plt.savefig("input_img.png") # resmi kaydediyorum çünkü daha sonra bu resmi tekrarda yüklücem ve sınıflandırmaya sokucam.
            
            self.close()   # en sonda canvas window'u kapatmak için
            
    def mousePressEvent(self, event):
        # mousenin sol butonunu kullanırsam bastığım noktanın pozisyonunu al ve lastpointe eşitle 
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()  
            self.drawing = True   # bastım ve çizmeye başladığım için true yaptık.
            print(self.lastPoint)
            
    # mousenin sol tuşuna bastıysam ve drawing true ise 
    def mouseMoveEvent(self, event):
        # birden fazla tıkladığım için buttons yaptık
        if (event.buttons() == Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)  # içine bizim oluşturduğumuz resmi alıcak.
            painter.setPen(QPen(Qt.white, 20, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            # 1.parametre: içine beyaz bir şey çizmek için,
            # 2.parametre: boyutu 20
            painter.drawLine(self.lastPoint, event.pos())  # ilk tıkladığım noktadan line çizicem 
            self.lastPoint = event.pos()
            self.update()   # bu yaptıklarımı hep güncellemek için 
            
    # kontrol niteliğinde bir event yani tam çizmeyi bitirdiysem çizme işlemini kapatıyor.
    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False
        
        
        
        
#%% GUI 

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # main window
        self.width = 1080  # eni
        self.height = 640  # boyu
        
        self.setWindowTitle("Digit Classification")
        self.setGeometry(50, 100, self.width, self.height)
        self.setWindowIcon(QIcon("icon1.png"))   # projede kullanacağımız resim için
        
        self.create_canvas = Canvas()   # yukarda yaptığımız canvas classını ekledik.
        
        self.tabWidget()
        self.widgets()
        self.layouts()
        
        self.show()
    
        # 2 tane tabımız var, classification tabı içinde tüm olay gerçekleşiyor.
        # parametre tabı içinde nöral networkte kullandığım parametreleri gösterdiğim kısım olucak.
        # 1 tane ana tabs widget'im olucak, bunun altına 2 tane tab ekliyeceğim
    def tabWidget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Classification")
        self.tabs.addTab(self.tab2, "Parameters")
        
# classification tabı üzerinde input img, settings, output, result olmak üzere 4 tane layout var.
    def widgets(self):
        
        # tab1 left;
        # 2 tane buton, 2 label, 1 tane line edit yapmayı sağlayan entry widget bulunmaktadır.
        
        self.drawCanvas = QPushButton("Draw Canvas")
        self.drawCanvas.clicked.connect(self.drawCanvasFunction)   
        # buna bastığımız zaman bizim kullanıcı arayüzü sayesinde oraya bir tane rakam yazabilmemiz gerekiyor.
        # bu rakamı yazabilmemiz için de bir tane fonksiyona bağlanması gerekiyor.
        
        self.openCanvas = QPushButton("Open Canvas")
        self.openCanvas.clicked.connect(self.openCanvasFunction)

        self.inputImage = QLabel(self)     # bu input image variable'yle oraya bir tane rakam çizdikten sonra onu oraya yükleme işlemi gerçekleştiricem.
        self.inputImage.setPixmap(QPixmap("input.png"))
        
        self.searchText = QLabel("Real number: ")  
        # sınıflandırmak istediğim aradığım sayısını labeli yani gerçekte resmini çizdiğim rakamın ne olduğunu yazıyorum.
        
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Which number do you write?")

        # tab1 left middle;
        # 1 combobox, 1 label, 1 slider, 1 checkbox, 1 buton bulunmaktadır.
        
        self.methodSelection = QComboBox(self)
        self.methodSelection.addItems(["model1","model2"])   # 2 tane item ekledik.
        
        self.noiseText = QLabel("Add Noise: % " + "0")   # sonuçların ne çıktığını görmek için ekledik. 
        # en sonda default olarak 0 değerini koyuyoruz yani başlangıçta burada herhangi bir noise bulunmuyor demektir.
        self.noiseSlider = QSlider(Qt.Horizontal)  # noise değerini seçeceğimiz slider ekledik. yatay olarak
        self.noiseSlider.setMinimum(0)    # min değeri
        self.noiseSlider.setMaximum(100)  # max değeri
        self.noiseSlider.setTickPosition(QSlider.TicksBelow)   # slider üzerinde bulunan tiklerin yani birimlerin nerede bulunacağını belirliyoruz.
        # bunların pozisyonunu slider altına koyuyoruz TickBelow methodu ile
        self.noiseSlider.setTickInterval(1)   # tiklerin kalınlığını 1 birim belirledik. 
        self.noiseSlider.valueChanged.connect(self.noiseSliderFunction)
        # slider da meydana gelen değişikliği yansıtacağım bir fonksiyon ekledik.
        
        self.remember = QCheckBox("Save Result", self) 
        # bunu sonuçlarımı kaydetmek isteyip istememe göre seçeceğim bir checkbox olarak oluşturuyorum. eğer buna tıklarsam sonuçlarım kaydedilecek.
        
        self.predict = QPushButton("Predict")
        self.predict.clicked.connect(self.predictionFunction)
        
        # tab1 right middle
        # 2 tane label mevcut, labellerin üzerine resim ekliyoruz.
        # 1. label de prediction sonucunu yazıcağımız image olucak,
        self.outputImage = QLabel(self)
        self.outputImage.setPixmap(QPixmap("icon1.png"))   # pixmap: bir resmi yüklemek 
        # 2. label prediction sonucunu yani outputu yazacağımız label.
        self.outputLabel = QLabel("", self)
        self.outputLabel.setAlignment(Qt.AlignCenter)   # bu komutla output labeli merkeze hizalamış olduk.
        
        # tab1 right; 1 tane table widget bulunmaktadır.
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(2)   # 2 sütuna sahip
        self.resultTable.setRowCount(10)     # 10 satır çünkü 10 sınıfımız var
        self.resultTable.setHorizontalHeaderItem(0, QTableWidgetItem("Label(Class)"))  # 0.indeks column yazdık
        self.resultTable.setHorizontalHeaderItem(1, QTableWidgetItem("Probability"))   # 1.indeks column yazdık.
        # probability: class'ların sonucunda çıkan değerlerdir yani diyelim ki 1 sayısı çıktı olasılığı da %5;
        # %5 olasılıkla  benim left kısmına çizeceğim resim 1 sayısına aittir şeklinde bir sonuç ortaya çıkacak.
            
        # parametre tabında 2 tane list widget mevcut, bunların üzerinde method1 ve method2 adlı layout bulunuyor.
        # tab2 method1
        self.parameter_list1  = QListWidget(self)
        # kullandığımız parametreleri ekledik.
        self.parameter_list1.addItems(["batch_size = 256","epochs = 5","img_rows = 28",
                                       "img_cols = 28","Filter # = [16,32,64]","Activation Function = Relu",
                                       "loss = categorical cross entropy",
                                       "optimizer = Adadelta","metrics = accuracy"])
        
        # tab2 method2
        self.parameter_list2  = QListWidget(self)
        self.parameter_list2.addItems(["batch_size = 256","epochs = 5","img_rows = 28",
                                       "img_cols = 28","Filter # = [8,16,32]","Activation Function = Relu",
                                       "loss = categorical cross entropy",
                                       "optimizer = Adadelta","metrics = accuracy"])

    # sınıflandırma aşaması 
    # gerçekte ne çizdiğimizi real number kısmına yazıyoruz çünkü resultları kaydederken kullanıcaz.
    def predictionFunction(self):
        save_string = ""   # entry den aldığımız değerleri depolucaz.
        
        real_entry = self.searchEntry.text()
        save_string = save_string + " real entry: " + str(real_entry) + ", "
        
        # CNN model selection
        # hangi modeli seçeceğim işlemi 
        model_name = self.methodSelection.currentText()
        # currentText şu işe yarayabilir;
        if model_name == "model1":
            model = load_model("model1.h5")
        elif model_name == "model2":
            model = load_model("model2.h5")
        else:
            print("Error")
        
        # kaydetmek istediğimiz modeli de ekledik içine 
        save_string = save_string + "model name: " + str(model_name) + ", "
        
        # slider e noise ekleme işlemi yani resmi bozmak gibi 
        noise_val = self.noiseSlider.value()   # slider üzerinde belirlediğim değeri alıyor.
        
        # 0 dan farklı bir noise değerim varsa 
        if noise_val != 0:
            noise_array = np.random.randint(0, noise_val, (28, 28))/100
            # random integer: 0 ile noise_val değerleri arasında noise değerleri üret demek, bundan kaç tane üret demek 28x28'lik bir matris şeklinde üret demektir.
            # 3. parametre de 28'e 28'lik bir integer oluşturmak istiyorum ve normalize etmek için 100'e bölüyoruz.
            # yani 0 ile 1 arasında sıkıştır demek oluyor.
        else:
            noise_array = np.zeros([28, 28])   # boş bir array
            
        save_string = save_string + "noise value: " + str(noise_val) + ", "
        print(save_string)

        # load image as numpy 
        # img okuyoruz, en sonda ayar yapıyoruz çünkü kendisi otomatik olarak bir offset koyuyor
        # böyle yapmazsak 0 dan 26 ya olan kısımlar boş sayfa olarak gözüküyor
        img_array = mpimg.imread("input_img.png")[26:175, 26:175, 0]
        
        # resmin boyutunu 28x28 küçültüyor
        resized_img_array = cv2.resize(img_array, dsize=(28, 28), interpolation = cv2.INTER_CUBIC)
        
        # add noise
        resized_img_array = resized_img_array + noise_array
        
        # vis noise image
        plt.imshow(resized_img_array, cmap = "gray")
        plt.title("image after adding noise and resize")
        
        # predict
        # elde ettiğimiz resmin önce boyutlarını ayarlıyoruz.
        result = model.predict(resized_img_array.reshape(1, 28, 28, 1))
        QMessageBox.information(self,"Information","Classification is completed.")
        predicted_class = np.argmax(result)   # sonuçların maxını bulma
        print("Prediction: ", predicted_class)
        
        save_string = save_string + "Predicted class: " + str(predicted_class)
        
        # save result, eğer kaydetmeyi seçersem
        if self.remember.isChecked():
            text_file = open("Output.txt","w")
            text_file.write(save_string)
            text_file.close()
        else:
            print("not save")
        
        # prediction'u output label üzerine görüntü olarak ekleme 
        self.outputImage.setPixmap(QPixmap("images\\" + str(predicted_class) + ".png"))
        # outpu labele okuduğum dosyayı setText methodu kullanarak yazmak istiyoruz.
        self.outputLabel.setText("Real: " + str(real_entry) + " and Predicted: " + str(predicted_class))
        
        
        # set result
        for row in range(10):
            self.resultTable.setItem(row, 0, QTableWidgetItem(str(row)))  
            self.resultTable.setItem(row, 1, QTableWidgetItem(str(np.round(result[0][row], 5))))  
            # 1.column da 0. indeksi virgülden sonra 5 basamak göster.
        
    # bunun içinde oluşturduğum classı göstermem gerekiyor. Bunun öncesinde canvas objesi oluşturmamız gerekiyor.
    # bunu yapabilmek için canvas classını yazmamız gerekiyor yani sıfırdan kodluyacağımız bir class olacak.
    def drawCanvasFunction(self):
        self.create_canvas.show()   # butona bastığım zaman canvası görselleştirmiş olacağım.
        
    def openCanvasFunction(self):
        self.inputImage.setPixmap(QPixmap("input_img.png"))  # bu butona basınca soru işareti olan yere çizdiğimiz resim yüklenmiş olacak.
    
    def noiseSliderFunction(self):
        val = self.noiseSlider.value()   # slider değerini okuyoruz ve val içierisine yazıyoruz.
        self.noiseText.setText("Add Noise: % " + str(val))    # orada bulunan labeli set ediyoruz. Bu sefer 0 yerinde kendi sliderimde olan değeri seçicem.
    
    # sayfa düzeni için; 
    # her bir tabın üzerinde bulunan şeylere widget diyoruz. bu widgetler formlayout üzerinde bulunuyor.
    # formlayout adlandırdığım şey aslında left diye yazdığım yer.
    # formlayout üzerinde yani left layoutta groupbox bulunuyor, left kısmında input image yazan kısım groupbox'ımız.
    # gorupbox üzerinde bir tane horizontol layout bulunuyor.
    # horizontol layout üzerinde tab1 widget bulunuyor. tab1 değiğimiz şey burdaki classification
    def layouts(self):
        
        # tab1 layout
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.leftMiddleLayout = QFormLayout()
        self.rightMiddleLayout = QFormLayout()
        self.rightLayout = QFormLayout()
    
        # left
        self.leftLayoutGroupBox = QGroupBox("Input Image")  # en dışında
        self.leftLayout.addRow(self.drawCanvas)
        self.leftLayout.addRow(self.openCanvas)
        self.leftLayout.addRow(self.inputImage)
        self.leftLayout.addRow(self.searchText)
        self.leftLayout.addRow(self.searchEntry)
        self.leftLayoutGroupBox.setLayout(self.leftLayout)   # groupboxa left layout ekledik.
        
        # left middle
        self.leftMiddleLayoutGroupBox = QGroupBox("Settings")
        self.leftMiddleLayout.addRow(self.methodSelection)
        self.leftMiddleLayout.addRow(self.noiseText)
        self.leftMiddleLayout.addRow(self.noiseSlider)
        self.leftMiddleLayout.addRow(self.remember)
        self.leftMiddleLayout.addRow(self.predict)
        self.leftMiddleLayoutGroupBox.setLayout(self.leftMiddleLayout)
    
        # right middle 
        self.rightMiddleLayoutGroupBox = QGroupBox("Output")
        self.rightMiddleLayout.addRow(self.outputImage)
        self.rightMiddleLayout.addRow(self.outputLabel)
        self.rightMiddleLayoutGroupBox.setLayout(self.rightMiddleLayout)
    
        # right 
        self.rightLayoutGroupBox = QGroupBox("Result")
        self.rightLayout.addRow(self.resultTable)
        self.rightLayoutGroupBox.setLayout(self.rightLayout)
    
        # tab1 deki layoutları main layouta ekliyoruz.
        self.mainLayout.addWidget(self.leftLayoutGroupBox, 25)   # en sonuncu parametre yüzdelik olarak ne kadar yer kaplıyacağı
        self.mainLayout.addWidget(self.leftMiddleLayoutGroupBox, 25)
        self.mainLayout.addWidget(self.rightMiddleLayoutGroupBox, 25)
        self.mainLayout.addWidget(self.rightLayoutGroupBox, 25)
        self.tab1.setLayout(self.mainLayout)    # mainlayoutu tab1'e ekledik.
        
        # tab2 layout
        self.tab2Layout = QHBoxLayout()
        self.tab2Method1Layout = QFormLayout()
        self.tab2Method2Layout = QFormLayout()
        
        # tab2 Method1 Layout
        self.tab2Method1LayoutGroupBox = QGroupBox("Method1")
        self.tab2Method1Layout.addRow(self.parameter_list1)    
        self.tab2Method1LayoutGroupBox.setLayout(self.tab2Method1Layout)
        
        # tab2 Method2 Layout
        self.tab2Method2LayoutGroupBox = QGroupBox("Method2")
        self.tab2Method2Layout.addRow(self.parameter_list2)
        self.tab2Method2LayoutGroupBox.setLayout(self.tab2Method2Layout)
    
        # tab2 deki layoutları main layouta ekliyoruz.
        self.tab2Layout.addWidget(self.tab2Method1LayoutGroupBox, 50)
        self.tab2Layout.addWidget(self.tab2Method2LayoutGroupBox, 50)
        self.tab2.setLayout(self.tab2Layout)   # tab2 layoutu tab2'ye ekledik
     
    
app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())









































