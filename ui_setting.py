# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.lineEdit_thickness = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_thickness.setGeometry(QtCore.QRect(100, 20, 51, 25))
        self.lineEdit_thickness.setObjectName("lineEdit_thickness")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 71, 17))
        self.label.setObjectName("label")
        self.btn_Check = QtWidgets.QPushButton(Dialog)
        self.btn_Check.setGeometry(QtCore.QRect(20, 260, 89, 25))
        self.btn_Check.setObjectName("btn_Check")
        self.btn_Save = QtWidgets.QPushButton(Dialog)
        self.btn_Save.setGeometry(QtCore.QRect(270, 260, 89, 25))
        self.btn_Save.setObjectName("btn_Save")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Setting"))
        self.label.setText(_translate("Dialog", "thickness"))
        self.btn_Check.setText(_translate("Dialog", "Check"))
        self.btn_Save.setText(_translate("Dialog", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
