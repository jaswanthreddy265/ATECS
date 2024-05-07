import sys

import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView
from DataBase.TESTTBDB.FreqAccTestTableDB import FreqAccTestTableDB
from DataBase.TestCases.refreshtesttable import Ui_MainWindow_Test
import pyqtgraph as pg
########################################################################################################################
class DBTestReader(Ui_MainWindow_Test, QMainWindow):
    def __init__(self, Debug=False):
        super(DBTestReader, self).__init__()
        pg.setConfigOption('background', (255, 255, 255))                           #####plot background color
        pg.setConfigOption('foreground', 'k')                                          #####plot foreground color
        self.setupUi(self)
        self.DBConnectTryFlag = False
        self.Debug = Debug
        self.getdata = FreqAccTestTableDB()
        self.CurRowInd=0
        self.tableWidget_Test.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_Test.resizeColumnToContents(0)
        self.tableWidget_Test.resizeColumnToContents(1)
        self.tableWidget_Test.resizeColumnToContents(2)
        self.tableWidget_Test.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_Test.SelectionBehavior(QAbstractItemView.SingleSelection)
        self.tableWidget_Test.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.PB_Test_Retrieve.hide()
        #self.PB_Test_Retrieve.clicked.connect(self.getrwrfreqacctesttableread)
        self.TestGraph=self.TestGraphPlot.addPlot()

        self.lineEdit_Test_Tablename.textChanged.connect(self.GetDataFromDBtoUiTable)
        self.PB_Test_Plot.clicked.connect(self.UiTabletoGraphPlot)
        self.TestGraph.setTitle('<font size="15"><strong>Frequency Accuracy Test</strong></font>', color='blue')
        self.TestGraph.setLabel(
            "left",
            '<span style="color: purple; font-size: 18px">Error </span>'
        )
        self.TestGraph.setLabel(
            "bottom",
            '<span style="color: green; font-size: 18px">Set Frequency (MHz)</span>'
        )
    ####################################################################################################################
    # This Function gets the data from the DB through dataframe of the Test Table
    ####################################################################################################################
    def GetDataFromDBtoUiTable(self):
        self.getdata.GetFreqAccTestTable(self.lineEdit_Test_Tablename.text())
        dfreadtoui=self.getdata.CurDbTableFreq
        dfreadtoui["set_freq"]=dfreadtoui["set_freq"].astype(str)
        dfreadtoui["meas_freq"] = dfreadtoui["meas_freq"].astype(str)
        dfreadtoui["error"] = dfreadtoui["error"].astype(str)
        no_of_rows=dfreadtoui.shape[0]
        no_of_cols=dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget_Test.setRowCount(row+1)
            for col in range(no_of_cols):
                self.tableWidget_Test.setItem(row,col,QTableWidgetItem(dfreadtoui.iloc[row][col]))
    ####################################################################################################################
    # This Function plots the data from the DB through dataframe of the Test Table
    ####################################################################################################################
    def UiTabletoGraphPlot(self):
        col_count = 3
        row_count = self.tableWidget_Test.rowCount()
        data= []
        for row in range(row_count):
            rowdata=[]
            for col in range(col_count):
                table_item = self.tableWidget_Test.item(row, col)
                rowdata.append(table_item.text())
            data.append(rowdata)
        self.df=pd.DataFrame(data, columns=['set_freq', 'meas_freq','Error'])
        self.setfreq=self.df['set_freq'].tolist()
        self.setfreqvalue=[float(i) for i in self.setfreq]
        self.error=self.df['Error'].tolist()
        self.errorvalue=[float(i) for i in self.error]
        self.TestGraph.plot(self.setfreqvalue, self.errorvalue, pen='m')
        #self.TestGraphPlot.setPalette(0)


    ####################################################################################################################
    # This Function plots the data from the DB through dataframe of the Test Table
    ####################################################################################################################
if __name__ == "__main__":
    DBTestReaderui=QApplication(sys.argv)
    dbread=DBTestReader()
    dbread.show()
    sys.exit(DBTestReaderui.exec_())


    #############################