import pandas as pd
import datetime
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR


########################################################################################################################
#   Frequency Accuracy Test Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   05 Mar 2024
#   InstConfigTableDB Class has the following member Functions
#   1. init()
#   2. CreateInstConfigTableDB()
#   3. AddInstRecord()
#   4. ModifyInstIp()---------
#   5. SelFreqDateFilter()-----------
#   6. GetInstRecord()
#   7. FreqIndxDbConClose()
########################################################################################################################
# This Creating the InstConfigTableDB Class
########################################################################################################################
class InstConfigTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        self.tablename = 'instconfig'

    ####################################################################################################################
    # This Function creates The Instrument Configuration Database Table
    ####################################################################################################################
    def CreateInstConfigTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (   inst_desc          TEXT          NOT NULL,
                                         remote_id          TEXT          NOT NULL,
                                         model_no           TEXT          NOT NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("InstConfigTableDB(CreateInstConfigTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("InstConfigTableDB(CreateInstConfigTableDB) - Error while creating FreqAccTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The New Instrument data in Instrument Configuration Database Table
    ####################################################################################################################
    def AddInstRecord(self, instcred={'inst_desc': 'ssg', 'remote_id': '192', 'model_no': 'new' }):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{instcred['inst_desc']}',
                                    '{instcred['remote_id']}', '{instcred['model_no']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("InstConfigTableDB(AddInstRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("InstConfigTableDB(AddInstRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR
    def ModifyInstIp(self, newip='', inst_name=''):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f'''UPDATE instconfig SET remote_ip = '{newip}' where inst_desc = '{inst_name}'; ''')
            self.connection.commit()
            if self.Debug == True:
                print("InstConfigTableDB(ModifyInstIp) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("InstConfigTableDB(ModifyInstIp)- Error in updating to table", error)
            return DATABASE_ADDDATA_ERROR
    def ModifyInstModelNo(self, newmodel='', inst_name=''):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f'''UPDATE instconfig SET remote_ip = '{newmodel}' where inst_desc = '{inst_name}'; ''')
            self.connection.commit()
            pass
            if self.Debug == True:
                print("InstConfigTableDB(ModifyInstModelNo) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("InstConfigTableDB(ModifyInstModelNo)- Error in updating to table", error)
            return DATABASE_ADDDATA_ERROR
    ####################################################################################################################
    # This Function Gets The Instrument data in Instrument Configuration Database Table For pandas Reading
    ####################################################################################################################
    def GetInstRecord(self, field='ssg', ipaddr=''):
        try:
            self.InstRecord = pd.read_sql_query(
                f'''SELECT * FROM instconfig WHERE inst_desc = {field}  AND remote_id = {ipaddr}''',
                con=self.connestablish)
            print(self.InstRecord)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to instconfig ", error)

    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelFreqDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.FreqDateFil = pd.read_sql_query(
                f'''SELECT * FROM freqaccindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            # print(self.FreqDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to freqaccindxtable ", error)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def FreqIndxDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################


if __name__ == "__main__":
    pass
########################################################################################################################