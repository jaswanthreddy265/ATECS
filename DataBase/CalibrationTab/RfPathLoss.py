import pandas as pd
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR
from sqlalchemy import create_engine

########################################################################################################################
#   RF Path Loss Injection/Radiation Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   27 May 2024
#   RFPathLossDB Class has the following member Functions
#   1. init()
#   2. CreateRFPathLossDB()
#   3. AddRecord()
#   4. DropRecord()
#   5. DropRecordInRange()
#   6. RetrieveRecordInRange()
#   7. RetrieveAll()
#   8. FreqIndxDbConClose()
########################################################################################################################
# This Creating the RFPathLossDB Class
########################################################################################################################
class RFPathLossDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        #self.tablename = 'rfpathlossradmode'

    ####################################################################################################################
    # This Function creates The RF Path Loss Radiation or Injection Mode Database Table
    ####################################################################################################################
    def CreateRFPathLossDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (   frequency          FLOAT         NOT NULL,
                                         path_loss          FLOAT         NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RFPathLossDB(CreateRFPathLossDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("RFPathLossDB(CreateRFPathLossDB) - Error while creating FreqAccTable", error)
            return error
    ####################################################################################################################
    # This Function Adds The New Records to the Database Table
    ####################################################################################################################
    def AddRecord(self, lossrecord={'frequency': '500', 'path_loss': '192'}):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{lossrecord['frequency']}', '{lossrecord['path_loss']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("RFPathLossDB(AddRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("RFPathLossDB(AddRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR
    """####################################################################################################################
    # This Function Deletes The Record from rfpathlossradmode or rfpathlossinjmode Index Database Table
    ####################################################################################################################
    def DeleteRecord(self,freqrecord=500):
        try:
            cursor = self.connestablish.cursor()
            delrecord = f'''DELETE FROM {self.tablename} WHERE frequency='{freqrecord}' '''
            cursor.execute(delrecord)
            self.connestablish.commit()
            print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
          print("Error while delating from the table", error)"""
    ####################################################################################################################
    # This Function Deletes The range of Records from rfpathlossradmode or rfpathlossinjmode Index Database Table
    ####################################################################################################################
    def DropRecordInRange(self,tablename = 'rfpathloss', freqfrom=1000, freqto=1500):
        try:
            cursor = self.connestablish.cursor()
            delfreqrecord = f'''DELETE FROM {tablename} WHERE frequency BETWEEN '{freqfrom}' AND '{freqto}' '''
            cursor.execute(delfreqrecord)
            self.connestablish.commit()
            print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
          print("Error while delating from the table", error)
    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def RetrieveRecordInRange(self,tablename='', rangefrom='', rangeto=''):
        try:
            self.RetrieveRange = pd.read_sql_query(
                f'''SELECT * FROM '{tablename}' WHERE frequency BETWEEN '{rangefrom}' AND '{rangeto}' ORDER BY CAST(frequency AS FLOAT) ASC''',
                con=self.connestablish)
            print(self.RetrieveRange)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Gets The RF Path Loss Data of Injection or Radiation from Database Table For pandas Reading
    ####################################################################################################################
    def RetrieveAll(self, tablename=''):
        try:
            self.CurDbTable = pd.read_sql_query(f'''SELECT * FROM {tablename} ORDER BY CAST(frequency AS FLOAT) ASC ''',
                                                con=self.connestablish)
            print(self.CurDbTable)
            self.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading from the table ", error)
    ####################################################################################################################
    # This Function Gets The RF Path Loss Data of Injection or Radiation from Database Table For pandas Reading
    ####################################################################################################################
    def DfUpdateDbTable(self, updatedata='', tablename=''):

        df = pd.DataFrame(updatedata)
        engine = create_engine(
            'postgresql+psycopg2://postgres:Platinum0435#@localhost:6543/atec')
        df.to_sql(f'{tablename}', engine, if_exists='append', index=False)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def RfPathLossDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################
if __name__ == "__main__":
    demotest = RFPathLossDB(Debug=True)
    demotest.tablename='rfpathlossinjmode'                          #
    demotest.CreateRFPathLossDB()


    """newrow = {'frequency':'700','path_loss':5}
    start_freq = 30100
    stop_freq = 39999
    step_freq = 100
    while start_freq<=stop_freq:
        print(start_freq)
        newrow['frequency'] = start_freq
        newrow['path_loss'] = float(newrow['frequency'])-5
        demotest.AddRecord(lossrecord=newrow)
        start_freq += step_freq"""
    """demotest.DeleteRecord(freqrecord='4000')
    demotest.RetrieveAll(tablename='rfpathlossradmode')
    demotest.RetrieveRecordInRange(tablename='rfpathlossradmode', rangefrom='1000', rangeto='3500')"""
    demotest.DropRecordInRange(tablename='rfpathlossinjmode', freqfrom=35000,freqto=40000)

    #demotest.RetrieveAll(tablename='rfpathlossinjmode')
    """data = {
              "frequency": [500, 600, 650],
              "path_loss": [60, 50, 95]
            }
    demotest.DfUpdateDbTable(updatedata=data,tablename='rfpathlossradmode')"""
    demotest.RetrieveAll(tablename='rfpathlossinjmode')
    demotest.CurDbTable.to_csv('rfpathlosstableasc_order.csv')
########################################################################################################################
