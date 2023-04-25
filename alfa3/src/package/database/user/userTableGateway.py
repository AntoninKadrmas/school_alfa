import sys
from typing import Generator
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import TableGatewayInterface

class UserTableGateway(TableGatewayInterface):
    __GET_USER_SQL = 'select * from user where idUser LIKE %s and userType LIKE %s and nickName like %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
        self.to_string = ['user id','user type','nickname','cash']
    def select(self,user_id:str='%',user_type:str='%',nick_name:str='%')->Generator:
        """
        public Method select return result of select query
        :param user_id: str - user id of the user to select(default %)
        :param user_type: str - user type of the user to select(default %)
        :param nick_name: str - nickname of the user to select(default %)
        :return: yield resulted data from sql query 
        """
        self.cursor.execute(UserTableGateway.__GET_USER_SQL,(user_id,user_type,nick_name))
        for value in self.cursor:
            yield value

