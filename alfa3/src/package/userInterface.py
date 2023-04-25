from package.database.myEnum import UserType,CostumerType
from package.database.user.userTableGateway import UserTableGateway
from package.database.user.userRowGateway import UserRowGateway
from package.applicationAdmin import ApplicationAdmin
from package.applicationUser import ApplicationUser
from package.database import connection,userLogin
from typing import Union
from prettytable import PrettyTable
class UserInterface():
    """
    Class that manage console output and input
    """
    def __init__(self) -> None:
        self.user:userLogin.User=None
        self.connection=None
        self.applications:Union[ApplicationAdmin,ApplicationUser]
    def run(self)->None:
        """
        public Method run call decide which set of commands would be available.
        """
        self.__login()
        if str(self.user.type)==CostumerType.CUSTOMER.value.lower():
            self.connection = connection.Connection.getConnection(UserType.USER)
            self.applications = ApplicationUser()
        else:
            self.connection = connection.Connection.getConnection(UserType.ADMIN)
            self.applications = ApplicationAdmin()
        used_dict = self.applications.options
        self.__user_input(used_dict)
    def __user_input(self,used_dict:Union[ApplicationAdmin,ApplicationUser])->None:
        """
        private Method user_input take care of user interaction with used_dict to that contains commands user can call.
        :param user_dict: is used dictionary of key name of action value function pair
        """
        while True:
            for count,options in enumerate(used_dict.keys()):
                print(f'{count+1}. {options}')
            try:
                chose = int(input('Chose one of the options:'))
            except:
                print('error: input has to be integer')
            else:
                if(chose<1 or chose > len(used_dict)):print('error: Integer out of range')
                else:
                    self.connection.start_transaction()
                    result_list:list = []
                    helper = None
                    for result in used_dict[list(used_dict.keys())[chose-1]]():#load all data into PrettyTable
                        helper =result
                        if type(helper)==str:break #result is not a select
                        if result[0]:
                            result_list.append(PrettyTable())
                            result_list[len(result_list)-1].field_names=result[1:]
                        else:result_list[len(result_list)-1].add_row(result[1:])
                    else:
                        for elements in result_list:# print PrettyTable
                            print(elements)
                    if type(helper)==str:
                        if 'error' in helper:self.connection.rollback()
                        print(helper)
                    self.connection.commit()
    def __login(self)->None:
        """
        private Method login waiting for user input name and then find user with same name or create new one.
        """
        self.connection = connection.Connection.getConnection(UserType.ADMIN)
        self.connection.start_transaction()
        table = UserTableGateway()
        while True:
            try:
                user = input('login name:').strip().lower()
                if user=='':continue
            except:
                self.connection.commit()
                connection.Connection.close()
                exit()
            for user_el in table.select(nick_name=user):#find user
                self.user = userLogin.UserSingleton.getUser(user_el)#get user data
            if self.user==None:
                yes_no = input(f'user with name {user} does not exist do you want to create it?(y/n):').strip().lower()
                if yes_no=='y':#create new user
                    UserRowGateway().insert(CostumerType.CUSTOMER.value,user)
                    for user_el in table.select(nick_name=user):
                        self.user = userLogin.UserSingleton.getUser(user_el)
                else:continue
            if self.user!=None:
                self.connection.commit()
                connection.Connection.close()
                return