#%%
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from PIL import ImageTk, Image

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from keras.models import load_model

#%%
# veri setini okumak
skin_df = pd.read_csv("HAM10000_metadata.csv")

# data analizi için
skin_df.head()
skin_df.info()  # dataframe hakkında genel bir bilgi sağlaması için.

# kanser hücrelerinin kaç tane sınıfa ait olduğu
# skin_df içinde bulunan kanser hücresi sınıflarından kaç tane olduğunu ve
# kanser hücresi sınıflarının dağılımlarını gösteriyor.
sns.countplot(x = "dx", data = skin_df)

#%%
# preprocess
data_folder_name = "HAM10000_images_part_1/"
# resimlerin extaion'u
ext = ".jpg"

"""
# bu resimleri pathini daha önce tanımlamış olduğum skin_df de bir tane path isimli feature yazmak istiyorum
# yazmam için bir tane data folder name ihtiyacım var. daha sonra resimlerimin Id si olması gerek.
# daha sonra da formatını eklemem gerek (.jpg)
"HAM10000_images_part_1/ISIC_0027419.jpg"
#data_folder_name + image_id[i] + ext
"""
"""
#path isimli feature oluşturduk. dataframe'min image_id'sinde dolaşıcak.
#dolaştığım zaman sırasıyla resimlerimin idlerine erişimim olucak.
"""
skin_df["path"] = [data_folder_name + i + ext for i in skin_df["image_id"]]

# bu path üzerinde dolaşarak bu her bir resme skin_df içerisine array olarak yüklicem.

# resimlerimi image isimli bir feature yüklemek istiyorum. Bu path' map etmiş olacağım
# map: skin_df path2in içerisindeki her bir satırı kullanarak bir fonksiyon yap demek.
# fonksiyonu lambda ile tanımlıyoruz. x: input, açmak istediğimiz resim olucak.
# daha sonra resize ile resmin boyutunu tekrardan ayarlıyoruz.
# ama bu resmi numpy array olarak tanımlamak istiyorum.
skin_df["image"] = skin_df["path"].map(lambda x: np.asarray(Image.open(x).resize((100,75))))

# görselleştirmek için
plt.imshow(skin_df["image"][0]) # kanser hücresinin resmi geldi.


# kanser hücresi sınıflarımız stringti. Bunları int çevirmemiz gerekiyor.
# dx_id diye bir feature oluşturarak sayısal bir şekilde kodlucam.

skin_df["dx_idx"] = pd.Categorical(skin_df["dx"]).codes

skin_df.to_pickle("skin_df.pkl") # verimizi depolayan bir dosyadır.

#%%
# load pkl
# bunu nasıl yüklicez.
skin_df = pd.read_pickle("skin_df.pkl")

#%%
# standardization: farklı verileri karşılaştırılabilir edebilmemizi sağlıyor.
# array olan bir şeyi ilk önce listeye daha sonra tekrardan arraye çevirmiş oluyoruz.
# x_train isimli data setim oluyor.
x_train = np.asarray(skin_df["image"].tolist())
# burdaki resimlerin nöral network'üme input olarak yani train olarak kullanacağım için burdaki resimleri
# bir arraye çevirip daha sonra  x_train isimli bir variable ye eşitliyorum.
# x_train i standardazation etmek için;
# önce ortalamasını buluyoruz.
x_train_mean = np.mean(x_train)
# std için;
x_train_std = np.std(x_train)


# standardzation için;
x_train = (x_train - x_train_mean)/x_train_std
# standardize edilmiş nöral networkümde eğitime hazır verim olmuş olucak.

#%%
# one hot encoding

# şimdi labelleri elde etmemiz gerekiyor.
# 7 tane kanser hücresi sınıfım var.
# skin_df içerisinde bulunan dx_idx i categorical hale getiriyoruz.
y_train = to_categorical(skin_df["dx_idx"], num_classes = 7)

#%%
# CNN 
input_shape = (75, 100, 3)
num_classes = 7 

# feature exration kısmı
# CNN oluşturmak için ilk olarak sequential bir diziye ihtiyacım var.
model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), activation="relu", padding="Same", input_shape=input_shape))  
# 32 tane nörondan oluşsun, filtrenin boyutu: (3,3)

