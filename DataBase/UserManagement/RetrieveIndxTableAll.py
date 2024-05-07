import pandas as pd
import psycopg2
from DataBase.TestCases.ErrorCodesDatabase import DATABASE_CONNECTION_ERROR, SUCCESS, DATABASE_ADDDATA_ERROR
from ConnectDB import Connect_to_Database


########################################################################################################################
#   Get Index Table Database Class and Member Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   20 Apr 2024
#   GetIndxTableDB Class has the following member Functions
#   1. init  function
#   2. connect function
#   3. getindxtable()
#   4. DeleteRow()
#   5. Close()
########################################################################################################################
# This Creating the FreqAccIndxTableDB Class
########################################################################################################################


class GetIndxTableDB():
    def __init__(self, Debug=False):
        self.Debug = Debug
        #self.connection = True

    ####################################################################################################################
    # This Function Establish Connection with Database
    ####################################################################################################################
    def connect(self):
        self.connectDB = Connect_to_Database(Debug=True)

        print(self.connectDB.connection)
    ####################################################################################################################
    # This Function Gets The Frequency Accuracy Test Index Database Table With Pandas For CSV Reading
    ####################################################################################################################
    def GetIndxTable(self, indxtabname='freqaccindxtable',datefilterfrom="2024-04-01", datefilterto="2024-04-20", sysfilter='rwr'):

        pass

    ####################################################################################################################
    # This Function Deletes The Row By "test_tab_ref" from Frequency Accuracy Test Index Database Table
    ####################################################################################################################
    """def DeleteRow(self, table_ref_id='freq_acc_test_0'):
        try:
            cursor = self.connection.cursor()
            delete = f'''DELETE FROM {self.tablename} WHERE test_tab_ref='{table_ref_id}' '''
            cursor.execute(delete)
            self.connection.commit()
        # print("deleted the row successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error in reading from to freqaccindxtable ", error)"""
    ####################################################################################################################
    # This Function call All Functions & Class for connecting, creating,adding, delete, Writes the output of table in
    # CSV format, closes the connection of PostgreSQL
    ####################################################################################################################
if __name__ == "__main__":
    DataBaseSettings = {
        'user': 'postgres',
        'password': 'Platinum0435#',
        'host': 'localhost',
        'database': 'atec',
        'port': 6543
    }

    freqaccdb = GetIndxTableDB(Debug=True)
    freqaccdb.connect()
    #print(freqaccdb.connect(DataBaseSettings))

    freqaccdb.GetIndxTable(indxtabname='pwaccindxtable',datefilterfrom="2024-04-01", datefilterto="2024-04-20", sysfilter='rwr')
    """freqaccdb.CurDbTable.to_csv("freqaccindxtabledb.csv")
    print(freqaccdb.CurDbTable)
    freqaccdb.SelDateFilter(indxtabname='pwaccindxtable', datefilterfrom="2024-04-01", datefilterto="2024-04-20",
                            sysfilter='rwr')"""
    #freqaccdb.close()

##f'''SELECT date, test_tab_ref FROM freqaccindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}' AND test_tab_ref='{testtabname}' ''',
###("SELECT date, username, system_id, system, mode, test_tab_ref FROM freqaccindxtable, pwaccindxtable, priaccindxtable, amplaccindxtable, doaaccindxtable, sensmeasindxtable WHERE date BETWEEN '{datefilterfrom}' AND '{datefilterto}'")

