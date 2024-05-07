import datetime
from DataBase.TestCases.ErrorCodesDatabase import *
from UserManagementDB import UserManagementDB
########################################################################################################################
#   User Management Functions Database Class and its Functions
#   Author  :   Bandi Jaswanth Reddy
#   Date    :   25 Feb 2024
#   UserManagementDBFuns Class has the following member Functions
#   1. init()
#   2. connect()
#   3. AddNewUser()
#   4. ModifyUserName()
#   5. ModifyPassword()
#   6. ModifyAccessLevel()
#   7. GetActiveUserListfromDB()
#   8. DeleteUser()
#   9. Close()
########################################################################################################################
# This Creating the UserManagementFuns Class
########################################################################################################################
class UserManagementFuns():
    def __init__(self,Debug = False, ):
        self.Debug = Debug
        self.tablename = 'tableusrmngt'
        usrmgtdb = UserManagementDB(Debug=True)
        usrmgtdb.tablename = self.tablename
        self.DataBaseSettings = {
                                'user' :'postgres',
                                'password':'Platinum0435#',
                                'host':'localhost',
                                'database' : 'atec',
                                'port': 6543
                                }
    ###################################################################################################################
    #         userdata={ 'username': 'aditya','password': 'password', 'accesslevel': 'view'
    ###################################################################################################################
    def AddNewUser(self,userdata={ 'username': 'admin','password': 'password', 'accesslevel': 'view'}):
        newuser = {
                    'date'          : datetime.datetime.now(),
                    'username'      : userdata['username'],
                    'password'      : userdata['password'],
                    'accesslevel'   : userdata['accesslevel'],
                    'status'        : 'active',
                    'usercode'      :   0 ,
                    'remarks'       : 'new user created,'
                   }
        usrmgtdb = UserManagementDB(Debug=True)
        if usrmgtdb.connect(self.DataBaseSettings) == SUCCESS :
            if usrmgtdb.CheckUserCredentials(username=userdata['username']) is None:
                newuser['usercode'] = usrmgtdb.GetnewuserCode() + 1
                usrmgtdb.AddUser(usercred=newuser)
                if self.Debug==False:
                    print("UserManagementFuns(AddNewUser)-ADD NEW USER")
                return SUCCESS
            else:
                print("UserManagementFuns(AddNewUser)-USER ALREADY EXIST")
                return USERNAME_AVAIALIBITY_ERROR

            usrmgtdb.close()
        else:
            print('UserManagementFuns(AddNewUser)- DATABASE_CONNECTION_ERROR')
            return DATABASE_CONNECTION_ERROR

    ###################################################################################################################
    #         This Function Adds the new user in database
    ###################################################################################################################
    def ModifyUsername(self,olduserame = 'bhaskar', newusername = 'navya'):
        usrmgtdb = UserManagementDB(Debug=True)
        if usrmgtdb.connect(self.DataBaseSettings) == SUCCESS:
            if usrmgtdb.CheckUserCredentials(username=olduserame) is not None:    #old User name is Exist
                if usrmgtdb.CheckUserCredentials(username=newusername) is None:  #New User name is Not Existing
                    usercode  =usrmgtdb.GetuserCode(field='username',data=olduserame)
                    usrmgtdb.ModifyUserData(usercode=usercode,field='username',data=newusername)
                    #print(usercode)
                    if self.Debug == False:
                        print("UserManagementFuns(ModifyUsername)- MODIFIED USERNAME")
                    return SUCCESS

                else:
                    print('UserManagementFuns(ModifyUsername)- NEW USER ALREADY EXIST')
                    return NEWUSERNAME_ALREADY_EXIST
            else:
                print('UserManagementFuns(ModifyUsername)- USER DOES NOT EXIST')
                return OLDUSERNAME_DOES_NOT_EXIST
            usrmgtdb.close()
        else:
            print('UserManagementFuns(ModifyUsername)- DATABASE_CONNECTION_ERROR')
            return DATABASE_CONNECTION_ERROR
    ###################################################################################################################
    #         This Function modifies the username of user in database
    ###################################################################################################################
    def Modifypassword(self,username = 'admin', newpassword = 'aditya', ResetFlag = False):
        usrmgtdb = UserManagementDB(Debug=True)
        if usrmgtdb.connect(self.DataBaseSettings) == SUCCESS:
            if usrmgtdb.CheckUserCredentials(username=username) is not None:    #old User name is Exist
                usercode  =usrmgtdb.GetuserCode(field='username',data=username)
                if ResetFlag == True:
                    newpassword = "Init@1234"
                usrmgtdb.ModifyUserData(usercode=usercode,field='password',data=newpassword)
                if self.Debug == False:
                    print("UserManagementFuns(Modifypassword)- MODIFIED PASSWORD")
                #print(usercode)
                return SUCCESS
            else:
                print('UserManagementFuns(Modifypassword)- USER DOES NOT EXIST')
                return OLDUSERNAME_DOES_NOT_EXIST
            usrmgtdb.close()
        else:
            print('UserManagementFuns(Modifypassword)- DATABASE_CONNECTION_ERROR')
            return DATABASE_CONNECTION_ERROR
    ###################################################################################################################
    #         This Function modifies the password of user in database
    ###################################################################################################################
    def ModifyAccessLevel(self, username='admin', newaccesslvl='exec'):
        usrmgtdb = UserManagementDB(Debug=True)
        if usrmgtdb.connect(self.DataBaseSettings) == SUCCESS:
            if usrmgtdb.CheckUserCredentials(username=username) is not None:  # old User name is Exist
                usercode = usrmgtdb.GetuserCode(field='username', data=username)
                usrmgtdb.ModifyUserData(usercode=usercode, field='accesslevel', data=newaccesslvl)
                # print(usercode)
                if self.Debug == False:
                    print("UserManagementFuns(ModifyAccessLevel)- MODIFIED ACCESS LEVEL")
                return SUCCESS
            else:
                print('UserManagementFuns(ModifyAccessLevel)- USER DOES NOT EXIST')
                return OLDUSERNAME_DOES_NOT_EXIST
            usrmgtdb.close()
        else:
            print('UserManagementFuns(ModifyAccessLevel)- DATABASE_CONNECTION_ERROR')
            return DATABASE_CONNECTION_ERROR
    ###################################################################################################################
    #         This Function modifies the access level of user in database
    ###################################################################################################################
    def GetActiveUserListfromDB(self,status = 'active'):
        usrmgtdb = UserManagementDB(Debug=True)
        if usrmgtdb.connect(self.DataBaseSettings) == SUCCESS:
            usrlist = usrmgtdb.GetUserListfromDB(status)
            usrmgtdb.close()
            if self.Debug == False:
                print("UserManagementFuns(GetActiveUserListfromDB)- GET USER LIST SUCCESSFULLY")
            return SUCCESS, usrlist

        else:
            print('UserManagementFuns(GetActiveUserListfromDB)- DATABASE_CONNECTION_ERROR')
            return DATABASE_CONNECTION_ERROR
    ###################################################################################################################
    #         This Function Activate or Inactivate the User
    ###################################################################################################################
    def DeleteUser(self, username='admin', newstatus='Inactive'):
        usrmgtdb = UserManagementDB(Debug=True)
        if usrmgtdb.connect(self.DataBaseSettings) == SUCCESS:
            if usrmgtdb.CheckUserCredentials(username=username) is not None:  # old User name is Exist
                usercode = usrmgtdb.GetuserCode(field='username', data=username)
                usrmgtdb.DeleteUser(usercode=usercode, field='status', data=newstatus)
                if self.Debug == False:
                    print("UserManagementFuns(DeleteUser)- ACTIVATE OR INACTIVATE USER")
                # print(usercode)
                return SUCCESS
            else:
                print('UserManagementFuns(DeleteUser)- USER DOES NOT EXIST')
                return OLDUSERNAME_DOES_NOT_EXIST
            usrmgtdb.close()
        else:
            print('UserManagementFuns(DeleteUser)- DATABASE_CONNECTION_ERROR')
            return DATABASE_CONNECTION_ERROR
    ###################################################################################################################
    #         This Function Delete the User
    ###################################################################################################################
    def close(self):
      #  time.sleep(10)
        self.connection.close()
        if self.Debug == True:
            print("PostgreSQL connection is closed")
    ####################################################################################################################
    # This function Closes the DataBase Connection with DataBase
    ####################################################################################################################
if __name__ == "__main__":
    usrmngt = UserManagementFuns()
    usrmngt.tablename = 'tableusrmngt'
    usrmngt.DataBaseSettings =  {
                                'user' :'postgres',
                                'password':'Platinum0435#',
                                'host':'localhost',
                                'database' : 'atec',
                                'port': 6543
                                }
    usrmngt.AddNewUser(userdata={ 'username': 'platinumTECHN','password': 'wert', 'accesslevel': 'exec'})
   # usrmngt.ModifyUsername(olduserame='platinum', newusername='aditya')
   # usrmngt.Modifypassword(username='madhavi',newpassword='hello', ResetFlag=False)
   # usrmngt.ModifyAccessLevel(username="Jaswanth", newaccesslvl='view')
   # usrmngt.DeleteUser(username='Madhavi', newstatus='active')
  #  print(xx)
    status, usrlist = usrmngt.GetActiveUserListfromDB(status='active')
    if status == SUCCESS:
        if len(usrlist) > 0:
            print(usrlist)