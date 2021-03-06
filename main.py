from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QApplication,QMessageBox, \
    QScrollArea,QTreeView ,QPushButton,QGridLayout,QLabel,QLineEdit, QSpinBox, QWidget
import sys
import datetime
import pandas as pd
from PIL import Image, ImageDraw , ImageFont
from PIL import ImageEnhance
from PIL import Image
import shutil
import os
import matplotlib
matplotlib.use('Qt5Agg')

class mainwindow(QWidget):

    def __init__(self, fileName, parent=None):
        super(mainwindow, self).__init__(parent)

        self.zoom_count = 0
        self.zoom_flag = False

        self.CSV_fileName = fileName
        self.zoom_file_path = "photo_edit/zoom/temp.jpg"

        widget = QWidget()
        self.mainLayout = QGridLayout(widget)
        self.btn_layout = QGridLayout(self)
        self.push_layout = QGridLayout()




        self.Qtree = QTreeView()
        # self.Qtree.setStyleSheet('QTreeView {background-color: purple; color: white; border:5px;'
        #                          'border-style:outset;border-color: white;selection-color: yellow}')
        self.model = QtGui.QStandardItemModel(self)

        self.setWindowTitle("Main")
        self.setFixedSize(700,550)

        self.Qtree.doubleClicked.connect(self.show_details)

        self.add_patient_pushbotton = QPushButton("Add New Patient")
        # self.add_patient_pushbotton.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:5px;border-color: white}')
        self.add_patient_pushbotton.clicked.connect(self.add_patient)
        self.add_patient_pushbotton.setFixedSize(200, 30)



        self.zoom_in_push = QPushButton("Zoom In")
        # self.zoom_in_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.zoom_in_push.clicked.connect(self.zoom)



        self.zoom_out_push = QPushButton("Zoom Out")
        # self.zoom_out_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.zoom_out_push.clicked.connect(self.zoom)



        self.brightness_push = QPushButton("Brightness")
        # self.brightness_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.brightness_push.clicked.connect(self.brightness)


        self.sharpness_push = QPushButton("Sharpness")
        # self.sharpness_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.sharpness_push.clicked.connect(self.sharpness)


        self.color_push = QPushButton("Color")
        # self.color_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.color_push.clicked.connect(self.color)

        self.reset_push = QPushButton("Reset")
        # self.reset_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.reset_push.clicked.connect(self.reset)


        self.close_push = QPushButton("Close")
        # self.close_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.close_push.clicked.connect(self.end)

        self.save_push = QPushButton("Add")
        # self.save_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.save_push.clicked.connect(self.write_to_csv)
        self.save_push.setFixedSize(200, 30)

        self.back_push = QPushButton("Cancel")
        # self.back_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.back_push.clicked.connect(self.loadCsv)
        self.back_push.setFixedSize(200, 30)

        self.back1_push = QPushButton("Back")
        # self.back1_push.setStyleSheet('QPushButton {background-color:yellow;border-style:outset;'
        #                                           'border-width:2px;border-color: white}')
        self.back1_push.clicked.connect(self.loadCsv)
        self.back1_push.setFixedSize(200, 30)

        self.save_push.hide()
        self.back_push.hide()
        self.back1_push.hide()


        self.name_edit_line = QLineEdit()
        self.name_edit_line.setFixedHeight(50)
        self.age_edit_line = QSpinBox()
        self.age_edit_line.setFixedHeight(50)
        self.date_edit_line = QLineEdit()
        self.date_edit_line.setFixedHeight(50)
        self.photo_edit_line = QLineEdit()
        self.photo_edit_line.setFixedHeight(50)
        self.diagnose_edit_line = QLineEdit()
        self.diagnose_edit_line.setFixedHeight(100)
        # self.diagnose_edit_line.setFixedSize(360, 100)

        self.Name_label = QLabel("Name:")
        # self.Name_label.setFixedHeight(20)
        self.Age_label = QLabel("Age:")
        self.Date_label = QLabel("visit Date:")
        self.photo_label = QLabel("Upload Photo:")
        self.diagnose_label = QLabel("Diagnose:")

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

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)

        self.imageLabel = QLabel()


        self.listWidget = QListWidget(self)
        # self.listWidget.setStyleSheet('QListWidget{background-color: purple; color: white; border:5px;'
        #                          'border-style:outset;border-color: white;selection-color: yellow}')
        self.listWidget.itemDoubleClicked.connect(self.image)


        self.listWidget.hide()
        self.Qtree.setModel(self.model)
        self.Qtree.hide()

        self.push_layout.addWidget(self.add_patient_pushbotton,0,0,0,1)
        self.push_layout.addWidget(self.zoom_in_push,0,0)
        self.push_layout.addWidget(self.zoom_out_push,0,1)
        self.push_layout.addWidget(self.brightness_push,0,2)
        self.push_layout.addWidget(self.sharpness_push,0,3)
        self.push_layout.addWidget(self.color_push,0,4)
        self.push_layout.addWidget(self.reset_push,0,5)
        self.push_layout.addWidget(self.close_push,0,6)
        self.push_layout.addWidget(self.save_push, 0, 0)
        self.push_layout.addWidget(self.back_push, 0, 1)
        self.push_layout.addWidget(self.back1_push,0,0)
        self.push_layout.addWidget(self.listWidget,1,0)


        self.btn_layout.addLayout(self.push_layout, 5, 0)
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
        self.btn_layout.addWidget(self.scroll)
        self.btn_layout.addWidget(self.Qtree, 0, 0)


        self.mainLayout.addWidget(self.imageLabel, 0, 0)

        self.scroll.hide()

    def loadCsv(self):
        self.model.clear()
        self.add_patient_pushbotton.show()
        self.back1_push.hide()
        self.listWidget.hide()

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


        r = signal.row() - 1

        if r >= 0:
            self.back1_push.show()

            self.listWidget.clear()
            data = pd.read_csv(self.CSV_fileName)
            data = data.values.tolist()
            self.d = data[r]

            txt = "id is: " + str(self.d[0]) + "\nname is: " + str(self.d[1]) + "\nage is: " + str(
                self.d[2]) + "\nDiagnoses: " + str(
                self.d[5]) \
                  + "\nPress to show the image"

            QListWidgetItem(txt, self.listWidget)

            self.listWidget.setGeometry(1,1,500,200)

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


    def image(self):
        self.scroll.show()
        self.listWidget.close()
        self.back1_push.hide()
        self.fileName_edit = "photo_edit/temp.jpg"
        try:
            image = Image.open(self.d[4])

            image.save("photo_edit/temp.jpg")


            # self.scaleFactor = 0.0
            self.scaleFactor = 1.0

            fileName = self.d[4]
            if fileName:
                image = QtGui.QImage(fileName)
                # print(type(image))

                if image.isNull():
                    QMessageBox.information(self, "Image Viewer",
                                            "Cannot load %s." % fileName)
                    return
                self.qpixmap = QtGui.QPixmap.fromImage(image)
                self.imageLabel.setPixmap(self.qpixmap)

            self.imageLabel.show()

        except:
            # img = np.zeros((500,500,3))
            # image = QtGui.QImage(img, img.shape[1],img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_RGB888)

            img = Image.new('RGB', (700, 600), (0, 0, 0))

            draw = ImageDraw.Draw(img)
            draw.text((200, 200), "No Photo To Display!", fill='rgb(255, 255, 255)',
                      font=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 25))

            img.save(self.fileName_edit)
            img.save(self.d[4])
            img = img.convert("RGBA")
            data = img.tobytes("raw", "RGBA")


            qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_ARGB32)
            pix = QtGui.QPixmap.fromImage(qim)

            self.imageLabel.setPixmap(pix)
            self.imageLabel.show()


        self.add_patient_pushbotton.hide()
        self.zoom_out_push.show()
        self.zoom_in_push.show()
        self.close_push.show()
        self.reset_push.show()
        self.sharpness_push.show()
        self.brightness_push.show()
        self.color_push.show()


    def adjustScrollBar(self, scrollBar, scale):
        scrollBar.setValue(int(scale * scrollBar.value()
                               + ((scale - 1) * scrollBar.pageStep() / 2)))


    def zoom(self):
        if "zoom" not in os.listdir("photo_edit"):
            os.mkdir("photo_edit/zoom")
        sender = self.sender()
        self.zoom_flag = True
        image = Image.open(self.fileName_edit)

        if sender == self.zoom_in_push:
            self.zoom_count += 1
        else:
            self.zoom_count += -1
        scale = 1.2
        scale = (scale)**self.zoom_count
        self.adjustScrollBar(self.scroll.horizontalScrollBar(),scale)
        self.adjustScrollBar(self.scroll.verticalScrollBar(),scale)

        h = int(image.size[1]*scale)
        w = int(image.size[0]*scale)
        image = image.resize((w,h),Image.BICUBIC)
        image.save(self.zoom_file_path)
        self.imageLabel.clear()
        image = QtGui.QImage(self.zoom_file_path)
        self.qpixmap = QtGui.QPixmap.fromImage(image)
        self.imageLabel.setPixmap(self.qpixmap)




    def brightness(self):
        if self.zoom_flag:
            shutil.copy(self.zoom_file_path,self.fileName_edit)
            self.zoom_flag = False
            self.zoom_count = 0

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
        if self.zoom_flag:
            shutil.copy(self.zoom_file_path,self.fileName_edit)
            self.zoom_flag = False
            self.zoom_count = 0

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
        if self.zoom_flag:
            shutil.copy(self.zoom_file_path,self.fileName_edit)
            self.zoom_flag = False
            self.zoom_count = 0

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
        self.zoom_flag = False
        self.zoom_count = 0
        self.imageLabel.clear()
        o_i = QtGui.QImage(self.d[4])
        qpixmap = QtGui.QPixmap.fromImage(o_i)
        self.imageLabel.setPixmap(qpixmap)
        self.imageLabel.adjustSize()
        self.image = Image.open(self.d[4])
        self.image.save("photo_edit/temp.jpg")

    def end(self):
        self.scroll.hide()
        self.imageLabel.close()

        self.loadCsv()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exp=mainwindow("database/patient.csv")
    exp.loadCsv()
    exp.show()
    sys.exit(app.exec_())
