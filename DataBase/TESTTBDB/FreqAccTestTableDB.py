import random
from datetime import datetime
from time import sleep

import pandas as pd
import psycopg2

from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR
########################################################################################################################
#   Frequency Accuracy Test Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   06 Mar 2024
#   FreqAccTestTableDB Class has the following member Functions
#   1. init()
#   2. CreateFreqAccTestTableDB()
#   3. AddFreqRow()
#   4. GetFreqAccTestTable()
#   5. DropFreqTestTable()
#   6. close()
########################################################################################################################
# This Creating the FreqAccTestTableDB Class
########################################################################################################################
class FreqAccTestTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        timestamp = datetime.now()
        self.tablename= f'''freqacctest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    ####################################################################################################################
    # This Function creates The  Frequency Accuracy Test Database Table
    ####################################################################################################################
    def CreateFreqAccTestTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (
                                         set_freq          FLOAT        NOT NULL,
                                         meas_freq         FLOAT        NOT NULL,
                                         error             FLOAT        NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("FreqAccTestTableDB(CreateFreqAccTestTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("FreqAccTestTableDB(CreateFreqAccTestTableDB) - Error while creating FreqAccTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Frequency Accuracy Test Database Table
    ####################################################################################################################
    def AddFreqTestRow(self, freqtestvalues={'set_freq' : 4614, 'meas_freq' : 26565, 'error' : 3 }):
      #  print("AddFreqRow")
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{freqtestvalues['set_freq']}','{freqtestvalues['meas_freq']}',
                                     '{freqtestvalues['error']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("FreqAccTestTableDB(AddFreqRow) - New Row added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("FreqAccTestTableDB(AddFreqRow)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetFreqAccTestTable(self, testtablename='freqacctest_2024_03_24_11_41_05'):
        try:
            self.CurDbTableFreq = pd.read_sql_query(
                f'''SELECT * FROM {testtablename} ''',
                con=self.connestablish)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to freqacctesttable ", error)

    ####################################################################################################################
    # This Function Drops The Frequency Accuracy Test Database Table
    ####################################################################################################################
    def DropFreqTestTable(self, deletetable='esmfreqacctest'):
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
    freqacctestdb = FreqAccTestTableDB(Debug=False)
    timestamp = datetime.now()
    freqacctestdb.tablename =  f'''rfpsfreqacctest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    print(freqacctestdb.tablename)
    freqacctestdb.CreateFreqAccTestTableDB()


    newrow = {'set_freq' : 4614, 'meas_freq' : 26565, 'error':5}
    start_freq = 1000
    stop_freq = 30000
    while start_freq <= stop_freq:
        print(start_freq)
        sleep(0)
        newrow['set_freq'] = start_freq
        newrow['meas_freq'] = newrow['set_freq'] - random.randrange(-1, 1)
        newrow['error'] = newrow['set_freq'] - newrow['meas_freq']

        freqacctestdb.AddFreqTestRow(freqtestvalues=newrow)
        start_freq += 600
    """for i in tqdm(range(0,100)):
        sleep(0)
        newrow['set_freq']=random.randrange(500,1000)
        newrow['meas_freq']=newrow['set_freq']-random.randrange(-10,10)
        newrow['error']=newrow['set_freq']-newrow['meas_freq']
        freqacctestdb.AddFreqTestRow(freqtestvalues=newrow)"""

    #freqacctestdb.GetFreqAccTestTable(testtablename="rfpsfreqacctest_2024_04_26_11_53_59")
    #freqacctestdb.CurDbTableFreq.to_csv("freqacctest_2024_03_24_11_41_05.csv")
    #print(freqacctestdb.CurDbTableFreq)
    #freqacctestdb.DropFreqTestTable(deletetable="esmfreqacctest_2024_04_15_14_52_52")
    freqacctestdb.close()



