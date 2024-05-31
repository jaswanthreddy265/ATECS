import random
from datetime import datetime
from time import sleep

import pandas as pd
import psycopg2

from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR
########################################################################################################################
#   Pulse Width Measurement Test Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   06 Mar 2024
#   PwMeasTestTableDB Class has the following member Functions
#   1. init()
#   2. CreatePwMeasTestTableDB()
#   3. AddPwRow()
#   4. GetPwMeasTestTable()
#   5. DropPwTestTable()
#   6. close()
########################################################################################################################
# This Creating the PwMeasTestTableDB Class
########################################################################################################################
class PwMeasTestTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        timestamp = datetime.now()
        self.tablename= f'''pwmeastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    ####################################################################################################################
    # This Function creates The  Pulse Width Measurement Test Database Table
    ####################################################################################################################
    def CreatePwMeasTestTableDB(self, system=''):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {system}{self.tablename}
                                     (
                                         set_pw          FLOAT        NOT NULL,
                                         meas_pw         FLOAT        NOT NULL,
                                         error             FLOAT        NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PwMeasTestTableDB(CreatePwMeasTestTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("PwMeasTestTableDB(CreatePwMeasTestTableDB) - Error while creating PwMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Pulse Width Measurement Test Database Table
    ####################################################################################################################
    def AddPwTestRow(self, pwtestvalues={'set_pw' : 4614, 'meas_pw' : 26565, 'error' : 3 }):
      #  print("AddPwRow")
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{pwtestvalues['set_pw']}','{pwtestvalues['meas_pw']}',
                                     '{pwtestvalues['error']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PwMeasTestTableDB(AddPwRow) - New Row added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("PwMeasTestTableDB(AddPwRow)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The Pulse Width Measurement Test Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetPwMeasTestTable(self, testtablename='pwmeastest_2024_03_24_11_41_05'):
        try:
            self.CurDbTablePw = pd.read_sql_query(
                f'''SELECT * FROM {testtablename} ''',
                con=self.connestablish)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to pwmeastesttable ", error)

    ####################################################################################################################
    # This Function Drops The Pulse Width Measurement Test Database Table
    ####################################################################################################################
    def DropPwTestTable(self, deletetable='esmpwmeastest'):
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
    pwmeastestdb = PwMeasTestTableDB(Debug=False)
    timestamp = datetime.now()
    pwmeastestdb.tablename =  f'''rfpspwmeastest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    print(pwmeastestdb.tablename)
    pwmeastestdb.CreatePwMeasTestTableDB()

    newrow = {'set_pri': 4614, 'meas_pri': 26565, 'error': 5}
    start_pw = 79
    stop_pw = 550
    while start_pw <= stop_pw:
        print(start_pw)
        sleep(0)
        newrow['set_pw'] = start_pw
        newrow['meas_pw'] = newrow['set_pw'] - random.randrange(-1, 1)
        newrow['error'] = newrow['set_pw'] - newrow['meas_pw']

        pwmeastestdb.AddPwTestRow(pwtestvalues=newrow)
        start_pw += 15
    """newrow = {'set_pw' : 4614, 'meas_pw' : 26565, 'error':5}
    for i in tqdm(range(0,100)):
        sleep(0)
        newrow['set_pw']=random.randrange(500,1000)
        newrow['meas_pw']=newrow['set_pw']-random.randrange(-10,10)
        newrow['error']=newrow['set_pw']-newrow['meas_pw']
        pwmeastestdb.AddPwTestRow(pwtestvalues=newrow)"""

    #pwmeastestdb.GetPwMeasTestTable(testtablename="rfpspwmeastest_2024_04_26_11_53_59")
    #pwmeastestdb.CurDbTablePw.to_csv("pwmeastest_2024_03_24_11_41_05.csv")
    #print(pwmeastestdb.CurDbTablePw)
    #pwmeastestdb.DropPwTestTable(deletetable="esmpwmeastest_2024_04_15_14_52_52")
    pwmeastestdb.close()