from PyQt5.QtWidgets import QDialog
from ui_classdlg import Ui_Dialog


class Class_dlg(QDialog):
    def __init__(self, parent):
        super(Class_dlg, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def __del__(self):
        del self.ui
