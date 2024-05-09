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
from DataBase.INDXTBDB.PWMeasIndxTableDB import PwMeasIndxTableDB
from DataBase.TESTTBDB.PwMeasTestTableDB import PwMeasTestTableDB
from DataBase.TESTSWMOD.PwAccTestP import Ui_PwAccTest


########################################################################################################################
#  Pulse Width Measurement Test Table Database Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   10 Mar 2023
#   PwMeasTestMain Class has following member Functions
#
########################################################################################################################
# This Creating the pwMeastestmain Class
########################################################################################################################
class PwMeasTestMain(QMainWindow, Ui_PwAccTest):
    def __init__(self):
        super(PwMeasTestMain,self).__init__()
        self.setupUi(self)
        self.indxtbpw = PwMeasIndxTableDB()
        self.datatb = PwMeasTestTableDB()
        self.PB_Close_PW.clicked.connect(self.CloseProcess)
        self.PB_Save_PW.clicked.connect(self.SaveProcess)
        self.PB_Step_PW.clicked.connect(self.StepModeProcess)
        self.PB_Run_PW.clicked.connect(self.RuNModeProcess)
        self.PB_Pause_PW.clicked.connect(self.PauseProcess)
        self.PB_Abort_PW.clicked.connect(self.AbortProcess)
        self.PB_Continue_PW.clicked.connect(self.ContinueProcess)
        self.PB_Print_PW.clicked.connect(self.PrintProcess)
        #self.comboBox_System.currentTextChanged.connect(self.ComboTextSystem)
        # Read Configuration files Here if any Ex  database table names, default Data values, Previous Test Values
        #self.ConfigJSON = {'indxtabname' : 'pwMeasindxtable'}
        #print(self.ConfigJSON['indxtabname'])
        # initialise the variables here with previous Test Data Values
        self.PB_Save_PW.setDisabled(True)
        self.PB_Print_PW.setDisabled(True)
        self.PB_Pause_PW.setDisabled(True)
        self.PB_Continue_PW.setDisabled(True)
        self.PB_Abort_PW.setDisabled(True)
        self.InitVariables()
        self.CompletionFlag = True
    ####################################################################################################################
    # This Function Adds the data to gui table
    ####################################################################################################################
    def InitVariables(self):
        self.StartPw = float(self.lineEdit_start_pw.text())
        self.StopPw = float(self.lineEdit_stop_pw.text())
        self.StepPw = float(self.lineEdit_step_pw.text())
        self.SetPw = self.StartPw
        self.PauseFlag = False
        self.AbortFlag = False
        self.ContinueFlag = False
        self.tableWidget_pw.clear()
        #self.DBConnectTryFlag = False
        self.CompletionFlag = False
       # self.ConnectDB()
        self.row = 0
        self.tableWidget_pw.setColumnCount(3)
        self.tableWidget_pw.setHorizontalHeaderLabels(["Set PW\n(µs)", "Measured PW\n(µs)", "Error"])
        self.tableWidget_pw.resizeColumnToContents(0)
        self.tableWidget_pw.resizeColumnToContents(1)
        self.tableWidget_pw.resizeColumnToContents(2)
        self.tableWidget_pw.setColumnWidth(0, 150)
        self.tableWidget_pw.setColumnWidth(1, 150)
        self.tableWidget_pw.setColumnWidth(2, 100)
        self.tableWidget_pw.resize(550,400)
        self.SetProgressBar()
    ####################################################################################################################
    # This Function Adds the data to database index table
    ####################################################################################################################
    def StepModeProcess(self):
        if self.CompletionFlag == True:
            self.InitVariables()
        self.PB_Pause_PW.setDisabled(True)
        self.PB_Continue_PW.setDisabled(True)
        self.PB_Abort_PW.setDisabled(True)
        self.PB_Run_PW.setDisabled(True)
        self.PB_Close_PW.setDisabled(True)
        self.PB_Save_PW.setDisabled(True)
        self.PB_Print_PW.setDisabled(True)
        self.PB_Step_PW.setDisabled(True)
        QApplication.processEvents()
        self.PerformMeasurements()
        time.sleep(1)
        self.SetPw = self.SetPw + self.StepPw
        self.PB_Run_PW.setEnabled(True)
        self.PB_Save_PW.setEnabled(True)
        self.PB_Print_PW.setEnabled(True)
        self.PB_Close_PW.setEnabled(True)
        self.PB_Step_PW.setEnabled(True)
        QApplication.processEvents()
        self.SetProgressBar()
        if self.SetPw > self.StopPw:
            self.CompletionFlag = True
            self.PB_Pause_PW.setDisabled(True)
            self.PB_Continue_PW.setDisabled(True)
            self.PB_Abort_PW.setDisabled(True)
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def RuNModeProcess(self):
        self.InitVariables()
        self.PB_Pause_PW.setEnabled(True)
        self.PB_Continue_PW.setDisabled(True)
        self.PB_Abort_PW.setEnabled(True)
        self.PB_Run_PW.setDisabled(True)
        self.PB_Step_PW.setDisabled(True)
        self.PB_Close_PW.setDisabled(True)
        self.PB_Save_PW.setDisabled(True)
        self.PB_Print_PW.setDisabled(True)
        QApplication.processEvents()
        time.sleep(1)
        while self.SetPw <= self.StopPw:
            self.PerformMeasurements()
            self.SetProgressBar()

            QApplication.processEvents()
            time.sleep(1)
            self.SetPw = self.SetPw + self.StepPw
            if self.PauseFlag == True:
                self.PauseFlag = False
                return
            if self.AbortFlag == True:
                self.AbortFlag = False
                self.CompletionFlag = True
                return
        self.CompletionFlag = True
        self.PB_Run_PW.setEnabled(True)
        self.PB_Step_PW.setEnabled(True)
        self.PB_Pause_PW.setDisabled(True)
        self.PB_Continue_PW.setDisabled(True)
        self.PB_Abort_PW.setDisabled(True)

        self.PB_Print_PW.setEnabled(True)
        self.PB_Close_PW.setEnabled(True)
        self.PB_Save_PW.setEnabled(True)

    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def PerformMeasurements(self):
        MeasPw = self.SetPw + random.uniform(1,-1)        # SET PW+ RANDOM -0.05 TO +0.05
        self.tableWidget_pw.setRowCount(self.row + 1)
        self.tableWidget_pw.setItem(self.row, 0, QTableWidgetItem(str(self.SetPw)))
        self.tableWidget_pw.setItem(self.row, 1, QTableWidgetItem(str(MeasPw)))
        Error=self.SetPw - MeasPw
        self.tableWidget_pw.setItem(self.row, 2, QTableWidgetItem(str(Error)))
        newrow = {'set_pw': self.SetPw, 'meas_pw': MeasPw, 'error': Error}
        self.AppendtoDataTable(newrow)

        # table vertical scrolling
        tabvertscroll = self.tableWidget_pw.item(self.row, 0)
        self.tableWidget_pw.scrollToItem(tabvertscroll, QAbstractItemView.PositionAtTop)
        self.tableWidget_pw.selectRow(self.row)
        self.row = self.row + 1


    ###################################################################################################################
    # Enabling or disabling Pause process
    #
    ###################################################################################################################
    def PauseProcess(self):
        self.PauseFlag = True
        self.PB_Close_PW.setEnabled(True)
        self.PB_Pause_PW.setDisabled(True)
        self.PB_Step_PW.setEnabled(True)
        self.PB_Continue_PW.setEnabled(True)
    ###################################################################################################################
    # This function stops the ongoing test forcefully
    #
    ###################################################################################################################
    def AbortProcess(self):
        self.AbortFlag = True
        self.PB_Pause_PW.setDisabled(True)
        self.PB_Continue_PW.setDisabled(True)
        self.PB_Abort_PW.setDisabled(True)
        self.PB_Run_PW.setEnabled(True)
        self.PB_Step_PW.setEnabled(True)
        self.PB_Save_PW.setEnabled(True)
        self.PB_Print_PW.setEnabled(True)
        self.PB_Close_PW.setEnabled(True)

    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def SetProgressBar(self):
        No_of_steps = ((self.StopPw-self.StartPw)) / self.StepPw + 1
        percentage_of_completion = int(self.row*100/No_of_steps)
        self.progressBar_pw.setValue(percentage_of_completion)
        self.lineEdit_pw_PB.setText(str(percentage_of_completion))
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
        sheetonename = f'''{self.comboBox_System.currentText().lower()}pwMeastest{timestamp.strftime("%Y_%m_%d_%H_%M")}'''
        sheettwoname=self.ConfigJSON['indxtabname']+timestamp.strftime("%Y_%m_%d")
        sheet1 = workbook.active
        sheet1.title =sheetonename
        sheet2 = workbook.create_sheet(sheettwoname)
        # Construct test worksheets with some content.
        sheet1['A1'] = 'Set PW(µs)'
        sheet1['B1'] = 'Measure PW(µs)'
        sheet1['C1'] = 'Error'
        sheet1['A1'].font = Font(bold=True)         #for Font type
        sheet1['B1'].font = Font(bold=True)
        sheet1['C1'].font = Font(bold=True)
        sheet1['A1'].alignment = Alignment(horizontal='center')         #for text alignment for headers
        sheet1['B1'].alignment = Alignment(horizontal='center')
        sheet1['C1'].alignment = Alignment(horizontal='center')
        sheet2['A1'].alignment = Alignment(horizontal='center')
        sheet2['B1'].alignment = Alignment(horizontal='center')
        for i in range(0,self.tableWidget_pw.rowCount()):
            sheet1[f'''A{i-2 + 3}'''] = self.tableWidget_pw.item(i, 0).text()
            sheet1[f'''B{i-2 + 3}'''] = self.tableWidget_pw.item(i, 1).text()
            sheet1[f'''C{i-2 + 3}'''] = self.tableWidget_pw.item(i, 2).text()
        self.set_border(sheet1, f'''A1:C{3 + i-1}''')                    #for excel sheet table cell borders

        sheet2['A1'] = 'Parameter'
        sheet2['B1'] = 'Value'
        sheet2['A1'].font=Font(bold=True)
        sheet2['B1'].font = Font(bold=True)
        sheet1.column_dimensions['A'].width = 20                      #for Column width
        sheet1.column_dimensions['B'].width = 25
        sheet1.column_dimensions['C'].width = 9

        sheet2['A2'] = 'Start PW (µs)'
        sheet2['A3'] = 'Stop PW (µs)'
        sheet2['A4'] = 'Step PW (µs)'
        sheet2['A5'] = 'Servo Position'
        sheet2['A6'] = 'Signal Category'
        sheet2['A7'] = 'Frequency'
        sheet2['A8'] = 'PRI'
        sheet2['A9'] = 'Power'

        sheet2['B2'] = float(self.lineEdit_start_pw.text())
        sheet2['B3'] = float(self.lineEdit_stop_pw.text())
        sheet2['B4'] = float(self.lineEdit_step_pw.text())
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
        outfile = sysnamecache +"PwMeas" + datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '.xlsx'
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
        if dialog.exec_() == QPrintDialog.Measepted:
            self.handlePaintRequest(printer)

    def handlePaintRequest(self, printer):
        painter = QPainter()
        painter.begin(printer)
        self.tableWidget_pw.render(painter)
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def CloseProcess(self):
        self.close()
        self.indxtbpw.close()
    ###################################################################################################################
    # Establish Connection with Database
    #
    ###################################################################################################################
    def ConnectDB(self):
        """#self.DBConnectTryFlag = True
        self.indxtbpw = PwMeasIndxTableDB(Debug=True)
        #self.indxtbpw.tablename = self.ConfigJSON['indxtabname']
        self.datatb = PwMeasTestTableDB(Debug=PwMeasTestMain)
        DataBaseSettings = {
            'user': 'postgres',
            'password': 'Platinum0435#',
            'host': 'localhost',
            'database': 'atec',
            'port': 6543
        }
        dbStatus =  self.indxtbpw.connect(DataBaseSettings)
        self.datatb.connection =  self.indxtbpw.connection

        if dbStatus != SUCCESS:
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
        table_ref_id = f'''{self.comboBox_System.currentText().lower()}pwMeastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
        print(table_ref_id)
        pw_list = [123.6, 167, 189]
        if self.CB_SigCat_pw.currentText() == "PULSE":
            newrow = {'date': timestamp, 'username': 'ravi', 'system_id': 1, 'system': self.comboBox_System , 'mode': self.comboBox_Mode_pw,
                      'test_tab_ref': table_ref_id, 'start_pw' : 500, 'stop_pw' : 1000, 'step_pw' : 50,
                      'pw_list' : pw_list, 'set_power': -30, 'pos_angle': 140, 'signal_cat': 'CW', 'freq': 1500,
                      'pri': 0, 'ampl': 850, 'rms_error': 1, 'test_status': 'Incomplete', 'remarks': 'new row added'}
            self.indxtbpw.AddPwRecord(usercred=newrow)
            self.datatb.tablename = table_ref_id
        elif  self.CB_SigCat_pw.currentText() == "CW":
            self.lineEdit_pw.setDisabled(True)
            self.lineEdit_pri.setDisabled(True)
            newrow = {'date': timestamp, 'username': 'ravi', 'system_id': 1, 'system': self.comboBox_System , 'mode': self.comboBox_Mode_pw,
                      'test_tab_ref': table_ref_id, 'start_pw' : 500, 'stop_pw' : 1000, 'step_pw' : 50,
                      'pw_list' : pw_list, 'set_power': -30, 'pos_angle': 140, 'signal_cat': 'PULSE', 'freq': 0,
                      'pri': 0, 'ampl': 850, 'rms_error': 1, 'test_status': 'Incomplete', 'remarks': 'new row added'}
            self.indxtbpw.AddPwRecord(usercred=newrow)
            self.datatb.tablename =table_ref_id
        self.CreateDataTable()

  ####################################################################################################################
    def AppendtoDataTable(self, newrow={'set_pw':500,'meas_pw':4,'error':5}):
        self.datatb.Debug = True
        test_record={'set_pw' :newrow['set_pw'] , 'meas_pw' : newrow['meas_pw'], 'error' : newrow['error'] }
        self.datatb.AddPwTestRow(pwtestvalues=test_record)

    ####################################################################################################################
    def CreateDataTable(self):
        self.datatb.CreatePwMeasTestTableDB()

########################################################################################################################
    # This Function call All Functions & Class closes the connection of PostgreSQL
########################################################################################################################

if __name__=='__main__':
    pwMeasapp=QApplication(sys.argv)
    pwMeasmain=PwMeasTestMain()
    pwMeasmain.show()
    sys.exit(pwMeasapp.exec_())