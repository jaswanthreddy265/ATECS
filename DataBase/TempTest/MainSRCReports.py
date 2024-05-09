import random
import sys

import pyqtgraph
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QAbstractItemView

from DataBase.INDXTBDB.AmplAccIndxTableDB import AmplAccIndxTableDB
from DataBase.INDXTBDB.DOAMeasIndxTableDB import DoaMeasIndxTableDB
from DataBase.INDXTBDB.FreqAccIndxTableDB import FreqAccIndxTableDB
from DataBase.INDXTBDB.PRIMeasIndxTableDB import PriMeasIndxTableDB
from DataBase.INDXTBDB.PWMeasIndxTableDB import PwMeasIndxTableDB
from DataBase.INDXTBDB.SensMeasAccIndxTableDB import SensMeasIndxTableDB
from DataBase.TESTTBDB.FreqAccTestTableDB import FreqAccTestTableDB
from DataBase.TESTTBDB.PwMeasTestTableDB import PwMeasTestTableDB
from MainSrc.MainSRC import Ui_ATEC_App

########################################################################################################################
class MainGUI(QMainWindow, Ui_ATEC_App):
    def __init__(self):
        super(MainGUI, self).__init__()
        pyqtgraph.setConfigOption('background', (255, 255, 255))
        self.setupUi(self)

        # Graphs Disabled for Network Setting
        self.frame_NET_ESMTracks.setDisabled(True)
        self.frame_NET_RFPS.setDisabled(True)
        self.frame_NET_ErrorGraphs.setDisabled(True)
        self.frame_NET_PolarPlot.setDisabled(True)


        # ReportsBin Tab

        self.PB_Get.clicked.connect(self.ATECDataRetrieve)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        #self.tableWidget.keyPressEvent()
        #self.tableWidget.clicked.connect(self.TableKeyValue)

        self.PlotGraph = self.Reports_ErrorGraph.addPlot()

#        self.PlotGraph = self.PlotGraph.setBackground("w")
        self.PB_Plot.clicked.connect(self.TableKeyValue)

        # Buttons
        self.PB_System.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.System_Parameters))
        self.PB_SubSystem.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Subsystem_Parameters))
        self.PB_Complex.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.ComplexEmiiter_Parameters))
        self.PB_Reports.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.Reports_Parameters))
        self.PB_NetWork.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.Network_Parameters))
        self.PB_View.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.View_parameters))
        self.PB_Help.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.Help_Parameters))

        self.PB_System.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.System_Graphs))
        self.PB_SubSystem.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.Subsystem_Graphs))
        self.PB_Complex.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.ComplexEmitter_Graphs))
        self.PB_Reports.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.Reports_Graphs))
        self.PB_NetWork.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.Network_Graphs))
        self.PB_View.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.View_Graphs))
        self.PB_Help.clicked.connect(lambda:self.stackedWidget_2.setCurrentWidget(self.Help_Docs))

        # File Browser
        self.PB_Report_PC.clicked.connect(self.file_open)

        # Graphs
        self.sys_error = self.SYS_ErrorGraph.addPlot(row=0, col=0)
        self.sys_polar = self.SYS_PolarPlot.addPlot(row=0, col=0)

        self.subsys_error = self.SUBSYS_ErrorGraph.addPlot(row=0, col=0)
        self.subsys_polar = self.SUBSYS_PolarPlot.addPlot(row=0, col=0)

        self.emitter_error = self.Emitter_ErrorGraph.addPlot(row=0, col=0)
        self.emitter_polar = self.Emitter_PolarPlot.addPlot(row=0, col=0)

        self.network_error = self.Network_ErrorGraph.addPlot(row=0, col=0)
        self.network_polar = self.Network_PolarPlot.addPlot(row=0, col=0)
        self.networ_rfps = self.Network_RFPSGraph.addPlot(row=0, col=0)

        self.view_error=self.View_ErrorGraph.addPlot(row=0, col=0)
        self.view_polar=self.View_PolarPlot.addPlot(row=0, col=0)
        self.view_rfps=self.View_RFPSGraph.addPlot(row=0, col=0)

        self.Add.clicked.connect(self.Sys_Add)

        # Current date and time display to label
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start()

        self.graph_plot()

########################################################################################################################
    def showTime(self):
        self.time=QtCore.QDateTime.currentDateTime()
        self.timeDisplay=self.time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.label_date.setText(self.timeDisplay)

