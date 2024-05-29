import random
import sys
import time

import pandas as pd
import pyqtgraph
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, Qt, QEasingCurve
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMdiSubWindow, QTableWidgetItem, QMessageBox, \
    QAbstractItemView

from Calibration.CalRfPathLoss import CalRfPathLoss
from DataBase.INDXTBDB.AmplAccIndxTableDB import AmplAccIndxTableDB
from DataBase.INDXTBDB.DOAMeasIndxTableDB import DoaMeasIndxTableDB
from DataBase.INDXTBDB.FreqAccIndxTableDB import FreqAccIndxTableDB
from DataBase.INDXTBDB.PRIMeasIndxTableDB import PriMeasIndxTableDB
from DataBase.INDXTBDB.PWMeasIndxTableDB import PwMeasIndxTableDB
from DataBase.INDXTBDB.SensMeasAccIndxTableDB import SensMeasIndxTableDB
from DataBase.RFPathLoss.RfPathLoss import RFPathLossDB
from DataBase.TESTTBDB.AmplAccTestTableDB import AmplAccTestTableDB
from DataBase.TESTTBDB.DoaMeasTestTableDB import DoaMeasTestTableDB
from DataBase.TESTTBDB.FreqAccTestTableDB import FreqAccTestTableDB
from DataBase.TESTTBDB.PriMeasTestTableDB import PriMeasTestTableDB
from DataBase.TESTTBDB.PwMeasTestTableDB import PwMeasTestTableDB
from DataBase.TESTTBDB.SensMeasTestTableDB import SensMeasTestTableDB
from MainSRC import Ui_ATEC_App
import pyqtgraph as pg

from Reports.ReportPrint import ReportPdf
from Reports.ReportSave import ReportExcel


########################################################################################################################
class MainGUI(QMainWindow, Ui_ATEC_App):
    def __init__(self):
        pyqtgraph.setConfigOption('background', (255, 255, 255))
        super(MainGUI, self).__init__()

        self.setupUi(self)

        # Flags for Floating Windows
        self.Esm_Flag = False
        self.Error_Flag = False
        self.rfps_Flag = False

        self.polar_Flag = False
        self.scatter_Flag = False
        self.hist_Flag = False

        #REPORTS TAB

        self.dateEdit_From.dateChanged.connect(self.ReportDate)
        self.dateEdit_To.dateChanged.connect(self.ReportDate)
        self.Reports_PB_Get.clicked.connect(self.ATECDataRetrieve)
        self.Reports_System.setDisabled(True)
        self.Reports_PB_Plot.setDisabled(True)
        self.Reports_Test.currentTextChanged.connect(self.SystemDisable)
        self.Reports_Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Reports_Table.horizontalHeader().setStretchLastSection(True)
        self.PlotGraph = self.Reports_ErrorGraph.addPlot()
        self.Reports_PB_Plot.clicked.connect(self.TableKeyValue)
        self.Reports_PB_Clear.clicked.connect(self.RemoveFilters)
        self.Reports_PB_Save.clicked.connect(self.SaveProcess)
        self.Reports_PB_Print.clicked.connect(self.printpreviewDialog)

        #CALIBRATION TAB
        self.row = 0
        self.PB_Rad_Calib.clicked.connect(self.CalibRfPathLoss)
        self.PB_Rad_Abort.setDisabled(True)
        self.RFPath_graph = self.RFPath_Loss_Graph.addPlot(row = 0, col = 0)
        self.PB_Export.clicked.connect(self.CalRfPathExport)
        self.PB_Update.clicked.connect(self.RfPathDBUpdate)

        # Graphs Disabled for Network Setting
        self.frame_NET_ESMTracks.setDisabled(True)
        self.frame_NET_RFPS.setDisabled(True)
        self.frame_NET_ErrorGraphs.setDisabled(True)
        self.frame_NET_PolarPlot.setDisabled(True)

        # Buttons
        self.PB_System.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.System_Parameters))
        self.PB_SubSystem.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Subsystem_Parameters))
        self.PB_Complex.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.ComplexEmiiter_Parameters))
        self.PB_Reports.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.Reports_Parameters))
        self.PB_NetWork.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.Network_Parameters))
        self.PB_View.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.View_parameters))
        self.PB_Help.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.Help_Parameters))
        self.PB_Calibration.clicked.connect(self.Calib_functions)
        #self.PB_Calibration.clicked.connect(lambda:self.status.hide())
        #self.PB_Calibration.clicked.connect(lambda :self.PB_Abort_Cal.setDisabled(True))

        self.PB_System.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.System_Graphs))
        self.PB_SubSystem.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.Subsystem_Graphs))
        self.PB_Complex.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.ComplexEmitter_Graphs))
        self.PB_Reports.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.Reports_Graphs))
        self.PB_NetWork.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.Network_Graphs))
        self.PB_View.clicked.connect(lambda :self.stackedWidget_2.setCurrentWidget(self.View_Graphs))
        self.PB_Help.clicked.connect(lambda:self.stackedWidget_2.setCurrentWidget(self.Help_Docs))
        self.PB_Calibration.clicked.connect(lambda:self.stackedWidget_2.setCurrentWidget(self.Calib_Window))

        # Add
        self.Sys_PB_Add.clicked.connect(self.Sys_Add)

        # File Browser
        self.Reports_PB_PC.clicked.connect(self.file_open)

        ########################### GRAPHS #############################
        ################################################################
        # Add markers(x,y co-ordinates) to label
        self.sys_label_Error = pg.LabelItem(justify='right')
        self.sys_label_polar = pg.LabelItem(justify='right')
        self.subsys_label_Error = pg.LabelItem(justify='right')
        self.subsys_label_polar = pg.LabelItem(justify='right')
        self.emitter_label_Error = pg.LabelItem(justify='right')
        self.emitter_label_polar = pg.LabelItem(justify='right')

        # Add labels to Graphics Layout widget variables
        self.Sys_ErrorGraph.addItem(self.sys_label_Error)
        self.Sys_PolarPlot.addItem(self.sys_label_polar)
        self.SubSys_ErrorGraph.addItem(self.subsys_label_Error)
        self.SubSys_PolarPlot.addItem(self.subsys_label_polar)
        self.Emitter_ErrorGraph.addItem(self.emitter_label_Error)
        self.Emitter_PolarPlot.addItem(self.emitter_label_polar)

        # Add plot to Graphics Layout widget variables from GUI
        self.sys_error = self.Sys_ErrorGraph.addPlot(row=0, col=0)
        self.sys_polar = self.Sys_PolarPlot.addPlot(row=0, col=0)

        self.subsys_error = self.SubSys_ErrorGraph.addPlot(row=0, col=0)
        self.subsys_polar = self.SubSys_PolarPlot.addPlot(row=0, col=0)

        self.emitter_error = self.Emitter_ErrorGraph.addPlot(row=0, col=0)
        self.emitter_polar = self.Emitter_PolarPlot.addPlot(row=0, col=0)

        self.network_error = self.Network_ErrorGraph.addPlot(row=0, col=0)
        self.network_polar = self.Network_PolarPlot.addPlot(row=0, col=0)

        self.view_error=self.View_ErrorGraph.addPlot(row=0, col=0)
        self.view_polar=self.View_PolarPlot.addPlot(row=0, col=0)

        self.graph_plot()

        # Floating Windows for View Tab
        self.View_ESM.clicked.connect(self.ESM_Plot)
        self.View_Polar.clicked.connect(self.Polar_Plot)
        self.View_Error.clicked.connect(self.Error_Plot)
        self.View_RFPS.clicked.connect(self.RFPS_Plot)
        self.View_Scatter.clicked.connect(self.Scatter_Plot)
        self.View_Hist.clicked.connect(self.Hist_Plot)

        # Current date and time display to label
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start()

        #Set Ip Address for Network Setting
        self.Net_ESMP.clicked.connect(self.ESMP_IpAdrees_Set)
        self.Net_RFPS.clicked.connect(self.RFPS_IpAddress_Set)
        self.Net_WBLRU.clicked.connect(self.WBLRU_IpAddress_Set)
        self.Net_DigitalRx.clicked.connect(self.DigitalRx_IpAddress_Set)
        self.Net_ATE.clicked.connect(self.ATE_IpAddress_Set)
        self.Net_SigGen.clicked.connect(self.SigGen_IpAddress_Set)
        self.Net_Spect_Anlyz.clicked.connect(self.SpecAnly_IpAddress_Set)
        self.Net_PSG.clicked.connect(self.Psg_IpAddress_Set)
        self.Net_Servo.clicked.connect(self.Servo_IpAddress_Set)
        self.Net_VNA.clicked.connect(self.VNA_IpAddress_Set)
        self.Net_FieldFox.clicked.connect(self.FieldFox_IpAddress_Set)

        self.PB_System.clicked.connect(self.SystemPage_Active)
        self.PB_SubSystem.clicked.connect(self.SubsystemPage_Active)
        self.PB_Complex.clicked.connect(self.EmitterPage_Active)
        self.PB_NetWork.clicked.connect(self.NetworkPage_Active)
        self.PB_Reports.clicked.connect(self.ReportsPage_Active)
        self.PB_View.clicked.connect(self.ViewPage_Active)
        self.PB_Help.clicked.connect(self.HelpPage_Active)
        self.PB_Calibration.clicked.connect(self.CalibPage_Active)

        # Calibration (system,Rf Path)
        self.Calib_RWR.clicked.connect(self.Calib_RwrConfig)
        self.Calib_Radiation.clicked.connect(self.Calib_RadConfig)
        self.Calib_Injection.clicked.connect(self.Calib_RadConfig)

