import pandas as pd
import datetime
import psycopg2
from DataBase.UserManagement.ConnectDB import Connect_to_Database
from DataBase.UserManagement.ErrorCodesDatabase import SUCCESS, DATABASE_ADDDATA_ERROR


########################################################################################################################
#   Sensitivity Measurement Test Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   05 Mar 2024
#   SensMeasIndxTableDB Class has the following member Functions
#   1. init()
#   2. CreateSensMeasIndxTableDB()
#   3. AddSensMeasRecord()
#   4. GetSensMeasIndxTable()
#   5. SelSensMeasDateFilter()
#   6. SelSensMeasDateSysFilter()
#   7. DeleteSensMeasRecord()
#   8. DropSensMeasIndxTable()
#   9. SensMeasIndxDbConClose()
########################################################################################################################
# This Creating the SensMeasIndxTableDB Class
########################################################################################################################
class SensMeasIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = Connect_to_Database()
        self.connestablish = self.connection.connection
        self.tablename = 'sensmeasindxtable'

    ####################################################################################################################
    # This Function creates The Sensitivity Measurement Test Index Database Table
    ####################################################################################################################
    def CreateSensMeasIndxTableDB(self):
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
                                         start_sens           FLOAT         NOT NULL,
                                         stop_sens            FLOAT         NOT NULL,
                                         step_sens            FLOAT         NOT NULL,
                                         sens_list            TEXT          NULL,
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
                print("SensMeasIndxTableDB(CreateSensMeasIndxTableDB) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("SensMeasIndxTableDB(CreateSensMeasIndxTableDB) - Error while creating SensMeasTable", error)
            return error

    ####################################################################################################################
    # This Function Adds The Data in Sensitivity Measurement Test Index Database Table
    ####################################################################################################################
    def AddSensMeasRecord(self,
                      usercred={'date': datetime.datetime.now(), 'username': 'ranger', 'system_id': 7, 'system': 'RWR',
                                'mode': 'INJECTION', 'test_tab_ref': 'warnersensmeastest_2024_04_15_14_52_57', 'start_sens': 500,
                                'stop_sens': 1000, 'step_sens': 50, 'sens_list': '600', 'set_power': -30, 'pos_angle': 140,
                                'signal_cat': 'PULSED', 'freq': 1881, 'pri': 1, 'ampl': 850, 'rms_error': 1,
                                'test_status': 'Completed', 'remarks': 'new row added'
                                }):
        try:
            cursor = self.connestablish.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{usercred['date']}','{usercred['username']}',
                                    '{usercred['system_id']}', '{usercred['system']}', '{usercred['mode']}',
                                    '{usercred['test_tab_ref']}', '{usercred['start_sens']}', '{usercred['stop_sens']}',
                                    '{usercred['step_sens']}', '{usercred['sens_list']}', '{usercred['set_power']}',
                                    '{usercred['pos_angle']}', '{usercred['signal_cat']}', '{usercred['freq']}',
                                    '{usercred['pri']}','{usercred['ampl']}', '{usercred['rms_error']}',
                                    '{usercred['test_status']}', '{usercred['remarks']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connestablish.commit()
            if self.Debug == True:
                print("SensMeasIndxTableDB(AddSensMeasRecord) - New Record added successfully")
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == False:
                print("SensMeasIndxTableDB(AddSensMeasRecord)- Error in inserting to table", error)
            return DATABASE_ADDDATA_ERROR

    ####################################################################################################################
    # This Function Gets The Sensitivity Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetSensMeasIndxTable(self):
        try:
            self.SensMeasCurDbTable = pd.read_sql_query(
                f'''SELECT * FROM sensmeasindxtable ''',
                con=self.connestablish)
            print(self.SensMeasCurDbTable)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to sensmeasindxtable ", error)
    ####################################################################################################################
    # This Function Gets The DOA Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetSensRowRecord(self, select_record='esmsensmeastest_2024_04_30_15_50_45'):
        try:
            self.GetSensIndxRowRecord = pd.read_sql_query(
                f'''SELECT * FROM sensmeasindxtable WHERE test_tab_ref = '{select_record}' ''',
                con=self.connestablish)
            print(self.GetSensIndxRowRecord)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to sensmeasindxtable ", error)

    ####################################################################################################################
    # This Function Gets The Sensitivity Measurement Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def SelSensMeasDateFilter(self, datefilterfrom='', datefilterto=''):
        try:
            self.SensMeasDateFil = pd.read_sql_query(
                f'''SELECT * FROM sensmeasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' ''',
                con=self.connestablish)
            #print(self.SensMeasDateFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to sensmeasindxtable ", error)

    ##################################################################
    def SelSensMeasDateSysFilter(self, datefilterfrom='', datefilterto='', sysfilter=''):
        try:
            self.SensMeasDateSysFil = pd.read_sql_query(
                f'''SELECT * FROM sensmeasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' AND system='{sysfilter}' ''',
                con=self.connestablish)
            print(self.SensMeasDateSysFil)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to sensmeasindxtable ", error)

    ####################################################################################################################
    # This Function Deletes The Record By "test_tab_ref" from Sensitivity Measurement Test Index Database Table
    ####################################################################################################################
    def DeleteSensMeasRecord(self, table_ref_id='sens_meas_test_0'):
        try:
            cursor = self.connestablish.cursor()
            delsensrecord = f'''DELETE FROM {self.tablename} WHERE test_tab_ref='{table_ref_id}' '''
            cursor.execute(delsensrecord)
            self.connestablish.commit()
        # print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to sensmeasindxtable ", error)
    ####################################################################################################################
    # This Function Drops The Sensitivity Measurement Index Table from Database
    ####################################################################################################################
    def DropSensMeasIndxTable(self, deletetable='esmsensmeastest'):
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
    def SensMeasIndxDbConClose(self):
        self.connection.ConnectClose()
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ###################################################################################################################


if __name__ == "__main__":
    sensmeasdb = SensMeasIndxTableDB(Debug=True)
    sensmeasdb.tablename = 'sensmeasindxtable'
    sensmeasdb.CreateSensMeasIndxTableDB()

    # sens_list = [123.6,167,189]
    """sens_list_str=json.dumps(sens_list)
    print(type(sens_list_str))
    deser_sens = json.loads(sens_list_str)
    print(type(deser_sens[0]))"""
    newrow = {'date' : datetime.datetime.now(),'username' : 'Madhavi',  'system_id' :2, 'system': 'rfps', 'mode': 'INJECTION',
              'test_tab_ref' : 'rfpssensmeastest_2024_05_18_15_25_29', 'start_sens' : -100, 'stop_sens' :50,
              'step_sens' :2, 'sens_list' : '', 'set_power' : -30, 'pos_angle' : 140,'signal_cat' : 'PULSE', 'freq' : 1881,
              'pri' : 1, 'ampl' : 850, 'rms_error' : 1, 'test_status' : 'Incomplete', 'remarks' : 'new row added'  }

    """for i in tqdm(range(0,5)):
        sleep(0)
        newrow['date']= datetime.datetime.now()

        newrow['username']=random.choice(['BHASKAR', 'ADITYA', 'KALYANI', 'SATHISH', 'RAJU', 'SAGAR','MADHAVI', 'NAVYA',
                                          'JASWANTH','SUDHAKAR', 'AKHIL', 'KRISHNA'])
        newrow['system_id']=random.randrange(1,10)
        newrow['system'] = random.choice(['rwr', 'warner', 'esm', 'rfps'])
        newrow['mode'] = random.choice(['INJECTION', 'RADIATION'])
        newrow['test_tab_ref']=f'''{newrow["system"]}sensmeastest_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'''
        #newrow['start_sens'] = random.randrange(0, 1000)
        #newrow['stop_sens'] = random.randrange(0, 1000)
        #newrow['step_sens'] = random.randrange(0, 1000)
        #newrow['sens_list'] = random.randrange(0, 1000)
        newrow['set_power']=random.randrange(-90,0)
        newrow['pos_angle']=random.randrange(0,360)
        newrow['signal_cat']=random.choice(['CW', 'PULSE'])                          #'STAGGER', 'JITTER', 'D&S', 'STABLE'
        newrow['freq']=random.randrange(2,300000)
        newrow['pri']=random.randrange(0,1000)
        newrow['ampl'] = random.randrange(-30, 0)
        newrow['rms_error'] = random.randrange(0, 100)
        newrow['test_status'] = random.choice(['Completed', 'Incomplete'])"""
    sensmeasdb.AddSensMeasRecord(usercred=newrow)

    """for i in tqdm(range(0,30)):
        sensmeasdb.DeleteSensMeasRecord(table_ref_id=f'''sens_meas_test_{i}''')"""
    #sensmeasdb.DeleteSensMeasRecord(table_ref_id='warnersensmeastest_2024_05_10_11_09_51')
    """sensmeasdb.getsensmeasindxtable()
    sensmeasdb.CurDbTable.to_csv("sensmeasindxtabledb.csv")
    print(sensmeasdb.SensMeasCurDbTable)
    sensmeasdb.DropSensMeasIndxTable(deletetable="")"""
    #sensmeasdb.GetSensMeasIndxTable()
    # sensmeasdb.SelSensMeasDateFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26")
    # sensmeasdb.SelSensMeasDateSysFilter(datefilterfrom="2024-04-01", datefilterto="2024-04-26", sysfilter='rwr')
    sensmeasdb.SensMeasIndxDbConClose()

########################################################################################################################