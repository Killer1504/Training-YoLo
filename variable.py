import threading


class Variable:
    def __init__(self):
        self.onThreadSocket = False
        self.onThreadTakepic = False
        self.lock = threading.Lock()

        # bien nhan du lieu socket
        self.dataSocketReceive = ""
        # bien kiem tra da nhan du lieu lan nao chua
        self.onCheckdataReceive = False

        # bien kiem tra connect camera
        self.is_connect = True
        # bien kiem tra xem da listen hay chua
        self.isListen = False
        self.isConnectSocket = False

        self.img_Origin = None
        self.img_ShowResult = None

        # ti le giua anh va lable image
        self.ratio_x = 0
        self.ratio_y = 0

        self.DirImage = None
        self.DirLabel = None
        self.listImage = []
        self.idxCurrentImg = 0
        self.currentImg = None
        self.currentImg_show = None
        self.information = None
        # contain labels
        self.listClassLabel = []
        self.current_listClassLabel = []
        self.isSaveLabel = False
        self.nameImageCurrent = None

        self.dir_darknet_yolonames = "/darknet/yolo.names"
        self.dir_darknet_yolodata = "/darknet/yolo.data"
        self.dir_darknet_traintxt = "/darknet/train.txt"
        self.dir_darknet_valtxt = "/darknet/val.txt"
        self.dir_darknet_cfg = "/darknet/cfg/yolov3.cfg"

        self.isThreadTrain = False
        self.isThreadUpdateUiTrain = False
        self.p_cmd = None
        self.output_cmd = ""
        self.p_lock = None
        self.isLoadModel = False

        self.isLive = False

    def __del__(self):
        print("del variable")
        del self.onThreadSocket, self.onThreadTakepic, self.onCheckdataReceive, self.is_connect, self.isListen
        del self.isConnectSocket, self.img_Origin, self.img_ShowResult, self.ratio_x, self.ratio_y
        del self.DirImage, self.DirLabel, self.listImage, self.idxCurrentImg, self.currentImg
        del self.information, self.listClassLabel, self.isSaveLabel, self.nameImageCurrent
        del self.dir_darknet_yolonames, self.dir_darknet_yolodata


class Rect:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def __del__(self):
        print("del rect")
        del self.x, self.y, self.height, self.width
