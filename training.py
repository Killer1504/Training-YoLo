from PyQt5.QtWidgets import QDialog, QApplication
from ui_training import Ui_Dialog


class TrainingAI(QDialog):
    def __init__(self, parent):
        super(TrainingAI, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btn_Clear.clicked.connect(self.btnClear)

    def btnClear(self):
        self.ui.listWidget_training.clear()
        pass

    def __del__(self):
        del self.ui
