from PyQt5.QtWidgets import QDialog, QMessageBox
from ui_setting import Ui_Dialog


class SettingDlg(QDialog):
    def __init__(self, parent):
        super(SettingDlg, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def __del__(self):
        del self.ui