########################################################################################################################

    def Sys_Add(self):
        if self.ESM.isChecked():
            if self.Injection.isChecked():

                if self.Frequency.isChecked():
                    self.listWidget_test.addItem("ESM Injection Frequency Test")
                    print("ESM Injection Frequency Test")

                elif self.Amplitude.isChecked():
                    self.listWidget_test.addItem("ESM Injection Amplitude Test")
                    print("ESM Injection Amplitude Test")

                elif self.Sensitivity.isChecked():
                    self.listWidget_test.addItem("ESM Injection Sensitivity Test")
                    print("ESM Injection Sensitivity Test")

                elif self.PW.isChecked():
                    self.listWidget_test.addItem("ESM Injection PW Test")
                    print("ESM Injection PW Test")

                elif self.PRI.isChecked():
                    self.listWidget_test.addItem("ESM Injection PRI Test")
                    print("ESM Injection PRI Test")

                elif self.DOA.isChecked():
                    self.listWidget_test.addItem("ESM Injection DOA Test")
                    print("ESM Injection DOA Test")
                else:
                    print("Select Test")

            elif self.Radiation.isChecked():

                if self.Frequency.isChecked():
                    self.listWidget_test.addItem("ESM Radiation Frequency Test")
                    print("ESM Radiation Frequency Test")

                elif self.Amplitude.isChecked():
                    self.listWidget_test.addItem("ESM Radiation Amplitude Test")
                    print("ESM Radiation Amplitude Test")

                elif self.Sensitivity.isChecked():
                    self.listWidget_test.addItem("ESM Radiation Sensitivity Test")
                    print("ESM Radiation Sensitivity Test")

                elif self.PW.isChecked():
                    self.listWidget_test.addItem("ESM Radiation PW Test")
                    print("ESM Radiation PW Test")

                elif self.PRI.isChecked():
                    self.listWidget_test.addItem("ESM Radiation PRI Test")
                    print("ESM Radiation PRI Test")

                elif self.DOA.isChecked():
                    self.listWidget_test.addItem("ESM Radiation DOA Test")
                    print("ESM Radiation DOA Test")

                else:
                    print("Select Test")

            else:
                print("Select any Mode")
        else:
            print("Select any System")

########################################################################################################################
    def file_open(self):
        filenames,_=QFileDialog.getOpenFileNames(self,"Select a file",'',"All Files (*)")
        if filenames:
            print(filenames)
            self.listWidget_Reports.addItems([str(filename) for filename in filenames ])
