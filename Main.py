from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction,QWidget, QListWidget, QListWidgetItem, QApplication,QMessageBox, \
    QSizePolicy, QMainWindow, QScrollArea, QVBoxLayout,QHBoxLayout, QTreeView ,QPushButton,QGridLayout,\
    QGroupBox,QLabel,QLineEdit, QSpinBox
import sys
import datetime
import pandas as pd
from PIL import Image
from PIL import ImageEnhance


class mainwindow(QWidget):

    def __init__(self, fileName, parent=None):
        super(mainwindow, self).__init__(parent)

        self.CSV_fileName = fileName

        self.mainLayout = QGridLayout(self)
        self.btn_layout = QGridLayout()


        self.Qtree = QTreeView()

        self.model = QtGui.QStandardItemModel(self)

        self.setWindowTitle("Main")
        self.setFixedSize(700,550)

        self.Qtree.doubleClicked.connect(self.show_details)

        self.add_patient_pushbotton = QPushButton("Add New Patient")
        self.add_patient_pushbotton.clicked.connect(self.add_patient)
        self.add_patient_pushbotton.setFixedSize(200, 30)
        self.btn_layout.addWidget(self.add_patient_pushbotton,0,0)

        self.zoom_in_push = QPushButton("Zoom In")
        self.zoom_in_push.clicked.connect(self.zoom_in)
        self.btn_layout.addWidget(self.zoom_in_push,0,0)

        self.zoom_out_push = QPushButton("Zoom Out")
        self.zoom_out_push.clicked.connect(self.zoom_out)
        self.btn_layout.addWidget(self.zoom_out_push,0,1)

        self.brightness_push = QPushButton("Brightness")
        self.brightness_push.clicked.connect(self.brightness)
        self.btn_layout.addWidget(self.brightness_push,0,2)

        self.sharpness_push = QPushButton("Sharpness")
        self.sharpness_push.clicked.connect(self.sharpness)
        self.btn_layout.addWidget(self.sharpness_push,0,3)

        self.color_push = QPushButton("Color")
        self.color_push.clicked.connect(self.color)
        self.btn_layout.addWidget(self.color_push,0,4)

        self.reset_push = QPushButton("Reset")
        self.reset_push.clicked.connect(self.reset)
        self.btn_layout.addWidget(self.reset_push,0,5)

        self.close_push = QPushButton("Close")
        self.close_push.clicked.connect(self.end)
        self.btn_layout.addWidget(self.close_push,0,6)

        self.save_push = QPushButton("Add")
        self.save_push.clicked.connect(self.write_to_csv)
        self.mainLayout.addWidget(self.save_push, 1, 0)
        self.save_push.setFixedSize(200, 30)

        self.back_push = QPushButton("Cancel")
        self.back_push.clicked.connect(self.loadCsv)
        self.mainLayout.addWidget(self.back_push, 1, 1)
        self.back_push.setFixedSize(200, 30)

        self.save_push.hide()
        self.back_push.hide()

        self.name_edit_line = QLineEdit()
        self.age_edit_line = QSpinBox()
        self.date_edit_line = QLineEdit()
        self.photo_edit_line = QLineEdit()
        self.diagnose_edit_line = QLineEdit()
        # self.diagnose_edit_line.setFixedSize(360, 100)

        self.Name_label = QLabel("Name:")
        self.Age_label = QLabel("Age:")
        self.Date_label = QLabel("visit Date:")
        self.photo_label = QLabel("Upload Photo:")
        self.diagnose_label = QLabel("Diagnose:")

        self.btn_layout.addWidget(self.Name_label,0,0)
        self.btn_layout.addWidget(self.name_edit_line, 0, 1)

        self.btn_layout.addWidget(self.Age_label, 1, 0)
        self.btn_layout.addWidget(self.age_edit_line, 1, 1)

        self.btn_layout.addWidget(self.Date_label, 2, 0)
        self.btn_layout.addWidget(self.date_edit_line, 2, 1)

        self.btn_layout.addWidget(self.photo_label, 3, 0)
        self.btn_layout.addWidget(self.photo_edit_line, 3, 1)

        self.btn_layout.addWidget(self.diagnose_label, 4, 0)
        self.btn_layout.addWidget(self.diagnose_edit_line, 4, 1)


        self.name_edit_line.hide()
        self.Name_label.hide()
        self.Age_label.hide()
        self.age_edit_line.hide()
        self.date_edit_line.hide()
        self.Date_label.hide()
        self.photo_edit_line.hide()
        self.photo_label.hide()
        self.diagnose_label.hide()
        self.diagnose_edit_line.hide()


        self.imageLabel = QLabel()
        self.mainLayout.addWidget(self.imageLabel, 2, 0)


        self.listWidget = QListWidget(self)
        self.listWidget.itemDoubleClicked.connect(self.image)


        self.listWidget.hide()
        self.Qtree.setModel(self.model)
        self.Qtree.hide()
        self.mainLayout.addWidget(self.Qtree,1,0)
        self.mainLayout.addLayout(self.btn_layout, 0, 0)


    def loadCsv(self):
        self.model.clear()
        self.add_patient_pushbotton.show()

        self.name_edit_line.hide()
        self.Name_label.hide()
        self.Age_label.hide()
        self.age_edit_line.hide()
        self.date_edit_line.hide()
        self.Date_label.hide()
        self.photo_edit_line.hide()
        self.photo_label.hide()
        self.diagnose_label.hide()
        self.diagnose_edit_line.hide()
        self.save_push.hide()
        self.back_push.hide()

        self.zoom_out_push.hide()
        self.zoom_in_push.hide()
        self.close_push.hide()
        self.reset_push.hide()
        self.sharpness_push.hide()
        self.brightness_push.hide()
        self.color_push.hide()


        data = pd.read_csv(self.CSV_fileName)
        header = list(data)
        data = data.values.tolist()
        self.next_id = len(data)
        items = [QtGui.QStandardItem(str(l)) for l in header]
        self.model.appendRow(items)
        for lst in data:
            items = [QtGui.QStandardItem(str(l)) for l in lst]
            self.model.appendRow(items)

        self.Qtree.show()


    def show_details(self,signal):
        self.listWidget.clear()

        r = signal.row() - 1

        if r >= 0:
            data = pd.read_csv(self.CSV_fileName)
            data = data.values.tolist()
            d = data[r]

            txt = "id is: " + str(d[0]) + "\nname is: " + str(d[1]) + "\nage is: " + str(d[2]) + "\nDiagnoses: " + str(
                d[5]) \
                  + "\nPress to show the image"

            QListWidgetItem(txt, self.listWidget)

            self.mainLayout.addWidget(self.listWidget)

            self.Qtree.close()
            self.add_patient_pushbotton.hide()
            self.listWidget.show()

        else:
            pass






    def add_patient(self):
        self.Qtree.close()
        self.add_patient_pushbotton.hide()

        self.name_edit_line.clear()
        self.age_edit_line.clear()
        self.date_edit_line.clear()
        self.photo_edit_line.clear()
        self.diagnose_edit_line.clear()

        self.name_edit_line.show()
        self.Name_label.show()
        self.Age_label.show()
        self.age_edit_line.show()
        self.date_edit_line.show()
        self.Date_label.show()
        self.photo_edit_line.show()
        self.photo_label.show()
        self.diagnose_label.show()
        self.diagnose_edit_line.show()
        self.save_push.show()
        self.back_push.show()

        currentDT = datetime.datetime.now()
        self.date_edit_line.setText(str(currentDT))



        # self.formGroupBox = QGroupBox("Patient Information")
        # layout = QFormLayout()
        #
        #
        # self.formGroupBox.setLayout(layout)


    def write_to_csv(self):
        name = self.name_edit_line.text()
        age = str(self.age_edit_line.value())
        date = self.date_edit_line.text()
        image_name = "data/" + name + "_" + date + ".jpg"
        diag = self.diagnose_edit_line.text()

        l2 = [self.next_id, name, age, date, image_name, diag]

        data = pd.read_csv(self.CSV_fileName)
        header = list(data)

        l1 = data.values.tolist()
        dict = {}
        for i, key in enumerate(header):
            lst = []
            for l in l1:
                lst.append(l[i])
            lst.append(l2[i])
            dict[str(key)] = lst

        df = pd.DataFrame(dict)
        df.to_csv(self.CSV_fileName, index=False)

        self.loadCsv()

        # Dialog.close(self)
        # self.parent.model.clear()
        # self.parent.loadCsv()


    def image(self):
        self.listWidget.close()

        try:
            image = Image.open(self.d[4])

            image.save("photo_edit/temp.jpg")
            self.fileName_edit = "photo_edit/temp.jpg"

            self.scaleFactor = 0.0

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

            self.imageLabel.show()

        except:
            print("no photo")


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

        # self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        # self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoom_in)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoom_out)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)


    # def adjustScrollBar(self, scrollBar, factor):
    #     scrollBar.setValue(int(factor * scrollBar.value()
    #                            + ((factor - 1) * scrollBar.pageStep() / 2)))

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

        self.loadCsv()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exp=mainwindow("database/patient.csv")
    exp.loadCsv()
    exp.show()
    sys.exit(app.exec_())