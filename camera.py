import cv2
from pypylon import pylon
from PyQt5.QtWidgets import QMessageBox


def read_SerialNumber():
    try:
        f = open("baslerSerial.txt", "r")
        serial_number = f.readline()
        f.close()
        return str(serial_number)
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Can't read baslerSerial.text")
        # msg.setInformativeText(str(error))
        msg.setWindowTitle("Error")
        msg.exec_()
        pass


class Camera:
    def __init__(self):
        self.p_list_camera = ["webcam", "dino", "adb", "basler"]
        # p_type_camera dung de chi loai camera dang dung
        self.p_type_camera = "webcam"
        # max_cam dung de luu so luong camera can dung
        self.p_max_camera = 1
        # bien image dung de luu anh
        self.p_image = None

        # p_webcam de quan ly webcam
        self.m_Webcam = None

        # Basler
        self.m_Basler = None
        self.converter = None
        # self.m_serialNumber = read_SerialNumber()
        self.isOpen = False

    def OnConnect(self):
        if self.p_type_camera == "webcam":
            self.m_Webcam = cv2.VideoCapture(0)
            self.isOpen = self.m_Webcam.isOpened()
            return self.isOpen
            pass
        elif self.p_type_camera == "dino":
            pass
        elif self.p_type_camera == "adb":
            pass
        elif self.p_type_camera == "basler":
            # Create an instant camera object with the camera device found first.
            infor = None
            for i in pylon.TlFactory.GetInstance().EnumerateDevices():
                if i.GetSerialNumber() == self.m_serialNumber:
                    infor = i
                    break
                else:
                    pass
            if infor is not None:
                try:
                    self.m_Basler = pylon.InstantCamera(
                        pylon.TlFactory.GetInstance().CreateFirstDevice(infor))
                    self.m_Basler.Open()
                    self.m_Basler.MaxNumBuffer = 5
                    self.m_Basler.StartGrabbing(
                        pylon.GrabStrategy_LatestImageOnly)
                    self.converter = pylon.ImageFormatConverter()
                    self.isOpen = self.m_Basler.IsOpen()
                except:
                    self.isOpen = False
                return self.isOpen
            pass
        pass

    def OnDisconnect(self):
        self.isOpen = False
        return
        m_camera = self.p_type_camera
        if self.p_type_camera == "webcam":
            try:
                self.m_Webcam.release()
            except:
                pass
        elif self.p_type_camera == "dino":
            pass
        elif self.p_type_camera == "adb":
            pass
        elif self.p_type_camera == "basler":
            try:
                self.m_Basler.StopGrabbing()
            except:
                pass
            pass
        pass

    def OnClose(self):
        if self.p_type_camera == "webcam":
            try:
                self.m_Webcam.release()
            except:
                pass
        elif self.p_type_camera == "dino":
            pass
        elif self.p_type_camera == "adb":
            pass
        elif self.p_type_camera == "basler":
            try:
                self.m_Basler.StopGrabbing()
                self.m_Basler.Close()
            except:
                pass
            pass
        pass

    def OnTakeImage(self):
        if self.p_type_camera == "webcam":
            _, _ = self.m_Webcam.read()
            _, _ = self.m_Webcam.read()
            _, _ = self.m_Webcam.read()
            _, _ = self.m_Webcam.read()
            _, img = self.m_Webcam.read()
            return img

        elif self.p_type_camera == "dino":
            pass
        elif self.p_type_camera == "adb":
            pass
        elif self.p_type_camera == "basler":
            if self.isOpen and self.m_Basler.IsGrabbing():
                # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
                grab_result = self.m_Basler.RetrieveResult(
                    1000, pylon.TimeoutHandling_ThrowException)
                # Image grabbed successfully?
                if grab_result.GrabSucceeded():
                    image = self.converter.Convert(grab_result)
                    img = image.GetArray()
                else:
                    error = "Error:" + \
                        str(grab_result.ErrorCode) + \
                        str(grab_result.ErrorDescription)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Grab not success")
                    msg.setWindowTitle("Error grab")
                    msg.exec_()
                    img = None
                grab_result.Release()
                return img
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Can't grab image or open camare")
                msg.setWindowTitle("Error Camera")
                msg.exec_()
                pass
        pass

    def __del__(self):
        del self.p_max_camera, self.p_list_camera, self.p_type_camera, self.p_image, self.m_Webcam, self.m_Basler