########################################################################################################################
########################################################################################################################
    def ATECDataRetrieve(self):
        self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        if self.CB_Type_Report.currentText() == 'Frequency Test':
            self.PlotGraph.clear()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
            #self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
            GetFreqIndexTable = FreqAccIndxTableDB()
            GetFreqIndexTable.SelFreqDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
            freqaccindxtabledata=GetFreqIndexTable.FreqDateFil
            print(freqaccindxtabledata)
            freqdataappend = GetFreqIndexTable.FreqDateFil
            freqdataappend = freqdataappend.astype(str)
            no_of_rows = freqdataappend.shape[0]
            no_of_cols = freqdataappend.shape[1]
            for row in range(no_of_rows):
                self.tableWidget.setRowCount(row + 1)
                for col in range(no_of_cols):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(freqdataappend.iloc[row][col]))
            self.PlotGraph.setTitle('<font size="15"><strong>Frequency Accuracy Test</strong></font>', color='blue')
            self.PlotGraph.setLabel(
                "left",
                '<span style="color: purple; font-size: 18px">Error </span>'
            )
            self.PlotGraph.setLabel(
                "bottom",
                '<span style="color: green; font-size: 18px">Set Frequency (MHz)</span>'
            )
        elif self.CB_Type_Report.currentText() == 'Pulse Width Test':
            self.PlotGraph.clear()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
            GetPwIndexTable = PwMeasIndxTableDB()
            GetPwIndexTable.SelPwDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
            pwmeasindxtabledata=GetPwIndexTable.PwDateFil
            print(pwmeasindxtabledata)
            pwdataappend = GetPwIndexTable.PwDateFil
            pwdataappend = pwdataappend.astype(str)
            no_of_rows = pwdataappend.shape[0]
            no_of_cols = pwdataappend.shape[1]
            for row in range(no_of_rows):
                self.tableWidget.setRowCount(row + 1)
                for col in range(no_of_cols):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(pwdataappend.iloc[row][col]))
            self.PlotGraph.setTitle('<font size="15"><strong>Pulse Width Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel(
                "left",
                '<span style="color: purple; font-size: 18px">Error </span>'
            )
            self.PlotGraph.setLabel(
                "bottom",
                '<span style="color: green; font-size: 18px">Set Pulse Width (μs)</span>'
            )
        elif self.CB_Type_Report.currentText() == 'Pri Test':
            self.PlotGraph.clear()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
            GetPriIndexTable = PriMeasIndxTableDB()
            GetPriIndexTable.SelPriDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
            primeasindxtabledata=GetPriIndexTable.PriDateFil
            print(primeasindxtabledata)
            pridataappend = GetPriIndexTable.PriDateFil
            pridataappend = pridataappend.astype(str)
            no_of_rows = pridataappend.shape[0]
            no_of_cols = pridataappend.shape[1]
            for row in range(no_of_rows):
                self.tableWidget.setRowCount(row + 1)
                for col in range(no_of_cols):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(pridataappend.iloc[row][col]))
            self.PlotGraph.setTitle('<font size="15"><strong>PRI Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel(
                "left",
                '<span style="color: purple; font-size: 18px">Error </span>'
            )
            self.PlotGraph.setLabel(
                "bottom",
                '<span style="color: green; font-size: 18px">Set Pri (μs)</span>'
            )
        elif self.CB_Type_Report.currentText() == 'DOA Test':
            self.PlotGraph.clear()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
            GetDoaIndexTable = DoaMeasIndxTableDB()
            GetDoaIndexTable.SelDoaDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
            doameasindxtabledata=GetDoaIndexTable.DoaDateFil
            print(doameasindxtabledata)
            doadataappend = GetDoaIndexTable.DoaDateFil
            doadataappend = doadataappend.astype(str)
            no_of_rows = doadataappend.shape[0]
            no_of_cols = doadataappend.shape[1]
            for row in range(no_of_rows):
                self.tableWidget.setRowCount(row + 1)
                for col in range(no_of_cols):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(doadataappend.iloc[row][col]))
            self.PlotGraph.setTitle('<font size="15"><strong>DOA Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel(
                "left",
                '<span style="color: purple; font-size: 18px">Error </span>'
            )
            self.PlotGraph.setLabel(
                "bottom",
                '<span style="color: green; font-size: 18px">Set Angle (μs)</span>'
            )
        elif self.CB_Type_Report.currentText() == 'Amplitude Test':
            self.PlotGraph.clear()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
            GetAmplIndexTable = AmplAccIndxTableDB()
            GetAmplIndexTable.SelAmplDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
            amplaccindxtabledata=GetAmplIndexTable.AmplDateFil
            print(amplaccindxtabledata)
            ampldataappend = GetAmplIndexTable.AmplDateFil
            ampldataappend = ampldataappend.astype(str)
            no_of_rows = ampldataappend.shape[0]
            no_of_cols = ampldataappend.shape[1]
            for row in range(no_of_rows):
                self.tableWidget.setRowCount(row + 1)
                for col in range(no_of_cols):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(ampldataappend.iloc[row][col]))
            self.PlotGraph.setTitle('<font size="15"><strong>Amplitude Accuracy Test</strong></font>', color='blue')
            self.PlotGraph.setLabel(
                "left",
                '<span style="color: purple; font-size: 18px">Error </span>'
            )
            self.PlotGraph.setLabel(
                "bottom",
                '<span style="color: green; font-size: 18px">Set Amplitude (dBm)</span>'
            )
        elif self.CB_Type_Report.currentText() == 'Sensitivity Measurement Test':
            self.PlotGraph.clear()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
            GetSensIndexTable = SensMeasIndxTableDB()
            GetSensIndexTable.SelSensMeasDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
            sensmeasindxtabledata=GetSensIndexTable.SensMeasDateFil
            print(sensmeasindxtabledata)
            sensmeasdataappend = GetSensIndexTable.SensMeasDateFil
            sensmeasdataappend = sensmeasdataappend.astype(str)
            no_of_rows = sensmeasdataappend.shape[0]
            no_of_cols = sensmeasdataappend.shape[1]
            for row in range(no_of_rows):
                self.tableWidget.setRowCount(row + 1)
                for col in range(no_of_cols):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(sensmeasdataappend.iloc[row][col]))
            self.PlotGraph.setTitle('<font size="15"><strong>Sensitivity Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel(
                "left",
                '<span style="color: purple; font-size: 18px">Error </span>'
            )
            self.PlotGraph.setLabel(
                "bottom",
                '<span style="color: green; font-size: 18px">Set Freq (MHz)</span>'
            )
