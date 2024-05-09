from datetime import datetime
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView
from openpyxl import load_workbook
from openpyxl.styles import Font
from DataBase.RWR.RWRFreqAccTestTableDB import RWRFreqAccTestTableDB
class freqaccimpcsv():
    def __int__(self):
        self.connection = True
        self.getdata = RWRFreqAccTestTableDB()
        self.CurRowInd = 0
    def connect(self):
        self.getdata.connect({
        'user': 'postgres',
        'password': 'Platinum0435#',
        'host': 'localhost',
        'database': 'atec',
        'port': 6543
        })
        self.getdata.getrwrfreqacctesttable('rwrfreqacctest_2024_03_24_11_41_05')
        self.dfreadtoui=self.getdata.CurDbTable
        self.dfreadtoui["set_freq"]= self.dfreadtoui["set_freq"].astype(str)
        self.dfreadtoui["meas_freq"] = self.dfreadtoui["meas_freq"].astype(str)
        self.dfreadtoui["error"] = self.dfreadtoui["error"].astype(str)
        print(self.dfreadtoui)
        """no_of_rows=self.dfreadtoui.shape[0]
        no_of_cols=self.dfreadtoui.shape[1]
        for row in range(no_of_rows):
            self.tableWidget.setRowCount(row+1)
            for col in range(no_of_cols):
                self.tableWidget.setItem(row,col,QTableWidgetItem(dfreadtoui.iloc[row][col]))"""

    def TabletoCSV(self):
        workbook = load_workbook(filename="FreqAccTestTemplate.xlsx")
        sheet = workbook.active
        sheet.page_setup=Font(name='Arial')
        csvFile = pd.read_csv('FreqAccTDR.csv')
        df = pd.DataFrame(csvFile)
        sheet['F5'] = df.iloc[0, 0]
        sheet['F6'] = df.iloc[1, 0]
        sheet['E8'] = df.iloc[2, 0]
        sheet['I8'] = df.iloc[3, 0]
        sheet['E9'] = datetime.now().strftime('%d-%m-%Y')
        sheet['I9'] = datetime.now().strftime('%H:%M:%S')
        sheet['E12'] = df.iloc[6, 0]
        sheet['I12'] = df.iloc[7, 0]
        sheet['E13'] = df.iloc[8, 0]
        sheet['I13'] = df.iloc[9, 0]
        sheet['E14'] = df.iloc[10, 0]
        sheet['I14'] = df.iloc[11, 0]
        sheet['E15'] = df.iloc[12, 0]
        sheet['I15'] = df.iloc[13, 0]
        for i in range(0, self.tableWidget.rowCount()):
            sheet[f'''C{i + 18}'''] = self.tableWidget.item(i, 0).text()
            sheet[f'''E{i + 18}'''] = self.tableWidget.item(i, 1).text()
            sheet[f'''I{i + 18}'''] = self.tableWidget.item(i, 2).text()
        print(len(self.dfreadtoui))
        outfile = "freqacctest " + datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '.xlsx'
        workbook.save(filename=outfile)


if __name__ == "__main__":
    impcsv=freqaccimpcsv()
    impcsv.TabletoCSV()
    """impcsv.getrwrfreqacctesttable()
    impcsv.CurDbTable.to_csv("rwrfreqacctesttabledb.csv")
    print(impcsv.CurDbTable)"""