# 2. layer Conv2D ekliyoruz.
model.add(Conv2D(32, kernel_size=(3,3), activation="relu", padding="Same"))
# neden input shape yok? 
# Sequential(1,2)
# bunları bir sequential yapı içerisine yazdığımız için 
# burda 1 ve 2 yi ard arda sıraladık. Bunun sonucunda çıkan outputu 
# bu 2'nin inputu olmuş olucak.
# 1'in outputu eşittir 2'nin inputu

# 1'in inputunu belirlememiz gerekiyor. Çünkü 1'in önünde hiçbir şey yok.
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))  # %25 oranında drop yapacağı anlamına geliyor.
# diyelim ki 8 tane nöronum var, %25'i 2 yapıyor.
# her seferinde bu 8 tane nörondan 2'sini drop yapıcam yani söndürücem sanki bunlar kapalıymış orda yokmuş gibi davranıcam.
 
model.add(Conv2D(64, kernel_size=(3,3), activation="relu", padding="Same"))
model.add(Conv2D(64, kernel_size=(3,3), activation="relu", padding="Same"))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))
# bir tane daha output layer belirliyoruz. output layer de ortaya çıkacak sonucu sınıflara bölebilmem için
# 7 tane sonuç ortaya çıkması gerek. Bu 7 tane sonuçtan en büyüğünü seçip clasımın  sonucu budur diyebileyim.
model.add(Dense(num_classes, activation="softmax"))
# softmax fonksiyonu: class sayısı 2'den fazlaysa kullanılan bir yöntemdir.
model.summary()  # özetleyeceğimiz kısmımız

# learning read parametresine sahip
#optimizer = Adam(lr = 0.001)   # model1 için 
optimizer = Adam(lr = 0.0001)   # model2 için    
model.compile(optimizer = optimizer, loss = "categorical_crassentropy" , metrics = ["accuracy"])  # değerlendirme için kullanacağım metrikler

# tüm resimlerimin kaç kez train edileceği
epochs=5
# örneğin; her bir epochs ta train edilecek 10 bin tane resmimim nasıl train edileceği
# resimlerim her bir epochta toplu bir şekilde 10 bini aynı anda train edilecek 
# burda resimlerim 1'er 1'er train edilecek yani 10 bin kere train edilecek ve bu 1 epocha eşit olacak.
# epoch 5 olduğu için toplamda 50 bin resim train edilmiş olucak.
batch_size=25

# train etme aşaması
history=model.fit(x=x_train, y=y_train, batch_size=batch_size, epochs=epochs, verbose=1, shuffle=True)
# verbose = 1: 0 ve 1 değerlerini alıyor. 1 yaptığım zaman modelim eğitilirken konsol kısmında eğitim sonuçlarını aynı anda bana göstermesini sağlıyor.
# shuffle: veriyi eğitmeden önce karıştırıyor. karışık bir şekilde eğitim yapıyor, sırayla değil.

# modeli kaybetmemek için
model.save("my_model1.h5")
model.save("my_model2.h5")

# %% load
model1 = load_model("my_model1.h5")
model2 = load_model("my_model2.h5")

#%% prediction
# prediction yapabilmemiz için elimizde veri olması gerekiyor.
# önce dataframi yüklücez. sonra x_train ve y_train variable'lerini elde etmek istiyorum.
# x_trainlere göre prediction yapabiliriz ve y_train'ide karşılaştırabiliriz.

# x_train'in 5.indeksine prediction yapıyoruz. bunu ne olduğunu öğrenmek için konsol da y_train[index]'e bakmamız gerekiyor.
# sonucu: y_train[index]
# Out[57]: array([0., 0., 1., 0., 0., 0., 0.], dtype=float32)
# yani 2 numaralı indekse sahip deri kanseri hücremde
index = 5

y_pred = model1.predict(x_train[index].reshape(1,75,100,3))  # prediction bu formattaki resimleri kabul ediyor.
# y_pred: 7 tane değerden oluşan bir yapı. Bunlar olasılık değerleri yani bunların toplamının 1 olmasını bekliyorum.
# np.sum(y_pred)
# Out[60]: 1.0  # 1 olduğunu gördük.
y_pred_class = np.argmax(y_pred, axis = 1)  
# bu bana y_pred içindeki en büyük değerin indeksini return ediyor. 
# satır ekseninde olduğu için 1 dedik ve bize 2'yi return ediyor.

#np.argmax(y_train[index], axis = 0)   
# sonucu: 2 çıkıyor. yani elimde bir resim vardı, bu resmin gerçekteki label'i 2 idi. yani 2 numaralı classa aitti.
# bu resmi eğittiğimiz modele göre model1'e göre predict ettiğimiz zamanda sonucumuz 2 olmuş oldu.

