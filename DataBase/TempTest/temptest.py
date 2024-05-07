import datetime

import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import Side, Border

from DataBase.INDXTBDB.AmplAccIndxTableDB import AmplAccIndxTableDB
from DataBase.INDXTBDB.DOAMeasIndxTableDB import DoaMeasIndxTableDB
from DataBase.INDXTBDB.FreqAccIndxTableDB import FreqAccIndxTableDB
from DataBase.INDXTBDB.PRIMeasIndxTableDB import PriMeasIndxTableDB
from DataBase.INDXTBDB.PWMeasIndxTableDB import PwMeasIndxTableDB
from DataBase.INDXTBDB.SensMeasAccIndxTableDB import SensMeasIndxTableDB
from DataBase.TESTTBDB.DoaMeasTestTableDB import DoaMeasTestTableDB
from DataBase.TESTTBDB.FreqAccTestTableDB import FreqAccTestTableDB
from DataBase.TESTTBDB.PriMeasTestTableDB import PriMeasTestTableDB
from DataBase.TESTTBDB.PwMeasTestTableDB import PwMeasTestTableDB

def SaveProcess(self, dataappend):
    ####################################################
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
    dataappend = pd.concat(
        [freqdataappend, pwdataappend, pridataappend, ampldataappend, doadataappend, sensmeasdataappend],
        ignore_index=True)
    # print(dataappend)
    # dataappend.to_csv("freqaccindxtabledb.csv")
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

    for i in range(0, len(TableSelection)):
        ForTablename = TableSelection[i]
        if (self.CB_Test.currentText() == 'All'):
            GetFreqTestTable = FreqAccTestTableDB()
            GetFreqTestTable.GetFreqAccTestTable(testtablename=ForTablename)

            # print(GetFreqTestTable.CurDbTableFreq)
            dfreadtoui = GetFreqTestTable.CurDbTableFreq
            self.setfreqvalue = dfreadtoui["set_freq"]
            self.measfreqvalue = dfreadtoui["meas_freq"]
            self.errorvalue = dfreadtoui["error"]
            workbook = load_workbook('C:/Users/jaswa/PycharmProjects/ATEC1/DataBase/Templates/FreqAccTestTemplate.xlsx')
            timestamp = datetime.datetime.now()
            sheetonename = f'''{(self.tableWidget_Reports.item(RowsSelected[i], 6)).text()}'''
            CurrentRow = self.tableWidget_Reports.currentRow()
            # print(sheetonename)
            sheet1 = workbook.active
            sheet1.title = sheetonename
            dfRowFil = dataappend.loc[dataappend['test_tab_ref'] == TableSelection[i]]
            # print(dfRowFil)
            datetrim = dfRowFil.iloc[0][0]
            dateformat = str(datetrim)[:10]
            timeformat = str(datetrim)[11:19]
            # print(timeformat)
            # sheet1['F4'] = self.tableWidget_Reports.item(CurrentRow,6).text()
            sheet1['F4'] = (self.tableWidget_Reports.item(RowsSelected[i], 6)).text()
            sheet1['F5'] = (dfRowFil.iloc[0][3]).upper()
            sheet1['F6'] = dfRowFil.iloc[0][4]
            sheet1['E8'] = dfRowFil.iloc[0][1]
            sheet1['E9'] = dateformat
            sheet1['I8'] = dfRowFil.iloc[0][2]
            sheet1['I9'] = timeformat
            sheet1['E12'] = dfRowFil.iloc[0][7]
            sheet1['E13'] = (dfRowFil.iloc[0][9])
            sheet1['E14'] = (dfRowFil.iloc[0][12])
            sheet1['E15'] = (dfRowFil.iloc[0][14])
            sheet1['I12'] = (dfRowFil.iloc[0][8])
            sheet1['I13'] = (dfRowFil.iloc[0][11])
            sheet1['I14'] = (dfRowFil.iloc[0][13])
            sheet1['I15'] = (dfRowFil.iloc[0][15])
            if self.tableWidget_Reports.item(RowsSelected[i], 6).text() == 'Frequency Test':
                sheet1['C17'] = 'Set Frequency(MHz)'
                sheet1['E17'] = 'Measure Frequency(MHz)'
            elif self.tableWidget_Reports.item(RowsSelected[i], 6).text() == 'Pulse Width Test':
                sheet1['C17'] = 'Set Frequency(MHz)'
                sheet1['E17'] = 'Measure Frequency(MHz)'
            sheet1['I17'] = 'Error'
            for i in range(0, len(dfreadtoui)):
                # print(len(dfreadtoui))
                sheet1[f'''C{18 + i}'''] = self.setfreqvalue.values[i]
                sheet1[f'''E{18 + i}'''] = self.measfreqvalue.values[i]
                sheet1[f'''I{18 + i}'''] = self.errorvalue.values[i]
            self.set_border(sheet1, f'''C18:I18''')  # for excel sheet table cell borders

            TestName = self.tableWidget_Reports.item(CurrentRow, 6).text()
            # save the file
            outfile = ForTablename + '.xlsx'
            workbook.save(filename=outfile)
            QMessageBox.information(self, "Self Test", "Reports Saved to " + outfile)
    ################################################################################################################


def set_border(self, worksheet, cell_range):
    thin = Side(border_style="thin", color="000000")
    for row in worksheet[cell_range]:
        for cell in row:
            cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)