import pandas as pd
import datetime
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR


########################################################################################################################
#   DOA Measurement Test Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   05 Mar 2024
#   DoaMeasIndxTableDB Class has the following member Functions
#   1. init()
#   2. CreateDoaMeasIndxTableDB()
#   3. AddDoaRecord()
#   4. GetDoaMeasIndxTable()
#   5. SelDoaDateFilter()
#   6. SelDoaDateSysFilter()
#   7. DeleteDoaRecord()
#   8. DropDoaIndxTable()
#   9. DoaIndxDbConClose()
########################################################################################################################
# This Creating the DoaMeasIndxTableDB Class
########################################################################################################################
class DoaMeasIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        self.tablename = 'doameasindxtable'

    ####################################################################################################################
    # This Function creates The DOA Measurement Test Index Database Table
    ####################################################################################################################
    def CreateDoaMeasIndxTableDB(self):
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
                                         start_doa          FLOAT         NOT NULL,
                                         stop_doa           FLOAT         NOT NULL,
                                         step_doa           FLOAT         NOT NULL,
                                         doa_list           TEXT          NULL,
                                         set_power          FLOAT         NOT NULL,
                                         freq               FLOAT         NOT NULL,
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
                print("DoaMeasIndxTableDB(CreateDoaMeasIndxTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("DoaMeasIndxTableDB(CreateDoaMeasIndxTableDB) - Error while creating DoaMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in DOA Measurement Test Index Database Table
    ####################################################################################################################
    def AddDoaRecord(self,
                      usercred={'date': datetime.datetime.now(), 'username': 'ranger', 'system_id': 7, 'system': 'RWR',
                                'mode': 'INJECTION', 'test_tab_ref': 'warnerdoameastest_2024_04_15_14_52_57', 'start_doa': 500,
                                'stop_doa': 1000, 'step_doa': 50, 'doa_list': '600', 'set_power': -30, 'freq': 140,
                                'signal_cat': 'PULSED', 'pw': 1881, 'pri': 1, 'ampl': 850, 'rms_error': 1,
                                'test_status': 'Completed', 'remarks': 'new row added'
                                }):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{usercred['date']}','{usercred['username']}',
                                    '{usercred['system_id']}', '{usercred['system']}', '{usercred['mode']}',
                                    '{usercred['test_tab_ref']}', '{usercred['start_doa']}', '{usercred['stop_doa']}',
                                    '{usercred['step_doa']}', '{usercred['doa_list']}', '{usercred['set_power']}',
                                    '{usercred['freq']}', '{usercred['signal_cat']}', '{usercred['pw']}',
                                    '{usercred['pri']}','{usercred['ampl']}', '{usercred['rms_error']}',
                                    '{usercred['test_status']}', '{usercred['remarks']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("DoaMeasIndxTableDB(AddDoaRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("DoaMeasIndxTableDB(AddDoaRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The DOA Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetDoaMeasIndxTable(self):
        try:
            self.DoaCurDbTable = pd.read_sql_query(
                f'''SELECT * FROM doameasindxtable ''',
                con=self.connestablish)
            print(self.DoaCurDbTable)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to doameasindxtable ", error)

    ####################################################################################################################
    # This Function Gets The DOA Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelDoaDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.DoaDateFil = pd.read_sql_query(
                f'''SELECT * FROM doameasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            #print(self.DoaDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to doameasindxtable ", error)

    ##################################################################
    def SelDoaDateSysFilter(self, datefilterfrom='', datefilterto='', sysfilter=''):
        try:
            self.DoaDateSysFil = pd.read_sql_query(
                f'''SELECT * FROM doameasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' AND system='{sysfilter}' ''',
                con=self.connestablish)
            print(self.DoaDateSysFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to doameasindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Record By "test_tab_ref" from DOA Measurement Test Index Database Table
    ####################################################################################################################
    def DeleteDoaRecord(self, table_ref_id='doa_meas_test_0'):
        try:
            cursor = self.connestablish.cursor()
            deldoarecord = f'''DELETE FROM {self.tablename} WHERE test_tab_ref='{table_ref_id}' '''
            cursor.execute(deldoarecord)
            self.connestablish.commit()
        # print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to doameasindxtable ", error)
    ####################################################################################################################
    # This Function Drops The DOA Measurement Index Table from Database
    ####################################################################################################################
    def DropDoaIndxTable(self, deletetable='esmdoameastest'):
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
    def DoaIndxDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################


if __name__ == "__main__":
    doameasdb = DoaMeasIndxTableDB(Debug=True)
    doameasdb.tablename = 'doameasindxtable'
    doameasdb.CreateDoaMeasIndxTableDB()

    # doa_list = [123.6,167,189]
    """doa_list_str=json.dumps(doa_list)
    print(type(doa_list_str))
    deser_doa = json.loads(doa_list_str)
    print(type(deser_doa[0]))"""
    newrow = {'date' : datetime.datetime.now(),'username' : 'Madhavi',  'system_id' : 1, 'system': 'rfps', 'mode': 'INJECTION',
              'test_tab_ref' : 'rfpsdoameastest_2024_05_18_15_15_04', 'start_doa' : -90, 'stop_doa' : 83,
              'step_doa' : 1.7, 'doa_list' : '', 'set_power' : -30, 'freq' : 140,'signal_cat' : 'PULSE', 'pw' : 1881,
              'pri' : 1, 'ampl' : 850, 'rms_error' : 1, 'test_status' : 'Incomplete', 'remarks' : 'new row added'  }

    """for i in tqdm(range(0,5)):
        sleep(0)
        newrow['date']= datetime.datetime.now()

        newrow['username']=random.choice(['BHASKAR', 'ADITYA', 'KALYANI', 'SATHISH', 'RAJU', 'SAGAR','MADHAVI', 'NAVYA',
                                          'JASWANTH','SUDHAKAR', 'AKHIL', 'KRISHNA'])
        newrow['system_id']=random.randrange(1,10)
        newrow['system'] = random.choice(['rwr', 'warner', 'esm', 'rfps'])
        newrow['mode'] = random.choice(['INJECTION', 'RADIATION'])
        newrow['test_tab_ref']=f'''{newrow["system"]}doameastest_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'''
        #newrow['start_doa'] = random.randrange(0, 1000)
        #newrow['stop_doa'] = random.randrange(0, 1000)
        #newrow['step_doa'] = random.randrange(0, 1000)
        #newrow['doa_list'] = random.randrange(0, 1000)
        newrow['set_power']=random.randrange(-90,0)
        newrow['freq']=random.randrange(0,360)
        newrow['signal_cat']=random.choice(['CW', 'PULSE'])                          #'STAGGER', 'JITTER', 'D&S', 'STABLE'
        newrow['pw']=random.randrange(2,300000)
        newrow['pri']=random.randrange(0,1000)
        newrow['ampl'] = random.randrange(-30, 0)
        newrow['rms_error'] = random.randrange(0, 100)
        newrow['test_status'] = random.choice(['Completed', 'Incomplete'])"""
    doameasdb.AddDoaRecord(usercred=newrow)

    """for i in tqdm(range(0,30)):
        doameasdb.DeleteDoaRecord(table_ref_id=f'''doa_meas_test_{i}''')
    doameasdb.DeleteDoaRecord(table_ref_id='rfpsdoameastest_2024_05_09_17_17_01')
    doameasdb.getdoameasindxtable()
    doameasdb.CurDbTable.to_csv("doameasindxtabledb.csv")
    print(doameasdb.DoaCurDbTable)
    doameasdb.DropDoaIndxTable(deletetable="")"""
    #doameasdb.GetDoaMeasIndxTable()
    # doameasdb.SelDoaDateFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26")
    # doameasdb.SelDoaDateSysFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26", sysfilter='rwr')
    doameasdb.DoaIndxDbConClose()

########################################################################################################################