# %% Skin Cancer Classification GUI

window = tk.Tk()
window.geometry("1080x640")
window.wm_title("Skin Cancer Classification")

## global variables
img_name = ""
count = 0
img_jpg = ""

## frames
frame_left = tk.Frame(window, width = 540, height = 640, bd = "2")   # sınırlarının genişliği:2
frame_left.grid(row = 0, column = 0)

frame_right = tk.Frame(window, width = 540, height = 640, bd = "2")
frame_right.grid(row = 0, column = 1)

frame1 = tk.LabelFrame(frame_left, text = "Image", width = 540, height = 500)
frame1.grid(row = 0, column = 0)

frame2 = tk.LabelFrame(frame_left, text = "Model and Save", width = 540, height = 140)
frame2.grid(row = 1, column = 0)

frame3 = tk.LabelFrame(frame_right, text = "Features", width = 270, height = 640)
frame3.grid(row = 0, column = 0)

frame4 = tk.LabelFrame(frame_right, text = "Result", width = 270, height = 640)
frame4.grid(row = 0, column = 1, padx = 10)


# frame1
def imageResize(img):
    
    basewidth = 500  # bu oranla resmi büyültüp küçültebiliriz.
    wpercent = (basewidth/float(img.size[0]))  # oranlama # 1000 *1200 # img.size[0]: 1000 yani 500/1000:0.5
    hsize = int((float(img.size[1])*float(wpercent)))    # 1200*0.5: 600 oldu
    img = img.resize((basewidth,hsize),Image.ANTIALIAS)   # bu metot resize yaparken araları doldurmaya yarayan bir yöntem.
    # 500x600'lük resim oluştu. 
    return img
    
def openImage():
    
    global img_name
    global count
    global img_jpg
    
    count += 1
    # count 1 değilse 
    if count != 1:
        messagebox.showinfo(title = "Warning", message = "Only one image can be opened")
    else:
        img_name = filedialog.askopenfilename(initialdir = "D:\codes",title = "Select an image file")
        
        img_jpg = img_name.split("/")[-1].split(".")[0]  
        # img_name içinden ilk önce /'lara göre ayırıcaz, ayırınca bir liste ortaya çıkıyor
        # içinde 5 tane item var bu item'lardan en sonuncusunu alıcaz çünkü en sondaki img_name
        # jpg nin de olmaması için noktaya göre ayırma işlemi yapıyoruz ve 0. indekste olanını sadece alıyoruz.
        # bu şekilde img_name elde ettik.
        
        # image label
        tk.Label(frame1, text =img_jpg, bd = 3 ).pack(pady = 10)
        
        # img_name kullanrak img'i ara yüze yüklemem gerekiyor.
        # open and show image
        img = Image.open(img_name)
        img = imageResize(img)  
        
        img = ImageTk.PhotoImage(img)
        # görselleştirme aşaması
        panel = tk.Label(frame1, image = img)
        panel.image = img
        panel.pack(padx = 15, pady = 10)
        
        # image feature
        # resim seçtikten sonra özellikler feturede otomatik yazılması için 
        data = pd.read_csv("HAM10000_metadata.csv")  # resimleri burdan okuruz.
        cancer = data[data.image_id == img_jpg]      # kanserleri bulmak için

        for i in range(cancer.size):
            x = 0.4
            y = (i/10)/2
            tk.Label(frame3, font = ("Times",12), text = str(cancer.iloc[0,i])).place(relx = x, rely = y)
            # iloc indekse bağlı çalışıyor
menubar = tk.Menu(window)
window.config(menu = menubar)
file = tk.Menu(menubar)
menubar.add_cascade(label = "File",menu = file)  # bir tane buton gibi bir yapı ekledik.
file.add_command(label = "Open", command = openImage)


