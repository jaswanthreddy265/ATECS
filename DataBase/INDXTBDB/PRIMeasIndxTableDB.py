import pandas as pd
import datetime
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR


########################################################################################################################
#   PRI Measurement Test Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   05 Mar 2024
#   PriMeasIndxTableDB Class has the following member Functions
#   1. init()
#   2. CreatePriMeasIndxTableDB()
#   3. AddPriRecord()
#   4. GetPriMeasIndxTable()
#   5. SelPriDateFilter()
#   6. SelPriDateSysFilter()
#   7. DeletePriRecord()
#   8. DropPriIndxTable
#   9. PriIndxDbConClose()
########################################################################################################################
# This Creating the PriMeasIndxTableDB Class
########################################################################################################################
class PriMeasIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        self.tablename = 'primeasindxtable'

    ####################################################################################################################
    # This Function creates The PRI Measurement Test Index Database Table
    ####################################################################################################################
    def CreatePriMeasIndxTableDB(self):
        try:
            self.connestablish = self.connection.connection
            cursor = self.connestablish.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (   date              TIMESTAMP     NOT NULL,
                                         username          TEXT          NOT NULL,
                                         system_id         FLOAT         NOT NULL,
                                         system            TEXT          NOT NULL,
                                         mode              TEXT          NOT NULL,
                                         test_tab_ref      TEXT          NOT NULL,
                                         start_pri         FLOAT         NOT NULL,
                                         stop_pri          FLOAT         NOT NULL,
                                         step_pri          FLOAT         NOT NULL,
                                         pri_list          TEXT          NULL,
                                         set_power         FLOAT         NOT NULL,
                                         pos_angle         FLOAT         NOT NULL,
                                         signal_cat        TEXT          NOT NULL,
                                         pw                FLOAT         NOT NULL,
                                         freq              FLOAT         NOT NULL,
                                         ampl              FLOAT         NOT NULL,
                                         rms_error         FLOAT         NOT NULL,
                                         test_status       TEXT          NOT NULL,
                                         remarks           TEXT          NULL
                                     ); '''
            cursor.execute(create_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PriMeasIndxTableDB(CreatePriMeasIndxTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("PriMeasIndxTableDB(CreatePriMeasIndxTableDB) - Error while creating PriMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in PRI Measurement Test Index Database Table
    ####################################################################################################################
    def AddPriRecord(self,
                      usercred={'date': datetime.datetime.now(), 'username': 'ranger', 'system_id': 7, 'system': 'RWR',
                                'mode': 'INJECTION', 'test_tab_ref': 'warnerprimeastest_2024_04_15_14_52_57', 'start_pri': 500,
                                'stop_pri': 1000, 'step_pri': 50, 'pri_list': '600', 'set_power': -30, 'pos_angle': 140,
                                'signal_cat': 'PULSED', 'pw': 1881, 'freq': 1, 'ampl': 850, 'rms_error': 1,
                                'test_status': 'Completed', 'remarks': 'new row added'
                                }):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{usercred['date']}','{usercred['username']}',
                                    '{usercred['system_id']}', '{usercred['system']}', '{usercred['mode']}',
                                    '{usercred['test_tab_ref']}', '{usercred['start_pri']}', '{usercred['stop_pri']}',
                                    '{usercred['step_pri']}', '{usercred['pri_list']}', '{usercred['set_power']}',
                                    '{usercred['pos_angle']}', '{usercred['signal_cat']}', '{usercred['pw']}',
                                    '{usercred['freq']}','{usercred['ampl']}', '{usercred['rms_error']}',
                                    '{usercred['test_status']}', '{usercred['remarks']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("PriMeasIndxTableDB(AddPriRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("PriMeasIndxTableDB(AddPriRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The PRI Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetPriMeasIndxTable(self):
        try:
            self.PriCurDbTable = pd.read_sql_query(
                f'''SELECT * FROM primeasindxtable ''',
                con=self.connestablish)
            print(self.PriCurDbTable)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to primeasindxtable ", error)
    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetPriRowRecord(self, select_record='esmprimeastest_2024_04_30_15_50_45'):
        try:
            self.GetPriIndxRowRecord = pd.read_sql_query(
                f'''SELECT * FROM primeasindxtable WHERE test_tab_ref = '{select_record}' ''',
                con=self.connestablish)
            print(self.GetPriIndxRowRecord)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to primeasindxtable ", error)

    ####################################################################################################################
    # This Function Gets The PRI Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelPriDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.PriDateFil = pd.read_sql_query(
                f'''SELECT * FROM primeasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            print(self.PriDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to primeasindxtable ", error)

    ##################################################################
    def SelPriDateSysFilter(self, datefilterfrom='', datefilterto='', sysfilter=''):
        try:
            self.PriDateSysFil = pd.read_sql_query(
                f'''SELECT * FROM primeasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' AND system='{sysfilter}' ''',
                con=self.connestablish)
            print(self.PriDateSysFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to primeasindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Record By "test_tab_ref" from PRI Measurement Test Index Database Table
    ####################################################################################################################
    def DeletePriRecord(self, table_ref_id='pri_meas_test_0'):
        try:
            cursor = self.connestablish.cursor()
            delprirecord = f'''DELETE FROM {self.tablename} WHERE test_tab_ref='{table_ref_id}' '''
            cursor.execute(delprirecord)
            self.connestablish.commit()
        # print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to primeasindxtable ", error)
    ####################################################################################################################
    # This Function Drops The PRI Measurement Index Table from Database
    ####################################################################################################################
    def DropPriIndxTable(self, deletetable='esmprimeastest'):
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
    def PriIndxDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################


if __name__ == "__main__":
    primeasdb = PriMeasIndxTableDB(Debug=True)
    primeasdb.tablename = 'primeasindxtable'
    primeasdb.CreatePriMeasIndxTableDB()

    # pri_list = [123.6,167,189]
    """pri_list_str=json.dumps(pri_list)
    print(type(pri_list_str))
    deser_pri = json.loads(pri_list_str)
    print(type(deser_pri[0]))"""
    newrow = {'date' : datetime.datetime.now(),'username' : 'Madhavi',  'system_id' : 2, 'system': 'rfps', 'mode': 'INJECTION',
              'test_tab_ref' : 'rfpsprimeastest_2024_05_18_14_47_12', 'start_pri' : 40, 'stop_pri' : 500,
              'step_pri' : 5, 'pri_list' : '', 'set_power' : -30, 'pos_angle' : 140,'signal_cat' : 'PULSE', 'pw' : 1881,
              'freq' : 1, 'ampl' : 850, 'rms_error' : 1, 'test_status' : 'Incomplete', 'remarks' : 'new row added'  }

    """for i in tqdm(range(0,5)):
        sleep(0)
        newrow['date']= datetime.datetime.now()

        newrow['username']=random.choice(['BHASKAR', 'ADITYA', 'KALYANI', 'SATHISH', 'RAJU', 'SAGAR','MADHAVI', 'NAVYA',
                                          'JASWANTH','SUDHAKAR', 'AKHIL', 'KRISHNA'])
        newrow['system_id']=random.randrange(1,10)
        newrow['system'] = random.choice(['rwr', 'warner', 'esm', 'rfps'])
        newrow['mode'] = random.choice(['INJECTION', 'RADIATION'])
        newrow['test_tab_ref']=f'''{newrow["system"]}primeastest_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'''
        #newrow['start_pri'] = random.randrange(0, 1000)
        #newrow['stop_pri'] = random.randrange(0, 1000)
        #newrow['step_pri'] = random.randrange(0, 1000)
        #newrow['pri_list'] = random.randrange(0, 1000)
        newrow['set_power']=random.randrange(-90,0)
        newrow['pos_angle']=random.randrange(0,360)
        newrow['signal_cat']=random.choice(['CW', 'PULSE'])                          #'STAGGER', 'JITTER', 'D&S', 'STABLE'
        newrow['pw']=random.randrange(2,300000)
        newrow['freq']=random.randrange(0,1000)
        newrow['ampl'] = random.randrange(-30, 0)
        newrow['rms_error'] = random.randrange(0, 100)
        newrow['test_status'] = random.choice(['Completed', 'Incomplete'])
        primeasdb.AddPriRecord(usercred=newrow)"""
    primeasdb.AddPriRecord(usercred=newrow)

    """for i in tqdm(range(0,30)):
        primeasdb.DeletePriRecord(table_ref_id=f'''pri_meas_test_{i}''')
    primeasdb.DeletePriRecord(table_ref_id='warnerprimeastest_2024_04_15_14_52_80')
    primeasdb.getprimeasindxtable()
    primeasdb.CurDbTable.to_csv("primeasindxtabledb.csv")
    print(primeasdb.PriCurDbTable)
    primeasdb.DropPriIndxTable(deletetable="")"""
    #primeasdb.GetPriMeasIndxTable()
    #primeasdb.SelPriDateFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26")
    # primeasdb.SelPriDateSysFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26", sysfilter='rwr')
    primeasdb.PriIndxDbConClose()

########################################################################################################################