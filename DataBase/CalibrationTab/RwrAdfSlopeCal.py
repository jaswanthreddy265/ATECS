import random
from datetime import datetime
from time import sleep

import pandas as pd
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR

########################################################################################################################
#   RWR or WARNER Amplitude Calibration Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   31 May 2024
#   RwrAdfSlopeCalDB Class has the following member Functions
#   1. init()
#   2. CreateRwrAmplCalbDB()
#   3. AddRecord()
#   4. DropRecord()
#   5. DropRecordInRange()
#   6. RetrieveRecordInRange()
#   7. RetrieveAll()
#   8. FreqIndxDbConClose()
########################################################################################################################
# This Creating the RwrAdfSlopeCalDB Class
########################################################################################################################
class RwrAdfSlopeCalDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
    ####################################################################################################################
    # This Function creates The RwrAdfSlopeCalDB Database Table
    ####################################################################################################################
    def CreateRwrAdfSlopeCalTable(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                    (    frequency                FLOAT             NOT NULL,
                                         s1_slope_31              FLOAT             NOT NULL,
                                         s1_const_31              FLOAT             NOT NULL,
                                         s2_slope_0               FLOAT             NOT NULL,
                                         s2_const_0               FLOAT             NOT NULL,
                                         s3_slope_45              FLOAT             NOT NULL,
                                         s3_const_45              FLOAT             NOT NULL,
                                         s4_slope_90              FLOAT             NOT NULL,
                                         s4_const_90              FLOAT             NOT NULL,
                                         s5_slope_13              FLOAT             NOT NULL,
                                         s5_const_13              FLOAT             NOT NULL,
                                         s6_slope_18              FLOAT             NOT NULL,
                                         s6_const_18              FLOAT             NOT NULL,
                                         s7_slope_22              FLOAT             NOT NULL,
                                         s7_const_22              FLOAT             NOT NULL,
                                         s8_slope_27              FLOAT             NOT NULL,
                                         s8_const_27              FLOAT             NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAdfSlopeCalDB(CreateRwrAdfSlopeCalTable) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("RwrAdfSlopeCalDB(CreateRwrAdfSlopeCalTable) - Error while creating RwrAdfSlopeCalTable", error)
            return error
    ####################################################################################################################
    # This Function Adds The New Records to the Database Table
    ####################################################################################################################
    def AddAdfAlopeCalRecord(self, adfsloperecord={'freq':0,'s1_slope_31':5,'s1_const_31':5,'s2_slope_0':5,'s2_const_0':5,
                                               's3_slope_45':5,'s3_const_45':5,'s4_slope_90':5,'s4_const_90':5, 's5_slope_13':5,
                                               's5_const_13':5,'s6_slope_18':5,'s6_const_18':5, 's7_slope_22':5,'s7_const_22':5,
                                                   's8_slope_22':5,'s8_const_22':5}):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{adfsloperecord['freq']}', '{adfsloperecord['s1_slope_31']}',
                    '{adfsloperecord['s1_const_31']}', '{adfsloperecord['s2_slope_0']}', '{adfsloperecord['s2_const_0']}', 
                    '{adfsloperecord['s3_slope_45']}', '{adfsloperecord['s3_const_45']}', '{adfsloperecord['s4_slope_90']}',
                    '{adfsloperecord['s4_const_90']}', '{adfsloperecord['s5_slope_13']}', '{adfsloperecord['s5_const_13']}', 
                    '{adfsloperecord['s6_slope_18']}', '{adfsloperecord['s6_const_18']}', '{adfsloperecord['s7_slope_22']}',
                    '{adfsloperecord['s7_const_22']}', '{adfsloperecord['s8_slope_27']}', '{adfsloperecord['s8_const_27']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAdfSlopeCalDB(AddAmplCalFreqRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("RwrAdfSlopeCalDB(AddAmplCalFreqRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR
    ####################################################################################################################
    # This Function Deletes The Record from rfpathlossradmode or rfpathlossinjmode Index Database Table
    ####################################################################################################################
    def DeleteRwrAdfSlopeCalFreqRecord(self,tablename='', AdfSlopeCalFreq=500):
        try:
            cursor = self.connestablish.cursor()
            delrecord = f'''DELETE FROM {tablename} WHERE freq='{AdfSlopeCalFreq}' '''
            cursor.execute(delrecord)
            self.connestablish.commit()
            print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
          print("Error while delating from the table", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records between range from RWRAmplCal Database Table For pandas Reading
    ####################################################################################################################
    def RetrieveRwrAdfSlopeCalFreqRange(self,tablename='rwradfslope', adffreqfrom=0, adffreqto=0):
        try:
            self.RetrieveFreqRange = pd.read_sql_query(
                f'''SELECT * FROM {tablename} WHERE freq BETWEEN '{adffreqfrom}' AND '{adffreqto}' ''',
                con=self.connestablish)
            print(self.RetrieveFreqRange)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records from RWRAmplCal Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def RetrieveRwrAdfSlopeCalTable(self, tablename='rwradfslope'):
        try:
            self.CurDbTable = pd.read_sql_query(f'''SELECT * FROM {tablename}  ''',
                                                con=self.connestablish)
            print(self.CurDbTable)
            #self.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def RwrAdfSlopeCalDBClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################
if __name__ == "__main__":
    demotest = RwrAdfSlopeCalDB(Debug=True)
    timestampfortable=datetime.now()
    #demotest.tablename=f'rwradfslopecal_{timestampfortable.strftime("%Y_%m_%d_%H_%M_%S")}'
    #demotest.CreateRwrAdfSlopeCalTable()

    #demotest.RetrieveRwrAdfSlopeCalFreqRange(tablename='rwradfslopecal_2024_05_31_18_14_51', adffreqfrom=0, adffreqto=30000)
    #demotest.RetrieveRwrAdfSlopeCalTable(tablename='rwradfslopecal_2024_05_31_18_14_51')
    #demotest.DeleteRwrAdfSlopeCalFreqRecord(tablename='rwradfslopecal_2024_05_31_18_14_51', AdfSlopeCalFreq=22500)

    """newrow = {'freq':0,'s1_slope_31':5,'s1_const_31':5,'s2_slope_0':5,'s2_const_0':5, 's3_slope_45':5,'s3_const_45':5,
              's4_slope_90':5,'s4_const_90':5, 's5_slope_13':5, 's5_const_13':5,'s6_slope_18':5,'s6_const_18':5,
              's7_slope_22':5,'s7_const_22':5}
    start_freq = 20000
    stop_freq = 25000
    step_freq = 500
    while start_freq<=stop_freq:
        print(start_freq)
        newrow['freq'] = start_freq
        newrow['s1_slope_31'] = random.randrange(0, 10)
        newrow['s1_const_31'] = random.randrange(0, 10)
        newrow['s2_slope_0'] = random.randrange(0, 10)
        newrow['s2_const_0'] = random.randrange(0, 10)
        newrow['s3_slope_45'] = random.randrange(0, 10)
        newrow['s3_const_45'] = random.randrange(0, 10)
        newrow['s4_slope_90'] = random.randrange(0, 10)
        newrow['s4_const_90'] = random.randrange(0, 10)
        newrow['s5_slope_13'] = random.randrange(0, 10)
        newrow['s5_const_13'] = random.randrange(0, 10)
        newrow['s6_slope_18'] = random.randrange(0, 10)
        newrow['s6_const_18'] = random.randrange(0, 10)
        newrow['s7_slope_22'] = random.randrange(0, 10)
        newrow['s7_const_22'] = random.randrange(0, 10)

        #demotest.AddAdfAlopeCalRecord(adfsloperecord=newrow)
        start_freq += step_freq

    demotest.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
    #       rwradfslopecal_2024_05_31_18_14_51"""
#######################################################################################################################