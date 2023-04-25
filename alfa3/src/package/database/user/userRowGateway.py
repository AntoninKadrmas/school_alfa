import sys
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType,CostumerType
from package.database.interfaceDB import RowGatewayInterface
from package.database.userLogin import UserSingleton
from package.database.user.userTableGateway import UserTableGateway
class UserRowGateway(RowGatewayInterface):
    __INSERT_USER_SQL = 'insert into user(userType,nickName) values (%s,%s)'
    __UPDATE_USER_NICKNAME_SQL = 'update user set nickName = %s where idUser LIKE %s and userType LIKE %s and nickName like %s'
    __UPDATE_USER_CASH_SQL = 'update user set cash = %s where idUser LIKE %s and userType LIKE %s and nickName like %s'
    __DELETE_USER_SQL = 'delete from user where idUser LIKE %s and userType LIKE %s and nickName like %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """ 
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
    def insert(self,user_type:str,nick_name:str)->list:
        """
        public Method for insert user into database
        :param user_type: str - type of the user
        :param nick_name: str - nickname of the user
        :return: list[str] - result of insert success or error
        """
        if user_type!=CostumerType.CUSTOMER.value and \
            user_type!=CostumerType.EMPLOYEE.value: return['incorrect type has to be employee/customer']
        try:
            self.cursor.execute(UserRowGateway.__INSERT_USER_SQL,(user_type,nick_name))
        except:
            return [f'error: nickname {nick_name} is already exists']
        return ['insert run correctly' ]
    def update(self,new_nick_name:str='',new_cash:str='',user_id:str='%',user_type:str='%',nick_name:str='%')->list:
        """
        public Method for update user in database
        :param new_nick_name: str - new nickname of the user (default is '')
        :param new_cash: str - new cash of the user (default is '')
        :param user_id: str - id of the user to update (default is '%')
        :param user_type: str - type of the user to update (default is '%')
        :param nick_name: str - nickname of the user to update (default is '%')
        :return: list[str] - result of update success or error
        """
        try:
            if new_nick_name!='': self.cursor.execute(UserRowGateway.__UPDATE_USER_NICKNAME_SQL,(new_nick_name,user_id,user_type,nick_name))
        except:
            return [f'error: nickname {nick_name} is already exists']
        try:
            if new_cash!='': self.cursor.execute(UserRowGateway.__UPDATE_USER_CASH_SQL,(new_cash,user_id,user_type,nick_name))
        except:
            return ['error: something went wrong']
        if self.cursor.rowcount==0:return ['error: no user has been updated']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} user has been updated']
        else: return [f'{self.cursor.rowcount} users have been updated']
    def delete(self,user_id:str='%',type:str='%',nick_name:str='%')->list:
        """
        public Method for delete user from database
        :param user_id: str - id of the user to update (default is '%')
        :param user_type: str - type of the user to update (default is '%')
        :param nick_name: str - nickname of the user to update (default is '%')
        :return: list[str] - result of delete success or error
        """
        self.cursor.execute(UserRowGateway.__DELETE_USER_SQL,(user_id,type,nick_name))
        try:
            iter(next(UserTableGateway().select(user_id=UserSingleton.getUser().id)))#can not delete yourself
        except: return['error: can not delete your account']
        if self.cursor.rowcount==0:return ['error: no user has been deleted']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} user has been deleted']
        else: return [f'{self.cursor.rowcount} users have been deleted']
