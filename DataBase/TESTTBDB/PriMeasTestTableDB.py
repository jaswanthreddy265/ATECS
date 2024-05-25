import random
from datetime import datetime
from time import sleep

import pandas as pd
import psycopg2

from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR
########################################################################################################################
#   PRI Measurement Test Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   06 Mar 2024
#   PriMeasTestTableDB Class has the following member Functions
#   1. init()
#   2. CreatePriMeasTestTableDB()
#   3. AddPriRow()
#   4. GetPriMeasTestTable()
#   5. DropPriTestTable()
#   6. close()
########################################################################################################################
# This Creating the PriMeasTestTableDB Class
########################################################################################################################
class PriMeasTestTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        timestamp = datetime.now()
        #self.tablename= f'''primeastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    ####################################################################################################################
    # This Function creates The  PRI Measurement Test Database Table
    ####################################################################################################################
    def CreatePriMeasTestTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (
                                         set_pri          FLOAT        NOT NULL,
                                         meas_pri         FLOAT        NOT NULL,
                                         error             FLOAT        NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PriMeasTestTableDB(CreatePriMeasTestTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("PriMeasTestTableDB(CreatePriMeasTestTableDB) - Error while creating PriMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in PRI Measurement Test Database Table
    ####################################################################################################################
    def AddPriTestRow(self, pritestvalues={'set_pri' : 4614, 'meas_pri' : 26565, 'error' : 3 }):
      #  print("AddPriRow")
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{pritestvalues['set_pri']}','{pritestvalues['meas_pri']}',
                                     '{pritestvalues['error']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PriMeasTestTableDB(AddPriRow) - New Row added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("PriMeasTestTableDB(AddPriRow)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The PRI Measurement Test Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetPriMeasTestTable(self, testtablename='primeastest_2024_03_24_11_41_05'):
        try:
            self.CurDbTablePri = pd.read_sql_query(
                f'''SELECT * FROM {testtablename} ''',
                con=self.connestablish)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to primeastesttable ", error)

    ####################################################################################################################
    # This Function Drops The PRI Measurement Test Database Table
    ####################################################################################################################
    def DropPriTestTable(self, deletetable='esmprimeastest'):
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
    primeastestdb = PriMeasTestTableDB(Debug=False)
    timestamp = datetime.now()
    primeastestdb.tablename =  f'''rfpsprimeastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    print(primeastestdb.tablename)
    primeastestdb.CreatePriMeasTestTableDB()

    newrow = {'set_pri': 4614, 'meas_pri': 26565, 'error': 5}
    start_pri = 40
    stop_pri = 500
    while start_pri <= stop_pri:
        print(start_pri)
        sleep(0)
        newrow['set_pri'] = start_pri
        newrow['meas_pri'] = newrow['set_pri'] - random.randrange(-1, 1)
        newrow['error'] = newrow['set_pri'] - newrow['meas_pri']

        primeastestdb.AddPriTestRow(pritestvalues=newrow)
        start_pri += 5
    """newrow = {'set_pri' : 4614, 'meas_pri' : 26565, 'error':5}
    for i in tqdm(range(0,100)):
        sleep(0)
        newrow['set_pri']=random.randrange(500,1000)
        newrow['meas_pri']=newrow['set_pri']-random.randrange(-10,10)
        newrow['error']=newrow['set_pri']-newrow['meas_pri']
        primeastestdb.AddPriTestRow(pritestvalues=newrow)"""

    #primeastestdb.GetPriMeasTestTable(testtablename="rfpsprimeastest_2024_04_26_11_53_59")
    #primeastestdb.CurDbTablePri.to_csv("primeastest_2024_03_24_11_41_05.csv")
    #print(primeastestdb.CurDbTablePri)
    #primeastestdb.DropPriTestTable(deletetable="esmprimeastest_2024_04_15_14_52_52")
    primeastestdb.close()