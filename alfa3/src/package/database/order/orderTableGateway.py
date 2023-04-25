import sys
from typing import Generator
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import TableGatewayInterface

class OrderTableGateway(TableGatewayInterface):
    __GET_ORDER_SQL = 'select * from `Order` where idOrder LIKE %s and User_idUser LIKE %s and paid like %s and send like %s order by `Order`.createDate desc;'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
        self.to_string=['order id','create date','user id','paid','send']
    def select(self,order_id:str='%',user_id:str='%',paid:str='%',send:str='%')->Generator:
        """
        public Method select return result of select query
        :param order_id: str - order id of the order to select(default %)
        :param user_id: str - order user id of the order to select(default %)
        :param paid: str - paid status of the order to select(default %)
        :param send: str - send status of the order to select(default %)
        :return: yield resulted data from sql query 
        """
        self.cursor.execute(OrderTableGateway.__GET_ORDER_SQL,(order_id,user_id,paid,send))
        for value in self.cursor:
            yield value[:3]+(int(value[3])==1,int(value[4])==1)