########################################################################################################################
########################################################################################################################
    def TableKeyValue(self):
        #self.tableWidget.QApplication.clipboard().setText(self.serialize(useSelection=True))
        self.PlotGraph.clear()
        TableRef = self.tableWidget.currentRow()
        self.create_new_list = []
        for col in range(self.tableWidget.columnCount()):
            value = self.tableWidget.item(TableRef, col).text()
            self.create_new_list.append(value)



        if self.CB_Type_Report.currentText() == 'Frequency Test':
            GetFreqTestTable = FreqAccTestTableDB()
            GetFreqTestTable.GetFreqAccTestTable(testtablename=self.create_new_list[5])
            #print(GetFreqTestTable.CurDbTableFreq)
            dfreadtoui = GetFreqTestTable.CurDbTableFreq
            leftlabel = dfreadtoui["set_freq"].tolist()
            self.setfreqvalue = [float(i) for i in leftlabel]
            bottomlabel = dfreadtoui["error"].tolist()
            self.errorvalue = [float(i) for i in bottomlabel]
            self.PlotGraph.addLegend()
            self.rgb_full = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            self.PlotGraph.plot(self.setfreqvalue, self.errorvalue, pen=pyqtgraph.mkPen(color=(self.rgb_full), width=2,
                                        style=QtCore.Qt.SolidLine), name=self.create_new_list[5])
        elif self.CB_Type_Report.currentText() == 'Pulse Width Test':
            GetPwTestTable = PwMeasTestTableDB()
            GetPwTestTable.GetPwMeasTestTable(testtablename=self.create_new_list[5])
            #print(GetPwTestTable.CurDbTablePw)
            dfreadtoui = GetPwTestTable.CurDbTablePw
            leftlabel = dfreadtoui["set_pw"].tolist()
            self.setpwvalue = [float(i) for i in leftlabel]
            bottomlabel = dfreadtoui["error"].tolist()
            self.errorvalue = [float(i) for i in bottomlabel]
            self.rgb_full=(random.randint(1,255), random.randint(1,255), random.randint(1,255))
            self.PlotGraph.addLegend()
            self.PlotGraph.plot(self.setpwvalue, self.errorvalue, pen = pyqtgraph.mkPen(color=(self.rgb_full), width=2, style=QtCore.Qt.SolidLine), name=self.create_new_list[5])
            #line2 = plt.plot(x, y2, pen='b', symbol='o', symbolPen='b', symbolBrush=0.2, name='blue')
########################################################################################################################
########################################################################################################################
    def graph_plot(self):
        x1 = [2, 3, 4, 5]
        y1 = [10, 20, 15, 5]
        self.sys_error.plot(x1, y1, pen='r')
        x2 = [2, 3, 4, 5, 9, 15, 18, 20]
        y2 = [19, 22, 16, 67, 22, 34, 45, 100]
        self.sys_polar.plot(x2, y2, pen='y')

        x3 = [2, 3, 4, 5]
        y3 = [5, 25, 2, 45]
        self.subsys_error.plot(x3, y3, pen='m')
        x4 = [2, 3, 4, 5, 9, 15, 18, 20]
        y4 = [10, 20, 30, 15, 25, 35, 20, 5]
        self.subsys_polar.plot(x4, y4, pen='c')

        x5 = [2, 3, 4, 5]
        y5 = [5, 25, 2, 45]
        self.emitter_error.plot(x5, y5, pen='c')
        x6 = [2, 3, 4, 5, 9, 15, 18, 20]
        y6 = [10, 20, 30, 15, 25, 35, 20, 5]
        self.emitter_polar.plot(x6, y6, pen='g')

        """net_x=[2,3,5,7]
        net_error=[2,4,5,9]
        net_polar=[1,9,2,4]
        net_rfps=[1,9,2,6]
        self.network_error.plot(net_x,net_error,pen='g')
        self.network_polar.plot(net_x,net_polar,pen='b')
        self.networ_rfps.plot(net_x,net_rfps,pen='c')

        view_x = [2, 3, 5, 7,10]
        view_error = [10, 20, 30, 15, 25]
        view_polar = [20, 30, 15, 25, 35]
        view_rfps = [19, 22, 16, 67, 22]
        self.view_error.plot(view_x, view_error, pen='c')
        self.view_polar.plot(view_x, view_polar, pen='r')
        self.view_rfps.plot(view_x, view_rfps, pen='y')"""

########################################################################################################################

########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainGUI()
    win.show()
    sys.exit(app.exec_())
