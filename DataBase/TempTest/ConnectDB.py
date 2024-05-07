import psycopg2
from DataBase.TestCases.ErrorCodesDatabase import SUCCESS, DATABASE_CONNECTION_ERROR


class Connect_to_Database():
    def __init__(self, Debug=True):
        self.Debug = Debug
        DataBaseSettings = {
            'user': 'postgres',
            'password': 'Platinum0435#',
            'host': 'localhost',
            'database': 'atec',
            'port': 6543
        }
        try:
            self.connection =psycopg2.connect(
                user=DataBaseSettings['user'],
                password=DataBaseSettings['password'],
                host=DataBaseSettings['host'],
                database=DataBaseSettings['database'],
                port=DataBaseSettings['port']
            )
            if self.Debug == True:
                print("ConnectionDB(connect) - Connection Established")
            #return SUCCESS
        except (Exception, psycopg2.Error) as error:
            if self.Debug == True:
                print("ConnectionDB(connect) -Error while connecting to PostgreSQL", error)
            #return DATABASE_CONNECTION_ERROR
    ####################################################################################################################
    # This Function Closes The Database
    ####################################################################################################################
    def ConnectClose(self):
        self.connection.close()
        if self.Debug == True:
            print("PostgreSQL connection is closed")
        else:
            print("Error while Closing the PostgreSQL Connection")

    ####################################################################################################################
    # This Function calls ConnectionDB Class for connecting, closing the connection of PostgreSQL
    ####################################################################################################################
if __name__ == "__main__":
    DataBaseSettings = {
        'user': 'postgres',
        'password': 'Platinum0435#',
        'host': 'localhost',
        'database': 'atec',
        'port': 6543
    }
    curconndb = Connect_to_Database(Debug=True)
    #print(curconndb.ConnectToDB(DataBaseSettings))
    curconndb.ConnectClose()