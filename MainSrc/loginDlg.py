import sys

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow

from login import Ui_Login_Screen


class LoginDlg(QDialog,Ui_Login_Screen):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.validcred = False
        self.setupUi(self)
        self.pushButton_Login.clicked.connect(self.validatecredentials)

    def validatecredentials(self):
        """print('Validate Credentials')
        # Opening JSON file
        with open('logincred.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)

        for username, password in json_object.items():
            if (username == self.lineEdit_Username.text()) and (password == self.lineEdit_Password.text()):
                self.validcred = True
                self.close()"""
        username="admin"
        password="1234"
        if (self.lineEdit_Username.text()) and (self.lineEdit_Password.text()):
            self.validcred = True
            self.close()


########################################################################################################################
########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QMainWindow()
    main_win = LoginDlg()
    main_win.setupUi(main)
    validatecredential = main_win.Login()
    if validatecredential == True:
        main_win.Slots_and_Signals()
        main.show()
        sys.exit(app.exec_())

