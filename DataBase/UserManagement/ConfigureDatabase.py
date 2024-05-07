
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import extensions, sql

########################################################################################################################
#   Configure Database Class and its Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   25 Feb 2024
#   ConfigureDatabase Class has the following member Functions
#   1. init()
#   2. CONNECT()
#   3. CreateDb()
#   4. GetDb()
#   5. DeleteDb()
#   6. DropTable()
#   7. Close()
########################################################################################################################
# This Creating the ConfigureDataBase Class
########################################################################################################################
class ConfigureDataBase():
    def __init__(self, Debug=False):
        self.Debug = Debug
        self.connection = True
    ####################################################################################################################
    # This function establishes the Connection with DataBase and Validates the Connection
    ####################################################################################################################
    def CONNECT(self, host = 'localhost', port = '6543', user = 'postgres', password = 'Platinum0435#'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            if self.Debug == True:
                print('Connection Established')
            return True
        except (Exception, psycopg2.Error) as error:
            if self.Debug == True:
                print("Error while connecting to PostgreSQL", error)
            return False

    ####################################################################################################################
    # This function Creates the DataBase Folder in DataBase and Name of the DataBase is in string
    ####################################################################################################################
    def CreateDb(self,dbname = 'atec'):
        # string for the new database name to be created
        # get the isolation level for autocommit
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
        #print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        """
        ISOLATION LEVELS for psycopg2
        0 = READ UNCOMMITTED
        1 = READ COMMITTED
        2 = REPEATABLE READ
        3 = SERIALIZABLE
        4 = DEFAULT
        """
        # set the isolation level for the connection's cursors
        # will raise ActiveSqlTransaction exception otherwise
        self.connection.set_isolation_level(autocommit)
        # instantiate a cursor object from the connection
        cursor = self.connection.cursor()
        # use the execute() method to make a SQL request
        # cursor.execute('CREATE DATABASE ' + str(DB_NAME))
        # Doping database MYDATABASE if already exists.
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f'Database {dbname} created successfully........')
    ####################################################################################################################
    # This function Gets the DataBases Folder in DataBase
    ####################################################################################################################
    def GetDataBases(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT datname FROM pg_database;")
        dbdata = cursor.fetchall()
        dblist = []
        for dbase in dbdata:
            dblist.append(dbase[0])
        return dblist

    ####################################################################################################################
    # This function Deletes the DataBase Folder in DataBase and Name of the DataBase to be deleted is in string
    ####################################################################################################################
    def DeleteDb(self, dbname='atec'):
        # string for the new database name to be created
        # get the isolation leve for autocommit
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
        # print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        """
        ISOLATION LEVELS for psycopg2
        0 = READ UNCOMMITTED
        1 = READ COMMITTED
        2 = REPEATABLE READ
        3 = SERIALIZABLE
        4 = DEFAULT
        """
        # set the isolation level for the connection's cursors
        # will raise ActiveSqlTransaction exception otherwise
        self.connection.set_isolation_level(autocommit)
        # instantiate a cursor object from the connection
        cursor = self.connection.cursor()
        # use the execute() method to make a SQL request
        # cursor.execute('CREATE DATABASE ' + str(DB_NAME))
        # Doping database MYDATABASE if already exists.
        cursor.execute(sql.SQL(
            "DROP DATABASE {}"
        ).format(sql.Identifier(dbname)))

    ####################################################################################################################
    # This function Deletes the DataBase Table in DataBase and Name of the DataBase Table is in string
    ####################################################################################################################
    def DropTable(self, tablename='tbsample'):
        cursor = self.connection.cursor()
        create_table_query = '''DROP TABLE IF EXISTS {}; '''.format(tablename)
        cursor.execute(create_table_query)
        self.connection.commit()

    ####################################################################################################################
    # This function Closes the DataBase Connection with DataBase
    ####################################################################################################################
    def CLOSE(self):
        self.connection.close()
        if self.Debug == True:
            print("PostgreSQL connection is closed")
########################################################################################################################
if __name__ == "__main__":
    newdb = ConfigureDataBase()
    connstatus = newdb.CONNECT(host='localhost', port='6543', user='postgres', password='Platinum0435#')
    #print(connstatus)
    #print(newdb.GetDatabses())
    databasename = 'atec'               ######db name
    if connstatus == True:
        if databasename not in newdb.GetDataBases():
            print('database not found & Creating database')
            newdb.CreateDb(dbname=databasename)
        else:
            print('database already existing')              ######
    print(newdb.GetDataBases())                             ######Prints the Available DataBases Folder
    #  newdb.DeleteDb(dbname=databasename)
    #print(newdb.GetDatabses())
    newdb.CLOSE()
########################################################################################################################