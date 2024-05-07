import random
from datetime import datetime
from time import sleep

import pandas as pd
from tqdm import tqdm
import psycopg2

from DataBase.TempTest.ConnectDB import Connect_to_Database
from DataBase.TestCases.ErrorCodesDatabase import DATABASE_CONNECTION_ERROR, SUCCESS, DATABASE_ADDDATA_ERROR
########################################################################################################################
#   Sensitivity Measurement Test Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   06 Mar 2024
#   SensMeasTestTableDB Class has the following member Functions
#   1. init()
#   2. CreateSensMeasTestTableDB()
#   3. AddSensRow()
#   4. GetSensMeasTestTable()
#   5. DropSensMeasTestTable()
#   6. close()
########################################################################################################################
# This Creating the SensMeasTestTableDB Class
########################################################################################################################
class SensMeasTestTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        timestamp = datetime.now()
        self.tablename= f'''sensmeastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    ####################################################################################################################
    # This Function creates The  Sensitivity Measurement Test Database Table
    ####################################################################################################################
    def CreateSensMeasTestTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (
                                         set_sens          FLOAT        NOT NULL,
                                         meas_sens         FLOAT        NOT NULL,
                                         error             FLOAT        NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("SensMeasTestTableDB(CreateSensMeasTestTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("SensMeasTestTableDB(CreateSensMeasTestTableDB) - Error while creating SensMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Sensitivity Measurement Test Database Table
    ####################################################################################################################
    def AddSensTestRow(self, senstestvalues={'set_sens' : 4614, 'meas_sens' : 26565, 'error' : 3 }):
      #  print("AddSensRow")
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{senstestvalues['set_sens']}','{senstestvalues['meas_sens']}',
                                     '{senstestvalues['error']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("SensMeasTestTableDB(AddSensRow) - New Row added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("SensMeasTestTableDB(AddSensRow)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The Sensitivity Measurement Test Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetSensMeasTestTable(self, testtablename='sensmeastest_2024_03_24_11_41_05'):
        try:
            self.CurDbTableSens = pd.read_sql_query(
                f'''SELECT * FROM {testtablename} ''',
                con=self.connestablish)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to sensmeastesttable ", error)

    ####################################################################################################################
    # This Function Drops The Sensitivity Measurement Test Database Table
    ####################################################################################################################
    def DropSensMeasTestTable(self, deletetable='esmsensmeastest'):
        try:
            cursor = self.connestablish.cursor()
            delete_table_query = f'''DROP TABLE {deletetable}  '''
            cursor.execute(delete_table_query)
            self.connestablish.commit()
            print("success")
        except (Exception, psycopg2.DatabaseError) as error:
            print("table does not exist", error)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def close(self):
        self.connestablish.close()
        if self.Debug == True:
            print("PostgreSQL connection is closed")
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
########################################################################################################################
if __name__ == "__main__":
    sensmeastestdb = SensMeasTestTableDB(Debug=False)
    """timestamp = datetime.now()
    #sensmeastestdb.tablename =  f'''sensmeastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    sensmeastestdb.CreateSensMeasTestTableDB()"""


    """newrow = {'set_sens' : 4614, 'meas_sens' : 26565, 'error':5}
    for i in tqdm(range(0,100)):
        sleep(0)
        newrow['set_sens']=random.randrange(500,1000)
        newrow['meas_sens']=newrow['set_sens']-random.randrange(-10,10)
        newrow['error']=newrow['set_sens']-newrow['meas_sens']
        sensmeastestdb.AddSensTestRow(senstestvalues=newrow)"""

    sensmeastestdb.GetSensMeasTestTable(testtablename="rfpssensmeastest_2024_04_26_11_53_59")
    #sensmeastestdb.CurDbTableSens.to_csv("sensmeastest_2024_03_24_11_41_05.csv")
    print(sensmeastestdb.CurDbTableSens)
    #sensmeastestdb.DropSensMeasTestTable(deletetable="esmsensmeastest_2024_04_15_14_52_52")
    sensmeastestdb.close()