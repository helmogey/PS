from PyQt5.QtWidgets import (QApplication, QDialog,QDialogButtonBox, QFormLayout, QGroupBox,
                             QLabel, QLineEdit, QSpinBox,QVBoxLayout)
import sys

class Dialog(QDialog):

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.button(QDialogButtonBox.Ok).setText(self.tr("Add"))
        buttonBox.button(QDialogButtonBox.Cancel).setText(self.tr("Cancel"))

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Add New Patient")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Patient Information")
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), QLineEdit())
        layout.addRow(QLabel("Age:"), QSpinBox())
        layout.addRow(QLabel("visit Date:"), QLineEdit())
        layout.addRow(QLabel("Upload Photo:"), QLineEdit())
        layout.addRow(QLabel("Diagnose:"), QLineEdit())
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()

    sys.exit(dialog.exec_())

