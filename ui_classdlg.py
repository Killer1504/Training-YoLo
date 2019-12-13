# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'classdlg.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(256, 271)
        self.lineEdit_Label = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Label.setGeometry(QtCore.QRect(30, 10, 191, 25))
        self.lineEdit_Label.setObjectName("lineEdit_Label")
        self.btn_Cancel = QtWidgets.QPushButton(Dialog)
        self.btn_Cancel.setGeometry(QtCore.QRect(30, 50, 89, 25))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Cancel.setIcon(icon)
        self.btn_Cancel.setObjectName("btn_Cancel")
        self.btn_OK = QtWidgets.QPushButton(Dialog)
        self.btn_OK.setGeometry(QtCore.QRect(130, 50, 91, 25))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icon/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_OK.setIcon(icon1)
        self.btn_OK.setObjectName("btn_OK")
        self.listWidget_label = QtWidgets.QListWidget(Dialog)
        self.listWidget_label.setGeometry(QtCore.QRect(30, 90, 191, 141))
        self.listWidget_label.setObjectName("listWidget_label")
        self.btn_Remove = QtWidgets.QPushButton(Dialog)
        self.btn_Remove.setGeometry(QtCore.QRect(30, 240, 91, 25))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Icon/remove__.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Remove.setIcon(icon2)
        self.btn_Remove.setObjectName("btn_Remove")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Label"))
        self.btn_Cancel.setText(_translate("Dialog", "Cancel"))
        self.btn_OK.setText(_translate("Dialog", "OK"))
        self.btn_Remove.setText(_translate("Dialog", "Remove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
