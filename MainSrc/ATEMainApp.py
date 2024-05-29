import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow

from loginDlg import LoginDlg

from MainSRC import Ui_ATEC_App
from MainSRCWin import MainGUI

########################################################################################################################
class ATE_GUI(QMainWindow,Ui_ATEC_App):
    def __init__(self):
        super(ATE_GUI, self).__init__()
        pass

    def Login(self):
        self.dlg = LoginDlg()
        self.dlg.exec()
        print(self.dlg.lineEdit_Username.text())
        return self.dlg.validcred

########################################################################################################################
    def Slots_and_Signals(self):
        self.mainsrcwin=MainGUI()
        self.mainsrcwin.label.setText(self.dlg.lineEdit_Username.text())
        self.mainsrcwin.show()

########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QMainWindow()
    main_win = ATE_GUI()
    #main_win.setupUi(main)
    validatecredential = main_win.Login()
    if validatecredential == True:
        main_win.Slots_and_Signals()
        #main.show()
        sys.exit(app.exec_())
