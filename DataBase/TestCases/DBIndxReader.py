import sys

import psycopg2
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView

from DataBase.TestCases.DBTestReader import DBTestReader
from DataBase.INDXTBDB.FreqAccIndxTableDB import FreqAccIndxTableDB
from DataBase.TestCases.ErrorCodesDatabase import *
from DataBase.TestCases.refreshindxtable import Ui_MainWindow_Indx
class DBIndxReader(Ui_MainWindow_Indx, QMainWindow):
    def __init__(self, Debug=False):
        super(DBIndxReader, self).__init__()
        self.setupUi(self)
        self.DBConnectTryFlag = False
        self.Debug = Debug
        self.connection = True

        #self.getdatasensmeas = SensMeasIndxTableDB
        self.CurRowInd=0
        #self.tableWidget_Indx.setGeometry(QtCore.QRect(9, 81, 1900, 600))
        self.tableWidget_Indx.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_Indx.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_Indx.SelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_Indx.setSelectionMode(QAbstractItemView.MultiSelection)
        #self.PB_Indx_Refesh.clicked.connect(self.getfreqaccindxtableread)
        self.PB_Indx_Refresh.clicked.connect(self.FetchRecordDateFilterFromUi)

        self.tableWidget_Indx.clicked.connect(self.IndxCellClicked)
        #self.tableWidget_Indx.cellActivated.connect(self.cell)
    ####################################################################################################################
    # This Function Connects with Database,connecting to parent .py file,
    # getting data from the FreqAccIndxTableDB class, ui functions and it's modifications.
    ####################################################################################################################
    """def getfreqaccindxtableread(self):
        self.getdata.connect({
        'user': 'postgres',
        'password': 'Platinum0435#',
        'host': 'localhost',
        'database': 'atec',
        'port': 6543
        })
        self.getdata.getfreqaccindxtable()
        #print(self.getdata.CurDbTableFreq)
        dfreadtoui=self.getdata.CurDbTableFreq
        dfreadtoui["date"]=dfreadtoui["date"].astype(str)
        dfreadtoui["system"] = dfreadtoui["system"].astype(str)
        dfreadtoui["system_id"] = dfreadtoui["system_id"].astype(str)
        dfreadtoui["start_freq"] = dfreadtoui["start_freq"].astype(str)
        dfreadtoui["stop_freq"] = dfreadtoui["stop_freq"].astype(str)
        dfreadtoui["step_freq"] = dfreadtoui["step_freq"].astype(str)
        dfreadtoui["set_power"] = dfreadtoui["set_power"].astype(str)
        dfreadtoui["pos_angle"] = dfreadtoui["pos_angle"].astype(str)
        dfreadtoui["pw"] = dfreadtoui["pw"].astype(str)
        dfreadtoui["pri"] = dfreadtoui["pri"].astype(str)
        dfreadtoui["ampl"] = dfreadtoui["ampl"].astype(str)
        dfreadtoui["rms_error"] = dfreadtoui["rms_error"].astype(str)
        no_of_rows=dfreadtoui.shape[0]
        no_of_cols=dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_Indx.setRowCount(row+1)
            for col in range(no_of_cols):
                self.tableWidget_Indx.setItem(row,col,QTableWidgetItem(dfreadtoui.iloc[row][col]))
        print(len(dfreadtoui))
"""
    ####################################################################################################################
    # This Function Connects with Database,connecting to parent .py file,
    # getting data from the FreqAccIndxTableDB class, ui functions and it's modifications.
    ####################################################################################################################
    def connect(self, DataBaseSettings = {
                                'user' :'postgres',
                                'password':'Platinum0435#',
                                'host':'localhost',
                                'database' : 'atec',
                                'port': 6543
                                }):
        try:
            self.connection = psycopg2.connect(
                user=DataBaseSettings['user'],
                password=DataBaseSettings['password'],
                host=DataBaseSettings['host'],
                database=DataBaseSettings['database'],
                port=DataBaseSettings['port']
            )
            return SUCCESS
        except (Exception, psycopg2.Error) as error:
            return DATABASE_CONNECTION_ERROR
    ####################################################################################################################
    def FetchRecordDateFilterFromUi(self):
        #self.connection=True
        self.getdata = FreqAccIndxTableDB()
        self.getdata.SelFreqDateSysFilter(datefilterfrom=self.dateEdit_DateFilterFrom.text(), datefilterto=self.dateEdit_DateFilterTo.text(), sysfilter=self.comboBox_System.currentText().lower())
        dfreadtoui = self.getdata.SelFreqDateSysFilter
        if self.comboBox_TableName.currentText()=="freqaccindxtable":
            self.tableWidget_Indx.setColumnCount(19)
            self.tableWidget_Indx.setHorizontalHeaderLabels(
                ['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref', 'start_freq', 'stop_freq', 'step_freq',
                 'freq_list', 'set_power', 'pos_angle', 'signal_cat', 'pw', 'pri', 'ampl', 'rms_error', 'test_status',
                 'remarks'])
            dfreadtoui = dfreadtoui.astype(str)
        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_Indx.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_Indx.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        print(len(dfreadtoui))

        """elif self.comboBox_TableName.currentText()=="pwaccindxtable":
            self.tableWidget_Indx.setColumnCount(19)
            self.tableWidget_Indx.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref', 'start_pw', 'stop_pw', 'step_pw', 'pw_list', 'set_power', 'pos_angle', 'signal_cat', 'freq', 'pri', 'ampl', 'rms_error', 'test_status', 'remarks'])
            dfreadtoui = dfreadtoui.astype(str)

        elif self.comboBox_TableName.currentText()=="priaccindxtable":
            self.tableWidget_Indx.setColumnCount(19)
            self.tableWidget_Indx.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref', 'start_pri', 'stop_pri', 'step_pri', 'pri_list', 'set_power', 'pos_angle', 'signal_cat', 'freq', 'pw', 'ampl', 'rms_error', 'test_status', 'remarks'])
            dfreadtoui = dfreadtoui.astype(str)

        elif self.comboBox_TableName.currentText()=="doaaccindxtable":
            self.tableWidget_Indx.setColumnCount(19)
            self.tableWidget_Indx.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref', 'start_doa', 'stop_doa', 'step_doa', 'doa_list', 'set_power', 'freq', 'signal_cat', 'pw', 'pri', 'ampl', 'rms_error', 'test_status', 'remarks'])
            dfreadtoui = dfreadtoui.astype(str)

        elif self.comboBox_TableName.currentText()=="amplaccindxtable":
            self.tableWidget_Indx.setColumnCount(19)
            self.tableWidget_Indx.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref', 'start_ampl', 'stop_ampl', 'step_ampl', 'ampl_list', 'set_power', 'pos_angle', 'signal_cat', 'pw', 'pri', 'freq', 'rms_error', 'test_status', 'remarks'])
            dfreadtoui = dfreadtoui.astype(str)

        elif self.comboBox_TableName.currentText()=="sensmeasindxtable":
            self.tableWidget_Indx.setColumnCount(20)
            self.tableWidget_Indx.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref', 'start_sensmeas', 'stop_sensmeas', 'step_sensmeas', 'sensmeas_list', 'set_power','start_power', 'pos_angle', 'signal_cat', 'pw', 'pri', 'ampl', 'rms_error', 'test_status', 'remarks'])
            dfreadtoui = dfreadtoui.astype(str)"""

        no_of_rows = dfreadtoui.shape[0]
        no_of_cols = dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_Indx.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.tableWidget_Indx.setItem(row, col, QTableWidgetItem(dfreadtoui.iloc[row][col]))
        print(len(dfreadtoui))

    ####################################################################################################################
    # This Function triggers the table cell clicked event
    ####################################################################################################################
    """def IndxCellClicked(self):
        self.LEdit.show()
        self.LEdit.TestGraph.clear()
        indxcell=self.tableWidget_Indx.currentRow()
        self.create_new_list=[]
        for col in range (self.tableWidget_Indx.columnCount()):
            value=self.tableWidget_Indx.item(indxcell,col).text()
            self.create_new_list.append(value)
        self.LEdit.lineEdit_Test_Tablename.setText(self.create_new_list[5])
        print(self.create_new_list[5])"""

    ####################################################################################################################
    # This Function has Database Connection Details,
    # calling function from the FreqAccIndxTableDB class, displaying the table from dataframe to ui.
    ####################################################################################################################
if __name__ == "__main__":
    DBIndxReaderui=QApplication(sys.argv)
    dbread=DBIndxReader()
    dbread.show()
    sys.exit(DBIndxReaderui.exec_())