########################################################################################################################
            ###################################Calibration###########################################
                                #################Cable Loss #########################
    def Calib_RadConfig(self):
        if self.Calib_Radiation.isChecked()==True:
            self.stackedWidget_2.setCurrentWidget(self.Cable_Loss)
            self.PB_Rad_Abort.setDisabled(True)
            self.Calib_RWR.setChecked(False)
            self.Calib_ESMP.setChecked(False)
            self.Calib_Injection.setChecked(False)
        if self.Calib_Injection.isChecked() == True:
            self.stackedWidget_2.setCurrentWidget(self.Cable_Loss)
            self.PB_Rad_Abort.setDisabled(True)
            self.Calib_Radiation.setChecked(False)
            self.Calib_RWR.setChecked(False)
            self.Calib_ESMP.setChecked(False)


                              ##################### System Calibration ################
    def Calib_RwrConfig(self):
        self.stackedWidget_2.setCurrentWidget(self.Calib_Window)
        self.Calib_Radiation.setChecked(False)
        self.Calib_Injection.setChecked(False)


                    ###### Calibration Parameters, status frame(hide),Abort (Disabled) ######
    def Calib_functions(self):
        self.stackedWidget.setCurrentWidget(self.Calib_Parameters)
        self.status.hide()
        self.PB_Abort_Cal.setDisabled(True)

               ########################Calibration End ############################

########################################################################################################################
    ##########################***************Button Activation in Page *************############################
    def SystemPage_Active(self):
        self.PB_System.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_SubSystem.setStyleSheet("background-color: None;")
        self.PB_SubSystem.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Complex.setStyleSheet("background-color: None;")
        self.PB_Complex.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_NetWork.setStyleSheet("background-color: None;")
        self.PB_NetWork.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Reports.setStyleSheet("background-color: None;")
        self.PB_Reports.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_View.setStyleSheet("background-color: None;")
        self.PB_View.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Help.setStyleSheet("background-color: None;")
        self.PB_Help.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Calibration.setStyleSheet("background-color: None;")
        self.PB_Calibration.setStyleSheet("color: rgb(0, 85, 255);")

    ###################################################################################
    def SubsystemPage_Active(self):
        self.PB_SubSystem.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_System.setStyleSheet("background-color: None;")
        self.PB_System.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Complex.setStyleSheet("background-color: None;")
        self.PB_Complex.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_NetWork.setStyleSheet("background-color: None;")
        self.PB_NetWork.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Reports.setStyleSheet("background-color: None;")
        self.PB_Reports.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_View.setStyleSheet("background-color: None;")
        self.PB_View.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Help.setStyleSheet("background-color: None;")
        self.PB_Help.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Calibration.setStyleSheet("background-color: None;")
        self.PB_Calibration.setStyleSheet("color: rgb(0, 85, 255);")

    ###################################################################################
    def EmitterPage_Active(self):
        self.PB_Complex.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_System.setStyleSheet("background-color: None;")
        self.PB_System.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_SubSystem.setStyleSheet("background-color: None;")
        self.PB_SubSystem.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_NetWork.setStyleSheet("background-color: None;")
        self.PB_NetWork.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Reports.setStyleSheet("background-color: None;")
        self.PB_Reports.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_View.setStyleSheet("background-color: None;")
        self.PB_View.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Help.setStyleSheet("background-color: None;")
        self.PB_Help.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Calibration.setStyleSheet("background-color: None;")
        self.PB_Calibration.setStyleSheet("color: rgb(0, 85, 255);")

    ###################################################################################
    def NetworkPage_Active(self):
        self.PB_NetWork.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_System.setStyleSheet("background-color: None;")
        self.PB_System.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_SubSystem.setStyleSheet("background-color: None;")
        self.PB_SubSystem.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Complex.setStyleSheet("background-color: None;")
        self.PB_Complex.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Reports.setStyleSheet("background-color: None;")
        self.PB_Reports.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_View.setStyleSheet("background-color: None;")
        self.PB_View.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Help.setStyleSheet("background-color: None;")
        self.PB_Help.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Calibration.setStyleSheet("background-color: None;")
        self.PB_Calibration.setStyleSheet("color: rgb(0, 85, 255);")

    ###################################################################################
    def ReportsPage_Active(self):
        self.PB_Reports.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_System.setStyleSheet("background-color: None;")
        self.PB_System.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_SubSystem.setStyleSheet("background-color: None;")
        self.PB_SubSystem.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Complex.setStyleSheet("background-color: None;")
        self.PB_Complex.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_NetWork.setStyleSheet("background-color: None;")
        self.PB_NetWork.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_View.setStyleSheet("background-color: None;")
        self.PB_View.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Help.setStyleSheet("background-color: None;")
        self.PB_Help.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Calibration.setStyleSheet("background-color: None;")
        self.PB_Calibration.setStyleSheet("color: rgb(0, 85, 255);")

    ###################################################################################
    def ViewPage_Active(self):
        self.PB_View.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_System.setStyleSheet("background-color: None;")
        self.PB_System.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_SubSystem.setStyleSheet("background-color: None;")
        self.PB_SubSystem.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Complex.setStyleSheet("background-color: None;")
        self.PB_Complex.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_NetWork.setStyleSheet("background-color: None;")
        self.PB_NetWork.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Reports.setStyleSheet("background-color: None;")
        self.PB_Reports.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Help.setStyleSheet("background-color: None;")
        self.PB_Help.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Calibration.setStyleSheet("background-color: None;")
        self.PB_Calibration.setStyleSheet("color: rgb(0, 85, 255);")

    ###################################################################################
    def HelpPage_Active(self):
        self.PB_Help.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_System.setStyleSheet("background-color: None;")
        self.PB_System.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_SubSystem.setStyleSheet("background-color: None;")
        self.PB_SubSystem.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Complex.setStyleSheet("background-color: None;")
        self.PB_Complex.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_NetWork.setStyleSheet("background-color: None;")
        self.PB_NetWork.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Reports.setStyleSheet("background-color: None;")
        self.PB_Reports.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_View.setStyleSheet("background-color: None;")
        self.PB_View.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Calibration.setStyleSheet("background-color: None;")
        self.PB_Calibration.setStyleSheet("color: rgb(0, 85, 255);")
    def CalibPage_Active(self):

        self.PB_Calibration.setStyleSheet("background-color: rgb(255, 181, 166);")
        self.PB_System.setStyleSheet("background-color: None;")
        self.PB_System.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_SubSystem.setStyleSheet("background-color: None;")
        self.PB_SubSystem.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Complex.setStyleSheet("background-color: None;")
        self.PB_Complex.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_NetWork.setStyleSheet("background-color: None;")
        self.PB_NetWork.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Reports.setStyleSheet("background-color: None;")
        self.PB_Reports.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_View.setStyleSheet("background-color: None;")
        self.PB_View.setStyleSheet("color: rgb(0, 85, 255);")
        self.PB_Help.setStyleSheet("background-color: None;")
        self.PB_Help.setStyleSheet("color: rgb(0, 85, 255);")

        ###########***************Button Activation Page End ***************#########
