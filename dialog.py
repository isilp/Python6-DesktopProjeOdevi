import sys
import os
from AnaDB import Veritabani
from PyQt5.QtWidgets import QApplication,QDialog,QTableWidgetItem,QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        ## veritabanı ve arayüz dosyaları çağırılıyor
        self.vt = Veritabani(os.getcwd()+r"\IEDB.db")
        self.pencere = uic.loadUi(os.getcwd()+r"\sozluk.ui")
        self.pencere.btIptal.clicked.connect(self.pencere.close)
        self.pencere.btKaydet.clicked.connect(self.KaydetSozluk)
        # self.pencere.lstSozluk.itemDoubleClicked.connect(self.SecimSozluk)
        self.pencere.show()

    
    def TabloDoldurSozluk(self):
        self.pencere.lstSozluk.clear()
        self.liste = self.vt.SozlukGoruntule()
        self.pencere.lstSozluk.setHorizontalHeaderLabels(("ID", "SOZLUK_ID","SOZLUK_ADI","TABLO_ID"))
        self.pencere.lstSozluk.setRowCount(15)
        self.pencere.lstSozluk.setColumnCount(4)
        satir = 0
        for a,b,c,d in self.liste:
            self.pencere.lstSozluk.setItem(satir, 0, QTableWidgetItem(str(a)))
            self.pencere.lstSozluk.setItem(satir, 1, QTableWidgetItem(str(b)))
            self.pencere.lstSozluk.setItem(satir, 2, QTableWidgetItem(str(c)))
            self.pencere.lstSozluk.setItem(satir, 3, QTableWidgetItem(str(d)))
            satir += 1
            
    # def SecimSozluk(self):
    #     # print(self.liste[self.pencere.lstSozluk.currentRow()])
    #     sozlukID = str(self.liste[self.pencere.lstSozluk.currentRow()][3])
    #     sozlukadi = str(self.liste[self.pencere.lstSozluk.currentRow()][1])
    #     tabloID = = str(self.liste[self.pencere.lstSozluk.currentRow()][2])
    #     self.pencere.txtID.setText(sozlukID)
    #     self.pencere.txtAd.setText(sozlukadi)
    #     self.pencere.txtTablo.setText(tabloID)
    #     self.pencere.cmbKalem.setCurrentText(self.liste[self.pencere.lstSozluk.currentRow()][1])


    def MesajSozluk(self,icon,baslik,metin):
        sonuc = True
        if icon == 1:
            QMessageBox.information(self,baslik,metin,QMessageBox.Ok)
        elif icon == 2:
            QMessageBox.critical(self,baslik,metin,QMessageBox.Ok)
        elif icon == 3:
            QMessageBox.warning(self,baslik,metin,QMessageBox.Ok)
        elif icon == 4:
            try:
                cevap =  QMessageBox.question(self,baslik,metin,QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Cancel)
                if cevap == QMessageBox.Ok:
                    sonuc = True
                else:
                    sonuc = False
            except:
                print("Hata")
        return sonuc


    def KaydetSozluk(self):
        sozlukID = self.pencere.txtID.text()
        sozlukadi = self.pencere.txtAd.text()
        tabloID = self.pencere.txtTablo.text()
     
        if ID == 0:
            sonuc = self.vt.VeriEkleSozluk(sozlukID,sozlukadi,tabloID)
        else:
            sonuc = self.vt.VeriGuncelleSozluk(sozlukID,sozlukadi,tabloID,ID)

        if sonuc == "1":
            self.MesajSozluk(1,"Bilgi","Başarıyla Kaydedildi")
            self.InitUISozluk()
            self.TabloDoldurSozluk()
        else:
            self.Mesaj(2,"Kayıt Hatası",sonuc)
            

    def InitUISozluk(self):
        self.pencere.txtID.setText("")
        self.pencere.txtAd.setText("")
        self.pencere.txtTablo.setText("")