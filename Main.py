import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QPushButton,QWidget,QGridLayout, QListWidget, QListWidgetItem, \
    QApplication, QDialog,QTableView,QMessageBox, QLabel, QSizePolicy, QMainWindow, QScrollArea, QVBoxLayout, \
    QHBoxLayout
from PyQt5.QtCore import QDir, Qt
import pandas as pd
import numpy as np

from PIL import Image
from PIL import ImageEnhance


class mainwindow(QWidget):

    def __init__(self, fileName, parent=None):
        super(mainwindow, self).__init__(parent)

        self.CSV_fileName = fileName

        self.mainLayout = QVBoxLayout(self)
        self.btn_layout = QHBoxLayout()


        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.setGeometry(10, 50, 680, 425)

        self.setWindowTitle("Main")
        self.setFixedSize(700,550)

        self.tableView.doubleClicked.connect(self.show_details)

        self.add_patient_pushbotton = QPushButton("Add New Patient", self)
        self.add_patient_pushbotton.setFixedSize(200,30)


        self.zoom_in_push = QPushButton("Zoom In")
        self.zoom_in_push.clicked.connect(self.zoom_in)

        self.zoom_out_push = QPushButton("Zoom Out")
        self.zoom_out_push.clicked.connect(self.zoom_out)

        self.brightness_push = QPushButton("Brightness")
        self.brightness_push.clicked.connect(self.brightness)

        self.sharpness_push = QPushButton("Sharpness")
        self.sharpness_push.clicked.connect(self.sharpness)

        self.color_push = QPushButton("Color")
        self.color_push.clicked.connect(self.color)

        self.reset_push = QPushButton("Reset")
        self.reset_push.clicked.connect(self.reset)

        self.close_push = QPushButton("Close")
        self.close_push.clicked.connect(self.end)

        self.imageLabel = QLabel()

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)


        self.listWidget = QListWidget(self)
        self.listWidget.itemDoubleClicked.connect(self.image)

        self.listWidget.hide()

        self.btn_layout.addWidget(self.zoom_in_push)
        self.btn_layout.addWidget(self.zoom_out_push)
        self.btn_layout.addWidget(self.brightness_push)
        self.btn_layout.addWidget(self.sharpness_push)
        self.btn_layout.addWidget(self.color_push)
        self.btn_layout.addWidget(self.reset_push)
        self.btn_layout.addWidget(self.close_push)
        self.btn_layout.addWidget(self.add_patient_pushbotton)

        self.mainLayout.addLayout(self.btn_layout)


    def loadCsv(self):
        self.model.clear()
        self.tableView.show()

        self.zoom_out_push.hide()
        self.zoom_in_push.hide()
        self.close_push.hide()
        self.reset_push.hide()
        self.sharpness_push.hide()
        self.brightness_push.hide()
        self.color_push.hide()

        self.add_patient_pushbotton.clicked.connect(self.add_patient)

        data = pd.read_csv(self.CSV_fileName)
        header = list(data)
        data = data.values.tolist()
        self.next_id = len(data)
        items = [QtGui.QStandardItem(str(l)) for l in header]
        self.model.appendRow(items)
        for lst in data:
            items = [QtGui.QStandardItem(str(l)) for l in lst]
            self.model.appendRow(items)


    def show_details(self,signal):
        self.listWidget.clear()


        r = signal.row() - 1

        if r >= 0:
            data = pd.read_csv(self.CSV_fileName)
            data = data.values.tolist()

            d = data[r]

        else:
            pass

        self.tableView.close()
        self.add_patient_pushbotton.hide()
        self.listWidget.show()

        txt = "id is: " + str(d[0]) + "\nname is: " + str(d[1]) + "\nage is: " + str(d[2]) + "\nDiagnoses: " + str(
            d[5]) + "\nPress to show the image"
        self.d = d


        QListWidgetItem(txt,self.listWidget)

        self.mainLayout.addWidget(self.listWidget)



    def add_patient(self):
        self.destroy()


    def image(self):

        self.listWidget.close()

        image = Image.open(self.d[4])
        image.save("photo_edit/temp.jpg")
        self.fileName_edit = "photo_edit/temp.jpg"

        self.scaleFactor = 0.0

        self.mainLayout.addWidget(self.imageLabel)

        fileName = self.d[4]
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

        # self.imageLabel.setFixedSize(600,550)
        self.imageLabel.show()



        self.add_patient_pushbotton.hide()
        self.zoom_out_push.show()
        self.zoom_in_push.show()
        self.close_push.show()
        self.reset_push.show()
        self.sharpness_push.show()
        self.brightness_push.show()
        self.color_push.show()

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
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

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
        o_i = QtGui.QImage(self.d[4])
        qpixmap = QtGui.QPixmap.fromImage(o_i)
        self.imageLabel.setPixmap(qpixmap)
        self.imageLabel.adjustSize()
        self.image = Image.open(self.d[4])
        self.image.save("photo_edit/temp.jpg")

    def end(self):
        self.imageLabel.close()
        self.add_patient_pushbotton.show()

        self.loadCsv()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exp=mainwindow("database/patient.csv")
    exp.loadCsv()
    exp.show()
    sys.exit(app.exec_())