import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QPushButton,QWidget,QGridLayout, QListWidget, QListWidgetItem, \
    QApplication, QDialog,QTableView,QMessageBox, QLabel, QSizePolicy, QMainWindow, QScrollArea
from PyQt5.QtCore import QDir, Qt
import pandas as pd
import numpy as np
from add_patien import Dialog

from PIL import Image
from PIL import ImageEnhance
import glob
import os

class mainwindow(QWidget):

    def __init__(self, fileName , parent=None):
        super(mainwindow, self).__init__(parent)

        self.fileName = fileName

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.setGeometry(10, 50, 680, 425)

        self.setWindowTitle("Main")
        self.setFixedSize(700, 500)

        self.tableView.doubleClicked.connect(self.show_details)

        add_patient_pushbotton = QPushButton("Add New Patient",self)

        mainLayout= QGridLayout()
        mainLayout.setColumnStretch(1, 4)
        mainLayout.setRowStretch(1, 4)
        mainLayout.addWidget(add_patient_pushbotton,0,0)
        self.setLayout(mainLayout)
        add_patient_pushbotton.clicked.connect(self.add_patient)


    def loadCsv(self):
        data = pd.read_csv(self.fileName)
        header = list(data)
        data = data.values.tolist()
        self.next_id = len(data)
        items = [QtGui.QStandardItem(str(l)) for l in header]
        self.model.appendRow(items)
        for lst in data:
            items = [QtGui.QStandardItem(str(l)) for l in lst]
            self.model.appendRow(items)


    def show_details(self,signal):
        r = signal.row() - 1

        if r >= 0:
            data = pd.read_csv(self.fileName)
            data = data.values.tolist()

            d = data[r]
            # print(d)
            ex = Popup(d, self)
            ex.setWindowTitle("Pop")
            ex.show()
            # self.close()

        else:
            pass


    def add_patient(self):
        dialog = Dialog(self.next_id,self.fileName,self)
        dialog.show()






class ImageViewer(QMainWindow):
    def __init__(self,fileName,parent=None):
        super(ImageViewer, self).__init__(parent)

        self.parent = parent

        self.fileName = fileName
        image = Image.open(self.fileName)

        image.save("photo_edit/temp.jpg")
        self.fileName_edit = "photo_edit/temp.jpg"


        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        # self.resize(600, 800)

        zoom_in_push = QPushButton("Zoom In",self)
        zoom_in_push.clicked.connect(self.zoom_in)

        zoom_out_push = QPushButton("Zoom Out",self)
        zoom_out_push.clicked.connect(self.zoom_out)

        brightness_push = QPushButton("Brightness",self)
        brightness_push.clicked.connect(self.brightness)

        sharpness_push = QPushButton("sharpness", self)
        sharpness_push.clicked.connect(self.sharpness)

        color_push = QPushButton("color", self)
        color_push.clicked.connect(self.color)

        reset_push = QPushButton("Reset",self)
        reset_push.clicked.connect(self.reset)

        close_push = QPushButton("Close",self)
        close_push.clicked.connect(self.close)

        mainLayout = QGridLayout()

        # self.addDockWidget()

        mainLayout.addWidget(zoom_out_push,20,20)

        mainLayout.addWidget(zoom_in_push, 20, 20)
        zoom_in_push.move(100,0)

        mainLayout.addWidget(brightness_push,20,20)
        brightness_push.move(200,0)

        mainLayout.addWidget(sharpness_push, 20, 20)
        sharpness_push.move(300, 0)

        mainLayout.addWidget(color_push, 20, 20)
        color_push.move(400, 0)

        mainLayout.addWidget(reset_push,20,20)
        reset_push.move(500,0)

        mainLayout.addWidget(close_push,20,20)
        close_push.move(600,0)

        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return
            self.qpixmap = QtGui.QPixmap.fromImage(image)
            self.imageLabel.setPixmap(self.qpixmap)
            self.scaleFactor = 1.0
            self.imageLabel.adjustSize()


    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())


        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoom_in)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoom_out)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))

    def zoom_in(self):
        self.scaleImage(1.25)

    def zoom_out(self):
        self.scaleImage(0.8)


    def brightness(self):
        image = Image.open(self.fileName_edit)
        enhancer = ImageEnhance.Contrast(image)
        out = enhancer.enhance(1.7)
        out.save(self.fileName_edit)
        out = QtGui.QImage(self.fileName_edit)

        self.imageLabel.clear()
        qpixmap = QtGui.QPixmap.fromImage(out)
        self.imageLabel.setPixmap(qpixmap)
        self.scaleFactor = 1.0
        self.imageLabel.adjustSize()

    def sharpness(self):
        self.image = Image.open(self.fileName_edit)
        enhancer = ImageEnhance.Sharpness(self.image)
        out = enhancer.enhance(1.7)
        out.save(self.fileName_edit)
        out = QtGui.QImage(self.fileName_edit)

        self.imageLabel.clear()
        qpixmap = QtGui.QPixmap.fromImage(out)
        self.imageLabel.setPixmap(qpixmap)
        self.scaleFactor = 1.0
        self.imageLabel.adjustSize()

    def color(self):
        self.image = Image.open(self.fileName_edit)
        enhancer = ImageEnhance.Color(self.image)
        out = enhancer.enhance(1.7)
        out.save(self.fileName_edit)
        out = QtGui.QImage(self.fileName_edit)

        self.imageLabel.clear()
        qpixmap = QtGui.QPixmap.fromImage(out)
        self.imageLabel.setPixmap(qpixmap)
        self.scaleFactor = 1.0
        self.imageLabel.adjustSize()



    def reset(self):
        self.imageLabel.clear()
        o_i = QtGui.QImage(self.fileName)
        qpixmap = QtGui.QPixmap.fromImage(o_i)
        self.imageLabel.setPixmap(qpixmap)
        self.imageLabel.adjustSize()
        self.image = Image.open(self.fileName)
        self.image.save("photo_edit/temp.jpg")

    def close(self):
        self.destroy()

        self.parent.listWidget.itemDoubleClicked.connect(self.parent.image)



class Popup(QDialog):

    def __init__(self,d,parent=None):
        super(Popup, self).__init__(parent)
        self.listWidget = QListWidget(self)
        txt = "id is: " + str(d[0])+ "\nname is: " + str(d[1])+"\nage is: "+str(d[2])+"\nDiagnoses: "+str(d[5])+"\nPress to show the image"
        self.d = d
        QListWidgetItem(txt, self.listWidget)

        self.listWidget.itemDoubleClicked.connect(self.image)

        self.setGeometry(500, 500, 400, 400)
        self.show()


        # self.listWidget.clear()

    def image(self):
        show_image = ImageViewer(self.d[4],self)
        # self.hide()
        # self.listWidget.
        show_image.show()
        self.listWidget.itemDoubleClicked.disconnect(self.image)

        # self.listWidget.disconnect()







if __name__ == "__main__":
    app = QApplication(sys.argv)
    exp=mainwindow("database/patient.csv")
    exp.loadCsv()
    exp.show()
    sys.exit(app.exec_())