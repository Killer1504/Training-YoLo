# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hello.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1035, 612)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setGeometry(QtCore.QRect(0, 0, 1041, 571))
        self.mdiArea.setObjectName("mdiArea")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1035, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTool = QtWidgets.QMenu(self.menubar)
        self.menuTool.setObjectName("menuTool")
        self.menuCamera = QtWidgets.QMenu(self.menubar)
        self.menuCamera.setObjectName("menuCamera")
        self.menuUI = QtWidgets.QMenu(self.menubar)
        self.menuUI.setObjectName("menuUI")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionTakeImage = QtWidgets.QAction(MainWindow)
        self.actionTakeImage.setObjectName("actionTakeImage")
        self.actionDetect = QtWidgets.QAction(MainWindow)
        self.actionDetect.setObjectName("actionDetect")
        self.actionAuto = QtWidgets.QAction(MainWindow)
        self.actionAuto.setObjectName("actionAuto")
        self.actionLabel = QtWidgets.QAction(MainWindow)
        self.actionLabel.setObjectName("actionLabel")
        self.actionTraining = QtWidgets.QAction(MainWindow)
        self.actionTraining.setObjectName("actionTraining")
        self.actionCheckSystem = QtWidgets.QAction(MainWindow)
        self.actionCheckSystem.setObjectName("actionCheckSystem")
        self.actionLoadModel = QtWidgets.QAction(MainWindow)
        self.actionLoadModel.setObjectName("actionLoadModel")
        self.actionParameter = QtWidgets.QAction(MainWindow)
        self.actionParameter.setObjectName("actionParameter")
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionLive = QtWidgets.QAction(MainWindow)
        self.actionLive.setObjectName("actionLive")
        self.menuTool.addAction(self.actionTakeImage)
        self.menuTool.addAction(self.actionDetect)
        self.menuTool.addAction(self.actionCheckSystem)
        self.menuTool.addAction(self.actionLoadModel)
        self.menuCamera.addAction(self.actionConnect)
        self.menuCamera.addAction(self.actionDisconnect)
        self.menuCamera.addAction(self.actionLive)
        self.menuUI.addAction(self.actionAuto)
        self.menuUI.addAction(self.actionLabel)
        self.menuUI.addAction(self.actionTraining)
        self.menuSetting.addAction(self.actionParameter)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTool.menuAction())
        self.menubar.addAction(self.menuCamera.menuAction())
        self.menubar.addAction(self.menuUI.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTool.setTitle(_translate("MainWindow", "Tool"))
        self.menuCamera.setTitle(_translate("MainWindow", "Camera"))
        self.menuUI.setTitle(_translate("MainWindow", "UI"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.actionTakeImage.setText(_translate("MainWindow", "TakeImage"))
        self.actionDetect.setText(_translate("MainWindow", "Detect"))
        self.actionAuto.setText(_translate("MainWindow", "Auto"))
        self.actionLabel.setText(_translate("MainWindow", "Label"))
        self.actionTraining.setText(_translate("MainWindow", "Training"))
        self.actionCheckSystem.setText(_translate("MainWindow", "CheckSystem"))
        self.actionLoadModel.setText(_translate("MainWindow", "LoadModel"))
        self.actionParameter.setText(_translate("MainWindow", "Parameter"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.actionLive.setText(_translate("MainWindow", "Live"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
