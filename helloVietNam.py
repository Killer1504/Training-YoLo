import os
import time
import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap, QImageReader, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QEvent, QPoint

from ui_hello import Ui_MainWindow
from Autodlg import AutoDlg
from labelDlg import LabelDlg
from training import TrainingAI
from variable import Variable, Rect
from class_dlg import Class_dlg
from assistant import CommonParameter
from object_detect import ObjectDetection
from settingDlg import SettingDlg
from camera import Camera

import sys
import subprocess as sp
import threading


class HelloVietNam(QMainWindow):
    def __init__(self):
        super(HelloVietNam, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.setWindowIcon(QIcon("Icon/kimsohyun.jpg"))
        self.ui.setupUi(self)
        self.title = "Object Detection"
        self.setWindowTitle(self.title)

        self.p_Var = Variable()
        self.p_Rect = Rect()
        self.p_Detect = ObjectDetection()
        self.p_Para = CommonParameter()
        self.p_Camera = Camera()

        self.m_auto = AutoDlg(self)
        self.m_label = LabelDlg(self)
        self.m_train = TrainingAI(self)
        self.m_class = Class_dlg(self)
        self.m_setting = SettingDlg(self)

        # add other dialog in to mdiAre
        self.ui.mdiArea.addSubWindow(self.m_auto, Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(self.m_label, Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(self.m_train, Qt.FramelessWindowHint)
        self.ui.actionAuto.setCheckable(True)
        self.ui.actionLabel.setCheckable(True)
        self.ui.actionTraining.setCheckable(True)
        self.ui.actionAuto.setChecked(True)
        self.m_auto.showMaximized()

        # process Menu of hello UI
        self.ui.actionTakeImage.triggered.connect(self.processEventMenu)
        self.ui.actionCheckSystem.triggered.connect(self.processEventMenu)
        self.ui.actionDetect.triggered.connect(self.processEventMenu)
        self.ui.actionLoadModel.triggered.connect(self.processEventMenu)
        self.ui.actionParameter.triggered.connect(self.processEventMenu)
        self.ui.actionConnect.triggered.connect(self.processEventMenu)
        self.ui.actionDisconnect.triggered.connect(self.processEventMenu)
        self.ui.actionLive.triggered.connect(self.processEventMenu)

        # Update UI
        self.ui.actionAuto.triggered.connect(self.updateUI)
        self.ui.actionLabel.triggered.connect(self.updateUI)
        self.ui.actionTraining.triggered.connect(self.updateUI)

        # label UI
        self.m_label.ui.listWidget_labels.itemClicked.connect(self.eventLabel_listWidget_labels_itemClicked)
        self.m_label.ui.btn_SaveDir.clicked.connect(self.processEventLabel)
        self.m_label.ui.btn_SaveRect.clicked.connect(self.processEventLabel)
        self.m_label.ui.btn_OpenDir.clicked.connect(self.processEventLabel)
        self.m_label.ui.btn_NextImage.clicked.connect(self.processEventLabel)
        self.m_label.ui.btn_PreImage.clicked.connect(self.processEventLabel)
        self.m_label.ui.label_Img.installEventFilter(self)

        # class Dlg contain label class
        self.m_class.ui.btn_OK.clicked.connect(self.processEventClass)
        self.m_class.ui.btn_Cancel.clicked.connect(self.processEventClass)
        self.m_class.ui.btn_Remove.clicked.connect(self.processEventClass)
        self.m_class.ui.listWidget_label.itemClicked.connect(self.eventListWidget_label_itemClicked)

        # training ui
        self.m_train.ui.btn_Config.clicked.connect(self.processEventTraining)
        self.m_train.ui.btn_convert.clicked.connect(self.processEventTraining)
        self.m_train.ui.btn_make.clicked.connect(self.processEventTraining)
        self.m_train.ui.btn_checkCurrent.clicked.connect(self.processEventTraining)

        # setting ui
        self.m_setting.ui.btn_Save.clicked.connect(self.processEventSetting)
        self.m_setting.ui.btn_Check.clicked.connect(self.processEventSetting)

        # auto dlg
        # cv2.setMouseCallback(self.m_auto.ui.label_Image, onMouse=self.Auto_OnMouse)

    # --------------------------------------------------------------------------------------------
    def processEventMenu(self):
        if self.sender() == self.ui.actionTakeImage:
            self.openImage()
        if self.sender() == self.ui.actionCheckSystem:
            self.Check_System_GPU()
        if self.sender() == self.ui.actionDetect:
            self.ActionDetect()
        if self.sender() == self.ui.actionLoadModel:
            self.ActionLoadModel()
        if self.sender() == self.ui.actionParameter:
            self.ActionParameter()
        if self.sender() == self.ui.actionConnect:
            self.ActionConnect()
        if self.sender() == self.ui.actionDisconnect:
            self.ActionDisconnect()
        if self.sender() == self.ui.actionLive:
            self.ActionLive()

    def processEventClass(self):
        if self.sender() == self.m_class.ui.btn_OK:
            self.ClassDlg_btnOK(-1)
        if self.sender() == self.m_class.ui.btn_Cancel:
            self.ClassDlg_btnCancel()
        if self.sender() == self.m_class.ui.btn_Remove:
            self.ClassDlg_btnRemove()
        pass

    def processEventLabel(self):
        if self.sender() == self.m_label.ui.btn_SaveRect:
            self.Label_btnSaveRect()
        if self.sender() == self.m_label.ui.btn_OpenDir:
            self.Label_btnOpenDir()
        if self.sender() == self.m_label.ui.btn_NextImage:
            self.Label_btnNextImage()
        if self.sender() == self.m_label.ui.btn_PreImage:
            self.Label_btnPreImage()
        if self.sender() == self.m_label.ui.btn_SaveDir:
            self.Label_btnSaveDir()
        pass

    def processEventTraining(self):
        if self.sender() == self.m_train.ui.btn_Config:
            self.Train_btnConfig()
        if self.sender() == self.m_train.ui.btn_make:
            self.train_btn_make()
        if self.sender() == self.m_train.ui.btn_checkCurrent:
            self.Train_btnCheckCurrent()
        if self.sender() == self.m_train.ui.btn_convert:
            self.Train_btnConvert()

    def processEventSetting(self):
        if self.sender() == self.m_setting.ui.btn_Save:
            self.Setting_btnSave()
        if self.sender() == self.m_setting.ui.btn_Check:
            self.Setting_btnCheck()

    # --------------------------------------------------------------------------------------------------
    def updateUI(self):
        if self.sender() == self.ui.actionAuto:
            self.ui.actionAuto.setChecked(True)
            self.ui.actionLabel.setChecked(False)
            self.ui.actionTraining.setChecked(False)
            self.m_auto.showMaximized()
        if self.sender() == self.ui.actionLabel:
            self.ui.actionAuto.setChecked(False)
            self.ui.actionLabel.setChecked(True)
            self.ui.actionTraining.setChecked(False)
            self.m_label.showMaximized()
        if self.sender() == self.ui.actionTraining:
            self.ui.actionAuto.setChecked(False)
            self.ui.actionLabel.setChecked(False)
            self.ui.actionTraining.setChecked(True)
            self.m_train.showMaximized()
        pass

    # ----------------------------Auto dlg ------------------------------------------------------------

    def Auto_OnMouse(self, event, x, y, flags, param):
        if event.type() == cv2.EVENT_LBUTTONDOWN:
            print("Left click")
        if event.type() == cv2.EVENT_RBUTTONDOWN:
            print("Right click")
        pass

    # ---------------------------Setting dlg ----------------------------------------------------------
    def Setting_btnSave(self):
        str_thickness = self.m_setting.ui.lineEdit_thickness.text()
        if str_thickness == "":
            return
        thickness = int(str_thickness)
        self.p_Para.para_dict['thickness'] = thickness
        self.p_Para.savePara()
        self.p_Para.__init__()
        self.p_Var.information = QMessageBox()
        self.p_Var.information = QMessageBox.information(self, "Vision Information", "Saved!!!")
        pass

    def Setting_btnCheck(self):
        thickness = self.p_Para.para_dict['thickness']
        self.m_setting.ui.lineEdit_thickness.setText(thickness.__str__())
        pass

    # ---------------------------Training UI ----------------------------------------------------------

    def Train_btnConvert(self):
        cmd1 = "dos2unix train.txt"
        cmd2 = "dos2unix val.txt"
        cmd3 = "dos2unix cfg/yolov3.cfg"
        try:
            buffer = os.getcwd() + "/darknet/"
            self.m_train.ui.listWidget_training.addItem(cmd1)
            result = sp.Popen(cmd1, stdout=sp.PIPE, shell=True, cwd=buffer)
            (output, err) = result.communicate()
            # output = "output= " + output.decode()
            # self.m_train.ui.listWidget_training.addItem(output)

            cmd = cmd2
            self.m_train.ui.listWidget_training.addItem(cmd)
            result = sp.Popen(cmd, stdout=sp.PIPE, shell=True, cwd=buffer)
            (output, err) = result.communicate()

            cmd = cmd3
            self.m_train.ui.listWidget_training.addItem(cmd)
            result = sp.Popen(cmd, stdout=sp.PIPE, shell=True, cwd=buffer)
            (output, err) = result.communicate()
            self.m_train.ui.listWidget_training.addItem("Convert Done!!!")
            del buffer, result, output, err
        except:
            self.m_train.ui.listWidget_training.addItem("Cannot convert to unix, or wrong code")
        del cmd, cmd1, cmd2, cmd3
        return

    def Train_btnCheckCurrent(self):
        # check file yolov3.cfg
        buffer = os.getcwd() + self.p_Var.dir_darknet_cfg
        f_cfg = open(buffer, "r")
        buffer_lst = f_cfg.readlines()
        f_cfg.close()

        n_batch = buffer_lst[5].split("=")[-1].split("\n")[0]
        n_subdivision = buffer_lst[6].split("=")[-1].split("\n")[0]
        n_learning_rate = buffer_lst[17].split("=")[-1].split("\n")[0]
        n_max_batch = buffer_lst[19].split("=")[-1].split(" ")[-1].split("\n")[0]
        n_classes1 = buffer_lst[609].split("=")[-1].split("\n")[0]
        n_classes2 = buffer_lst[695].split("=")[-1].split("\n")[0]
        n_classes3 = buffer_lst[782].split("=")[-1].split("\n")[0]

        self.m_train.ui.lineEdit_batch.setText(str(n_batch))
        self.m_train.ui.lineEdit_subdivision.setText(str(n_subdivision))
        self.m_train.ui.lineEdit_learnRate.setText(str(n_learning_rate))
        self.m_train.ui.lineEdit_max_batches.setText(str(n_max_batch))
        if n_classes1 == n_classes2 == n_classes3:
            self.m_train.ui.lineEdit_classes.setText(str(n_classes1))
        else:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information",
                                                          "Wrong format classes yolov3.cfg file")
            return
        n_filter1 = buffer_lst[602].split("=")[-1].split("\n")[0]
        n_filter2 = buffer_lst[775].split("=")[-1].split("\n")[0]
        n_filter3 = buffer_lst[688].split("=")[-1].split("\n")[0]
        if n_filter1 == n_filter2 == n_filter3:
            self.m_train.ui.lineEdit_filter.setText(str(n_filter1))
        else:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information",
                                                          "Wrong format filters yolov3.cfg file")

        # check file yolo.names
        self.m_train.ui.listWidget_yoloNames.clear()
        buffer = os.getcwd() + self.p_Var.dir_darknet_yolonames
        f_names = open(buffer, "r")
        buffer_lst = []
        buffer_lst = f_names.readlines()
        f_names.close()
        if len(buffer_lst) > 0:
            for name in buffer_lst:
                name = name.split("\n")[0]
                self.m_train.ui.listWidget_yoloNames.addItem(name)
        else:
            pass

        # check file yolo.data
        self.m_train.ui.listWidget_yolodata.clear()
        buffer = os.getcwd() + self.p_Var.dir_darknet_yolodata
        f_data = open(buffer, "r")
        buffer_lst = []
        buffer_lst = f_data.readlines()
        f_data.close()
        for data in buffer_lst:
            data = data.split('\n')[0]
            self.m_train.ui.listWidget_yolodata.addItem(data)

        self.m_train.ui.listWidget_training.addItem("Check done!!!")

        del buffer, buffer_lst, n_batch, n_classes1, n_classes2, n_classes3
        del n_filter1, n_filter2, n_filter3, n_max_batch, n_learning_rate
        pass

    def train_btn_make(self):
        cmd = "Open folder " + os.getcwd() + "/darknet/ " + "and make, train in terminal."
        self.m_train.ui.listWidget_training.addItem(cmd)
        del cmd

    def threadExecuteCmd(self):
        time.sleep(1)
        while self.p_Var.isThreadTrain:
            line = self.p_Var.p_cmd.stdout.readline()
            self.p_Var.lock.acquire()
            self.p_Var.output_cmd = line.decode()
            self.p_Var.lock.release()
            if not line:
                break
            else:
                # pass
                print(self.p_Var.output_cmd)
                # print(line)

            pass
        pass

    def threadUpdateTrainingUI(self):
        time.sleep(1)
        while self.p_Var.isThreadUpdateUiTrain:
            self.p_Var.lock.acquire()
            if len(self.p_Var.output_cmd) > 0:
                self.m_train.ui.listWidget_training.addItem(self.p_Var.output_cmd)
                self.p_Var.output_cmd = ""
                self.p_Var.lock.release()
            else:
                pass
            time.sleep(1)
        pass

    def Train_btnConfig(self):
        k = 0
        k_class = 0
        k_class = len(self.p_Var.listClassLabel)
        if k_class <= 0:
            print("len label < 0")
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information",
                                                          "Empty label")
            return
        for i in self.p_Var.listClassLabel:
            self.m_train.ui.listWidget_training.addItem(i)
        # create  (yolo.names)
        # self.m_train.ui.listWidget_training.addItem("Creating yolo.names ")
        buffer = os.getcwd() + self.p_Var.dir_darknet_yolonames
        f_yolo_name = open(buffer, "w+")
        for i in range(0, k_class):
            if i < k_class - 1:
                str_buffer = self.p_Var.listClassLabel[i] + '\n'
                f_yolo_name.write(str_buffer)
            else:
                str_buffer = self.p_Var.listClassLabel[i]
                f_yolo_name.write(str_buffer)
        f_yolo_name.close()
        # self.m_train.ui.listWidget_training.addItem("Created yolo.names ")

        # create yolo.data
        # self.m_train.ui.listWidget_training.addItem("Creating yolo.data ")
        str_class = "classses = " + str(k_class)
        str_data = '\ntrain = train.txt\nvalid = val.txt\nnames = yolo.names\nbackup = backup'
        buffer = os.getcwd() + self.p_Var.dir_darknet_yolodata
        f_yolodata = open(buffer, "w+")
        data = str_class + str_data
        f_yolodata.write(data)
        f_yolodata.close()
        # self.m_train.ui.listWidget_training.addItem("Created yolo.names ")
        # create train.txt
        # self.m_train.ui.listWidget_training.addItem("Creating train.txt")
        buffer = os.getcwd() + self.p_Var.dir_darknet_traintxt
        f_train = open(buffer, "w+")
        k = len(self.p_Var.listImage)
        print("len image =%d" % k)
        if k <= 0:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information",
                                                          "Empty image")
            print("len image < 0")
            return
        for i in range(0, k):
            buffer_str = self.p_Var.listImage[i] + '\n'
            # print(buffer_str)
            f_train.write(buffer_str)
            # time.sleep(0.05)
        f_train.close()
        # self.m_train.ui.listWidget_training.addItem("Created train.txt ")

        # create val.txt
        # self.m_train.ui.listWidget_training.addItem("Creating val.txt")
        buffer = os.getcwd() + self.p_Var.dir_darknet_valtxt
        f_val = open(buffer, "w+")
        k = len(self.p_Var.listImage)
        for i in range(0, k):
            buffer_str = self.p_Var.listImage[i] + '\n'
            f_val.write(buffer_str)
            # time.sleep(0.05)
        f_val.close()
        # self.m_train.ui.listWidget_training.addItem("Created val.txt ")

        # create yolov3.cfg
        # self.m_train.ui.listWidget_training.addItem("Creating yolov3.cfg")
        buffer = os.getcwd() + self.p_Var.dir_darknet_cfg
        f_cfg = open(buffer, "r")
        buffer_lst = f_cfg.readlines()
        f_cfg.close()
        if len(buffer_lst) < 700:
            print("wrong file cfg")
            return
        if buffer_lst[609] == buffer_lst[695] == buffer_lst[782] and \
                buffer_lst[602] == buffer_lst[775] == buffer_lst[688]:
            f_cfg = open(buffer, "w")

            buffer_lst[609] = buffer_lst[695] = buffer_lst[782] = "classes=" + str(k_class) + '\n'
            buffer_lst[602] = buffer_lst[775] = buffer_lst[688] = "filters=" + str((k_class + 5) * 3) + '\n'
            n_batch = self.m_train.ui.lineEdit_batch.text()
            buffer_lst[5] = "batch=" + n_batch + '\n'
            n_subdivision = self.m_train.ui.lineEdit_subdivision.text()
            buffer_lst[6] = "subdivisions=" + n_subdivision + '\n'
            n_learning_rate = self.m_train.ui.lineEdit_learnRate.text()
            buffer_lst[17] = "learning_rate=" + n_learning_rate + '\n'
            n_max_batch = self.m_train.ui.lineEdit_max_batches.text()
            buffer_lst[19] = "max_batches =" + n_max_batch + "\n"

            for i in buffer_lst:
                f_cfg.write(i)
            f_cfg.close()
            # self.m_train.ui.listWidget_training.addItem("Created yolov3.cfg")
        else:
            self.m_train.ui.listWidget_training.addItem("wrong yolov3.cfg file")
        self.m_train.ui.listWidget_training.addItem("Config done")

    # ---------------------------classDlg---------------------------------------------------------------
    def eventListWidget_label_itemClicked(self):
        # click every labels class
        self.m_class.ui.lineEdit_Label.clear()
        buffer_item = self.m_class.ui.listWidget_label.currentItem().text()
        self.m_class.ui.lineEdit_Label.setText(buffer_item)
        pass

    def SaveFormat_YOLO(self, num_class):
        # add format yolo to listWidgets_labels
        if num_class < 0:
            return
        else:
            pass
        rate_buffer = self.m_label.ui.label_Yolo.text()
        text_format = str(num_class) + " " + rate_buffer
        self.m_label.ui.listWidget_labels.addItem(text_format)
        pass

    def ClassDlg_btnOK(self, num_class):
        # take text form lineEdit label
        buffer_class = self.m_class.ui.lineEdit_Label.text()
        if buffer_class == "":
            return
        else:
            pass
        if len(self.p_Var.listClassLabel) == 0:
            # check if empty label
            self.p_Var.listClassLabel.append(buffer_class)
            # class 0
            num_class = 0
        else:
            # check input line edit none or same label before
            check = False
            for i in range(0, len(self.p_Var.listClassLabel)):
                if self.p_Var.listClassLabel[i] != buffer_class:
                    pass
                else:
                    # same class
                    num_class = i
                    check = True
            if not check:
                k = len(buffer_class)
                if k > 0:
                    # check if label class is empty
                    self.p_Var.listClassLabel.append(buffer_class)
                    num_class = len(self.p_Var.listClassLabel) - 1
                else:
                    pass
            else:
                pass
            pass

        if len(self.p_Var.listClassLabel) > 0:
            self.m_class.ui.listWidget_label.clear()
            for i in self.p_Var.listClassLabel:
                k = len(i)
                if k > 0:
                    self.m_class.ui.listWidget_label.addItem(i)
                else:
                    pass
            # add format YOLO
            self.SaveFormat_YOLO(num_class)
        else:
            pass
        time.sleep(0.1)
        self.m_class.hide()
        pass

    def ClassDlg_btnCancel(self):
        self.m_class.hide()
        pass

    def ClassDlg_btnRemove(self):
        try:
            idx = self.m_class.ui.listWidget_label.currentRow()
            self.m_class.ui.listWidget_label.takeItem(idx)
            self.m_class.ui.lineEdit_Label.setText("")
            del self.p_Var.listClassLabel[idx]
        except:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information",
                                                          "Can't delete label")
            pass

    # ------------------------------------------LabelDlg------------------------------------------------
    def convert_Ratio(self, r):
        r[0] = int(r[0] * self.p_Var.ratio_x)
        r[1] = int(r[1] * self.p_Var.ratio_y)
        r[2] = int(r[2] * self.p_Var.ratio_x)
        r[3] = int(r[3] * self.p_Var.ratio_y)
        return r

    def format_YOLOV3(self, rect_yolov3):
        x_center = (rect_yolov3[0] + rect_yolov3[2] / 2) / self.p_Var.currentImg.shape[1]
        x_center = round(x_center, 8)
        y_center = (rect_yolov3[1] + rect_yolov3[3] / 2) / self.p_Var.currentImg.shape[0]
        y_center = round(y_center, 8)
        rate_width = abs(rect_yolov3[2]) / self.p_Var.currentImg.shape[1]
        rate_width = round(rate_width, 8)
        rate_height = abs(rect_yolov3[3]) / self.p_Var.currentImg.shape[0]
        rate_height = round(rate_height, 8)
        self.m_label.ui.label_Yolo.setText("%.6f %.6f %.6f %.6f" % (x_center, y_center, rate_width, rate_height))
        pass

    def eventFilter(self, q_object, event):
        if event.type() == QEvent.MouseButtonPress:
            self.p_Rect.x, self.p_Rect.y = event.x(), event.y()
            pass
        if event.type() == QEvent.MouseMove:
            self.p_Rect.width = event.x() - self.p_Rect.x
            self.p_Rect.height = event.y() - self.p_Rect.y

            r = [self.p_Rect.x, self.p_Rect.y, self.p_Rect.width, self.p_Rect.height]
            # r = p_as.convert_Ratio(r)
            r = self.convert_Ratio(r)
            x, y, w, h = int(r[0]), int(r[1]), int(r[2]), int(r[3])
            try:
                if len(self.p_Var.currentImg.shape) <= 2:
                    self.p_Var.currentImg_show = cv2.cvtColor(self.p_Var.currentImg, cv2.COLOR_GRAY2BGR)
                    pass
                else:
                    self.p_Var.currentImg_show = self.p_Var.currentImg.copy()
                # result_image = self.p_Var.currentImg_show.copy()
                cv2.rectangle(self.p_Var.currentImg_show, (x, y), (x + w, y + h), (0, 255, 0), self.p_Para.thickness)
                # blur image in rectangle
                # if w > 0 and h > 0:
                #     sub_rect = self.p_Var.currentImg_show[y:y+h, x:x+w]
                #     sub_rect = cv2.blur(sub_rect, (3, 3))
                # if sub_rect is not None:
                #     result_image[y:y+sub_rect.shape[0], x:x+sub_rect.shape[1]] = sub_rect
                self.showImage(self.m_label.ui.label_Img, self.p_Var.currentImg_show)
                self.m_label.ui.label_Posittion.setText("x:%d y:%d w:%d h:%d" % (x, y, w, h))
                r_buffer = [x, y, w, h]
                self.format_YOLOV3(r_buffer)
            except:
                self.p_Var.information = QMessageBox()
                self.p_Var.information = QMessageBox.critical(self, "Vision Information",
                                                              "Can't draw rectangle")
                pass
            pass
        if event.type() == QEvent.MouseButtonRelease:
            p1 = self.m_label.ui.label_Img.pos()
            # current position application
            p2 = self.pos()
            p_x, p_y = event.x() + p1.x() + p2.x(), event.y() + p1.y() + p2.y()
            self.m_class.setGeometry(QtCore.QRect(p_x, p_y, 256, 271))
            self.m_class.show()
            pass
        return QMainWindow.eventFilter(self, q_object, event)

    def eventLabel_listWidget_labels_itemClicked(self):
        buffer_item = self.m_label.ui.listWidget_labels.currentItem().text()
        self.p_Var.currentImg_show = self.p_Var.currentImg.copy()
        if len(buffer_item) > 0:
            list_buffer_item = buffer_item.split(" ")
            x1, y1, x2, y2 = self.findRectangle(list_buffer_item)
            cv2.rectangle(self.p_Var.currentImg_show, (x1, y1), (x2, y2), (255, 0, 0), 2)
            self.showImage(self.m_label.ui.label_Img, self.p_Var.currentImg_show)
        pass

    def findRectangle(self, list_ratio):
        if type(list_ratio) != type([]):
            return 0, 0, 0, 0
        if len(list_ratio) != 5:
            return 0, 0, 0, 0
        m1, m2, m3, m4 = float(list_ratio[1]), float(list_ratio[2]), float(list_ratio[3]), float(list_ratio[4])
        x1 = self.p_Var.currentImg.shape[1] * (m1 - m3 / 2)
        y1 = self.p_Var.currentImg.shape[0] * (m2 - m4 / 2)
        x2 = self.p_Var.currentImg.shape[1] * (m1 + m3 / 2)
        y2 = self.p_Var.currentImg.shape[0] * (m2 + m4 / 2)
        return int(x1), int(y1), int(x2), int(y2)

    def Label_btnSaveRect(self):
        # save format yolo
        if self.p_Var.DirLabel is None:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information",
                                                          "You need choose directory to save label, bro!")
            return

        # take format yolo from listwidgest labels
        self.p_Var.current_listClassLabel = []
        items = []
        for index in range(self.m_label.ui.listWidget_labels.count()):
            items.append(self.m_label.ui.listWidget_labels.item(index))
        self.p_Var.current_listClassLabel = [i.text() for i in items]

        # findNameLabel
        name_label, _ = self.findName_Label_toSave(".txt")
        dir_name_label = self.p_Var.DirLabel + "/" + name_label
        f = open(dir_name_label, "w+")
        for i in range(0, len(self.p_Var.current_listClassLabel)):
            if i < len(self.p_Var.current_listClassLabel):
                f.write(self.p_Var.current_listClassLabel[i] + '\n')
            else:
                f.write(self.p_Var.current_listClassLabel[i])
        f.close()
        self.m_label.ui.btn_SaveRect.setEnabled(False)
        self.p_Var.isSaveLabel = True
        pass

    def findName_Label_toSave(self, extension):
        # find Name image current
        if not self.p_Var.listImage:
            return False, False
        name_current_image = self.p_Var.listImage[self.p_Var.idxCurrentImg]
        list_name = name_current_image.split('/')
        name_image = list_name[-1]
        name_image_list = name_image.split(".")
        name_label = name_image_list[0] + extension
        return name_label, name_image

    def Label_load_formatYOLO_before(self):
        self.m_label.ui.listWidget_labels.clear()
        # load label if it's saved
        name_label, name_image = self.findName_Label_toSave(".txt")
        if not name_label or not name_image:
            return
        dir_label_current = self.p_Var.DirLabel + '/' + name_label
        try:
            f = open(dir_label_current, "r")
            list_format_yolo_str = f.read()
            if list_format_yolo_str:
                list_format_yolo_list = list_format_yolo_str.split('\n')
                str_empty = ""
                for j in list_format_yolo_list:
                    if j == str_empty:
                        del j
                    else:
                        pass
                for i in list_format_yolo_list:
                    if i != str_empty:
                        self.m_label.ui.listWidget_labels.addItem(i)
                self.p_Var.isSaveLabel = True
                pass
            else:
                pass
        except:
            pass
        pass

    def Label_btnNextImage(self):
        if not self.p_Var.isSaveLabel:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information", "You need to save labels, bro")
            self.m_label.ui.btn_SaveRect.setEnabled(True)
            return
        else:
            self.p_Var.isSaveLabel = False
            pass
        self.m_label.ui.btn_SaveRect.setEnabled(True)
        self.m_label.ui.progressBar_Image.setValue(self.p_Var.idxCurrentImg + 1)

        if self.p_Var.idxCurrentImg + 1 >= len(self.p_Var.listImage):
            pass
        else:
            self.p_Var.idxCurrentImg = self.p_Var.idxCurrentImg + 1
            self.Label_load_formatYOLO_before()
            self.p_Var.currentImg = cv2.imread(self.p_Var.listImage[self.p_Var.idxCurrentImg])
            _, self.p_Var.nameImageCurrent = self.findName_Label_toSave(".txt")
            self.showImage(self.m_label.ui.label_Img, self.p_Var.currentImg)
            self.m_label.ui.label_currentImage.setText(self.p_Var.listImage[self.p_Var.idxCurrentImg])
        pass

    def Label_btnPreImage(self):
        self.m_label.ui.btn_SaveRect.setEnabled(True)
        self.m_label.ui.progressBar_Image.setValue(self.p_Var.idxCurrentImg + 1)

        if self.p_Var.idxCurrentImg - 1 < 0:
            pass
        else:
            self.p_Var.idxCurrentImg = self.p_Var.idxCurrentImg - 1
            self.Label_load_formatYOLO_before()
            self.p_Var.currentImg = cv2.imread(self.p_Var.listImage[self.p_Var.idxCurrentImg])
            _, self.p_Var.nameImageCurrent = self.findName_Label_toSave(".txt")
            self.showImage(self.m_label.ui.label_Img, self.p_Var.currentImg)
            self.m_label.ui.label_currentImage.setText(self.p_Var.listImage[self.p_Var.idxCurrentImg])
        pass

    def Label_btnSaveDir(self):
        if self.p_Var.DirLabel:
            # directory labels already exists
            reply = QMessageBox.question(self, "Vision Information",
                                         "You saved directory labels, do you want to change?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
            else:
                pass
        else:
            # directory is empty
            pass
        self.p_Var.DirLabel = str(
            QFileDialog.getExistingDirectory(self, "Choose Directory to save label"))
        self.m_label.ui.label_dirLabel.setText(self.p_Var.DirLabel)
        pass

    def Label_btnOpenDir(self):
        self.p_Var.DirImage = str(
            QFileDialog.getExistingDirectory(self, "Open Directory Image"))
        self.m_label.ui.label_dirImage.setText(self.p_Var.DirImage)
        self.p_Var.listImage = []
        self.p_Var.listImage = self.scanAllImages(self.p_Var.DirImage)
        num_img = len(self.p_Var.listImage)
        self.m_label.ui.label_totalImage.setText(" %d image" % num_img)
        del num_img
        if len(self.p_Var.listImage) > 0:
            self.p_Var.listImage.sort()
            file_path = self.p_Var.listImage[self.p_Var.idxCurrentImg]
            self.p_Var.currentImg = cv2.imread(file_path)
            self.showImage(self.m_label.ui.label_Img, self.p_Var.currentImg)
            _, self.p_Var.nameImageCurrent = self.findName_Label_toSave(".txt")
            self.m_label.ui.label_currentImage.setText(file_path)
            # progress bar
            self.m_label.ui.progressBar_Image.setMaximum(len(self.p_Var.listImage))
            self.m_label.ui.progressBar_Image.setValue(self.p_Var.idxCurrentImg + 1)
        else:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information", "No image from Directory")
            self.m_label.ui.label_currentImage.setText("No Image")
            pass
        # print(self.p_Var.listImage)
        pass

    def scanAllImages(self, folder_path):
        extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        images = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relative_path = os.path.join(root, file)
                    path = os.path.abspath(relative_path)
                    images.append(path)
        return images

    # -----------------------------------------Hello----------------------------------------------------
    def ActionLive(self):
        if not self.p_Camera.isOpen:
            self.m_auto.ui.listWidget_infor.addItem("Camera not open")
            return
        if self.ui.actionLive.text() == "Live":
            # live camera
            self.ui.actionLive.setText("Stop")
            self.ui.actionConnect.setEnabled(False)
            self.ui.actionDisconnect.setEnabled(False)
            self.ui.actionTakeImage.setEnabled(False)
            self.p_Var.isLive = True
            thread1 = threading.Thread(target=self.threadOnLiveCamera, args=())
            thread1.start()
            return
        if self.ui.actionLive.text() == "Stop":
            # stop camera
            self.p_Var.isLive = False
            self.ui.actionConnect.setEnabled(True)
            self.ui.actionDisconnect.setEnabled(True)
            self.ui.actionTakeImage.setEnabled(True)
            self.ui.actionLive.setText("Live")
            return

    def threadOnLiveCamera(self):
        while self.p_Var.isLive:
            self.p_Var.img_Origin = self.p_Camera.OnTakeImage()
            # if self.p_Var.isLoadModel:
            #     class_id, _, boxes = self.p_Detect.detect(img_buffer, img_buffer.shape[1], img_buffer.shape[0])
            #     k = len(class_id)
            #     if k > 0:
            #         for i in range(0, k):
            #             # label = str(self.p_Detect.classes[class_id[i]])
            #             x = int(boxes[i][0])
            #             y = int(boxes[i][1])
            #             w = int(boxes[i][2])
            #             h = int(boxes[i][3])
            #             cv2.rectangle(img_buffer, (x, y), (x + w, y + h), (0, 255, 0), self.p_Para.thickness)
            self.showImage(self.m_auto.ui.label_Image, self.p_Var.img_Origin)
        pass

    def ActionConnect(self):
        if not self.p_Camera.isOpen:
            self.p_Camera.OnConnect()
        pass

    def ActionDisconnect(self):
        if self.p_Camera.isOpen:
            self.p_Camera.OnDisconnect()
        pass

    def ActionParameter(self):
        self.m_setting.show()
        pass

    def ActionLoadModel(self):
        self.p_Var.isLoadModel = self.p_Detect.loadSystem()
        if not self.p_Var.isLoadModel:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information", "Can't load model")
        pass

    def ActionDetect(self):
        count = self.m_auto.ui.listWidget_infor.count()
        if count > 10:
            self.m_auto.ui.listWidget_infor.clear()
        if not self.p_Var.isLoadModel:
            self.p_Var.information = QMessageBox()
            self.p_Var.information = QMessageBox.critical(self, "Vision Information", "You need to load model")
            return
        start = time.time()
        if type(self.p_Var.img_Origin) != type(np.zeros((1, 1))):
            return
        self.p_Var.img_ShowResult = self.p_Var.img_Origin.copy()
        width = self.p_Var.img_ShowResult.shape[1]
        height = self.p_Var.img_ShowResult.shape[0]
        class_id, confidences, boxes = self.p_Detect.detect(self.p_Var.img_ShowResult, width=width, height=height)
        delta_time = round(time.time() - start, 4)
        k = 0
        k = len(class_id)
        if k > 0:
            for i in range(0, k):
                label = str(self.p_Detect.classes[class_id[i]])
                buffer = label + "_" + str(round(float(confidences[i]), 2)) + "_" + delta_time.__str__() + "_s"
                self.m_auto.ui.listWidget_infor.addItem(buffer)
                x = int(boxes[i][0])
                y = int(boxes[i][1])
                w = int(boxes[i][2])
                h = int(boxes[i][3])
                cv2.rectangle(self.p_Var.img_ShowResult, (x, y), (x + w, y + h), (0, 255, 0), self.p_Para.thickness)
                del x, y, w, h, label, buffer
        else:
            self.m_auto.ui.listWidget_infor.addItem("Model can't detect object")
        self.showImage(self.m_auto.ui.label_Image, self.p_Var.img_ShowResult)
        del k, start, width, height, class_id, confidences, boxes
        pass

    def Check_System_GPU(self):
        cmd = "lspci | grep VGA"
        result = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
        (output, _) = result.communicate()
        output = output.decode()
        self.p_Var.information = QMessageBox()
        self.p_Var.information = QMessageBox.information(self, "GPU Information", output)
        del cmd, result, output

    def openFileNameDialogImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image file (*.jpg *.png *.bmp *.jpeg);;All file (*)", options=options)
        return file_name

    def saveFileDialogImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, extension = QFileDialog.getSaveFileName(
            self, "Save Image", "", "JPG (*.jpg);;BMP (*.bmp);;All file (*)", options=options)
        return file_name, extension

    def openImage(self):
        if self.p_Camera.isOpen:
            try:
                start = time.time()
                img = self.p_Camera.OnTakeImage()
                delta_time = round(time.time() - start, 4)
                self.m_auto.ui.listWidget_infor.addItem(delta_time.__str__() + "_s")
                self.p_Var.img_Origin = img.copy()
                self.p_Var.img_ShowResult = img.copy()
                self.showImage(self.m_auto.ui.label_Image,
                               self.p_Var.img_Origin)
            except:
                self.p_Var.information = QMessageBox()
                self.p_Var.information = QMessageBox.critical(
                    self, "Vision Error", "Can't take image from camera")
            pass
        else:
            file_name = self.openFileNameDialogImage()
            self.p_Var.img_Origin = None
            self.p_Var.img_ShowResult = None
            if file_name:
                img = cv2.imread(file_name)
                try:
                    if type(img) != type(np.zeros((1, 1))):
                        self.p_Var.information = QMessageBox()
                        self.p_Var.information = QMessageBox.critical(
                            self, "Vision Error", "Image is None, maybe wrong of path image")
                        return
                    else:
                        self.p_Var.img_Origin = img.copy()
                        self.p_Var.img_ShowResult = img.copy()
                        self.showImage(self.m_auto.ui.label_Image,
                                       self.p_Var.img_Origin)
                        self.ui.actionDetect.setEnabled(True)
                except:
                    self.p_Var.information = QMessageBox()
                    self.p_Var.information = QMessageBox.critical(
                        self, "Vision Error", "Error to take Image")
                    pass

    def showImage(self, frame, pic):
        # check image not empty
        if type(pic) != type(np.zeros((1, 1))):
            return
        # w, h = pic.shape[1], pic.shape[0]
        h_frame, w_frame = frame.height(), frame.width()
        self.p_Var.ratio_x = pic.shape[1] / w_frame
        self.p_Var.ratio_y = pic.shape[0] / h_frame
        img = cv2.resize(pic, (w_frame, h_frame))
        ch = 3
        if len(pic.shape) == 2:
            # ch = 3
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            q_img = QImage(img.data, w_frame, h_frame, ch *
                           w_frame, QImage.Format_RGB888)
            q_pix = QPixmap(q_img)
        else:
            # ch = 3
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            q_img = QImage(img.data, w_frame, h_frame, ch *
                           w_frame, QImage.Format_RGB888)
            q_pix = QPixmap(q_img)

        frame.setPixmap(q_pix)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit",
                                     "Do you want to save and Exit program?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            # quit and save program
            # dong luong live camera
            # dong luong socket va take image
            self.p_Var.onThreadSocket = False
            self.p_Var.onThreadTakepic = False
            self.p_Var.isLive = False
            if self.p_Camera.isOpen:
                self.p_Camera.OnDisconnect()
            try:
                sys.exit(0)
                pass
            except:
                sys.exit(0)
        if reply == QMessageBox.No:
            # quit and dont save program
            # self.thread_takepic = False
            self.p_Var.onThreadSocket = False
            self.p_Var.onThreadTakepic = False
            self.p_Var.isLive = False
            if self.p_Camera.isOpen:
                self.p_Camera.OnDisconnect()
            try:
                sys.exit(0)
                pass
            except:
                sys.exit(0)
        else:
            try:
                event.ignore()
            except:
                pass


def main():
    app = QApplication(sys.argv)
    hello = HelloVietNam()
    hello.show()
    sys.exit(app.exec_())


main()
