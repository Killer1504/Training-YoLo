import cv2
import numpy as np
import os


class ObjectDetection:
    def __init__(self):
        self.class_ids = []
        self.new_class_ids = []
        self.confidences = []
        self.new_confidences = []
        self.boxes = []
        self.new_box = []
        self.conf_threshold = 0.8
        self.nms_threshold = 0.4
        self.image = None
        self.scale = 0.00392
        self.classes = None
        self.output_layers = None
        self.path_class = os.getcwd() + "/darknet/yolo.names"
        self.path_cfg = os.getcwd() + "/darknet/cfg/yolov3.cfg"
        self.path_weights = os.getcwd() + "/darknet/backup/yolov3.backup"
        self.outs = None
        self.indices = None
        self.net = None

    def loadSystem(self):
        try:
            self.net = self.find_net(self.path_class, self.path_weights, self.path_cfg)
            return True
        except:
            return False
        pass

    def get_output_layers(self, net):
        layer_names = net.getLayerNames()

        self.output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return self.output_layers

    def draw_prediction(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        confidence = round(float(confidence), 2)
        label = str(self.classes[class_id])
        labels = label + " " + str(confidence)
        color_hung = (0, 255, 0)
        # cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color_hung, 2)
        # cv2.putText(img, labels, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_hung, 1)
        return img

    def detection_in_outs(self, outs, width, height):
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                # class id = 0 ---- person
                if class_id == 0:
                    # confidence la % ti le giong so voi vat
                    confidence = scores[class_id]
                    if confidence > self.conf_threshold:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = center_x - w / 2
                        y = center_y - h / 2
                        self.class_ids.append(class_id)
                        self.confidences.append(float(confidence))
                        self.boxes.append([x, y, w, h])
                else:
                    pass
        return self.boxes, self.confidences

    def findNew(self, indices):
        self.new_box.clear()
        self.new_class_ids.clear()
        self.new_confidences.clear()
        for i in indices:
            i = i[0]
            conf = self.confidences[i]
            class_id = self.class_ids[i]
            box = self.boxes[i]
            self.new_box.append(box)
            self.new_confidences.append(conf)
            self.new_class_ids.append(class_id)
        self.boxes.clear()
        self.class_ids.clear()
        self.confidences.clear()
        return self.new_box, self.new_class_ids, self.new_confidences

    def find_net(self, path_class, path_weights, path_cfg):
        with open(path_class, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.net = cv2.dnn.readNet(path_weights, path_cfg)
        return self.net

    def detect(self, image, width, height):
        if type(image) != type(np.zeros((1, 1))):
            return image, [], [], []
        blob = cv2.dnn.blobFromImage(image, self.scale, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        self.outs = self.net.forward(self.get_output_layers(self.net))
        self.boxes, self.confidences = self.detection_in_outs(self.outs, width, height)
        self.indices = cv2.dnn.NMSBoxes(self.boxes, self.confidences, self.conf_threshold, self.nms_threshold)
        self.findNew(self.indices)
        return self.new_class_ids, self.new_confidences, self.new_box

