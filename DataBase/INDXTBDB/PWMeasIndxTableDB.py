import pandas as pd
import datetime
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR


########################################################################################################################
#   Pulse Width Measurement Test Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   05 Mar 2024
#   PwMeasIndxTableDB Class has the following member Functions
#   1. init()
#   2. CreatePwMeasIndxTableDB()
#   3. AddPwRecord()
#   4. GetPwMeasIndxTable()
#   5. SelPwDateFilter()
#   6. SelPwDateSysFilter()
#   7. DeletePwRecord()
#   8. DropPwIndxTable()
#   9. PwIndxDbConClose()
########################################################################################################################
# This Creating the PwMeasIndxTableDB Class
########################################################################################################################
class PwMeasIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        self.tablename = 'pwmeasindxtable'

    ####################################################################################################################
    # This Function creates The Pulse Width Measurement Test Index Database Table
    ####################################################################################################################
    def CreatePwMeasIndxTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (   date               TIMESTAMP     NOT NULL,
                                         username           TEXT          NOT NULL,
                                         system_id          FLOAT         NOT NULL,
                                         system             TEXT          NOT NULL,
                                         mode               TEXT          NOT NULL,
                                         test_tab_ref       TEXT          NOT NULL,
                                         start_pw           FLOAT         NOT NULL,
                                         stop_pw            FLOAT         NOT NULL,
                                         step_pw            FLOAT         NOT NULL,
                                         pw_list            TEXT          NULL,
                                         set_power          FLOAT         NOT NULL,
                                         pos_angle          FLOAT         NOT NULL,
                                         signal_cat         TEXT          NOT NULL,
                                         freq               FLOAT         NOT NULL,
                                         pri                FLOAT         NOT NULL,
                                         ampl               FLOAT         NOT NULL,
                                         rms_error          FLOAT         NOT NULL,
                                         test_status        TEXT          NOT NULL,
                                         remarks            TEXT          NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PwMeasIndxTableDB(CreatePwMeasIndxTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("PwMeasIndxTableDB(CreatePwMeasIndxTableDB) - Error while creating PwMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Pulse Width Measurement Test Index Database Table
    ####################################################################################################################
    def AddPwRecord(self,
                      usercred={'date': datetime.datetime.now(), 'username': 'ranger', 'system_id': 7, 'system': 'RWR',
                                'mode': 'INJECTION', 'test_tab_ref': 'warnerpwmeastest_2024_04_15_14_52_57', 'start_pw': 500,
                                'stop_pw': 1000, 'step_pw': 50, 'pw_list': '600', 'set_power': -30, 'pos_angle': 140,
                                'signal_cat': 'PULSED', 'freq': 1881, 'pri': 1, 'ampl': 850, 'rms_error': 1,
                                'test_status': 'Completed', 'remarks': 'new row added'
                                }):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{usercred['date']}','{usercred['username']}',
                                    '{usercred['system_id']}', '{usercred['system']}', '{usercred['mode']}',
                                    '{usercred['test_tab_ref']}', '{usercred['start_pw']}', '{usercred['stop_pw']}',
                                    '{usercred['step_pw']}', '{usercred['pw_list']}', '{usercred['set_power']}',
                                    '{usercred['pos_angle']}', '{usercred['signal_cat']}', '{usercred['freq']}',
                                    '{usercred['pri']}','{usercred['ampl']}', '{usercred['rms_error']}',
                                    '{usercred['test_status']}', '{usercred['remarks']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PwMeasIndxTableDB(AddPwRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("PwMeasIndxTableDB(AddPwRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The Pulse Width Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetPwMeasIndxTable(self):
        try:
            self.PwCurDbTable = pd.read_sql_query(
                f'''SELECT * FROM pwmeasindxtable ''',
                con=self.connestablish)
            # print(self.PwCurDbTable)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to pwmeasindxtable ", error)
    ####################################################################################################################
    # This Function Gets The Pulse width measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetPwRowRecord(self, select_record='esmpwmeastest_2024_04_30_15_50_45'):
        try:
            self.GetPwIndxRowRecord = pd.read_sql_query(
                f'''SELECT * FROM pwmeasindxtable WHERE test_tab_ref = '{select_record}' ''',
                con=self.connestablish)
            print(self.GetPwIndxRowRecord)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to pwmeasindxtable ", error)

    ####################################################################################################################
    # This Function Gets The Pulse Width Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelPwDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.PwDateFil = pd.read_sql_query(
                f'''SELECT * FROM pwmeasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            #print(self.PwDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to pwmeasindxtable ", error)

    ##################################################################
    def SelPwDateSysFilter(self, datefilterfrom='', datefilterto='', sysfilter=''):
        try:
            self.PwDateSysFil = pd.read_sql_query(
                f'''SELECT * FROM pwmeasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' AND system='{sysfilter}' ''',
                con=self.connestablish)
            print(self.PwDateSysFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to pwmeasindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Record By "test_tab_ref" from Pulse Width Measurement Test Index Database Table
    ####################################################################################################################
    def DeletePwRecord(self, table_ref_id='pw_meas_test_0'):
        try:
            cursor = self.connestablish.cursor()
            delpwrecord = f'''DELETE FROM {self.tablename} WHERE test_tab_ref='{table_ref_id}' '''
            cursor.execute(delpwrecord)
            self.connestablish.commit()
        # print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to pwmeasindxtable ", error)
    ####################################################################################################################
    # This Function Drops The Pulse Width Measurement Index Table from Database
    ####################################################################################################################
    def DropPwIndxTable(self, deletetable='esmpwmeastest'):
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
    def PwIndxDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################


if __name__ == "__main__":
    pwmeasdb = PwMeasIndxTableDB(Debug=True)
    pwmeasdb.tablename = 'pwmeasindxtable'
    pwmeasdb.CreatePwMeasIndxTableDB()

    newrow = {'date' : datetime.datetime.now(),'username' : 'kalyani',  'system_id' : 5, 'system': 'rfps', 'mode': 'INJECTION',
              'test_tab_ref' : 'rfpspwmeastest_2024_05_18_14_25_12', 'start_pw' : 79, 'stop_pw' : 550,
              'step_pw' : 15, 'pw_list' : '', 'set_power' : -30, 'pos_angle' : 140,'signal_cat' : 'PULSE', 'freq' : 1881,
              'pri' : 1, 'ampl' : 850, 'rms_error' : 1, 'test_status' : 'Incomplete', 'remarks' : 'new row added'  }
    pwmeasdb.AddPwRecord(usercred=newrow)

    """pwmeasdb.DeletePwRecord(table_ref_id='warnerpwmeastest_2024_04_15_14_52_80')
    pwmeasdb.getpwmeasindxtable()
    pwmeasdb.CurDbTable.to_csv("pwmeasindxtabledb.csv")
    print(pwmeasdb.PwCurDbTable)
    pwmeasdb.DropPwIndxTable(deletetable="")"""
    #pwmeasdb.GetPwMeasIndxTable()
    # pwmeasdb.SelPwDateFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26")
    # pwmeasdb.SelPwDateSysFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26", sysfilter='rwr')
    pwmeasdb.PwIndxDbConClose()

########################################################################################################################