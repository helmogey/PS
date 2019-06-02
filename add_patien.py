import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QApplication, QDialog,QPushButton,QGridLayout, QFormLayout, QGroupBox,
                             QLabel, QLineEdit, QSpinBox,QVBoxLayout)
import sys
import datetime
import pandas as pd
# from final import mainwindow

class Dialog(QDialog):

    def __init__(self,nex_id ,filename, parent=None):
        super(Dialog, self).__init__(parent)
        self.parent= parent
        self.filename = filename
        self.nex_id= nex_id
        self.createFormGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.formGroupBox)
        add_patient_pushbotton = QPushButton("Add New Patient", self)
        cancel = QPushButton("Cancel", self)
        mainLayout.addWidget(add_patient_pushbotton)
        mainLayout.addWidget(cancel)

        add_patient_pushbotton.clicked.connect(self.write_to_csv)

        self.setLayout(mainLayout)

        self.setWindowTitle("Add New Patient")

        # self.load_image()

    def load_image(self):
        self.image = plt.imread("hany.jpg")


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Patient Information")
        layout = QFormLayout()

        self.name_edit_line = QLineEdit()
        self.age_edit_line = QSpinBox()
        self.date_edit_line = QLineEdit()
        self.photo_edit_line = QLineEdit()
        self.dignose_edit_line = QLineEdit()

        currentDT = datetime.datetime.now()
        self.date_edit_line.setText(str(currentDT))

        layout.addRow(QLabel("Name:"), self.name_edit_line)
        layout.addRow(QLabel("Age:"), self.age_edit_line)
        layout.addRow(QLabel("visit Date:"), self.date_edit_line)
        layout.addRow(QLabel("Upload Photo:"), self.photo_edit_line)
        layout.addRow(QLabel("Diagnose:"), self.dignose_edit_line)

        self.formGroupBox.setLayout(layout)

    def write_to_csv(self):

        name = self.name_edit_line.text()
        age = str(self.age_edit_line.value())
        date = self.date_edit_line.text()
        image_name = "data/" + name + "_" + date + ".jpg"
        diag = self.dignose_edit_line.text()

        # print(name, age)
        l2 = [self.nex_id, name, age, date, image_name, diag]

        data = pd.read_csv(self.filename)
        header = list(data)

        l1 = data.values.tolist()
        # print(l2)
        dict = {}
        for i, key in enumerate(header):
            lst = []
            for l in l1:
                lst.append(l[i])
            lst.append(l2[i])
            dict[str(key)] = lst

        df = pd.DataFrame(dict)
        df.to_csv(self.filename, index=False)

        Dialog.close(self)
        self.parent.model.clear()
        self.parent.loadCsv()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog(3,"patient.csv")
    # dialog = Dialog()
    sys.exit(dialog.exec_())

