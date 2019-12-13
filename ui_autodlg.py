# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autodlg.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1018, 581)
        self.label_Image = QtWidgets.QLabel(Dialog)
        self.label_Image.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.label_Image.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.label_Image.setStyleSheet("background-color:rgb(0, 0, 0)")
        self.label_Image.setObjectName("label_Image")
        self.listWidget_infor = QtWidgets.QListWidget(Dialog)
        self.listWidget_infor.setGeometry(QtCore.QRect(810, 20, 201, 192))
        self.listWidget_infor.setObjectName("listWidget_infor")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_Image.setText(_translate("Dialog", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
