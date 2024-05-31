import random
from time import sleep

import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

from DataBase.RFPathLoss.RfPathLoss import RFPathLossDB


class CalRfPathLoss():
    def __init__(self):
        self.rfpathlossdb = RFPathLossDB(Debug = True)
    def RfCalUpdateToDB(self, calrffreqfrom='', calrffreqto='', updatecaltbname='', calrftabdata=[]):
        self.rfpathlossdb.DropRecordInRange(tablename=updatecaltbname,  freqfrom=calrffreqfrom, freqto=calrffreqto)
        rflosstable = pd.DataFrame(calrftabdata, columns=["s.no", "frequency", "set_power", "meas_power", "path_loss"])
        appenddata = rflosstable.drop(rflosstable.columns[[0, 2, 3]], axis=1)
        print(appenddata)
        sleep(1)
        self.rfpathlossdb.DfUpdateDbTable(updatedata=appenddata, tablename=updatecaltbname)
        self.rfpathlossdb.RetrieveAll(tablename=updatecaltbname)
    def RfCalExport(self, exporttable=''):
        self.rfpathlossdb.RetrieveAll(tablename=exporttable)
    def GetMeasurement(self, freq=2000, power=0):
        measpower = power + random.randrange(-5,5)
        path_loss = power-measpower
        return measpower, path_loss

if __name__ == "__main__":
    demotest=CalRfPathLoss()
    demotest.GetMeasurement(freq=500, power=-40)