import psycopg2

from DataBase.TempTest.DataBaseTestFuns import SysPerTestDBFuns
from DataBase.INDXTBDB.AmplAccIndxTableDB import AmplAccIndxTableDB
from DataBase.INDXTBDB.DOAMeasIndxTableDB import DoaMeasIndxTableDB
from DataBase.INDXTBDB.FreqAccIndxTableDB import FreqAccIndxTableDB
from DataBase.INDXTBDB.PRIMeasIndxTableDB import PriMeasIndxTableDB
from DataBase.INDXTBDB.PWMeasIndxTableDB import PwMeasIndxTableDB
from DataBase.INDXTBDB.SensMeasAccIndxTableDB import SensMeasIndxTableDB
from DataBase.TestCases.ErrorCodesDatabase import *
########################################################################################################################
#   Automated Test Equipment & Calibration Software Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   23 Apr 2024
#   ATECDataBaseFuns Class has the following member Functions
#   1. connect()
#   2. CreateFreqAccIndxTableDB()
#   3. AddFreqRow()
#   4. getfreqaccindxtable()
#   5. close()
#   6.DeleteFreqRow
#   7.main()
########################################################################################################################
# This Creating the ATECDataBaseFuns Class
########################################################################################################################
class ATECDataBaseFuns():
    def __int__(self, Debug=False):
        self.Debug = Debug
        self.connection=True
    ####################################################################################################################
    # This Function Establish Connection with Database
    ####################################################################################################################
    def ATECConnect(self, DataBaseSettings={
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
    # This Function Creates The Index Database Table From Respective Index Classes
    ####################################################################################################################
    def ATECCreateIndxTable(self, CreateIndexTestName='PwMeasIndxTable'):
        if CreateIndexTestName == 'FreqAccIndxTable':
            CreateFreqIndexTable = FreqAccIndxTableDB()
            CreateFreqIndexTable.connection = self.connection
            CreateFreqIndexTable.CreateFreqAccIndxTableDB()
        elif CreateIndexTestName == 'PwMeasIndxTable':
            CreatePwIndexTable = PwMeasIndxTableDB()
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
            CreateSensMeasIndexTable.CreateSensMeasIndxTableDB()
    ####################################################################################################################
    # This Function Adds Records into Respective Index Database Table From Respective Index Classes
#    {'date': datetime.datetime.now(), 'username': 'ranger', 'system_id': 7, 'system': 'RWR', 'mode': 'INJECTION',
#     'test_tab_ref': 'warnerfreqacctest_2024_04_15_14_52_57', 'start_freq': 500, 'stop_freq': 1000, 'step_freq': 50,
#     'freq_list': '600', 'set_power': -30, 'pos_angle': 140, 'signal_cat': 'PULSED', 'pw': 1881, 'pri': 1, 'ampl': 850,
#     'rms_error': 1, 'test_status': 'Completed', 'remarks': 'new row added'}
    ####################################################################################################################
    def ATECAddRecordToIndxTable(self, AddRecordIndexTestName='FreqAccIndxTable'):
        if AddRecordIndexTestName == 'FreqAccIndxTable':
            AddRecordIndexTestName = FreqAccIndxTableDB()
            AddRecordIndexTestName.connection=self.connection
            AddRecordIndexTestName.AddFreqRecord()
        elif AddRecordIndexTestName == 'PwMeasIndxTable':
            AddRecordIndexTestName = PwMeasIndxTableDB()
            AddRecordIndexTestName.connection = self.connection
            AddRecordIndexTestName.AddPwRecord()
        elif AddRecordIndexTestName == 'PriMeasIndxTable':
            AddRecordIndexTestName = PriMeasIndxTableDB()
            AddRecordIndexTestName.connection = self.connection
            AddRecordIndexTestName.AddPriRecord()
        elif AddRecordIndexTestName == 'AmplAccIndxTable':
            AddRecordIndexTestName = AmplAccIndxTableDB()
            AddRecordIndexTestName.connection=self.connection
            AddRecordIndexTestName.AddAmplRecord()
        elif AddRecordIndexTestName == 'DoaMeasIndxTable':
            AddRecordIndexTestName = DoaMeasIndxTableDB()
            AddRecordIndexTestName.connection = self.connection
            AddRecordIndexTestName.AddDoaRecord()
        elif AddRecordIndexTestName == 'SensMeasMeasIndxTable':
            AddRecordIndexTestName = SensMeasIndxTableDB()
            AddRecordIndexTestName.connection = self.connection
            AddRecordIndexTestName.AddSensMeasRecord()
    ####################################################################################################################
    # This Function Gets The Index Database Table From Respective Index Classes
    ####################################################################################################################
    def ATECGetIndxTable(self, GetIndexTestName='PwMeasIndxTable'):
        if GetIndexTestName == 'FreqAccIndxTable':
            GetFreqIndexTable = FreqAccIndxTableDB()
            GetFreqIndexTable.connection = self.connection
            GetFreqIndexTable.GetFreqAccIndxTable()
        elif GetIndexTestName == 'PwMeasIndxTable':
            GetPwIndexTable = PwMeasIndxTableDB()
            GetPwIndexTable.connection = self.connection
            GetPwIndexTable.GetPwMeasIndxTable()
        elif GetIndexTestName == 'PriMeasIndxTable':
            GetPriIndexTable = PriMeasIndxTableDB()
            GetPriIndexTable.connection = self.connection
            GetPriIndexTable.GetPriMeasIndxTable()
        elif GetIndexTestName == 'AmplAccIndxTable' :
            GetAmplIndexTable = AmplAccIndxTableDB()
            GetAmplIndexTable.connection = self.connection
            GetAmplIndexTable.GetAmplAccIndxTable()
        elif GetIndexTestName == 'DoaMeasIndxTable' :
            GetDoaIndexTable = DoaMeasIndxTableDB()
            GetDoaIndexTable.connection = self.connection
            GetDoaIndexTable.GetDoaMeasIndxTable()
        elif GetIndexTestName == 'SensMeasIndxTable' :
            GetSensMeasIndexTable = SensMeasIndxTableDB()
            GetSensMeasIndexTable.connection = self.connection
            GetSensMeasIndexTable.GetSensMeasIndxTable()
    ####################################################################################################################
    # This Function Retrieves The Index Database Table From Respective Index Classes Function By Date Filter
    ####################################################################################################################
    def ATECSelDateFilIndxTable(self, SelDateFilIndexTestName='FreqAccIndxTable', fromdatefil='', todatefil=''):
        if SelDateFilIndexTestName == 'FreqAccIndxTable':
            SelDateFreqIndexTable = FreqAccIndxTableDB()
            SelDateFreqIndexTable.connection = self.connection
            SelDateFreqIndexTable.SelFreqDateFilter(datefilterfrom=fromdatefil, datefilterto=todatefil)
        elif SelDateFilIndexTestName == 'PwMeasIndxTable':
            SelDatePwIndexTable = PwMeasIndxTableDB()
            SelDatePwIndexTable.connection = self.connection
            SelDatePwIndexTable.SelPwDateFilter(datefilterfrom=fromdatefil, datefilterto=todatefil)
        elif SelDateFilIndexTestName == 'PriMeasIndxTable':
            SelDatePriIndexTable = PriMeasIndxTableDB()
            SelDatePriIndexTable.connection = self.connection
            SelDatePriIndexTable.SelDateFilter(datefilterfrom=fromdatefil, datefilterto=todatefil)
        elif SelDateFilIndexTestName == 'AmplAccIndxTable' :
            SelDateAmplIndexTable = AmplAccIndxTableDB()
            SelDateAmplIndexTable.connection = self.connection
            SelDateAmplIndexTable.SelAmplDateFilter(datefilterfrom=fromdatefil, datefilterto=todatefil)
        elif SelDateFilIndexTestName == 'DoaMeasIndxTable' :
            SelDateDoaIndexTable = DoaMeasIndxTableDB()
            SelDateDoaIndexTable.connection = self.connection
            SelDateDoaIndexTable.SelDoaDateFilter(datefilterfrom=fromdatefil, datefilterto=todatefil)
        elif SelDateFilIndexTestName == 'SensMeasIndxTable' :
            SelDateSensMeasIndexTable = SensMeasIndxTableDB()
            SelDateSensMeasIndexTable.connection = self.connection
            SelDateSensMeasIndexTable.SelSensMeasDateFilter(datefilterfrom=fromdatefil, datefilterto=todatefil)
    ####################################################################################################################
    # This Function Retrieves The Index Database Table From Respective Index Classes Function By System and Date Filtering
    ####################################################################################################################
    def ATECSelSysDateFilIndxTable(self, SelSysDateFilIndexTestName='FreqAccIndxTable', fromdatefil='', todatefil='', sysfil=''):
        if SelSysDateFilIndexTestName == 'FreqAccIndxTable':
            SelSysDateFreqIndexTable = FreqAccIndxTableDB()
            SelSysDateFreqIndexTable.connection = self.connection
            SelSysDateFreqIndexTable.SelFreqDateSysFilter(datefilterfrom=fromdatefil, datefilterto=todatefil, sysfilter=sysfil)
        elif SelSysDateFilIndexTestName == 'PwMeasIndxTable':
            SelSysDatePwIndexTable = PwMeasIndxTableDB()
            SelSysDatePwIndexTable.connection = self.connection
            SelSysDatePwIndexTable.SelPwDateSysFilter(datefilterfrom=fromdatefil, datefilterto=todatefil, sysfilter=sysfil)
        elif SelSysDateFilIndexTestName == 'PriMeasIndxTable':
            SelSysDatePriIndexTable = PriMeasIndxTableDB()
            SelSysDatePriIndexTable.connection = self.connection
            SelSysDatePriIndexTable.SelDateSysFilter(datefilterfrom=fromdatefil, datefilterto=todatefil, sysfilter=sysfil)
        elif SelSysDateFilIndexTestName == 'AmplAccIndxTable':
            SelSysDateAmplIndexTable = AmplAccIndxTableDB()
            SelSysDateAmplIndexTable.connection = self.connection
            SelSysDateAmplIndexTable.SelAmplDateSysFilter(datefilterfrom=fromdatefil, datefilterto=todatefil, sysfilter=sysfil)
        elif SelSysDateFilIndexTestName == 'DoaMeasIndxTable':
            SelSysDateDoaIndexTable = DoaMeasIndxTableDB()
            SelSysDateDoaIndexTable.connection = self.connection
            SelSysDateDoaIndexTable.SelDoaDateSysFilter(datefilterfrom=fromdatefil, datefilterto=todatefil, sysfilter=sysfil)
        elif SelSysDateFilIndexTestName == 'SensMeasIndxTable':
            SelSysDateSensMeasIndexTable = SensMeasIndxTableDB()
            SelSysDateSensMeasIndexTable.connection = self.connection
            SelSysDateSensMeasIndexTable.SelSensMeasDateSysFilter(datefilterfrom=fromdatefil, datefilterto=todatefil, sysfilter=sysfil)
    ####################################################################################################################
    # This Function Deletes The Record from The Respective Database Table
    ####################################################################################################################
    def ATECDeleteRecordFromIndxTable(self, SelIndexTableName='FreqAccIndxTable', indxtableref=''):
        if SelIndexTableName == 'FreqAccIndxTable':
            DelFreqIndxTabRecord = FreqAccIndxTableDB()
            DelFreqIndxTabRecord.connection = self.connection
            DelFreqIndxTabRecord.DeleteFreqRecord(table_ref_id=indxtableref)
        elif SelIndexTableName == 'PwMeasIndxTable':
            DelPwIndxTabRecord = PwMeasIndxTableDB()
            DelPwIndxTabRecord.connection = self.connection
            DelPwIndxTabRecord.DeletePwRecord(table_ref_id=indxtableref)
        elif SelIndexTableName == 'PriMeasIndxTable':
            DelPriIndxTabRecord = PriMeasIndxTableDB()
            DelPriIndxTabRecord.connection = self.connection
            DelPriIndxTabRecord.DeletePriRecord(table_ref_id=indxtableref)
        elif SelIndexTableName == 'AmplAccIndxTable' :
            DelAmplIndxTabRecord = AmplAccIndxTableDB()
            DelAmplIndxTabRecord.connection = self.connection
            DelAmplIndxTabRecord.DeleteAmplRecord(table_ref_id=indxtableref)
        elif SelIndexTableName == 'DoaMeasIndxTable' :
            DelDoaIndxTabRecord = DoaMeasIndxTableDB()
            DelDoaIndxTabRecord.connection = self.connection
            DelDoaIndxTabRecord.DeleteDoaRecord(table_ref_id=indxtableref)
        elif SelIndexTableName == 'SensMeasIndxTable' :
            DelSensMeasIndxTabRecord = SensMeasIndxTableDB()
            DelSensMeasIndxTabRecord.connection = self.connection
            DelSensMeasIndxTabRecord.DeleteSensMeasRecord(table_ref_id=indxtableref)

    ####################################################################################################################
    # This Function Calls DataBase Test Function The Database Connection
    ####################################################################################################################
    def ATECSysPerTestFunctions(self):
        SelIndexTableName=SysPerTestDBFuns()
        SelIndexTableName.connection = self.connection
        SelIndexTableName.SysPerTestDbFunExe()

    ####################################################################################################################
    # This Function Closes The Database Connection
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
    atecdatabasefunc = ATECDataBaseFuns()
    atecdatabasefunc.ATECConnect(DataBaseSettings)
    #atecdatabasefunc.ATECCreateIndxTable(CreateIndexTestName="AmplAccIndxTable")
    #atecdatabasefunc.ATECAddRecordToIndxTable(AddRecordIndexTestName="FreqAccIndxTable")
    #atecdatabasefunc.ATECGetIndxTable(GetIndexTestName="SensMeasIndxTable")
    #atecdatabasefunc.ATECSelDateFilIndxTable(SelDateFilIndexTestName="AmplAccIndxTable", fromdatefil="2024-04-22", todatefil="2024-04-25")
    #atecdatabasefunc.ATECSelSysDateFilIndxTable(SelSysDateFilIndexTestName="AmplAccIndxTable", fromdatefil="2024-04-22", todatefil="2024-04-25", sysfil="warner")
    #atecdatabasefunc.ATECDeleteRecordFromIndxTable(SelIndexTableName="AmplAccIndxTable", indxtableref="rfpsamplacctest_2024_04_23_12_59_26")
    atecdatabasefunc.ATECDbConClose()