########################################################################################################################

########################################################################################################################
                         ########### ****************MARKER POINTS ************##########
    def SysError_onClick(self, event):
        mousePoint = self.sys_error.vb.mapSceneToView(event._scenePos)
        sys_err_x = ("%.2f" % round(mousePoint.x(), 2))
        sys_err_y = ("%.2f" % round(mousePoint.y(), 2))
        self.sys_label_Error.setText("(x= {0} ,y= {1})".format(sys_err_x, sys_err_y))

    #################################################################################
    def SysPolar_onClick(self, event):
        polar_mousePoint = self.sys_polar.vb.mapSceneToView(event._scenePos)
        sys_polar_x = ("%.2f" % round(polar_mousePoint.x(), 2))
        sys_polar_y = ("%.2f" % round(polar_mousePoint.y(), 2))
        self.sys_label_polar.setText("(x= {0} ,y= {1})".format(sys_polar_x, sys_polar_y))

    ##################################################################################

    def SubSysError_onClick(self, event):
        mousePoint = self.subsys_error.vb.mapSceneToView(event._scenePos)
        subsys_err_x = ("%.2f" % round(mousePoint.x(), 2))
        subsys_err_y = ("%.2f" % round(mousePoint.y(), 2))
        self.subsys_label_Error.setText("(x= {0} ,y= {1})".format(subsys_err_x, subsys_err_y))

    ##################################################################################
    def SubSysPolar_onClick(self, event):
        polar_mousePoint = self.subsys_polar.vb.mapSceneToView(event._scenePos)
        subsys_polar_x = ("%.2f" % round(polar_mousePoint.x(), 2))
        subsys_polar_y = ("%.2f" % round(polar_mousePoint.y(), 2))
        self.subsys_label_polar.setText("(x= {0} ,y= {1})".format(subsys_polar_x, subsys_polar_y))

    def EmitterError_onClick(self, event):
        mousePoint = self.emitter_error.vb.mapSceneToView(event._scenePos)
        emitter_err_x = ("%.2f" % round(mousePoint.x(), 2))
        emitter_err_y = ("%.2f" % round(mousePoint.y(), 2))
        self.emitter_label_Error.setText("(x= {0} ,y= {1})".format(emitter_err_x, emitter_err_y))

    ###########################################################################################
    def EmitterPolar_onClick(self, event):
        polar_mousePoint = self.emitter_polar.vb.mapSceneToView(event._scenePos)
        emitter_polar_x = ("%.2f" % round(polar_mousePoint.x(), 2))
        emitter_polar_y = ("%.2f" % round(polar_mousePoint.y(), 2))
        self.emitter_label_polar.setText("(x= {0} ,y= {1})".format(emitter_polar_x, emitter_polar_y))
    ###########################################################################################
            ########### ****************MARKER POINTS END ************##########
########################################################################################################################

########################################################################################################################
                #################### Floating Subwindows ########################
    def ESM_Plot(self):
        sub = QMdiSubWindow()
        if self.Esm_Flag == False:
            sub.setWidget(self.subwindow_ESMP)
            sub.layout().addWidget(self.Subwin_ESMP_Widget)
            self.subwindow_esmp = self.mdiArea.addSubWindow(sub)
            self.subwindow_esmp.show()
            self.mdiArea.tileSubWindows()
            self.Esm_Flag = True

        elif self.Esm_Flag == True:
            self.subwindow_esmp.close()
            self.Esm_Flag = False
    #################################################################
    def Polar_Plot(self):
        if self.polar_Flag==False:
            sub = QMdiSubWindow()
            sub.setWidget(self.subwindow_Polar)
            sub.layout().addWidget(self.Subwin_Polar_Widget)
            self.subwindow_polar = self.mdiArea.addSubWindow(sub)
            self.subwindow_polar.show()
            self.mdiArea.tileSubWindows()
            self.polar_Flag=True

        elif self.polar_Flag == True:
            self.subwindow_polar.close()
            self.polar_Flag= False

    #################################################################
    def Error_Plot(self):
        if self.Error_Flag==False:
            sub = QMdiSubWindow()
            sub.setWidget(self.subwindow_Error)
            sub.layout().addWidget(self.Subwin_Error_Widget)
            self.subwindow_error = self.mdiArea.addSubWindow(sub)
            self.subwindow_error.show()
            self.mdiArea.tileSubWindows()
            self.Error_Flag=True

        elif self.Error_Flag == True:
            self.subwindow_error.close()
            self.Error_Flag = False

    ##################################################################
    def RFPS_Plot(self):
        if self.rfps_Flag == False:
            sub = QMdiSubWindow()
            sub.layout().addWidget(self.Subwin_RFPS_Widget)
            self.subwindow_rfps = self.mdiArea.addSubWindow(sub)
            self.subwindow_rfps.show()
            self.mdiArea.tileSubWindows()

            self.rfps_Flag = True

        elif self.rfps_Flag == True:
            self.subwindow_rfps.close()
            self.rfps_Flag = False

    ##########################################################################
    def Scatter_Plot(self):
        if self.scatter_Flag == False:
            sub = QMdiSubWindow()
            sub.setWidget(self.subwindow_Scatter)
            sub.layout().addWidget(self.Subwin_Scatter_Widget)
            self.subwindow_scatter = self.mdiArea.addSubWindow(sub)
            self.subwindow_scatter.show()
            self.mdiArea.tileSubWindows()

            self.scatter_Flag = True

        elif self.scatter_Flag == True:
            self.subwindow_scatter.close()
            self.scatter_Flag = False
    ########################################################################
    def Hist_Plot(self):
        if self.hist_Flag==False:
            sub = QMdiSubWindow()
            sub.setWidget(self.subwindow_Hist)
            sub.layout().addWidget(self.Subwin_Hist_Widget)
            self.subwindow_hist = self.mdiArea.addSubWindow(sub)
            self.subwindow_hist.show()
            self.mdiArea.tileSubWindows()

            self.hist_Flag=True

        elif self.hist_Flag == True:
            self.subwindow_hist.close()
            self.hist_Flag= False

                #################### Floating Subwindows END########################
