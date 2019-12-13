import json
import os

path = os.getcwd() + "/Setting/para.json"


def readPara(path_json):
    f = open(path, "r")
    data_dict = json.load(f)
    f.close()
    return data_dict


class CommonParameter:
    def __init__(self):
        self.para_dict = readPara(path)
        self.thickness = self.para_dict['thickness']

    def savePara(self):
        f = open(path, "w")
        json.dump(self.para_dict, f, indent=4)
        f.close()

    def __del__(self):
        del self.thickness, self.para_dict
