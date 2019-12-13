from PyQt5.QtWidgets import QDialog, QApplication
from ui_autodlg import Ui_Dialog


class AutoDlg(QDialog):
    def __init__(self, parent):
        super(AutoDlg, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def __del__(self):
        del self.ui