########################################################################################################################
########################################################################################################################
    def showTime(self):
        self.time=QtCore.QDateTime.currentDateTime()
        self.timeDisplay=self.time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.label_date.setText(self.timeDisplay)

########################################################################################################################
    def Sys_Add(self):
        if self.Sys_ESM.isChecked():
            if self.Sys_Injection.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--ESM->Injection->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--ESM->Injection->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--ESM->Injection->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--ESM->Injection->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--ESM->Injection->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--ESM->Injection->DOA->Test")
                else:
                    print("Select Test")

            elif self.Sys_Radiation.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--ESM->Radiation->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--ESM->Radiation->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--ESM->Radiation->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--ESM->Radiation->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--ESM->Radiation->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--ESM->Radiation->DOA Test")

                else:
                    print("Select Test")
            elif self.Sys_BTE.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--ESM->BTE->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--ESM->BTE->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--ESM->BTE->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--ESM->BTE->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--ESM->BTE->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--ESM->BTE->DOA Test")

                else:
                    print("Select Test")
            else:
                print("Select any Mode")

                    #########################################################
        elif self.Sys_RFPS.isChecked():
            if self.Sys_Injection.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--RFPS->Injection->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--RFPS->Injection->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--RFPS->Injection->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--RFPS->Injection->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--RFPS->Injection->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--RFPS->Injection->DOA->Test")
                else:
                    print("Select Test")

            elif self.Sys_Radiation.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--RFPS->Radiation->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--RFPS->Radiation->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--RFPS->Radiation->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--RFPS->Radiation->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--RFPS->Radiation->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--RFPS->Radiation->DOA Test")

                else:
                    print("Select Test")
            elif self.Sys_BTE.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--RFPS->BTE->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--RFPS->BTE->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--RFPS->BTE->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--RFPS->BTE->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--RFPS->BTE->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--RFPS->BTE->DOA Test")

                else:
                    print("Select Test")

            else:
                print("Select any Mode")

                ###########################################################
        elif self.Sys_Warner.isChecked():
            if self.Sys_Injection.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--Warner->Injection->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--Warner->Injection->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--Warner->Injection->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--Warner->Injection->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--Warner->Injection->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--Warner->Injection->DOA->Test")
                else:
                    print("Select Test")

            elif self.Sys_Radiation.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--Warner->Radiation->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--Warner->Radiation->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--Warner->Radiation->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--Warner->Radiation->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--Warner->Radiation->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--Warner->Radiation->DOA Test")

                else:
                    print("Select Test")
            elif self.Sys_BTE.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--Warner->BTE->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--Warner->BTE->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--Warner->BTE->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--Warner->BTE->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--Warner->BTE->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--Warner->BTE->DOA Test")

                else:
                    print("Select Test")
            else:
                print("Select any Mode")
        #######################################################################
        elif self.Sys_RWR.isChecked():
            if self.Sys_Injection.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--RWR->Injection->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--RWR->Injection->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--RWR->Injection->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--RWR->Injection->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--RWR->Injection->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--RWR->Injection->DOA->Test")
                else:
                    print("Select Test")

            elif self.Sys_Radiation.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--RWR->Radiation->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--RWR->Radiation->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--RWR->Radiation->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--RWR->Radiation->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--RWR->Radiation->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--RWR->Radiation->DOA Test")

                else:
                    print("Select Test")
            elif self.Sys_BTE.isChecked():
                if self.Sys_Frequency.isChecked():
                    self.listWidget_test.addItem("--RWR->BTE->Frequency Test")

                elif self.Sys_Amplitude.isChecked():
                    self.listWidget_test.addItem("--RWR->BTE->Amplitude Test")

                elif self.Sys_Sensitivity.isChecked():
                    self.listWidget_test.addItem("--RWR->BTE->Sensitivity Test")

                elif self.Sys_PW.isChecked():
                    self.listWidget_test.addItem("--RWR->BTE->PW Test")

                elif self.Sys_PRI.isChecked():
                    self.listWidget_test.addItem("--RWR->BTE->PRI Test")

                elif self.Sys_DOA.isChecked():
                    self.listWidget_test.addItem("--RWR->BTE->DOA Test")

                else:
                    print("Select Test")
            else:
                print("Select any Mode")
        else:
            print("Select any System")

########################################################################################################################
    def ESMP_IpAdrees_Set(self):

        self.Net_lineEdit_IPAdd.setText("192.168.1.100")
        self.Net_lineEdit_Port.setText("6500")
        self.Net_lineEdit_Speed.setText("25")

    def RFPS_IpAddress_Set(self):

        self.Net_lineEdit_IPAdd.setText("192.168.1.200")
        self.Net_lineEdit_Port.setText("5500")
        self.Net_lineEdit_Speed.setText("78")
    def WBLRU_IpAddress_Set(self):

        self.Net_lineEdit_IPAdd.setText("192.168.1.150")
        self.Net_lineEdit_Port.setText("7500")
        self.Net_lineEdit_Speed.setText("120")

    def DigitalRx_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.150.0.125")
        self.Net_lineEdit_Port.setText("8542")
        self.Net_lineEdit_Speed.setText("130")

    def ATE_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.150.0.125")
        self.Net_lineEdit_Port.setText("8500")
        self.Net_lineEdit_Speed.setText("200")

    def SigGen_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.150.0.125")
        self.Net_lineEdit_Port.setText("8700")
        self.Net_lineEdit_Speed.setText("500")

    def SpecAnly_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.100.0.140")
        self.Net_lineEdit_Port.setText("5000")
        self.Net_lineEdit_Speed.setText("150")

    def Psg_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.170.0.100")
        self.Net_lineEdit_Port.setText("7000")
        self.Net_lineEdit_Speed.setText("150")

    def Servo_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.100.0.150")
        self.Net_lineEdit_Port.setText("8900")
        self.Net_lineEdit_Speed.setText("100")

    def VNA_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.100.0.100")
        self.Net_lineEdit_Port.setText("5000")
        self.Net_lineEdit_Speed.setText("100")

    def FieldFox_IpAddress_Set(self):
        self.Net_lineEdit_IPAdd.setText("192.100.0.150")
        self.Net_lineEdit_Port.setText("7000")
        self.Net_lineEdit_Speed.setText("150")

