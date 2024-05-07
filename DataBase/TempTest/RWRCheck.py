import random
from datetime import datetime
from time import sleep

import pandas as pd
from tqdm import tqdm
import psycopg2
from ErrorCodesDatabase import DATABASE_CONNECTION_ERROR, SUCCESS, DATABASE_ADDDATA_ERROR
########################################################################################################################
#   RWR Frequency Accuracy Test Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   06 Mar 2023
#   RWR FreqAccTestTableDB Class has the following member Functions
#   1. connect()
#   2. CreateRWRFreqAccTestTableDB()
#   3. AddRWRFreqRow()
#   4. getrwrfreqacctesttable()
#   5. close()
#   6. main()
########################################################################################################################
# This Creating the RWR FreqAccTestTableDB Class
########################################################################################################################
class HealthDataDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection=True
        self.tablename=self.testtabname
    ########################################################################################################################
    # This Function Establish Connection with Database
    ####################################################################################################################
    def connect(self, DataBaseSettings = {
                                'user' :'postgres',
                                'password':'Platinum0435#',
                                'host':'localhost',
                                'database' : 'atec',
                                'port': 6543
                                }):
        try:
            self.connection = psycopg2.connect(
                user=DataBaseSettings['user'],
                password=DataBaseSettings['password'],
                host=DataBaseSettings['host'],
                database=DataBaseSettings['database'],
                port=DataBaseSettings['port']
            )
            self.CreateRWRFreqAccTestTableDB()
            if self.Debug == True:
                print('HealthDataDB(connect) - Connection Established  *****************')
            return SUCCESS
        except (Exception, psycopg2.Error) as error:
            if self.Debug == True:
                print("HealthDataDB(connect) -Error while connecting to PostgreSQL", error)
            return DATABASE_CONNECTION_ERROR
    ####################################################################################################################
    # This Function creates The RWR Frequency Accuracy Test Index Database Table
    ####################################################################################################################
    def CreateHealthDB(self):
        try:
            cursor = self.connection.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (
                                         date                TIMESTAMP        NOT NULL,
                                         sensor1             FLOAT         NULL,
                                         sensor2             FLOAT         NULL,
                                         sensor3             FLOAT         NULL,
                                         sensor4             FLOAT         NULL,
                                         sensor5             FLOAT         NULL,
                                         sensor6             FLOAT         NULL,
                                         sensor7             FLOAT         NULL,
                                         sensor8             FLOAT         NULL,
                                         sensor9             FLOAT         NULL,
                                         sensor10            FLOAT         NULL,
                                         sensor11            FLOAT         NULL,
                                         sensor12            FLOAT         NULL,
                                         sensor13            FLOAT         NULL,
                                         sensor14            FLOAT         NULL,
                                         sensor15            FLOAT         NULL
                                         
                                     ); '''
            cursor.execute(create_table_query)
            self.connection.commit()
            if self.Debug == True:
                print("HealthDataDB(CreateHealthDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("HealthDataDB(CreateHealthDB) - Error while creating RWRFreqAccTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in RWR Frequency Accuracy Test Index Database Table
    ####################################################################################################################
    def AddRWRFreqRow(self, insertrecord={'date' : 4614, 'sensor1' : 26565, 'error' : 3 }):
      #  print("AddRWRFreqRow")
        try:
            cursor = self.connection.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{insertrecord['date']}','{insertrecord['sensor1']}',
                                     '{insertrecord['error']}'  '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connection.commit()
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("RWRFreqAccTestTableDB(AddRWRFreqRow)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

        if self.Debug == True:
            print("RWRFreqAccTestTableDB(AddRWRFreqRow) - New Row added successfully")

    ####################################################################################################################
    # This Function Gets The RWR  Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def getrwrfreqacctesttable(self, testtablename='rwrfreqacctest_2024_03_24_11_41_05'):
        try:
            self.CurDbTable = pd.read_sql_query(
                f'''SELECT * FROM {testtablename} ''',
                con=self.connection)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to rwrfreqacctesttable ", error)

    ####################################################################################################################
    # This Function Gets The RWR  Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def testtabname(self, system='rwr'):
        timestamp = datetime.now()
        self.testtablename=f'''{system}freqacctest_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}'''
        print(self.testtablename)

    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def close(self):
        self.connection.close()
        if self.Debug == True:
            print("PostgreSQL connection is closed")
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
########################################################################################################################
if __name__ == "__main__":
    DataBaseSettings = {
        'user': 'postgres',
        'password': 'Platinum0435#',
        'host': 'localhost',
        'database': 'atec',
        'port': 6543
    }
    rwrfreqaccdb = RWRFreqAccTestTableDB(Debug=False)
    print(rwrfreqaccdb.connect(DataBaseSettings))
    rwrfreqaccdb.testtabname(system='rwr')
    rwrfreqaccdb.CreateRWRFreqAccTestTableDB()


    newrow = {'set_freq' : 4614, 'meas_freq' : 26565, 'error':5}
    """for i in tqdm(range(0,100)):
        sleep(0)
        newrow['set_freq']=random.randrange(500,1000)
        newrow['meas_freq']=newrow['set_freq']-random.randrange(-10,10)
        newrow['error']=newrow['set_freq']-newrow['meas_freq']"""
    rwrfreqaccdb.AddRWRFreqRow(freqtestvalues=newrow)

    """rwrfreqaccdb.getrwrfreqacctesttable()
    rwrfreqaccdb.CurDbTable.to_csv("rwrfreqacctest_2024_03_24_11_41_05.csv")
    print(rwrfreqaccdb.CurDbTable)"""
    rwrfreqaccdb.close()