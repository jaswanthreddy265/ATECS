import random
from datetime import datetime
from time import sleep

import pandas as pd
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR
from sqlalchemy import create_engine

########################################################################################################################
#   RWR or WARNER Amplitude Calibration Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   31 May 2024
#   RwrAmplCalbIndxTableDB Class has the following member Functions
#   1. init()
#   2. CreateRwrAmplCalbDB()
#   3. AddRecord()
#   4. DropRecord()
#   5. DropRecordInRange()
#   6. RetrieveRecordInRange()
#   7. RetrieveAll()
#   8. FreqIndxDbConClose()
########################################################################################################################
# This Creating the RwrAmplCalbIndxTableDB Class
########################################################################################################################
class RwrAmplCalbIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
    ####################################################################################################################
    # This Function creates The RF Path Loss Radiation or Injection Mode Database Table
    ####################################################################################################################
    def CreateRwrAmplCalIndxTable(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS amplcalindxtable
                                    (    date                     TIMESTAMP         NOT NULL,
                                         antenna                  FLOAT             NOT NULL,
                                         start_freq               FLOAT             NOT NULL,
                                         stop_freq                FLOAT             NOT NULL,
                                         amplitude                FLOAT             NOT NULL,
                                         ampl_cal_table_id        TEXT              NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAmplCalbIndxTableDB(CreateRwrAmplCalIndxTable) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("RwrAmplCalbIndxTableDB(CreateRwrAmplCalIndxTable) - Error while creating FreqAccTable", error)
            return error
    ####################################################################################################################
    # This Function Adds The New Records to the Database Table
    ####################################################################################################################
    def AddAmplCalFreqRecord(self, amplrecord={'date':0,'antenna':5, 'start_freq': 500, 'stop_freq': 192, 'amplitude': 500, 'ampl_cal_table_id': 'ampl'}):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO amplcalindxtable VALUES('{amplrecord['date']}', '{amplrecord['antenna']}', '{amplrecord['start_freq']}', '{amplrecord['stop_freq']}', '{amplrecord['amplitude']}', '{amplrecord['ampl_cal_table_id']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAmplCalbIndxTableDB(AddAmplCalFreqRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("RwrAmplCalbIndxTableDB(AddAmplCalFreqRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR
    ####################################################################################################################
    # This Function Deletes The Record from rfpathlossradmode or rfpathlossinjmode Index Database Table
    ####################################################################################################################
    def DeleteCalIndxRecord(self,ampl_cal_table_id=500):
        try:
            cursor = self.connestablish.cursor()
            delrecord = f'''DELETE FROM amplcalindxtable WHERE ampl_cal_table_id='{ampl_cal_table_id}' '''
            cursor.execute(delrecord)
            self.connestablish.commit()
            print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
          print("Error while delating from the table", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records between range from RWRAmplCal Database Table For pandas Reading
    ####################################################################################################################
    def RetrieveAmplCalIndxDateRange(self, amplindxfromdate=0, amplindxtodate=0):
        try:
            self.RetrieveFreqRange = pd.read_sql_query(
                f'''SELECT * FROM amplcalindxtable WHERE date BETWEEN '{amplindxfromdate}' AND '{amplindxtodate}' ''',
                con=self.connestablish)
            print(self.RetrieveFreqRange)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records from RWRAmplCal Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def RetrieveAmplCalIndxTable(self):
        try:
            self.CurDbTable = pd.read_sql_query(f'''SELECT * FROM amplcalindxtable  ''',
                                                con=self.connestablish)
            print(self.CurDbTable)
            #self.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def RwrAmplCalIndxDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################
if __name__ == "__main__":
    demotest = RwrAmplCalbIndxTableDB(Debug=True)
    demotest.CreateRwrAmplCalIndxTable()

    #demotest.AddAmplCalFreqRecord(amplrecord=newrow)
    #demotest.RetrieveAmplCalIndxDateRange(amplindxfromdate='01_01_2024', amplindxtodate='06_06_2024')
    #demotest.RetrieveAmplCalIndxTable()
    #demotest.DeleteCalIndxRecord(ampl_cal_table_id='amplcal2024-05-31 16:37:43.686453')

    newrow = {'date':datetime.now(), 'antenna':1, 'start_freq': 20000, 'stop_freq': 3000, 'amplitude': -40, 'ampl_cal_table_id': f'amplcal{datetime.now()}'}
    start_freq = 20000
    stop_freq = 25000
    step_freq = 500
    while start_freq<=stop_freq:
        sleep(5)
        print(start_freq)
        newrow['date'] = datetime.now()
        newrow['antenna'] = random.randrange(0, 10)
        newrow['start_freq'] = start_freq
        newrow['stop_freq'] = stop_freq
        newrow['amplitude'] = -40 +random.randrange(5)
        newrow['ampl_cal_table_id'] = f'amplcal{datetime.now()}'
        demotest.AddAmplCalFreqRecord(amplrecord=newrow)
        start_freq += step_freq

    """demotest.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
    #       amplcalindxtable"""
#######################################################################################################################