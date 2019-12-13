from PyQt5.QtWidgets import QDialog, QMessageBox
from ui_label import Ui_Dialog


class LabelDlg(QDialog):
    def __init__(self, parent):
        super(LabelDlg, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btn_clearLabel.clicked.connect(self.btnClearLabel)
        self.ui.btn_removeLabel.clicked.connect(self.btnRemoveLabel)

    def btnClearLabel(self):
        self.ui.listWidget_labels.clear()
        self.ui.btn_SaveRect.setEnabled(True)
        pass

    def btnRemoveLabel(self):
        try:
            self.ui.btn_SaveRect.setEnabled(True)
            idx = self.ui.listWidget_labels.currentRow()
            self.ui.listWidget_labels.takeItem(idx)
        except:
            information = QMessageBox()
            information = QMessageBox.critical(self, "Vision Information",
                                               "Can't delete label")
            pass
        pass

    def __del__(self):
        print("del ui label")
        del self.ui
