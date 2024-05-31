from datetime import datetime

import pandas as pd
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR
from sqlalchemy import create_engine

########################################################################################################################
#   RWR or WARNER Amplitude Calibration Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   31 May 2024
#   RwrAmplCalbDB Class has the following member Functions
#   1. init()
#   2. CreateRwrAmplCalbDB()
#   3. AddRecord()
#   4. DropRecord()
#   5. DropRecordInRange()
#   6. RetrieveRecordInRange()
#   7. RetrieveAll()
#   8. FreqIndxDbConClose()
########################################################################################################################
# This Creating the RwrAmplCalbDB Class
########################################################################################################################
class RwrAmplCalbTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection

    ####################################################################################################################
    # This Function creates The RWR/WARNER Amplitude Calibration Database Table
    ####################################################################################################################
    def CreateRwrAmplCalTable(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (   frequency                FLOAT         NOT NULL,
                                         input_ampl               FLOAT         NOT NULL,
                                         meas_ampl                FLOAT         NOT NULL,
                                         gain                     FLOAT         NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAmplCalbDB(CreateRwrAmplCalTable) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("RwrAmplCalbDB(CreateRwrAmplCalTable) - Error while creating FreqAccTable", error)
            return error

    """####################################################################################################################
    # This Function creates The RF Path Loss Radiation or Injection Mode Database Table
    ####################################################################################################################
    def CreateRwrAmplCalIndxTable(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS amplcalindxtable
                                    (    date                     TIMESTAMP         NOT NULL,
                                         start_freq               FLOAT             NOT NULL,
                                         stop_freq                FLOAT             NOT NULL,
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAmplCalbDB(CreateRwrAmplCalIndxTable) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("RwrAmplCalbDB(CreateRwrAmplCalIndxTable) - Error while creating FreqAccTable", error)
            return error
    ####################################################################################################################
    # This Function Adds The New Records to the Database Table
    ####################################################################################################################
    def AddAmplCalFreqRecord(self, lossrecord={'date':0, 'start_freq': 500, 'stop_freq': 192}):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO amplcalindxtable VALUES('{lossrecord['frequency']}', '{lossrecord['path_loss']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAmplCalbDB(AddAmplCalRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("RwrAmplCalbDB(AddAmplCalRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR
    ####################################################################################################################
    # This Function Deletes The Record from rfpathlossradmode or rfpathlossinjmode Index Database Table
    ####################################################################################################################
    def DeleteCalIndxRecord(self,amplcalfreqrecord=500):
        try:
            cursor = self.connestablish.cursor()
            delrecord = f'''DELETE FROM amplcalindxtable WHERE frequency='{amplcalfreqrecord}' '''
            cursor.execute(delrecord)
            self.connestablish.commit()
            print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
          print("Error while delating from the table", error)"""
    ####################################################################################################################
    # This Function Deletes The range of Frequency Records from RWRAmplCal Database Table
    ####################################################################################################################
    def DropAmplCalFreqRecordInRange(self,tablename = 'rfpathloss', amplcal_freqfrom=0, amplcal_freqto=0):
        try:
            cursor = self.connestablish.cursor()
            delfreqrecord = f'''DELETE FROM {tablename} WHERE frequency BETWEEN '{amplcal_freqfrom}' AND '{amplcal_freqto}' '''
            cursor.execute(delfreqrecord)
            self.connestablish.commit()
            print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
          print("Error while delating from the table", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records between range from RWRAmplCal Database Table For pandas Reading
    ####################################################################################################################
    def RetrieveAmplCalFreqRecordInRange(self,tablename='rfpathloss', rangefrom=0, rangeto=0):
        try:
            self.RetrieveFreqRange = pd.read_sql_query(
                f'''SELECT * FROM {tablename} WHERE frequency BETWEEN '{rangefrom}' AND '{rangeto}' ORDER BY CAST(frequency AS FLOAT) ASC''',
                con=self.connestablish)
            print(self.RetrieveFreqRange)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records from RWRAmplCal Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def RetrieveAmplCalTable(self, tablename=''):
        try:
            self.CurDbTable = pd.read_sql_query(f'''SELECT * FROM {tablename} ORDER BY CAST(frequency AS FLOAT) ASC ''',
                                                con=self.connestablish)
            print(self.CurDbTable)
            self.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records from RWRAmplCal Database Table  For pandas Reading
    ####################################################################################################################
    def DfUpdateToAmplCalTable(self):   #updatedata='',
        updatedata= pd.read_csv("C:/Users/jaswa/PycharmProjects/ATEC1/DataBase/CalibrationTab/amplcaldf.csv")
        df = pd.DataFrame(updatedata)
        engine = create_engine(
            'postgresql+psycopg2://postgres:Platinum0435#@localhost:6543/atec')
        df.to_sql(f'{self.tablename}', engine, if_exists='append', index=False)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def RwrAmplCalDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################
if __name__ == "__main__":
    demotest = RwrAmplCalbTableDB(Debug=True)
    timestamptable= datetime.now()
    demotest.tablename=f'''rfpathlossinjmode_{timestamptable.strftime("%Y_%m_%d_%H_%M_%S")}'''
    #demotest.CreateRwrAmplCalTable()
    #demotest.DfUpdateToAmplCalTable()
    #demotest.DropAmplCalFreqRecordInRange(tablename=demotest.tablename, amplcal_freqfrom=4000, amplcal_freqto=6000 )
    #demotest.RetrieveAmplCalFreqRecordInRange(tablename=demotest.tablename, rangefrom=400, rangeto=40000)
    #demotest.RetrieveAmplCalTable(tablename=demotest.tablename)

    """newrow = {'frequency':'700','path_loss':5}
    start_freq = 30100
    stop_freq = 39999
    step_freq = 100
    while start_freq<=stop_freq:
        print(start_freq)
        newrow['frequency'] = start_freq
        newrow['path_loss'] = float(newrow['frequency'])-5
        demotest.AddRecord(lossrecord=newrow)
        start_freq += step_freq
    demotest.DeleteRecord(freqrecord='4000')
    demotest.RetrieveAll(tablename='rfpathlossradmode')
    demotest.RetrieveRecordInRange(tablename='rfpathlossradmode', rangefrom='1000', rangeto='3500')
    #demotest.DropRecordInRange(tablename='rfpathlossinjmode', freqfrom=35000,freqto=40000)

    #demotest.RetrieveAll(tablename='rfpathlossinjmode')
    data = {
              "frequency": [500, 600, 650],
              "path_loss": [60, 50, 95]
            }
    demotest.DfUpdateDbTable(updatedata=data,tablename='rfpathlossradmode')
    demotest.RetrieveAll(tablename='rfpathlossinjmode')
    demotest.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
    #       rfpathlossinjmode_2024_05_31_14_16_51"""
#######################################################################################################################