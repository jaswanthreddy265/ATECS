import random
from datetime import datetime
from time import sleep

import pandas as pd
import psycopg2

from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR
########################################################################################################################
#   Amplitude Accuracy Test Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   06 Mar 2024
#   AmplAccTestTableDB Class has the following member Functions
#   1. init()
#   2. CreateAmplAccTestTableDB()
#   3. AddAmplRow()
#   4. GetAmplAccTestTable()
#   5. DropAmplTestTable()
#   6. close()
########################################################################################################################
# This Creating the AmplAccTestTableDB Class
########################################################################################################################
class AmplAccTestTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        timestamp = datetime.now()
        #self.tablename= f'''amplacctest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    ####################################################################################################################
    # This Function creates The  Amplitude Accuracy Test Database Table
    ####################################################################################################################
    def CreateAmplAccTestTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (
                                         set_ampl          FLOAT        NOT NULL,
                                         meas_ampl         FLOAT        NOT NULL,
                                         error             FLOAT        NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("AmplAccTestTableDB(CreateAmplAccTestTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("AmplAccTestTableDB(CreateAmplAccTestTableDB) - Error while creating AmplAccTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Amplitude Accuracy Test Database Table
    ####################################################################################################################
    def AddAmplTestRow(self, ampltestvalues={'set_ampl' : 4614, 'meas_ampl' : 26565, 'error' : 3 }):
      #  print("AddAmplRow")
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{ampltestvalues['set_ampl']}','{ampltestvalues['meas_ampl']}',
                                     '{ampltestvalues['error']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("AmplAccTestTableDB(AddAmplRow) - New Row added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("AmplAccTestTableDB(AddAmplRow)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The Amplitude Accuracy Test Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetAmplAccTestTable(self, testtablename='amplacctest_2024_03_24_11_41_05'):
        try:
            self.CurDbTableAmpl = pd.read_sql_query(
                f'''SELECT * FROM {testtablename} ''',
                con=self.connestablish)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to amplacctesttable ", error)

    ####################################################################################################################
    # This Function Drops The Amplitude Accuracy Test Database Table
    ####################################################################################################################
    def DropAmplTestTable(self, deletetable='esmamplacctest'):
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
    amplacctestdb = AmplAccTestTableDB(Debug=False)
    timestamp = datetime.now()
    amplacctestdb.tablename =  f'''rfpsamplacctest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
    print(amplacctestdb.tablename)
    amplacctestdb.CreateAmplAccTestTableDB()


    newrow = {'set_ampl' : 4614, 'meas_ampl' : 26565, 'error':5}
    start_ampl = -70
    stop_ampl = 10
    while start_ampl <= stop_ampl:
        print(start_ampl)
        sleep(1)
        newrow['set_ampl'] = start_ampl
        newrow['meas_ampl'] = newrow['set_ampl'] - random.randrange(-1, 1)
        newrow['error'] = newrow['set_ampl'] - newrow['meas_ampl']

        amplacctestdb.AddAmplTestRow(ampltestvalues=newrow)
        start_ampl += 2
    """for i in tqdm(range(0,50)):
        sleep(0)
        
        newrow['set_ampl'] = set_ampl+step_ampl
        #newrow['set_ampl']=random.randrange(-90,90)
        newrow['meas_ampl']=newrow['set_ampl']-random.randrange(-1,1)
        newrow['error']=newrow['set_ampl']-newrow['meas_ampl']
        amplacctestdb.AddAmplTestRow(ampltestvalues=newrow)"""

    #amplacctestdb.GetAmplAccTestTable(testtablename="rfpsamplacctest_2024_04_26_11_53_59")
    #amplacctestdb.CurDbTableAmpl.to_csv("amplacctest_2024_03_24_11_41_05.csv")
    #print(amplacctestdb.CurDbTableAmpl)
    #amplacctestdb.DropAmplTestTable(deletetable="esmamplacctest_2024_04_15_14_52_52")
    amplacctestdb.close()