########################################################################################################################
    def file_open(self):
        filenames,_=QFileDialog.getOpenFileNames(self,"Select a file",'',"All Files (*)")
        if filenames:
            print(filenames)
            self.listWidget_Reports.addItems([str(filename) for filename in filenames ])
########################################################################################################################
    def graph_plot(self):
        x1 = [2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
        y1 = [10, 20, 15, 5, 30, 40, 25, 30, 20, 45, 55, 40, 89, 67, 70, 59, 90, 55, 65, 83]
        self.sys_error.plot(x1, y1, pen='r')
        self.sys_error.scene().sigMouseClicked.connect(self.SysError_onClick)                        # Display markers(x,y coordinates) from function(self.SysError_onClick())

        x2 = [2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
        y2 = [19, 22, 16, 67, 22, 34, 45, 100, 50, 70, 55, 40, 78, 56, 89, 75, 30, 25, 58, 69]
        self.sys_polar.plot(x2, y2, pen='b')
        self.sys_polar.scene().sigMouseClicked.connect(self.SysPolar_onClick)                        # Display markers(x,y coordinates) from function(self.SysPolar_onClick())

        x3 = [2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
        y3 = [5, 25, 2, 45, 36, 49, 24, 37, 48, 53, 20, 15, 55, 38, 89, 72, 64, 58, 90, 82]
        self.subsys_error.plot(x3, y3, pen='m')
        self.subsys_error.scene().sigMouseClicked.connect(self.SubSysError_onClick)                  # Display markers(x,y coordinates) from function(self.SubSysError_onClick())

        x4 = [2, 3, 4, 5, 9, 15, 18, 20, 25, 30, 35, 43, 49, 55, 59, 65, 70, 74, 87, 95]
        y4 = [10, 20, 30, 15, 25, 35, 20, 5, 27, 35, 15, 36, 19, 49, 42, 56, 64, 34, 78, 87]
        self.subsys_polar.plot(x4, y4, pen='c')
        self.subsys_polar.scene().sigMouseClicked.connect(self.SubSysPolar_onClick)                  # Display markers(x,y coordinates) from function(self.SubSysPolar_onClick())

        x5 = [2, 3, 4, 5]
        y5 = [5, 25, 2, 45]
        self.emitter_error.plot(x5, y5, pen='c')
        self.emitter_error.scene().sigMouseClicked.connect(self.EmitterError_onClick)                # Display markers(x,y coordinates) from function(self.EmitterError_onClick())
        x6 = [2, 3, 4, 5, 9, 15, 18, 20]
        y6 = [10, 20, 30, 15, 25, 35, 20, 5]
        self.emitter_polar.plot(x6, y6, pen='g')
        self.emitter_polar.scene().sigMouseClicked.connect(self.EmitterPolar_onClick)                # Display markers(x,y coordinates) from function(self.EmitterPolar_onClick())

        view_x = [2, 3, 5, 7,10]
        view_error = [10, 20, 30, 15, 25]
        view_polar = [20, 30, 15, 25, 35]
        self.view_error.plot(view_x, view_error, pen='c')
        self.view_polar.plot(view_x, view_polar, pen='r')

########################################################################################################################
#############################************************DATABASE*********************######################################
    def ATECDataRetrieve(self):
        self.Reports_Table.setRowCount(0)
        if self.Reports_Test.currentText() == 'All':
            self.Reports_ErrorGraph.hide()
            self.Reports_Table.clear()
            self.Reports_Table.setColumnCount(7)
            self.Reports_Table.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref', 'Test'])
            GetFreqIndexTable = FreqAccIndxTableDB()
            GetFreqIndexTable.SelFreqDateFilter(datefilterfrom=self.dateEdit_From.text(),
                                                datefilterto=self.dateEdit_To.text())
            freqdataappend = GetFreqIndexTable.FreqDateFil
            freqdataappend.insert(6, "testname", 'Frequency Test', True)
            freqdataappend = freqdataappend.astype(str)
            #####
            GetPwIndexTable = PwMeasIndxTableDB()
            GetPwIndexTable.SelPwDateFilter(datefilterfrom=self.dateEdit_From.text(),
                                            datefilterto=self.dateEdit_To.text())
            pwdataappend = GetPwIndexTable.PwDateFil
            pwdataappend.insert(6, "testname", 'Pulse Width Test', True)
            pwdataappend = pwdataappend.astype(str)
            ##################
            GetPriIndexTable = PriMeasIndxTableDB()
            GetPriIndexTable.SelPriDateFilter(datefilterfrom=self.dateEdit_From.text(),
                                              datefilterto=self.dateEdit_To.text())
            pridataappend = GetPriIndexTable.PriDateFil
            print(pridataappend)
            pridataappend.insert(6, "testname", 'PRI Test', True)
            pridataappend = pridataappend.astype(str)
            ################
            GetAmplIndexTable = AmplAccIndxTableDB()
            GetAmplIndexTable.SelAmplDateFilter(datefilterfrom=self.dateEdit_From.text(),
                                                datefilterto=self.dateEdit_To.text())
            ampldataappend = GetAmplIndexTable.AmplDateFil
            ampldataappend.insert(6, "testname", 'Amplitude Test', True)
            ampldataappend = ampldataappend.astype(str)
            #################
            GetDoaIndexTable = DoaMeasIndxTableDB()
            GetDoaIndexTable.SelDoaDateFilter(datefilterfrom=self.dateEdit_From.text(),
                                              datefilterto=self.dateEdit_To.text())
            doadataappend = GetDoaIndexTable.DoaDateFil
            doadataappend.insert(6, "testname", 'DOA Test', True)
            doadataappend = doadataappend.astype(str)
            ####################
            GetSensMeasIndexTable = SensMeasIndxTableDB()
            GetSensMeasIndexTable.SelSensMeasDateFilter(datefilterfrom=self.dateEdit_From.text(),
                                                        datefilterto=self.dateEdit_To.text())
            sensmeasdataappend = GetSensMeasIndexTable.SensMeasDateFil
            sensmeasdataappend.insert(6, "testname", 'Sensitivity Test', True)
            sensmeasdataappend = sensmeasdataappend.astype(str)
            #######################
            dataappend = pd.concat( [freqdataappend, pwdataappend, pridataappend, ampldataappend, doadataappend, sensmeasdataappend],
                ignore_index=True)
            print(dataappend)
            self.PlotGraph.setLabel( "left", '<span style="color: purple; font-size: 18px">Error </span>' )

        elif (self.Reports_Test.currentText() == 'Frequency Test'):
            self.Reports_ErrorGraph.show()
            self.Reports_Table.setColumnCount(6)
            self.Reports_Table.clear()
            GetFreqIndexTable = FreqAccIndxTableDB()
            if self.Reports_System.currentText() == 'All' :
                GetFreqIndexTable.SelFreqDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
                dataappend = GetFreqIndexTable.FreqDateFil
            else:
                GetFreqIndexTable.SelFreqDateSysFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text(), sysfilter=self.Reports_System.currentText().lower())
                dataappend = GetFreqIndexTable.FreqDateSysFil
            self.PlotGraph.setTitle('<font size="15"><strong>Frequency Accuracy Test</strong></font>', color='blue')
            self.PlotGraph.setLabel( "bottom", '<span style="color: green; font-size: 18px">Set Frequency (MHz)</span>' )
        elif self.Reports_Test.currentText() == 'PulseWidth Test':
            self.Reports_ErrorGraph.show()
            self.Reports_Table.setColumnCount(6)
            self.Reports_Table.clear()
            GetPwIndexTable = PwMeasIndxTableDB()
            if self.Reports_System.currentText() == 'All':
                GetPwIndexTable.SelPwDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
                dataappend = GetPwIndexTable.PwDateFil
            else:
                GetPwIndexTable.SelPwDateSysFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text(), sysfilter=self.Reports_System.currentText().lower())
                dataappend = GetPwIndexTable.PwDateSysFil
            self.PlotGraph.setTitle('<font size="15"><strong>Pulse Width Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel( "bottom", '<span style="color: green; font-size: 18px">Set Pulse Width (μs)</span>' )
        elif self.Reports_Test.currentText() == 'PRI Test':
            self.Reports_ErrorGraph.show()
            self.Reports_Table.setColumnCount(6)
            self.Reports_Table.clear()
            GetPriIndexTable = PriMeasIndxTableDB()
            if self.Reports_System.currentText() == 'All' :
                GetPriIndexTable.SelPriDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
                dataappend = GetPriIndexTable.PriDateFil
            else :
                GetPriIndexTable.SelPriDateSysFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text(), sysfilter=self.Reports_System.currentText().lower())
                dataappend = GetPriIndexTable.PriDateSysFil
            self.PlotGraph.setTitle('<font size="15"><strong>PRI Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel( "bottom", '<span style="color: green; font-size: 18px">Set Pri (μs)</span>' )
        elif self.Reports_Test.currentText() == 'DOA Test':
            self.Reports_ErrorGraph.show()
            self.Reports_Table.setColumnCount(6)
            self.Reports_Table.clear()
            GetDoaIndexTable = DoaMeasIndxTableDB()
            if self.Reports_System.currentText() == 'All':
                GetDoaIndexTable.SelDoaDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
                dataappend = GetDoaIndexTable.DoaDateFil
            else:
                GetDoaIndexTable.SelDoaDateSysFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text(), sysfilter=self.Reports_System.currentText().lower())
                dataappend = GetDoaIndexTable.DoaDateSysFil
            self.PlotGraph.setTitle('<font size="15"><strong>DOA Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel("bottom",'<span style="color: green; font-size: 18px">Set Angle (μs)</span>')
        elif self.Reports_Test.currentText() == 'Amplitude Test':
            self.Reports_ErrorGraph.show()
            self.Reports_Table.setColumnCount(6)
            self.Reports_Table.clear()
            GetAmplIndexTable = AmplAccIndxTableDB()
            if self.Reports_System.currentText() == 'All' :
                GetAmplIndexTable.SelAmplDateFilter(datefilterfrom=self.dateEdit_From.text(),datefilterto=self.dateEdit_To.text())
                dataappend = GetAmplIndexTable.AmplDateFil
            else:
                GetAmplIndexTable.SelAmplDateSysFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text(), sysfilter=self.Reports_System.currentText().lower())
                dataappend = GetAmplIndexTable.AmplDateSysFil
            self.PlotGraph.setTitle('<font size="15"><strong>Amplitude Accuracy Test</strong></font>', color='blue')
            self.PlotGraph.setLabel("bottom",'<span style="color: green; font-size: 18px">Set Amplitude (dBm)</span>')
        elif self.Reports_Test.currentText() == 'Sensitivity Test':
            self.Reports_ErrorGraph.show()
            self.Reports_Table.setColumnCount(6)
            self.Reports_Table.clear()
            GetSensIndexTable = SensMeasIndxTableDB()
            if self.Reports_System.currentText() == 'All':
                GetSensIndexTable.SelSensMeasDateFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text())
                dataappend = GetSensIndexTable.SensMeasDateFil
            else :
                GetSensIndexTable.SelSensMeasDateSysFilter(datefilterfrom=self.dateEdit_From.text(), datefilterto=self.dateEdit_To.text(), sysfilter=self.Reports_System.currentText().lower())
                dataappend = GetSensIndexTable.SensMeasDateSysFil
            self.PlotGraph.setTitle('<font size="15"><strong>Sensitivity Measurement Test</strong></font>', color='blue')
            self.PlotGraph.setLabel( "bottom", '<span style="color: green; font-size: 18px">Set Freq (MHz)</span>' )
        self.PlotGraph.clear()
        self.PlotGraph.setYRange(-100, 100)
        self.Reports_Table.setHorizontalHeaderLabels(['date', 'username', 'system_id', 'system', 'mode', 'test_tab_ref'])
        self.PlotGraph.setLabel("left", '<span style="color: purple; font-size: 18px">Error </span>')
        dataappend = dataappend.astype(str)
        no_of_rows = dataappend.shape[0]
        no_of_cols = dataappend.shape[1]
        for row in range(no_of_rows):
            self.Reports_Table.setRowCount(row + 1)
            for col in range(no_of_cols):
                self.Reports_Table.setItem(row, col, QTableWidgetItem(dataappend.iloc[row][col]))
        if dataappend.empty == True:
            QMessageBox.information(self, "Error","No Data Found")
    ####################################################################################################################
    def SystemDisable(self):
        if self.Reports_Test.currentText() == "All":
            self.Reports_System.setDisabled(True)
            self.Reports_PB_Plot.setDisabled(True)
        else:
            self.Reports_System.setDisabled(False)
            self.Reports_PB_Plot.setDisabled(False)
    ####################################################################################################################
    def ReportDate(self):
        selected_date = self.dateEdit_To.date()
        if self.dateEdit_From.date()>self.dateEdit_To.date():
            self.dateEdit_From.setDate(selected_date)
        if self.dateEdit_To.date()<self.dateEdit_From.date():
            self.dateEdit_To.setDate(self.dateEdit_From.date())
    ####################################################################################################################
    def TableKeyValue(self):
        self.PlotGraph.clear()
        selRows = self.Reports_Table.selectedRanges()
        if (len(selRows) > 0):
            # print('length of ranges',len(selRanges))
            # selRanges.sort()
            RowsSelected = []
            for i in range(len(selRows)):
                selRange = selRows[i]
                topRow = selRange.topRow()
                bottomRow = selRange.bottomRow()
                for row in range(topRow, bottomRow + 1):
                    RowsSelected.append(row)
                RowsSelected.sort()
            print(RowsSelected)

        TableSelection = []
        for i in range(len(RowsSelected)):
            rowofcol = (self.Reports_Table.item(RowsSelected[i], 5)).text()
            TableSelection.append(rowofcol)
        print(TableSelection)

        for i in range(0, len(TableSelection)):
            ForTablename = TableSelection[i]
            if (self.Reports_Test.currentText() == 'Frequency Test'):
                GetFreqTestTable = FreqAccTestTableDB()
                GetFreqTestTable.GetFreqAccTestTable(testtablename=ForTablename)
                print(GetFreqTestTable.CurDbTableFreq)
                dfreadtoui = GetFreqTestTable.CurDbTableFreq
                leftlabel = dfreadtoui["set_freq"].tolist()
                self.setfreqvalue = [float(i) for i in leftlabel]
                bottomlabel = dfreadtoui["error"].tolist()
                self.errorvalue = [float(i) for i in bottomlabel]
                self.PlotGraph.addLegend()
                self.PlotGraph.setYRange(-100, 100)
                self.rgb_full = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                self.PlotGraph.plot(self.setfreqvalue, self.errorvalue,
                                    pen=pyqtgraph.mkPen(color=(self.rgb_full), width=2, style=QtCore.Qt.SolidLine),
                                    name=TableSelection[i])
            elif self.Reports_Test.currentText() == 'PulseWidth Test':
                GetPwTestTable = PwMeasTestTableDB()
                GetPwTestTable.GetPwMeasTestTable(testtablename=ForTablename)
                print(GetPwTestTable.CurDbTablePw)
                dfreadtoui = GetPwTestTable.CurDbTablePw
                leftlabel = dfreadtoui["set_pw"].tolist()
                self.setpwvalue = [float(i) for i in leftlabel]
                bottomlabel = dfreadtoui["error"].tolist()
                self.errorvalue = [float(i) for i in bottomlabel]
                self.PlotGraph.addLegend()
                self.PlotGraph.setYRange(-100, 100)
                self.rgb_full = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                self.PlotGraph.plot(self.setpwvalue, self.errorvalue,
                                    pen=pyqtgraph.mkPen(color=(self.rgb_full), width=2, style=QtCore.Qt.SolidLine),
                                    name=TableSelection[i])
            elif self.Reports_Test.currentText() == 'DOA Test':
                GetDoaTestTable = DoaMeasTestTableDB()
                GetDoaTestTable.GetDoaMeasTestTable(testtablename=ForTablename)
                print(GetDoaTestTable.CurDbTableDoa)
                dfreadtoui = GetDoaTestTable.CurDbTableDoa
                leftlabel = dfreadtoui["set_angle"].tolist()
                self.setanglevalue = [float(i) for i in leftlabel]
                bottomlabel = dfreadtoui["error"].tolist()
                self.errorvalue = [float(i) for i in bottomlabel]
                self.PlotGraph.addLegend()
                self.PlotGraph.setYRange(-100, 100)
                self.rgb_full = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                self.PlotGraph.plot(self.setanglevalue, self.errorvalue,
                                    pen=pyqtgraph.mkPen(color=(self.rgb_full), width=2, style=QtCore.Qt.SolidLine),
                                    name=TableSelection[i])
            elif self.Reports_Test.currentText() == 'Sensitivity Test':
                GetSensTestTable = SensMeasTestTableDB()
                GetSensTestTable.GetSensMeasTestTable(testtablename=ForTablename)
                print(GetSensTestTable.CurDbTableSens)
                dfreadtoui = GetSensTestTable.CurDbTableSens
                leftlabel = dfreadtoui["set_power"].tolist()
                self.setfreqvalue = [float(i) for i in leftlabel]
                bottomlabel = dfreadtoui["error"].tolist()
                self.errorvalue = [float(i) for i in bottomlabel]
                self.PlotGraph.addLegend()
                self.PlotGraph.setYRange(-100, 100)
                self.rgb_full = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                self.PlotGraph.plot(self.setfreqvalue, self.errorvalue,
                                    pen=pyqtgraph.mkPen(color=(self.rgb_full), width=2, style=QtCore.Qt.SolidLine),
                                    name=TableSelection[i])

            elif self.Reports_Test.currentText() == 'Amplitude Test':
                GetAmplTestTable = AmplAccTestTableDB()
                GetAmplTestTable.GetAmplAccTestTable(testtablename=ForTablename)
                print(GetAmplTestTable.CurDbTableAmpl)
                dfreadtoui = GetAmplTestTable.CurDbTableAmpl
                leftlabel = dfreadtoui["set_ampl"].tolist()
                self.setamplvalue = [float(i) for i in leftlabel]
                bottomlabel = dfreadtoui["error"].tolist()
                self.errorvalue = [float(i) for i in bottomlabel]
                self.PlotGraph.addLegend()
                self.PlotGraph.setYRange(-100, 100)
                self.rgb_full = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                self.PlotGraph.plot(self.setamplvalue, self.errorvalue,
                                    pen=pyqtgraph.mkPen(color=(self.rgb_full), width=2, style=QtCore.Qt.SolidLine),
                                    name=TableSelection[i])

            elif self.Reports_Test.currentText() == 'PRI Test':
                GetPriTestTable = PriMeasTestTableDB()
                GetPriTestTable.GetPriMeasTestTable(testtablename=ForTablename)
                print(GetPriTestTable.CurDbTablePri)
                dfreadtoui = GetPriTestTable.CurDbTablePri
                leftlabel = dfreadtoui["set_pri"].tolist()
                self.setprivalue = [float(i) for i in leftlabel]
                bottomlabel = dfreadtoui["error"].tolist()
                self.errorvalue = [float(i) for i in bottomlabel]
                self.PlotGraph.addLegend()
                self.PlotGraph.setYRange(-100, 100)
                self.rgb_full = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                self.PlotGraph.plot(self.setprivalue, self.errorvalue,
                                    pen=pyqtgraph.mkPen(color=(self.rgb_full), width=2, style=QtCore.Qt.SolidLine),
                                    name=TableSelection[i])
    ####################################################################################################################
    def RemoveFilters(self):
        self.Reports_Table.clear()
        self.Reports_Table.setRowCount(0)
        self.PlotGraph.clear()
    ####################################################################################################################
    def SaveProcess(self):
        selRows = self.tableWidget_Reports.selectedRanges()
        if (len(selRows) > 0):
            RowsSelected = []
            for i in range(len(selRows)):
                selRange = selRows[i]
                topRow = selRange.topRow()
                bottomRow = selRange.bottomRow()
                for row in range(topRow, bottomRow + 1):
                    RowsSelected.append(row)
                RowsSelected.sort()
            # print(RowsSelected)
        TableSelection = []
        for i in range(len(RowsSelected)):
            rowofcol = (self.tableWidget_Reports.item(RowsSelected[i], 5)).text()
            TableSelection.append(rowofcol)
        print(TableSelection)
        ReportsCls = ReportExcel()
        ReportsCls.SaveProcess(TableSelected=TableSelection)
        QMessageBox.information(self, "Self Test", "Reports Saved")
    ####################################################################################################################
    def printpreviewDialog(self):
        selRows = self.tableWidget_Reports.selectedRanges()
        if (len(selRows) > 0):
            RowsSelected = []
            for i in range(len(selRows)):
                selRange = selRows[i]
                topRow = selRange.topRow()
                bottomRow = selRange.bottomRow()
                for row in range(topRow, bottomRow + 1):
                    RowsSelected.append(row)
                RowsSelected.sort()
        TableSelection = []
        for i in range(len(RowsSelected)):
            rowofcol = (self.tableWidget_Reports.item(RowsSelected[i], 5)).text()
            TableSelection.append(rowofcol)
        print(TableSelection)
        ReportsCls = ReportPdf()
        ReportsCls.PdfPreview(TableSelected=TableSelection)
        #WaitDuration = sleep((len(TableSelection))*2.1)
        QMessageBox.information(self, "Reports Print", f'Reports are generating.... Please Wait ')
        time.sleep((len(TableSelection)) * 2 + 5)

        """self.printcall = PrinterDlg()
        self.printcall.show()"""
    ####################################################################################################################