# frame3
def classification():
    # bu işlemin gerçekleşmesi için önce 1 tane resim seçmeliyim ve modelimi de seçmeliyim.
    if img_name != "" and models.get() != "":
        
        # model selection
        if models.get() == "Model1":
            classification_model = model1
        else:
            classification_model = model2
        
        # resimi seçeceğimiz yer 
        z = skin_df[skin_df.image_id == img_jpg]
        z = z.image.values[0].reshape(1,75,100,3)  
        # z'nin image'ni almak için 0.indeksi alıyoruz ve 
        # sınıflandırma kullanmak istediğim boyuta getirdik.
        
        
        # z'yi standardization yapıyoruz
        z = (z - x_train_mean)/x_train_std
        
        # predic için
        h = classification_model.predict(z)[0]   # bunun sonucunda çıkan array'in 0.indeksini alıcaz.
        h_index = np.argmax(h)    # indeksini bulmamızı sağlayan numpy metodu.
        predicted_cancer = list(skin_df.dx.unique())[h_index]
        
        # görselleştirmek için
        for i in range(len(h)):
            x = 0.5
            y = (i/10)/2
            
            # prediction sonucunu farklı bir renkte yazıyoruz
            if i != h_index:
                tk.Label(frame4,text = str(h[i])).place(relx = x, rely = y)
            # i h_index'e eşitse;
            else:
                tk.Label(frame4,bg = "green",text = str(h[i])).place(relx = x, rely = y)
        
        # 1 ise seçili iken sınıflandırma sonuçlarını kaydetmem gerekiyor.
        if chvar.get() == 1:
            
            val = entry.get()
            # entry'e nasıl kaydedeceğimi yazdık.
            # yani entry'in orda yazılanları get ettikten sonra entry'e başka bişey ekleyemiyoruz.
            entry.config(state = "disabled")
            
            path_name = val + ".txt" # result1.txt
            
            # kayıt ederken img_name ve prediction sonucu ortaya çıkan değeri kayıt ediyoruz.
            # yani hangi sınıfa ait bir prediction yaptığı
            save_txt = img_name + "--" + str(predicted_cancer)
            
            text_file = open(path_name,"w")   # txt dosyası açıyoruz bunu write etmek için
            text_file.write(save_txt)         # yazmak istediğim içeriği write ediyorum.
            text_file.close()                 # sonra açılan dosyayı kapatıyoruz.
        else:
            print("Save is not selected")
    
    # modelim ve resmim seçili değilse 
    else:
        messagebox.showinfo(title = "Warning", message = "Choose image and Model First!")
        tk.Label(frame3, text = "Choose image and Model First!" ).place(relx = 0.1, rely = 0.6)
    
    
            
# resmime ait özellikler 
# localization: kanser hücresinin nereden alındığı 
columns = ["lesion_id","image_id","dx","dx_type","age","sex","localization"]
# bu stringleri label'leyebilmek için for döngüsüne alıyoruz.
for i in range(len(columns)):
    x = 0.1  # x hepsi için aynı
    y = (i/10)/2   # y hep artıyo, ince ayar için 2'ye böldük
    tk.Label(frame3, font = ("Times",12), text = str(columns[i]) + ": ").place(relx = x, rely = y)

classify_button = tk.Button(frame3, bg = "red", bd = 4, font = ("Times",13),activebackground = "orange",text = "Classify",command = classification)
classify_button.place(relx = 0.1, rely = 0.5)

# frame 4 : Result'lar olucak yani sınıflandırma sonuçlarım olucak.
# bunlar skin_df içinde tanımlı 7 adet bulunan label'lar
labels = skin_df.dx.unique()   
# dx: kanser sınıflarım, bunu run edince 7 tane fraklı sınıf çıkıyor.

# bu label'leri görselleştirmek için
for i in range(len(columns)):
    x = 0.1
    y = (i/10)/2
    tk.Label(frame4, font = ("Times",12), text = str(labels[i]) + ": ").place(relx = x, rely = y)

# frame 2 
# combo box
model_selection_label = tk.Label(frame2, text = "Choose classification model: ")
model_selection_label.grid(row = 0, column = 0, padx = 5)

models = tk.StringVar()
model_selection = ttk.Combobox(frame2,textvariable = models, values = ("Model1","Model2"), state = "readonly")  
# state'deki metot sadece bir şey seçebiliriz oraya bişey yazamyız demek.
model_selection.grid(row = 0, column = 1, padx = 5)

# check box
chvar = tk.IntVar()
chvar.set(0)  # int verileri kullanıcaz 0 ya da 1. 0 ise seçili değil
xbox = tk.Checkbutton(frame2, text = "Save Classification Result", variable = chvar)
xbox.grid(row = 1, column =0 , pady = 5)

# entry
entry = tk.Entry(frame2, width = 23)
entry.insert(string = "Saving name...",index = 0)  # kaydedeceğim dosyanın ismini yazmak için
entry.grid(row = 1, column =1 )
window.mainloop()

