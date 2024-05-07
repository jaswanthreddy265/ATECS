import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from DataBase.TestCases.DBTestReader import DBTestReader
from DataBase.INDXTBDB.FreqAccIndxTableDB import FreqAccIndxTableDB
from DataBase.TestCases.refreshindxtable_testwise import Ui_MainWindow_Indx
class DBIndxReader(Ui_MainWindow_Indx, QMainWindow):
    def __init__(self, Debug=False):
        super(DBIndxReader, self).__init__()
        self.setupUi(self)
        self.DBConnectTryFlag = False
        self.Debug = Debug
        self.connection = True
        self.getdata = FreqAccIndxTableDB()
        self.CurRowInd=0
        self.LEdit=DBTestReader()
        #self.tableWidget_IndxAll.setGeometry(QtCore.QRect(9, 81, 1900, 600))
        """self.tableWidget_IndxAll.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_IndxAll.SelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_IndxAll.setSelectionMode(QAbstractItemView.SingleSelection)"""
        #self.PB_Indx_Refesh.clicked.connect(self.getfreqaccindxtableread)
        self.PB_Indx_RefeshAll.clicked.connect(self.DateFilterFromUi)

        #self.tableWidget_IndxAll.clicked.connect(self.IndxCellClicked)
        #self.tableWidget_IndxAll.cellActivated.connect(self.cell)

    ####################################################################################################################
    # This Function Connects with Database,connecting to parent .py file,
    # getting data from the FreqAccIndxTableDB class, ui functions and it's modifications.
    ####################################################################################################################
    def DateFilterFromUi(self):
        self.getdata.connect({
        'user': 'postgres',
        'password': 'Platinum0435#',
        'host': 'localhost',
        'database': 'atec',
        'port': 6543
        })
        self.getdata.SelDateFilter(indxtabname='freqaccindxtable', datefilterfrom=self.dateEdit_AllDateFilterFrom.text(), datefilterto=self.dateEdit_AllDateFilterTo.text())
        self.tableWidget_IndxFreqAll.clear()
        #self.tableWidget_IndxAll.setSelection(self.removeAction)
        dfreadtoui = self.getdata.DateFil
        self.tableWidget_IndxFreqAll.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        dfreadtoui["date"] = dfreadtoui["date"].astype(str)
        dfreadtoui["username"] = dfreadtoui["username"].astype(str)
        dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["system"] = dfreadtoui["system"].astype(str)
        dfreadtoui["mode"] = dfreadtoui["mode"].astype(str)
        dfreadtoui["test_tab_ref"] = dfreadtoui["test_tab_ref"].astype(str)
        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_IndxFreqAll.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_IndxFreqAll.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        self.tableWidget_IndxFreqAll.setMaximumHeight(300)
        ######################
        self.getdata.SelDateFilter(indxtabname='pwaccindxtable', datefilterfrom = self.dateEdit_AllDateFilterFrom.text(), datefilterto = self.dateEdit_AllDateFilterTo.text())
        self.tableWidget_IndxPwAll.clear()
        dfreadtoui = self.getdata.DateFil
        self.tableWidget_IndxPwAll.setHorizontalHeaderLabels(
            ['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        dfreadtoui["date"] = dfreadtoui["date"].astype(str)
        dfreadtoui["username"] = dfreadtoui["username"].astype(str)
        dfreadtoui["system"] = dfreadtoui["system"].astype(str)
        dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["mode"] = dfreadtoui["mode"].astype(str)
        dfreadtoui["test_tab_ref"] = dfreadtoui["test_tab_ref"].astype(str)
        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_IndxPwAll.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_IndxPwAll.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        self.tableWidget_IndxPwAll.setMaximumHeight(300)
        ######################
        self.getdata.SelDateFilter(indxtabname='priaccindxtable', datefilterfrom = self.dateEdit_AllDateFilterFrom.text(), datefilterto = self.dateEdit_AllDateFilterTo.text())
        self.tableWidget_IndxPriAll.clear()
        dfreadtoui = self.getdata.DateFil
        self.tableWidget_IndxPriAll.setHorizontalHeaderLabels(
            ['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        dfreadtoui["date"] = dfreadtoui["date"].astype(str)
        dfreadtoui["username"] = dfreadtoui["username"].astype(str)
        dfreadtoui["system"] = dfreadtoui["system"].astype(str)
        dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["mode"] = dfreadtoui["mode"].astype(str)
        dfreadtoui["test_tab_ref"] = dfreadtoui["test_tab_ref"].astype(str)
        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_IndxPriAll.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_IndxPriAll.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        self.tableWidget_IndxPriAll.setMaximumHeight(300)
        ######################
        self.getdata.SelDateFilter(indxtabname='amplaccindxtable', datefilterfrom = self.dateEdit_AllDateFilterFrom.text(), datefilterto = self.dateEdit_AllDateFilterTo.text())
        self.tableWidget_IndxAmplAll.clear()
        dfreadtoui = self.getdata.DateFil
        self.tableWidget_IndxAmplAll.setHorizontalHeaderLabels(
            ['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        dfreadtoui["date"] = dfreadtoui["date"].astype(str)
        dfreadtoui["username"] = dfreadtoui["username"].astype(str)
        dfreadtoui["system"] = dfreadtoui["system"].astype(str)
        dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["mode"] = dfreadtoui["mode"].astype(str)
        dfreadtoui["test_tab_ref"] = dfreadtoui["test_tab_ref"].astype(str)
        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_IndxAmplAll.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_IndxAmplAll.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        self.tableWidget_IndxAmplAll.setMaximumHeight(300)
        ######################
        self.getdata.SelDateFilter(indxtabname='doaaccindxtable', datefilterfrom = self.dateEdit_AllDateFilterFrom.text(), datefilterto = self.dateEdit_AllDateFilterTo.text())
        self.tableWidget_IndxDoaAll.clear()
        dfreadtoui = self.getdata.DateFil
        self.tableWidget_IndxDoaAll.setHorizontalHeaderLabels(
            ['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        dfreadtoui["date"] = dfreadtoui["date"].astype(str)
        dfreadtoui["username"] = dfreadtoui["username"].astype(str)
        dfreadtoui["system"] = dfreadtoui["system"].astype(str)
        dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["mode"] = dfreadtoui["mode"].astype(str)
        dfreadtoui["test_tab_ref"] = dfreadtoui["test_tab_ref"].astype(str)
        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_IndxDoaAll.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_IndxDoaAll.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        self.tableWidget_IndxDoaAll.setMaximumHeight(300)
        ######################
        self.getdata.SelDateFilter(indxtabname='sensmeasindxtable', datefilterfrom = self.dateEdit_AllDateFilterFrom.text(), datefilterto = self.dateEdit_AllDateFilterTo.text())
        self.tableWidget_IndxSensMeasAll.clear()
        dfreadtoui = self.getdata.DateFil
        self.tableWidget_IndxSensMeasAll.setHorizontalHeaderLabels(
            ['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        dfreadtoui["date"] = dfreadtoui["date"].astype(str)
        dfreadtoui["username"] = dfreadtoui["username"].astype(str)
        #dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["system"] = dfreadtoui["system"].astype(str)
        dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["mode"] = dfreadtoui["mode"].astype(str)
        dfreadtoui["test_tab_ref"] = dfreadtoui["test_tab_ref"].astype(str)
        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_IndxSensMeasAll.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_IndxSensMeasAll.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        self.tableWidget_IndxSensMeasAll.setMaximumHeight(300)
    ####################################################################################################################
    def IndxCellClicked(self):
        self.LEdit.show()
        self.LEdit.TestGraph.clear()
        indxcell=self.tableWidget_Indx.currentRow()
        self.create_new_list=[]
        for col in range (self.tableWidget_Indx.columnCount()):
            value=self.tableWidget_Indx.item(indxcell,col).text()
            self.create_new_list.append(value)
        self.LEdit.lineEdit_Test_Tablename.setText(self.create_new_list[5])
        print(self.create_new_list[5])
    ####################################################################################################################
    # This Function has Database Connection Details,
    # calling function from the FreqAccIndxTableDB class, displaying the table from dataframe to ui.
    ####################################################################################################################
if __name__ == "__main__":
    DBIndxReaderui=QApplication(sys.argv)
    dbread=DBIndxReader()
    dbread.show()
    sys.exit(DBIndxReaderui.exec_())