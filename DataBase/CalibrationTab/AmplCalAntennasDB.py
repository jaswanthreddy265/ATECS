import random
from datetime import datetime
from time import sleep

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

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
class RwrAmplCalAntennasDB():
    def __init__(self, Debug=False, antenna_no = 0):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        timestampfortable = datetime.now()
        self.tablename = f'rwramplcalantenna{antenna_no}_{timestampfortable.strftime("%Y_%m_%d_%H_%M_%S")}'
    ####################################################################################################################
    # This Function creates The CreateRwrAmplCalAntennas DataBase Table
    ####################################################################################################################
    def CreateRwrAmplCalAntennasTable(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                    (    antenna_no                FLOAT             NOT NULL,
                                         frequency                 FLOAT             NOT NULL,
                                         amplitude                 FLOAT             NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RwrAmplCalAntennasDB(CreateRwrAmplCalAntennasTable) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("RwrAmplCalAntennasDB(CreateRwrAmplCalAntennasTable) - Error while creating RwrAmplCalAntennasTable", error)
            return error
    ####################################################################################################################
    # This Function Gets The Frequency Records from RWRAmplCal Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def RetrieveRwrAmplCalAntennasTable(self, tablename='rwradfslope'):
        try:
            self.CurDbTable = pd.read_sql_query(f'''SELECT * FROM {tablename}  ''',
                                                con=self.connestablish)
            print(self.CurDbTable)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Gets The Frequency Records from RWRAmplCal Database Table  For pandas Reading
    ####################################################################################################################
    def DfUpdateToAntennaCalTable(self, updatedata=''):   #
        #updatedata= pd.read_csv("C:/Users/jaswa/PycharmProjects/ATEC1/DataBase/CalibrationTab/amplcaldf.csv")
        self.CreateRwrAmplCalAntennasTable()
        df = pd.DataFrame(updatedata)
        engine = create_engine(
            'postgresql+psycopg2://postgres:Platinum0435#@localhost:6543/atec')
        df.to_sql(f'{self.tablename}', engine, if_exists='append', index=False)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def RwrAmplCalAntennasDBClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################
if __name__ == "__main__":
    #demotest.RetrieveRwrAmplCalAntennasTable(tablename='rwradfslopecal_2024_05_31_18_14_51')

    for i in range (0,4):
        demotest = RwrAmplCalAntennasDB(Debug=True, antenna_no= i)
        #demotest.CreateRwrAmplCalAntennasTable()
        demotest.DfUpdateToAntennaCalTable()

    """demotest.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
    #       rwradfslopecal_2024_05_31_18_14_51"""
#######################################################################################################################