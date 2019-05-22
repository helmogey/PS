import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtGui , QtCore
from PyQt5.QtWidgets import QPushButton,QWidget,QDialogButtonBox ,QGridLayout, QListWidget, QListWidgetItem,QVBoxLayout, QLabel, QApplication, QDialog,QTableView
import pandas as pd
import numpy as np
from add_patien import Dialog

class mainwindow(QWidget):

    def __init__(self, fileName , parent=None):
        super(mainwindow, self).__init__(parent)

        # print(parent)
        self.fileName = fileName

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.setGeometry(10, 50, 780, 645)

        self.setWindowTitle("Main")
        # self.setFixedSize(700, 500)
        self.tableView.doubleClicked.connect(self.show_details)

        # buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        # buttonBox.button(QDialogButtonBox.Ok).setLayout(self)
        # buttonBox.button(QDialogButtonBox.Ok).setText(self.tr("Add New Patient"))
        # buttonBox.setGeometry(30, 240, 341, 32)

        # self.buttonBox.accepted.connect(self.accept)

        # title = QLabel('Title')
        # grid = QGridLayout()
        # grid.addWidget(title,1, 0)
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

        else:
            pass

        # ex = mainwindow(txt, exp)
        # ex.setWindowTitle("Pop")
        # ex.show()


    def add_patient(self):
        print("we r here")
        dialog = Dialog(self)
        dialog.show()



class Popup(QDialog):

    def __init__(self,d,parent=None):
        super(Popup, self).__init__(parent)
        listWidget = QListWidget(self)
        txt = "id is: " + str(d[0])+ "\nname is: " + str(d[1])+"\nage is: "+str(d[2])+"\nDiagnoses: "+str(d[5])+"\nPress to show the image"
        self.d = d
        QListWidgetItem(txt, listWidget)

        self.setGeometry(500, 500, 400, 400)
        self.show()

        listWidget.itemDoubleClicked.connect(self.image)


    def image(self):

        image_path = self.d[4]

        try:
            img = plt.imread(image_path)
            plt.imshow(img)
            plt.show()

        except IsADirectoryError:
            print("no image found")
            img = np.zeros((512,512,3))
            plt.imshow(img)
            plt.show()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    exp=mainwindow("patient.csv")
    exp.loadCsv()
    exp.show()
    sys.exit(app.exec_())