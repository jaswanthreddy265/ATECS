import random
from datetime import datetime
from time import sleep

import pandas as pd
from tqdm import tqdm
import psycopg2

from DataBase.TempTest.ConnectDB import Connect_to_Database
from DataBase.TestCases.ErrorCodesDatabase import DATABASE_CONNECTION_ERROR, SUCCESS, DATABASE_ADDDATA_ERROR
########################################################################################################################
#   DOA Measurement Test Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   06 Mar 2024
#   DoaMeasTestTableDB Class has the following member Functions
#   1. init()
#   2. CreateDoaMeasTestTableDB()
#   3. AddDoaRow()
#   4. GetDoaMeasTestTable()
#   5. DropDoaTestTable()
#   6. close()
########################################################################################################################
# This Creating the DoaMeasTestTableDB Class
########################################################################################################################
class DoaMeasTestTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        timestamp = datetime.now()
        self.tablename= f'''doameastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    ####################################################################################################################
    # This Function creates The  DOA Measurement Test Database Table
    ####################################################################################################################
    def CreateDoaMeasTestTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (
                                         set_doa          FLOAT        NOT NULL,
                                         meas_doa         FLOAT        NOT NULL,
                                         error             FLOAT        NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("DoaMeasTestTableDB(CreateDoaMeasTestTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("DoaMeasTestTableDB(CreateDoaMeasTestTableDB) - Error while creating DoaMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in DOA Measurement Test Database Table
    ####################################################################################################################
    def AddDoaTestRow(self, doatestvalues={'set_doa' : 4614, 'meas_doa' : 26565, 'error' : 3 }):
      #  print("AddDoaRow")
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{doatestvalues['set_doa']}','{doatestvalues['meas_doa']}',
                                     '{doatestvalues['error']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("DoaMeasTestTableDB(AddDoaRow) - New Row added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("DoaMeasTestTableDB(AddDoaRow)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The DOA Measurement Test Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetDoaMeasTestTable(self, testtablename='doameastest_2024_03_24_11_41_05'):
        try:
            self.CurDbTableDoa = pd.read_sql_query(
                f'''SELECT * FROM {testtablename} ''',
                con=self.connestablish)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to doameastesttable ", error)

    ####################################################################################################################
    # This Function Drops The DOA Measurement Test Database Table
    ####################################################################################################################
    def DropDoaTestTable(self, deletetable='esmdoameastest'):
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
    doameastestdb = DoaMeasTestTableDB(Debug=False)
    """timestamp = datetime.now()
    #doameastestdb.tablename =  f'''doameastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    doameastestdb.CreateDoaMeasTestTableDB()"""


    """newrow = {'set_doa' : 4614, 'meas_doa' : 26565, 'error':5}
    for i in tqdm(range(0,100)):
        sleep(0)
        newrow['set_doa']=random.randrange(500,1000)
        newrow['meas_doa']=newrow['set_doa']-random.randrange(-10,10)
        newrow['error']=newrow['set_doa']-newrow['meas_doa']
        doameastestdb.AddDoaTestRow(doatestvalues=newrow)"""

    doameastestdb.GetDoaMeasTestTable(testtablename="rfpsdoameastest_2024_04_26_11_53_59")
    #doameastestdb.CurDbTableDoa.to_csv("doameastest_2024_03_24_11_41_05.csv")
    print(doameastestdb.CurDbTableDoa)
    #doameastestdb.DropDoaTestTable(deletetable="esmdoameastest_2024_04_15_14_52_52")
    doameastestdb.close()