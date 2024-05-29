import json
import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QDialog, QApplication

from ESMP.ESMPmessage import Ui_msg_dialog


class MsgDlg(QDialog,Ui_msg_dialog):
    def __init__(self,parent = None):
        super().__init__(parent)

        self.setupUi(self)

        self.CB_msg_sel.currentTextChanged.connect(self.MsgSel)

        self.CB_direct_RB.currentIndexChanged.connect(self.SecSel)
        self.CB_internal_RB.currentIndexChanged.connect(self.InternalSel)

        self.frame_direct_mode.setVisible(False)
        self.frame_calib_internal.setVisible(False)

########################################################################################################################
    def SecSel(self):
        if self.CB_direct_RB.currentIndex()==0:
            self.CB_Direct.clear()
            self.CB_Direct.addItems(["All Sectors","0-60°","60-120°","120-180°","180-240°","240-300°","300-360°"])

        elif self.CB_direct_RB.currentIndex()==2:
            self.CB_Direct.clear()
            self.CB_Direct.addItems(["All Sectors","0-60°","60-120°","120-180°","180-240°","240-300°","300-360°"])

        elif self.CB_direct_RB.currentIndex()==1:
            self.CB_Direct.clear()
            self.CB_Direct.addItems(["All Sectors","0-90°","90-180°","180-270°","270-360°"])
    def InternalSel(self):

        if self.CB_internal_RB.currentIndex()==0:
            self.CB_Internal.clear()
            self.CB_Internal.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_internal_RB.currentIndex()==2:
            self.CB_Internal.clear()
            self.CB_Internal.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_internal_RB.currentIndex()==1:
            self.CB_Internal.clear()
            self.CB_Internal.addItems(["All Sectors", "0-90°", "90-180°", "180-270°", "270-360°"])

########################################################################################################################
    def MsgSel(self):

        if self.CB_msg_sel.currentText() == "ATE_TO_ESMP_CAL_START":
            self.frame_direct_mode.setVisible(False)
            self.frame_calib_internal.setVisible(False)

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_CAL_STOP":
            self.frame_direct_mode.setVisible(False)
            self.frame_calib_internal.setVisible(False)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_DIRECTED_MODE":

            print("ATE_TO_ESMP_DIRECTED_MODE")
            self.frame_direct_mode.setVisible(True)
            self.frame_calib_internal.setVisible(False)
        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_DATA_CALIB_INTERNAL":
            print("ATE_TO_ESMP_DATA_CALIB_INTERNAL")

            self.frame_calib_internal.setVisible(True)
            self.frame_calib_internal.setGeometry(QRect(9, 43, 637, 300))
            self.frame_direct_mode.setVisible(False)

########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main =MsgDlg()
    main.show()
    sys.exit(app.exec_())
