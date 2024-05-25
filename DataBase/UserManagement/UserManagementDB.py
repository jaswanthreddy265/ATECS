# Database Functions of Deployed Systems
import psycopg2
import datetime
from DataBase.UserManagement.ErrorCodesDatabase import *

########################################################################################################################
#   User Management Database Class and its Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   25 Feb 2024
#   UserManagementDB Class has the following member Functions
#   1. init()
#   2. connect()
#   3. CreateUsrMngtdbTable()
#   4. AddUser()
#   5. GetUserListfromDB()
#   6. ModifyUserData()
#   7. DeleteUser()
#   8. CheckUserCredentials()
#   9. Close()
########################################################################################################################
# This Creating the UserManagement Class
########################################################################################################################
class UserManagementDB():
    def __init__(self,Debug = False):
        self.connection = None
        self.Debug = Debug
        self.tablename = 'tableurmngt'
    ####################################################################################################################
    # This function establishes the Connection with DataBase and Validates the Connection
    ####################################################################################################################
    def connect(self, DataBaseSettings = {
                                'user' :'postgres',
                                'password':'Platinum0435#',
                                'host':'localhost',
                                'database' : 'atec',
                                'port': 6543
                                }):
        try:
            self.connection = psycopg2.connect(
                                            user=DataBaseSettings['user'],
                                            password=DataBaseSettings['password'],
                                            host=DataBaseSettings['host'],
                                            database= DataBaseSettings['database'],
                                            port=DataBaseSettings['port']
                                            )
            self.CreateUsrMngtdbTable()
            if self.Debug == True:
                print('UserManagementDB(connect) - Connection Established  *****************')
            return SUCCESS
        except (Exception, psycopg2.Error) as error:
            if self.Debug == True:
                print("UserManagementDB(connect) -Error while connecting to PostgreSQL", error)
            return DATABASE_CONNECTION_ERROR
    ####################################################################################################################
    # This function Creates the User Management Table in DataBase with the fields
    ####################################################################################################################
    def CreateUsrMngtdbTable(self):
        try:
            cursor = self.connection.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.tablename}
                                     (   username       TEXT        NOT NULL,
                                         password       TEXT        NOT NULL,
                                         accesslevel    TEXT        NOT NULL,
                                         status         TEXT        NOT NULL,
                                         date           TIMESTAMP   NOT NULL,
                                         usercode       INT         NOT NULL,
                                         remarks        TEXT
                                     ); '''
            cursor.execute(create_table_query)
            self.connection.commit()
            if self.Debug == True:
                print("UserManagementDB(CreateUsrMngtdbTable) -  Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("UserManagementDB(CreateUsrMngtdbTable) - Error while creating table", error)
            return error
    ####################################################################################################################
    # This function adds the user data in DataBases Table
    ####################################################################################################################
    def AddUser(self,usercred = {'date' : datetime.datetime.now(),'username' : 'admin',
                                 'password' : 'password', 'accesslevel' : 'view', 'status' : 'active',
                                'usercode' : 4256,'remarks' : 'new user created,'
                                }):
        try:
            cursor = self.connection.cursor()
            insert_table_query = f'''INSERT INTO {self.tablename} VALUES('{usercred['username']}','{usercred['password']}','{usercred['accesslevel']}',
                                    '{usercred['status']}','{usercred['date']}',
                                    '{usercred['usercode']}','{usercred['remarks']}' '''
            insert_table_query = insert_table_query + ');'
            cursor.execute(insert_table_query)
            self.connection.commit()
            return SUCCESS
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("UserManagementDB (AddUser)- Error in inserting to table", error)
            return DATABASE_ADDUSER_ERROR
        if self.Debug == True:
            print("UserManagementDB(AddUser) - New User Added")
    ####################################################################################################################
    # This function Gets the user list from DataBases Table
    ####################################################################################################################
    def GetUserListfromDB(self,status = 'active'):
        try:
            create_table_query = f'''SELECT username, accesslevel FROM {self.tablename} where status = '{status}' '''
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            result = cursor.fetchall()
           # print(result)
            if result is not None:
                userlist = []
                for user in result:
                    #print(user)
                    userlist.append(user)
                return userlist
            else:
                return result
        except (Exception, psycopg2.DatabaseError) as error:
            print("UserManagementDB (GetUserListfromDB) - Error in query \n", error)
            return False
    ####################################################################################################################
    # This function Gets the new user code from DataBases Table
    ####################################################################################################################
    """def GetnewuserCode(self):
        try:
            create_table_query = f'''SELECT usercode FROM {self.tablename} '''
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            result = cursor.fetchall()
            print(len(result))
            if result is not None:
                userlist = []
                for user in result:
                    userlist.append(user[0])
                return max(userlist)
            else:
                return 0
        except (Exception, psycopg2.DatabaseError) as error:
            print("UserManagementDB (GetUserListfromDB) - Error in query \n", error)
            return False
    ####################################################################################################################
    # This function Gets the user code from DataBases Table
    ####################################################################################################################
    def GetuserCode(self,field = 'username', data = 'admin'):
        try:
            create_table_query = f'''SELECT usercode FROM {self.tablename} WHERE {field} LIKE '{data}' '''
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            usercode = cursor.fetchall()
            if len(usercode) == 0:
                return 0
            else:
                return usercode[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print("UserManagementDB (GetUserListfromDB) - Error in query \n", error)
            return False"""
    ####################################################################################################################
    # This function Modify the user data from DataBases Table
    ####################################################################################################################
    def ModifyUserData(self,usercode = 1234, field = 'username', data = 'admin'):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f'''update {self.tablename} set {field} = '{data}' where usercode = '{usercode}'; ''')
            self.connection.commit()
            if self.Debug == True:
                print("UserManagementDB(ModifyUserAccessLevel) - Success")
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("UserManagementDB(ModifyUserAccessLevel) - Error")
            return False
    ####################################################################################################################
    # This function Delete the user from DataBases Table
    ####################################################################################################################
    def DeleteUser(self,usercode = 8888, field = 'username', data = 'admin'):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f'''update {self.tablename} set {field} = '{data}' where usercode = '{usercode}'; ''')
            self.connection.commit()
            if self.Debug == True:
                print("UserManagementDB(DeleteUser) - Success")
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            if self.Debug == True:
                print("UserManagementDB(DeleteUser) - Error")
            return False
    ####################################################################################################################
    # This function Gets the user credentials list from DataBases Table
    ####################################################################################################################
    def CheckUserCredentials(self, username = 'admin'):
        try:
            create_table_query = f'''SELECT usercode FROM {self.tablename} WHERE username LIKE '{username}' '''
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            result = cursor.fetchone()
            if result is not None:
                return result[0]
            else :
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print("UserManagementDB(CheckUserCredentials) - Error in query \n", error)
            return False
    ####################################################################################################################
    # This function Closes the DataBase Connection with DataBase
    ####################################################################################################################
    def close(self):
      #  time.sleep(10)
        self.connection.close()
        if self.Debug == True:
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
    usrmgtdb = UserManagementDB(Debug=False)
    print(usrmgtdb.connect(DataBaseSettings))
    usrmgtdb.tablename = 'tableusrmngt'
    usrmgtdb.CreateUsrMngtdbTable()
    #print(usrmgtdb.CheckUserUserCode())

    newuser = {'date' : datetime.datetime.now(),'username' : 'jaswanth',
                'password' : 'password', 'accesslevel' : 'view', 'status' : 'active',
                'usercode' : 1,'remarks' : 'new user created,'
              }
    if usrmgtdb.CheckUserCredentials(username=newuser['username']) is None:
        usrmgtdb.AddUser(usercred=newuser)
    '''
    if usrmgtdb.CheckUserCredentials(username='bhaskar') is not None:
        usrmgtdb.ModifyUserAccessLevel(tablename='tableusrmngt',usercode=usrmgtdb.GetuserCode()+1,newaccesslevel='exec')
    if usrmgtdb.CheckUserCredentials(username='aditya') is not None:
        usrmgtdb.ModifyUserPassword(tablename='tableusrmngt', usercode=usrmgtdb.GetuserCode()+1, newpassword='exec')
    userlist = usrmgtdb.GetUserListfromDB(tablename='tableusrmngt')
    print(userlist)
   '''
    userlist = usrmgtdb.GetUserListfromDB(status='Inactive')
    print(userlist)
    usrmgtdb.close()

########################################################################################################################