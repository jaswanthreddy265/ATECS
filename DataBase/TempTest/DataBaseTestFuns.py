import psycopg2
from DataBase.TESTTBDB.AmplAccTestTableDB import AmplAccTestTableDB
#from DataBase.TESTTBDB.DoaAccTestTableDB import DoaMeasTestTableDB
from DataBase.TESTTBDB.FreqAccTestTableDB import FreqAccTestTableDB
"""from DataBase.TESTTBDB.PriAccTestTableDB import PriMeasTestTableDB
from DataBase.TESTTBDB.PwAccTestTableDB import PwMeasTestTableDB
from DataBase.TESTTBDB.SensMeasTestTableDB import SensMeasTestTableDB"""
from DataBase.TestCases.ErrorCodesDatabase import *
########################################################################################################################
#   Automated Test Equipment & Calibration Software Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   23 Apr 2024
#   ATECDataBaseFuns Class has the following member Functions
#   1. connect()
#   2. CreateFreqAccTestTableDB()
#   3. AddFreqRow()
#   4. getfreqaccindxtable()
#   5. close()
#   6.DeleteFreqRow
#   7.main()
########################################################################################################################
# This Creating the ATECDataBaseFuns Class
########################################################################################################################

class SysPerTestDBFuns():
    def __int__(self, Debug=False):
        self.Debug = Debug
        self.connection=True
    ####################################################################################################################
    # This Function Establish Connection with Database
    ####################################################################################################################
    def ConnectDB(self, DataBaseSettings={
                                'user': 'postgres',
                                'password': 'Platinum0435#',
                                'host': 'localhost',
                                'database': 'atec',
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
        except (Exception, psycopg2.Error) as error:
            if self.Debug == False:
                print("ATECDataBaseFuns(ATECConnect) -Error while connecting to PostgreSQL", error)
            return DATABASE_CONNECTION_ERROR

    ####################################################################################################################
    # This Function Creates The Test Database Table From Respective Test Classes

    ####################################################################################################################
    def SysPerTestDbFunExe(self, PerTestname = '', function = '', data = {}):
        if  PerTestname == 'FreqAccTest' :
            if function == 'Create':
                CreateFreqTestTable = FreqAccTestTableDB()
                CreateFreqTestTable.connection = self.connection
                CreateFreqTestTable.CreateFreqAccTestTableDB()
            elif function == 'Add':
                AddFreqTestTable = FreqAccTestTableDB()
                AddFreqTestTable.connection = self.connection
                AddFreqTestTable.AddFreqTestRow()
            elif function == 'Get':
                GetFreqTestTable = FreqAccTestTableDB()
                GetFreqTestTable.connection = self.connection
                GetFreqTestTable.GetFreqAccTestTable()
            """CreatePwIndexTable = PwMeasIndxTableDB()
            CreatePwIndexTable.connection = self.connection
            CreatePwIndexTable.CreatePwMeasIndxTableDB()
        elif CreateIndexTestName == 'PriMeasIndxTable':
            CreatePriIndexTable = PriMeasIndxTableDB()
            CreatePriIndexTable.connection = self.connection
            CreatePriIndexTable.CreatePriMeasIndxTableDB()
        elif CreateIndexTestName == 'AmplAccIndxTable':
            CreateAmplIndexTable = AmplAccIndxTableDB()
            CreateAmplIndexTable.connection = self.connection
            CreateAmplIndexTable.CreateAmplAccIndxTableDB()
        elif CreateIndexTestName == 'DoaMeasIndxTable':
            CreateDoaIndexTable = DoaMeasIndxTableDB()
            CreateDoaIndexTable.connection = self.connection
            CreateDoaIndexTable.CreateDoaMeasIndxTableDB()
        elif CreateIndexTestName == 'SensMeasIndxTable':
            CreateSensMeasIndexTable = SensMeasIndxTableDB()
            CreateSensMeasIndexTable.connection = self.connection
            CreateSensMeasIndexTable.CreateSensMeasIndxTableDB()"""


    ####################################################################################################################
    # This Function Creates The Test Database Table From Respective Test Classes

    ####################################################################################################################
    def ATECDbConClose(self):
        self.connection.close()
        print("PostgreSQL connection is closed")
########################################################################################################################
if __name__ == "__main__":
    DataBaseSettings = {
        'user': 'postgres',
        'password': 'Platinum0435#',
        'host': 'localhost',
        'database': 'atec',
        'port': 6543
    }
    atecdatabasefunc = SysPerTestDBFuns()
    atecdatabasefunc.ConnectDB(DataBaseSettings)
    atecdatabasefunc.SysPerTestDbFunExe(PerTestname = 'FreqAccTest', function = 'Create', data = {})
    #atecdatabasefunc.ATECAddRecordToTestTable(AddRecordTestTestName="FreqAccTestTable")
    #atecdatabasefunc.ATECGetTestTable(GetTestTestName="SensMeasTestTable")
    #atecdatabasefunc.ATECSelDateFilTestTable(SelDateFilTestTestName="AmplAccTestTable", fromdatefil="2024-04-22", todatefil="2024-04-25")
    #atecdatabasefunc.ATECSelSysDateFilTestTable(SelSysDateFilTestTestName="AmplAccTestTable", fromdatefil="2024-04-22", todatefil="2024-04-25", sysfil="warner")
    #atecdatabasefunc.ATECDeleteRecordFromTestTable(SelTestTableName="AmplAccTestTable", indxtableref="rfpsamplacctest_2024_04_23_12_59_26")
    atecdatabasefunc.ATECDbConClose()