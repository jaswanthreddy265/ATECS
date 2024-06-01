import random
from time import sleep

import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

from DataBase.CalibrationTab.AmplCalAntennasDB import RwrAmplCalAntennasDB
from DataBase.CalibrationTab.RfPathLoss import RFPathLossDB
from DataBase.CalibrationTab.RwrAmplCalTableDB import RwrAmplCalbTableDB


class CalibrationOperations():
    def __init__(self):
        pass
    def RfCalUpdateToDB(self, calrffreqfrom='', calrffreqto='', updatecaltbname='', calrftabdata=[]):
        self.rfpathlossdb = RFPathLossDB(Debug = True)
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
    def GetRwrAmplMeasurement(self,amplcalfreq=0, amplcalinputpower=0, amplcal_pw= 0, amplcal_pri= 0):
        rwramplcalmeaspower = amplcalinputpower + random.randrange(-5,5)
        rwramplcalgain = amplcalinputpower-rwramplcalmeaspower
        return rwramplcalmeaspower, rwramplcalgain
    def RfCalUpdateToDB(self):
        pass
        RwrAmplCalbTableDB(Debug=True)

    def RwrCalAntennaDataFromTarget(self):
        ant1freq = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        ant1ampl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ant2freq = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        ant2ampl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ant3freq = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        ant3ampl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ant4freq = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        ant4ampl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ant5freq = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        ant5ampl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ant1data = pd.Dataframe(list(zip(ant1freq, ant1ampl)), coulumns =['frequency', 'amplitude'])
        ant2data = pd.Dataframe(list(zip(ant2freq, ant2ampl)), coulumns =['frequency', 'amplitude'])
        ant3data = pd.Dataframe(list(zip(ant3freq, ant3ampl)), coulumns =['frequency', 'amplitude'])
        ant4data = pd.Dataframe(list(zip(ant4freq, ant4ampl)), coulumns =['frequency', 'amplitude'])
        ant5data = pd.Dataframe(list(zip(ant5freq, ant5ampl)), coulumns =['frequency', 'amplitude'])

        """
                        ##########if needed convert to dataframe
        # list of strings
        lst = [11, 22, 33, 44, 55, 66, 77]
        
        # list of int
        lst2 = [11, 22, 33, 44, 55, 66, 77]
        
        # Calling DataFrame constructor after zipping
        # both lists, with columns specified
        df = pd.DataFrame(list(zip(lst, lst2)),
                       columns =['Name', 'val'])
        print(df)"""
        return ant1data, ant2data, ant3data, ant4data, ant5data

    def RwrCalAmplAntToDb(self, ant_no=0, data=[]):
        if ant_no == 1:
            rdfromtrgt=RwrAmplCalAntennasDB(Debug=True, antenna_no= 1)
            rdfromtrgt.DfUpdateToAntennaCalTable(updatedata=data)
        elif ant_no == 2:
            rdfromtrgt=RwrAmplCalAntennasDB(Debug=True, antenna_no= 2)
            rdfromtrgt.DfUpdateToAntennaCalTable(updatedata=data)
        elif ant_no == 3:
            rdfromtrgt=RwrAmplCalAntennasDB(Debug=True, antenna_no= 3)
            rdfromtrgt.DfUpdateToAntennaCalTable(updatedata=data)
        elif ant_no == 4:
            rdfromtrgt=RwrAmplCalAntennasDB(Debug=True, antenna_no= 4)
            rdfromtrgt.DfUpdateToAntennaCalTable(updatedata=data)
        elif ant_no == 5:
            rdfromtrgt=RwrAmplCalAntennasDB(Debug=True, antenna_no= 5)
            rdfromtrgt.DfUpdateToAntennaCalTable(updatedata=data)

if __name__ == "__main__":
    #demotest=CalibrationOperations()
    #demotest.GetMeasurement(freq=500, power=-40)
    pass