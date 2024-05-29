import pandas as pd
import datetime
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR


########################################################################################################################
#   Amplitude Accuracy Test Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   05 Mar 2024
#   AmplAccIndxTableDB Class has the following member Functions
#   1. init()
#   2. CreateAmplAccIndxTableDB()
#   3. AddAmplRecord()
#   4. GetAmplAccIndxTable()
#   5. SelAmplDateFilter()
#   6. SelAmplDateSysFilter()
#   7. DeleteAmplRecord()
#   8. DropAmplIndxTable
#   9. AmplIndxDbConClose()
########################################################################################################################
# This Creating the AmplAccIndxTableDB Class
########################################################################################################################
class AmplAccIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        self.tablename = 'amplaccindxtable'

    ####################################################################################################################
    # This Function creates The Amplitude Accuracy Test Index Database Table
    ####################################################################################################################
    def CreateAmplAccIndxTableDB(self):
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
                                         start_ampl         FLOAT         NOT NULL,
                                         stop_ampl          FLOAT         NOT NULL,
                                         step_ampl          FLOAT         NOT NULL,
                                         ampl_list          TEXT          NULL,
                                         set_power          FLOAT         NOT NULL,
                                         pos_angle          FLOAT         NOT NULL,
                                         signal_cat         TEXT          NOT NULL,
                                         pw                 FLOAT         NOT NULL,
                                         pri                FLOAT         NOT NULL,
                                         freq               FLOAT         NOT NULL,
                                         rms_error          FLOAT         NOT NULL,
                                         test_status        TEXT          NOT NULL,
                                         remarks            TEXT          NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("AmplAccIndxTableDB(CreateAmplAccIndxTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("AmplAccIndxTableDB(CreateAmplAccIndxTableDB) - Error while creating AmplAccTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Amplitude Accuracy Test Index Database Table
    ####################################################################################################################
    def AddAmplRecord(self,
                      usercred={'date': datetime.datetime.now(), 'username': 'ranger', 'system_id': 7, 'system': 'RWR',
                                'mode': 'INJECTION',
                                'test_tab_ref': 'warneramplacctest_2024_04_15_14_52_57', 'start_ampl': 500,
                                'stop_ampl': 1000,
                                'step_ampl': 50, 'ampl_list': '600', 'set_power': -30, 'pos_angle': 140,
                                'signal_cat': 'PULSED', 'pw': 1881, 'pri': 1, 'freq': 850, 'rms_error': 1,
                                'test_status': 'Completed', 'remarks': 'new row added'
                                }):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{usercred['date']}','{usercred['username']}',
                                    '{usercred['system_id']}', '{usercred['system']}', '{usercred['mode']}',
                                    '{usercred['test_tab_ref']}', '{usercred['start_ampl']}', '{usercred['stop_ampl']}',
                                    '{usercred['step_ampl']}', '{usercred['ampl_list']}', '{usercred['set_power']}',
                                    '{usercred['pos_angle']}', '{usercred['signal_cat']}', '{usercred['pw']}',
                                    '{usercred['pri']}','{usercred['freq']}', '{usercred['rms_error']}',
                                    '{usercred['test_status']}', '{usercred['remarks']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("AmplAccIndxTableDB(AddAmplRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("AmplAccIndxTableDB(AddAmplRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The Amplitude Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetAmplAccIndxTable(self):
        try:
            self.AmplCurDbTable = pd.read_sql_query(
                f'''SELECT * FROM amplaccindxtable ''',
                con=self.connestablish)
            print(self.AmplCurDbTable)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to amplaccindxtable ", error)

    """####################################################################################################################
    # This Function Gets The Amplitude Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.AmplDateFil = pd.read_sql_query(
                f'''SELECT date, username, system_id, system, mode, test_tab_ref FROM amplaccindxtable WHERE date BETWEEN 
                '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            print(self.AmplDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to amplaccindxtable ", error)
    ####################################################################################################################
    # This Function Gets The Amplitude Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelAmplDateFilter(self,indxtablename='', datefilterfrom='', datefilterto=''):
        try:
            self.AmplIndxDateFil = pd.read_sql_query(
                f'''SELECT * FROM '{indxtablename}' WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            print(self.AmplIndxDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to amplaccindxtable ", error)
    ##################################################################"""

    ####################################################################################################################
    # This Function Gets The Amplitude Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelAmplDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.AmplDateFil = pd.read_sql_query(
                f'''SELECT * FROM amplaccindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            #print(self.AmplDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to amplaccindxtable ", error)

    ##################################################################
    def SelAmplDateSysFilter(self, datefilterfrom='', datefilterto='', sysfilter=''):
        try:
            self.AmplDateSysFil = pd.read_sql_query(
                f'''SELECT * FROM amplaccindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' AND system='{sysfilter}' ''',
                con=self.connestablish)
            print(self.AmplDateSysFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to amplaccindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Record By "test_tab_ref" from Amplitude Accuracy Test Index Database Table
    ####################################################################################################################
    def DeleteAmplRecord(self, table_ref_id='ampl_acc_test_0'):
        try:
            cursor = self.connestablish.cursor()
            delamplrecord = f'''DELETE FROM {self.tablename} WHERE test_tab_ref='{table_ref_id}' '''
            cursor.execute(delamplrecord)
            self.connestablish.commit()
        # print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to amplaccindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Amplitude Accuracy Index Table from Database
    ####################################################################################################################
    def DropAmplIndxTable(self, deleteindxtable='amplaccindxtable'):
        try:
            cursor = self.connestablish.cursor()
            delete_table_query = f'''DROP TABLE {deleteindxtable}  '''
            cursor.execute(delete_table_query)
            self.connestablish.commit()
            print("successfully deleted the amplaccindxtable from DataBase")
        except (Exception, psycopg2.DatabaseError) as error:
            print("table does not exist", error)
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def AmplIndxDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################


if __name__ == "__main__":
    amplaccdb = AmplAccIndxTableDB(Debug=True)
    amplaccdb.tablename = 'amplaccindxtable'
    amplaccdb.CreateAmplAccIndxTableDB()

    # ampl_list = [123.6,167,189]
    """ampl_list_str=json.dumps(ampl_list)
    print(type(ampl_list_str))
    deser_ampl = json.loads(ampl_list_str)
    print(type(deser_ampl[0]))"""
    newrow = {'date' : datetime.datetime.now(),'username' : 'Madhavi',  'system_id' : 1, 'system': 'rfps', 'mode': 'INJECTION',
              'test_tab_ref' : 'rfpsamplacctest_2024_05_18_15_01_25', 'start_ampl' : -70, 'stop_ampl' : 10,
              'step_ampl' :2, 'ampl_list' : '', 'set_power' : -30, 'pos_angle' : 140,'signal_cat' : 'PULSE', 'pw' : 1881,
              'pri' : 1, 'freq' : 850, 'rms_error' : 1, 'test_status' : 'Completed', 'remarks' : ''  }

    """for i in tqdm(range(0,5)):
        sleep(0)
        newrow['date']= datetime.datetime.now()

        newrow['username']=random.choice(['BHASKAR', 'ADITYA', 'KALYANI', 'SATHISH', 'RAJU', 'SAGAR','MADHAVI', 'NAVYA',
                                          'JASWANTH','SUDHAKAR', 'AKHIL', 'KRISHNA'])
        newrow['system_id']=random.randrange(1,10)
        newrow['system'] = random.choice(['rwr', 'warner', 'esm', 'rfps'])
        newrow['mode'] = random.choice(['INJECTION', 'RADIATION'])
        newrow['test_tab_ref']=f'''{newrow["system"]}amplacctest_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'''
        #newrow['start_ampl'] = random.randrange(0, 1000)
        #newrow['stop_ampl'] = random.randrange(0, 1000)
        #newrow['step_ampl'] = random.randrange(0, 1000)
        #newrow['ampl_list'] = random.randrange(0, 1000)
        newrow['set_power']=random.randrange(-90,0)
        newrow['pos_angle']=random.randrange(0,360)
        newrow['signal_cat']=random.choice(['CW', 'PULSE'])                          #'STAGGER', 'JITTER', 'D&S', 'STABLE'
        newrow['pw']=random.randrange(0,1000)
        newrow['pri']=random.randrange(0,1000)
        newrow['freq'] = random.randrange(-30, 0)
        newrow['rms_error'] = random.randrange(0, 100)
        newrow['test_status'] = random.choice(['Completed', 'Incomplete'])"""
    amplaccdb.AddAmplRecord(usercred=newrow)

    """for i in tqdm(range(0,30)):
        amplaccdb.DeleteAmplRecord(table_ref_id=f'''ampl_acc_test_{i}''')
    amplaccdb.DeleteAmplRecord(table_ref_id='warneramplacctest_2024_04_15_14_52_80')
    amplaccdb.getamplaccindxtable()
    amplaccdb.CurDbTable.to_csv("amplaccindxtabledb.csv")
    print(amplaccdb.AmplCurDbTable)
    amplaccdb.DropAmplIndxTable(deleteindxtable="amplaccindxtable")"""
    #amplaccdb.GetAmplAccIndxTable()
    # amplaccdb.SelAmplDateFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26")
    # amplaccdb.SelAmplDateSysFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26", sysfilter='rwr')
    amplaccdb.AmplIndxDbConClose()

########################################################################################################################