#############################************************CALIBRATION*********************###################################
    def CalibRfPathLoss(self):
        self.Rad_progressBar.setValue(0)
        self.RFPath_graph.clear()
        self.RFPath_graph.setTitle('<font size="15"><strong>RF Path Loss Calibration</strong></font>', color='blue')
        self.RFPath_graph.setLabel("bottom", '<span style="color: green; font-size: 18px">Frequency (MHz)</span>')
        self.RFPath_graph.setLabel("left", '<span style="color: green; font-size: 18px">Path Loss (dB)</span>')
        self.PB_Rad_Calib.setDisabled(True)
        self.PB_Rad_Abort.setDisabled(False)
        self.RFPath_tableWidget.setRowCount(0)
        self.RFPath_tableWidget.clear()
        self.RFPath_tableWidget.clearContents()
        self.RFPath_tableWidget.setColumnCount(4)
        self.RFPath_tableWidget.setHorizontalHeaderLabels(["SNo", "Freq(MHz)", "Meas_Power", "Path_Loss"])
        self.RFPath_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.RFPath_tableWidget.setColumnWidth(0,45)
        self.RFPath_tableWidget.setColumnWidth(1,90)
        self.RFPath_tableWidget.setColumnWidth(2,140)
        self.RFPath_tableWidget.setColumnWidth(3,140)
        startfreq = float(self.lineEdit_Rad_Start_Freq.text())
        stopfreq = float(self.lineEdit_Rad_Stop_Freq.text())
        stepfreq = float(self.lineEdit_Rad_Step_Freq.text())
        setampl = float(self.lineEdit_Rad_Ampl.text())
        self.calclass = CalRfPathLoss()
        QApplication.processEvents()
        time.sleep(1)
        freq = startfreq
        rowindx = 0
        TotalSteps = (stopfreq-startfreq) / stepfreq

        set_freq_rf = []
        path_loss_rf = []
        while freq <= stopfreq:
            Meas_Power, Path_Loss = self.calclass.GetMeasurement(freq = freq, power = setampl)
            self.UpdatePathLossTable(TableIndx = rowindx, Freq = freq, Meas_Power = Meas_Power, Path_Loss = Path_Loss)
            self.Rad_progressBar.setValue(int((rowindx+1)*100/TotalSteps))
            set_freq_rf.append(freq)
            path_loss_rf.append(Path_Loss)
            self.UpdateRfPathLossPlot(set_freq_list = set_freq_rf, path_loss_list = path_loss_rf)
            QApplication.processEvents()
            time.sleep(1)
            freq = freq + stepfreq
            rowindx = rowindx + 1
        self.PB_Rad_Calib.setDisabled(False)
        self.PB_Rad_Abort.setDisabled(True)
    ####################################################################################################################
    def UpdatePathLossTable(self,TableIndx = 0, Freq = 500, Meas_Power = 0, Path_Loss = 0):
        self.RFPath_tableWidget.setRowCount(TableIndx + 1)
        self.RFPath_tableWidget.setItem(TableIndx, 0, QTableWidgetItem(str(TableIndx)))
        self.RFPath_tableWidget.setItem(TableIndx, 1, QTableWidgetItem(str(Freq)))
        self.RFPath_tableWidget.setItem(TableIndx, 2, QTableWidgetItem(str(Meas_Power)))
        self.RFPath_tableWidget.setItem(TableIndx, 3, QTableWidgetItem(str(Path_Loss)))
        tableverticalscroll = self.RFPath_tableWidget.item(TableIndx, 0)
        self.RFPath_tableWidget.scrollToItem(tableverticalscroll, QAbstractItemView.PositionAtTop)
        self.RFPath_tableWidget.selectRow(TableIndx)
    ####################################################################################################################
    def UpdateRfPathLossPlot(self,set_freq_list = [], path_loss_list = []):
        setfreqvalue = [float(i) for i in set_freq_list]
        pathlossvalue = [float(i) for i in path_loss_list]
        self.RFPath_graph.setYRange(-30, 30)
        #self.PlotGraph.addLegend()
        #self.RFPath_graph.plot(setfreqvalue, pathlossvalue, pen='r', width=5, style=QtCore.Qt.SolidLine )
        if self.Calib_Radiation.isChecked():
            self.RFPath_graph.plot(setfreqvalue, pathlossvalue, pen='m', width=2, name='radiation')
        elif self.Calib_Injection.isChecked():
            self.RFPath_graph.plot(setfreqvalue, pathlossvalue, pen='m', width=2, name='injection')
    ####################################################################################################################
    def RfPathDBUpdate(self):
        col_count = 5
        row_count = self.RFPath_tableWidget.rowCount()
        calrftabgetdata = []
        for row in range(row_count):
            rowdata = []
            for col in range(col_count):
                table_item = self.RFPath_tableWidget.item(row, col)
                rowdata.append(table_item.text())
            calrftabgetdata.append(rowdata)
        if self.Calib_Radiation.isChecked():
            self.calclass.RfCalUpdateToDB(calrffreqfrom=self.lineEdit_Rad_Start_Freq.text(), calrffreqto=self.lineEdit_Rad_Stop_Freq.text(), updatecaltbname='rfpathlossradmode',calrftabdata = calrftabgetdata)
        elif self.Calib_Injection.isChecked():
            self.calclass.RfCalUpdateToDB(calrffreqfrom=self.lineEdit_Rad_Start_Freq.text(), calrffreqto=self.lineEdit_Rad_Stop_Freq.text(), updatecaltbname='rfpathlossinjmode', calrftabdata=calrftabgetdata)
    ####################################################################################################################
    def CalRfPathExport(self):
        if self.Calib_Radiation.isChecked():
            self.calclass.RfCalExport(exporttable='rfpathlossradmode')
        elif self.Calib_Injection.isChecked():
            self.calclass.RfCalExport(exporttable='rfpathlossinjmode')
########################################################################################################################


########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainGUI()
    win.show()
    sys.exit(app.exec_())
