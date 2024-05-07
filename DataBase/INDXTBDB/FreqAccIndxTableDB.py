import pandas as pd
import datetime
import psycopg2
import random
from time import sleep
from tqdm import tqdm
from DataBase.TempTest.ConnectDB import Connect_to_Database
from DataBase.TestCases.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR

########################################################################################################################
#   Frequency Accuracy Test Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   05 Mar 2024
#   FreqAccIndxTableDB Class has the following member Functions
#   1. init()
#   2. CreateFreqAccIndxTableDB()
#   3. AddFreqRecord()
#   4. GetFreqAccIndxTable()
#   5. SelFreqDateFilter()
#   6. SelFreqDateSysFilter()
#   7. DeleteFreqRecord()
#   8. DropFreqIndxTable()
#   9. FreqIndxDbConClose()
########################################################################################################################
# This Creating the FreqAccIndxTableDB Class
########################################################################################################################
class FreqAccIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        self.tablename='freqaccindxtable'
    ####################################################################################################################
    # This Function creates The Frequency Accuracy Test Index Database Table
    ####################################################################################################################
    def CreateFreqAccIndxTableDB(self):
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
                                         start_freq         FLOAT         NOT NULL,
                                         stop_freq          FLOAT         NOT NULL,
                                         step_freq          FLOAT         NOT NULL,
                                         freq_list          TEXT          NULL,
                                         set_power          FLOAT         NOT NULL,
                                         pos_angle          FLOAT         NOT NULL,
                                         signal_cat         TEXT          NOT NULL,
                                         pw                 FLOAT         NOT NULL,
                                         pri                FLOAT         NOT NULL,
                                         ampl               FLOAT         NOT NULL,
                                         rms_error          FLOAT         NOT NULL,
                                         test_status        TEXT          NOT NULL,
                                         remarks            TEXT          NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("FreqAccIndxTableDB(CreateFreqAccIndxTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("FreqAccIndxTableDB(CreateFreqAccIndxTableDB) - Error while creating FreqAccTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Frequency Accuracy Test Index Database Table
    ####################################################################################################################
    def AddFreqRecord(self, usercred={'date' : datetime.datetime.now(),'username' : 'ranger', 'system_id' : 7,'system': 'RWR', 'mode': 'INJECTION',
                                   'test_tab_ref' : 'warnerfreqacctest_2024_04_15_14_52_57', 'start_freq' : 500, 'stop_freq' : 1000,
                                   'step_freq' : 50,'freq_list' : '600', 'set_power' : -30, 'pos_angle' : 140,
                                   'signal_cat' : 'PULSED', 'pw' : 1881, 'pri' : 1, 'ampl' : 850, 'rms_error' : 1,
                                   'test_status' : 'Completed', 'remarks' : 'new row added'
                                    }):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{usercred['date']}','{usercred['username']}',
                                    '{usercred['system_id']}', '{usercred['system']}', '{usercred['mode']}',
                                    '{usercred['test_tab_ref']}', '{usercred['start_freq']}', '{usercred['stop_freq']}',
                                    '{usercred['step_freq']}', '{usercred['freq_list']}', '{usercred['set_power']}',
                                    '{usercred['pos_angle']}', '{usercred['signal_cat']}', '{usercred['pw']}',
                                    '{usercred['pri']}','{usercred['ampl']}', '{usercred['rms_error']}',
                                    '{usercred['test_status']}', '{usercred['remarks']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("FreqAccIndxTableDB(AddFreqRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("FreqAccIndxTableDB(AddFreqRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR


    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetFreqAccIndxTable(self):
        try:
            self.FreqCurDbTable = pd.read_sql_query(
                f'''SELECT * FROM freqaccindxtable ''',
                con=self.connestablish)
            #print(self.FreqCurDbTable)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to freqaccindxtable ", error)
    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetFreqRowRecord(self, select_record='esmfreqacctest_2024_04_30_15_50_45'):
        try:
            self.GetFreqRowRecord = pd.read_sql_query(
                f'''SELECT * FROM freqaccindxtable WHERE test_tab_ref = '{select_record}' ''',
                con=self.connestablish)
            print(self.GetFreqRowRecord)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to freqaccindxtable ", error)

    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelFreqDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.FreqDateFil = pd.read_sql_query(
                f'''SELECT * FROM freqaccindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            #print(self.FreqDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to freqaccindxtable ", error)
    ##################################################################
    def SelFreqDateSysFilter(self, datefilterfrom='2024-04-20', datefilterto='2024-05-20', sysfilter='warner'):
        try:
            self.FreqDateSysFil = pd.read_sql_query(
                f'''SELECT * FROM freqaccindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' AND system='{sysfilter}'   ''',
                con=self.connestablish)
            print(self.FreqDateSysFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to freqaccindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Record By "test_tab_ref" from Frequency Accuracy Test Index Database Table
    ####################################################################################################################
    def DeleteFreqRecord(self,table_ref_id='freq_acc_test_0'):
        try:
            cursor = self.connestablish.cursor()
            delfreqrecord = f'''DELETE FROM {self.tablename} WHERE test_tab_ref='{table_ref_id}' '''
            cursor.execute(delfreqrecord)
            self.connestablish.commit()
           # print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
          print("Error in reading from to freqaccindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Frequency Accuracy Index Table from Database
    ####################################################################################################################
    def DropFreqIndxTable(self, deleteindxtable='esmfreqacctest'):
        try:
            cursor = self.connestablish.cursor()
            delete_table_query = f'''DROP TABLE {deleteindxtable}  '''
            cursor.execute(delete_table_query)
            self.connestablish.commit()
            print("successfully deleted the freqaccindxtable from DataBase")
        except (Exception, psycopg2.DatabaseError) as error:
            print("table does not exist", error)
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
    freqaccdb = FreqAccIndxTableDB(Debug=True)
    freqaccdb.tablename = 'freqaccindxtable'
    #freqaccdb.CreateFreqAccIndxTableDB()

    freqaccdb.GetFreqRowRecord(select_record='esmfreqacctest_2024_04_30_15_50_45')    #freq_list = [123.6,167,189]
    """freq_list_str=json.dumps(freq_list)
    print(type(freq_list_str))
    deser_freq = json.loads(freq_list_str)
    print(type(deser_freq[0]))"""
    """newrow = {'date' : datetime.datetime.now(),'username' : 'ravi',  'system_id' : 20, 'system': 'RWR', 'mode': 'INJECTION',
              'test_tab_ref' : 'warnerfreqacctest_2024_04_15_14_52_57', 'start_freq' : 500, 'stop_freq' : 1000,
              'step_freq' : 50, 'freq_list' : '', 'set_power' : -30, 'pos_angle' : 140,'signal_cat' : 'PULSE', 'pw' : 1881,
              'pri' : 1, 'ampl' : 850, 'rms_error' : 1, 'test_status' : 'Incomplete', 'remarks' : 'new row added'  }

    for i in tqdm(range(0,100)):
        sleep(0)
        newrow['date']= datetime.datetime.now()
        
        newrow['username']=random.choice(['BHASKAR', 'ADITYA', 'KALYANI', 'SATHISH', 'RAJU', 'SAGAR','MADHAVI', 'NAVYA',
                                          'JASWANTH','SUDHAKAR', 'AKHIL', 'KRISHNA'])
        newrow['system_id']=random.randrange(1,10)
        newrow['system'] = random.choice(['rwr', 'warner', 'esm', 'rfps'])
        newrow['mode'] = random.choice(['INJECTION', 'RADIATION'])
        newrow['test_tab_ref']=f'''{newrow["system"]}freqacctest_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'''
        #newrow['start_freq'] = random.randrange(0, 1000)
        #newrow['stop_freq'] = random.randrange(0, 1000)
        #newrow['step_freq'] = random.randrange(0, 1000)
        #newrow['freq_list'] = random.randrange(0, 1000)
        newrow['set_power']=random.randrange(-90,0)
        newrow['pos_angle']=random.randrange(0,360)
        newrow['signal_cat']=random.choice(['CW', 'PULSE'])                          #'STAGGER', 'JITTER', 'D&S', 'STABLE'
        newrow['pw']=random.randrange(0,1000)
        newrow['pri']=random.randrange(0,1000)
        newrow['ampl'] = random.randrange(-30, 0)
        newrow['rms_error'] = random.randrange(0, 100)
        newrow['test_status'] = random.choice(['Completed', 'Incomplete'])
        freqaccdb.AddFreqRecord(usercred=newrow)"""


    """for i in tqdm(range(0,30)):
        freqaccdb.DeleteFreqRecord(table_ref_id=f'''freq_acc_test_{i}''')
    freqaccdb.DeleteFreqRecord(table_ref_id='warnerfreqacctest_2024_04_15_14_52_80')
    freqaccdb.getfreqaccindxtable()
    freqaccdb.CurDbTable.to_csv("freqaccindxtabledb.csv")
    print(freqaccdb.FreqCurDbTable)
    freqaccdb.DropFreqIndxTable(deleteindxtable="freqaccindxtable")"""
    #freqaccdb.GetFreqAccIndxTable()
    #freqaccdb.SelFreqDateFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26")
    #freqaccdb.SelFreqDateSysFilter(datefilterfrom="2024-03-01", datefilterto="2024-05-26", sysfilter="rfps")
    #freqaccdb.DeleteFreqRecord(table_ref_id='esmfreqacctest_2024_04_30_14_29_18')
    freqaccdb.FreqIndxDbConClose()

########################################################################################################################