import datetime
import random
import sys
import time
import openpyxl
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QAbstractItemView
from openpyxl.styles import Side, Border, Font, Alignment

from DataBase.TestCases.ErrorCodesDatabase import SUCCESS
from DataBase.INDXTBDB.FreqAccIndxTableDB import FreqAccIndxTableDB
from DataBase.TESTTBDB.FreqAccTestTableDB import FreqAccTestTableDB
from DataBase.TESTSWMOD.FreqAccTestP import Ui_FreqAccTestP


########################################################################################################################
#  Frequency Accuracy Test Table Database Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   10 Mar 2023
#   FreqAccTestMain Class has following member Functions
#
########################################################################################################################
# This Creating the freqacctestmain Class
########################################################################################################################
class FreqAccTestMain(QMainWindow, Ui_FreqAccTestP):
    def __init__(self):
        super(FreqAccTestMain,self).__init__()
        self.setupUi(self)
        self.tableWidget_Freq.resizeColumnToContents(0)
        self.tableWidget_Freq.resizeColumnToContents(1)
        self.tableWidget_Freq.resizeColumnToContents(2)
        self.datatb = FreqAccIndxTableDB(Debug=FreqAccTestMain)
        self.PB_Close_Freq.clicked.connect(self.CloseProcess)
        self.PB_Save_Freq.clicked.connect(self.SaveProcess)
        self.PB_Step_Freq.clicked.connect(self.StepModeProcess)
        self.PB_Run_Freq.clicked.connect(self.RuNModeProcess)
        self.PB_Pause_Freq.clicked.connect(self.PauseProcess)
        self.PB_Abort_Freq.clicked.connect(self.AbortProcess)
        self.PB_Continue_Freq.clicked.connect(self.ContinueProcess)
        self.PB_Print_Freq.clicked.connect(self.PrintProcess)
        #self.comboBox_System.currentTextChanged.connect(self.ComboTextSystem)
        # Read Configuration files Here if any Ex  database table names, default Data values, Previous Test Values
        self.ConfigJSON = {'indxtabname' : 'freqaccindxtable'}
        #print(self.ConfigJSON['indxtabname'])
        # initialise the variables here with previous Test Data Values
        self.PB_Save_Freq.setDisabled(True)
        self.PB_Print_Freq.setDisabled(True)
        self.PB_Pause_Freq.setDisabled(True)
        self.PB_Continue_Freq.setDisabled(True)
        self.PB_Abort_Freq.setDisabled(True)
        self.InitVariables()
        self.CompletionFlag = True
    ####################################################################################################################
    # This Function Adds the data to gui table
    ####################################################################################################################
    def InitVariables(self):
        self.StartFreq = float(self.lineEdit_start_freq.text())
        self.StopFreq = float(self.lineEdit_stop_freq.text())
        self.StepFreq = float(self.lineEdit_step_freq.text())
        self.SetFreq = self.StartFreq
        self.PauseFlag = False
        self.AbortFlag = False
        self.ContinueFlag = False
        self.tableWidget_Freq.clear()
        self.DBConnectTryFlag = False
        self.CompletionFlag = False
       # self.ConnectDB()
        self.row = 0
        self.tableWidget_Freq.setColumnCount(3)
        self.tableWidget_Freq.setHorizontalHeaderLabels(["Set Frequency\n(MHz)", "Measured Frequency\n(MHz)", "Error"])
        self.tableWidget_Freq.setColumnWidth(0, 150)
        self.tableWidget_Freq.setColumnWidth(1, 150)
        self.tableWidget_Freq.setColumnWidth(2, 100)
        self.tableWidget_Freq.resize(550,400)
        self.SetProgressBar()
    ####################################################################################################################
    # This Function Adds the data to database index table
    ####################################################################################################################
    def StepModeProcess(self):
        if self.CompletionFlag == True:
            self.InitVariables()
        self.PB_Pause_Freq.setDisabled(True)
        self.PB_Continue_Freq.setDisabled(True)
        self.PB_Abort_Freq.setDisabled(True)
        self.PB_Run_Freq.setDisabled(True)
        self.PB_Close_Freq.setDisabled(True)
        self.PB_Save_Freq.setDisabled(True)
        self.PB_Print_Freq.setDisabled(True)
        self.PB_Step_Freq.setDisabled(True)
        QApplication.processEvents()
        if self.DBConnectTryFlag == False:
            self.ConnectDB()
        self.PerformMeasurements()
        time.sleep(1)
        self.SetFreq = self.SetFreq + self.StepFreq
        self.PB_Run_Freq.setEnabled(True)
        self.PB_Save_Freq.setEnabled(True)
        self.PB_Print_Freq.setEnabled(True)
        self.PB_Close_Freq.setEnabled(True)
        self.PB_Step_Freq.setEnabled(True)
        QApplication.processEvents()
        self.SetProgressBar()
        if self.SetFreq > self.StopFreq:
            self.CompletionFlag = True
            self.PB_Pause_Freq.setDisabled(True)
            self.PB_Continue_Freq.setDisabled(True)
            self.PB_Abort_Freq.setDisabled(True)
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def RuNModeProcess(self):
        if self.DBConnectTryFlag == False:
            self.ConnectDB()
        if self.CompletionFlag == True:
            self.InitVariables()
        self.PB_Pause_Freq.setEnabled(True)
        self.PB_Continue_Freq.setDisabled(True)
        self.PB_Abort_Freq.setEnabled(True)
        self.PB_Run_Freq.setDisabled(True)
        self.PB_Step_Freq.setDisabled(True)
        self.PB_Close_Freq.setDisabled(True)
        self.PB_Save_Freq.setDisabled(True)
        self.PB_Print_Freq.setDisabled(True)
        QApplication.processEvents()
        time.sleep(1)
        while self.SetFreq <= self.StopFreq:
            self.PerformMeasurements()
            self.SetProgressBar()

            QApplication.processEvents()
            time.sleep(1)
            self.SetFreq = self.SetFreq + self.StepFreq
            if self.PauseFlag == True:
                self.PauseFlag = False
                return
            if self.AbortFlag == True:
                self.AbortFlag = False
                self.CompletionFlag = True
                return
        self.DBConnectTryFlag = False
        self.CompletionFlag = True
        self.PB_Run_Freq.setEnabled(True)
        self.PB_Step_Freq.setEnabled(True)
        self.PB_Pause_Freq.setDisabled(True)
        self.PB_Continue_Freq.setDisabled(True)
        self.PB_Abort_Freq.setDisabled(True)

        self.PB_Print_Freq.setEnabled(True)
        self.PB_Close_Freq.setEnabled(True)
        self.PB_Save_Freq.setEnabled(True)

    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def PerformMeasurements(self):
        MeasFreq = self.SetFreq + random.randrange(-7,7)        # SET FREQ+ RANDOM -7 TO +7
        self.tableWidget_Freq.setRowCount(self.row + 1)
        self.tableWidget_Freq.setItem(self.row, 0, QTableWidgetItem(str(self.SetFreq)))
        self.tableWidget_Freq.setItem(self.row, 1, QTableWidgetItem(str(MeasFreq)))
        Error=self.SetFreq - MeasFreq
        self.tableWidget_Freq.setItem(self.row, 2, QTableWidgetItem(str(Error)))
        newrow = {'set_freq': self.SetFreq, 'meas_freq': MeasFreq, 'error': Error}
        self.AppendtoDataTable(newrow)

        # table vertical scrolling
        tabvertscroll = self.tableWidget_Freq.item(self.row, 0)
        self.tableWidget_Freq.scrollToItem(tabvertscroll, QAbstractItemView.PositionAtTop)
        self.tableWidget_Freq.selectRow(self.row)
        self.row = self.row + 1


    ###################################################################################################################
    # Enabling or disabling Pause process
    #
    ###################################################################################################################
    def PauseProcess(self):
        self.PauseFlag = True
        self.PB_Close_Freq.setEnabled(True)
        self.PB_Pause_Freq.setDisabled(True)
        self.PB_Step_Freq.setEnabled(True)
        self.PB_Continue_Freq.setEnabled(True)
    ###################################################################################################################
    # This function stops the ongoing test forcefully
    #
    ###################################################################################################################
    def AbortProcess(self):
        self.AbortFlag = True
        self.PB_Pause_Freq.setDisabled(True)
        self.PB_Continue_Freq.setDisabled(True)
        self.PB_Abort_Freq.setDisabled(True)
        self.PB_Run_Freq.setEnabled(True)
        self.PB_Step_Freq.setEnabled(True)
        self.PB_Save_Freq.setEnabled(True)
        self.PB_Print_Freq.setEnabled(True)
        self.PB_Close_Freq.setEnabled(True)

    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def SetProgressBar(self):
        No_of_steps = ((self.StopFreq-self.StartFreq)) / self.StepFreq + 1
        percentage_of_completion = int(self.row*100/No_of_steps)
        self.progressBar_Freq.setValue(percentage_of_completion)
        self.lineEdit_Freq_PB.setText(str(percentage_of_completion))
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def ContinueProcess(self):
        self.ContinueFlag = True
        self.RuNModeProcess()
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def HelpProcess(self):
        pass
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def SaveProcess(self):
        workbook = openpyxl.Workbook()
        timestamp = datetime.datetime.now()
        sheetonename = f'''{self.comboBox_System.currentText().lower()}freqacctest{timestamp.strftime("%Y_%m_%d_%H_%M")}'''
        sheettwoname=self.ConfigJSON['indxtabname']+timestamp.strftime("%Y_%m_%d")
        sheet1 = workbook.active
        sheet1.title =sheetonename
        sheet2 = workbook.create_sheet(sheettwoname)
        # Construct test worksheets with some content.
        sheet1['A1'] = 'Set Frequency(MHz)'
        sheet1['B1'] = 'Measure Frequency(MHz)'
        sheet1['C1'] = 'Error'
        sheet1['A1'].font = Font(bold=True)         #for Font type
        sheet1['B1'].font = Font(bold=True)
        sheet1['C1'].font = Font(bold=True)
        sheet1['A1'].alignment = Alignment(horizontal='center')         #for text alignment for headers
        sheet1['B1'].alignment = Alignment(horizontal='center')
        sheet1['C1'].alignment = Alignment(horizontal='center')
        sheet2['A1'].alignment = Alignment(horizontal='center')
        sheet2['B1'].alignment = Alignment(horizontal='center')
        for i in range(0,self.tableWidget_Freq.rowCount()):
            sheet1[f'''A{i-2 + 3}'''] = self.tableWidget_Freq.item(i, 0).text()
            sheet1[f'''B{i-2 + 3}'''] = self.tableWidget_Freq.item(i, 1).text()
            sheet1[f'''C{i-2 + 3}'''] = self.tableWidget_Freq.item(i, 2).text()
        self.set_border(sheet1, f'''A1:C{3 + i-1}''')                    #for excel sheet table cell borders

        sheet2['A1'] = 'Parameter'
        sheet2['B1'] = 'Value'
        sheet2['A1'].font=Font(bold=True)
        sheet2['B1'].font = Font(bold=True)
        sheet1.column_dimensions['A'].width = 20                      #for Column width
        sheet1.column_dimensions['B'].width = 25
        sheet1.column_dimensions['C'].width = 9

        sheet2['A2'] = 'Start Frequency (MHz)'
        sheet2['A3'] = 'Stop Frequency (MHz)'
        sheet2['A4'] = 'Step Frequency (MHz)'
        sheet2['A5'] = 'Servo Position'
        sheet2['A6'] = 'Signal Category'
        sheet2['A7'] = 'Pulse Width'
        sheet2['A8'] = 'PRI'
        sheet2['A9'] = 'Power'

        sheet2['B2'] = float(self.lineEdit_start_freq.text())
        sheet2['B3'] = float(self.lineEdit_stop_freq.text())
        sheet2['B4'] = float(self.lineEdit_step_freq.text())
        sheet2['B5'] = float(self.lineEdit_pos_angle.text())
        sheet2['B6'] = self.CB_SigCat.currentText()
        sheet2['B7'] = float(self.lineEdit_pw.text())
        sheet2['B8'] = float(self.lineEdit_pri.text())
        sheet2['B9'] = float(self.lineEdit_set_power.text())
        sheet2.column_dimensions['A'].width = 20
        sheet2.column_dimensions['B'].width = 9
        self.set_border(sheet2, f'''A1:B{0+ i-1}''')
        sysnamecache=self.comboBox_System.currentText().lower()
        # save the file
        outfile = sysnamecache +"FreqAcc" + datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '.xlsx'
        workbook.save(filename=outfile)
        QMessageBox.information(self, "Self Test", "ReportsBin Saved to " + outfile)
    ####################################################################################################################
    def set_border(self,worksheet, cell_range):
        thin = Side(border_style="thin", color="000000")
        for row in worksheet[cell_range]:
            for cell in row:
                cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def PrintProcess(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.handlePaintRequest(printer)

    def handlePaintRequest(self, printer):
        painter = QPainter()
        painter.begin(printer)
        self.tableWidget_Freq.render(painter)
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def CloseProcess(self):
        self.close()
        self.indxtb.close()
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def ConnectDB(self):
        self.DBConnectTryFlag = True
        self.indxtb = FreqAccIndxTableDB(Debug=True)
        self.indxtb.tablename = self.ConfigJSON['indxtabname']
        self.datatb = FreqAccTestTableDB(Debug=FreqAccTestMain)
        """DataBaseSettings = {
            'user': 'postgres',
            'password': 'Platinum0435#',
            'host': 'localhost',
            'database': 'atec',
            'port': 6543
        }
        dbStatus =  self.indxtb.connect(DataBaseSettings)
        self.datatb.connection =  self.indxtb.connection"""

        """if dbStatus != SUCCESS:
            msgbox = QMessageBox()
            msgbox.setWindowIcon(QIcon('Resources/PlatinumLogo.ico'))
            msgbox.setWindowTitle('Connect Database')
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText('Unable to Establish Connection with Database Server\nDo You Want to Proceed')
            msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgReply = msgbox.exec_()
            if msgReply == QMessageBox.No:
                print()
                return"""
        self.AppendNewRecordtoIndxTable()
    ###################################################################################################################
    def AppendNewRecordtoIndxTable(self):
        timestamp = datetime.datetime.now()
        table_ref_id = f'''{self.comboBox_System.currentText().lower()}freqacctest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
        print(table_ref_id)
        freq_list = [123.6, 167, 189]
        if self.CB_SigCat_Freq.currentText() == "CW":
            self.lineEdit_pw.setDisabled(True)
            self.lineEdit_pri.setDisabled(True)
            newrow = {'date': timestamp, 'username': 'ravi', 'system_id': 1, 'system': 'RWR', 'mode': 'INJECTION',
                      'test_tab_ref': table_ref_id, 'start_freq' : 500, 'stop_freq' : 1000, 'step_freq' : 50,
                      'freq_list' : freq_list, 'set_power': -30, 'pos_angle': 140, 'signal_cat': 'CW', 'pw': 0,
                      'pri': 0, 'ampl': 850, 'rms_error': 1, 'test_status': 'Incomplete', 'remarks': 'new row added'}
            self.indxtb.AddFreqRow(usercred=newrow)
            self.datatb.tablename = table_ref_id
        elif  self.CB_SigCat_Freq.currentText() == "PULSE":
             newrow = {'date': timestamp, 'username': 'ravi', 'system_id': 1, 'system': 'RWR', 'mode': 'INJECTION',
                      'test_tab_ref': table_ref_id, 'start_freq' : 500, 'stop_freq' : 1000, 'step_freq' : 50,
                      'freq_list' : freq_list, 'set_power': -30, 'pos_angle': 140, 'signal_cat': 'PULSE', 'pw': 0,
                      'pri': 0, 'ampl': 850, 'rms_error': 1, 'test_status': 'Incomplete', 'remarks': 'new row added'}
             self.indxtb.AddFreqRow(usercred=newrow)
             self.datatb.tablename =table_ref_id
        self.CreateDataTable()

  ####################################################################################################################
    def AppendtoDataTable(self, newrow={'set_freq':500,'meas_freq':4,'error':5}):
        self.datatb.Debug = True
        test_record={'set_freq' :newrow['set_freq'] , 'meas_freq' : newrow['meas_freq'], 'error' : newrow['error'] }
        self.datatb.AddFreqRow(freqtestvalues=test_record)

    ####################################################################################################################
    def CreateDataTable(self):
        self.datatb.CreateFreqAccTestTableDB()

########################################################################################################################
    # This Function call All Functions & Class closes the connection of PostgreSQL
########################################################################################################################

if __name__=='__main__':
    freqaccapp=QApplication(sys.argv)
    freqaccmain=FreqAccTestMain()
    freqaccmain.show()
    sys.exit(freqaccapp.exec_())