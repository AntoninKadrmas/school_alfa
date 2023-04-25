import sys
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import RowGatewayInterface

class OrderRowGateway(RowGatewayInterface):
    __INSERT_ORDER_SQL = 'insert into `Order`(User_idUser) values (%s)'
    __UPDATE_ORDER_PAID_SQL = 'update `Order` set paid = %s where idOrder LIKE %s and User_idUser LIKE %s and paid like %s and send like %s'
    __UPDATE_ORDER_SEND_SQL = 'update `Order` set send = %s where idOrder LIKE %s and User_idUser LIKE %s and paid like %s and send like %s'
    __DELETE_ORDER_SQL = 'delete from `Order` where idOrder LIKE %s and User_idUser LIKE %s and paid like %s and send like %s'
    def __init__(self,user_type:UserType='') -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
    def insert(self,user_id:str)->list:
        """
        public Method for insert order into database
        :param user_id: str - user id of the order
        :return: list[str] - result of insert success or error
        """
        try:
            self.cursor.execute(OrderRowGateway.__INSERT_ORDER_SQL,(user_id,))
        except:
            return [f'error: user with id {user_id} does not exists']
        return ['insert run correctly']
    def update(self,new_paid:str='',new_send:str='',order_id:str='%',user_id:str='%',paid:str='%',send:str='%')->list:
        """
        public Method for update order in database
        :param new_paid: str - new paid status of the order (default is '')
        :param new_send: str - new send status of the order (default is '')
        :param order_id: str - id of the order to update (default is '%')
        :param user_id: str - user id of the order to update (default is '%')
        :param paid: str - paid status of the order to update (default is '%')
        :param send: str - send status of the order to update (default is '%')
        :return: list[str] - result of update success or error
        """
        try:
            if new_paid!='': self.cursor.execute(OrderRowGateway.__UPDATE_ORDER_PAID_SQL,(new_paid,order_id,user_id,paid,send))
        except:
            return [f'incorrect datatype or out of range {new_paid}']
        try:
            if new_send!='': self.cursor.execute(OrderRowGateway.__UPDATE_ORDER_SEND_SQL,(new_send,order_id,user_id,paid,send))
        except:
            return [f'error: incorrect datatype or out of range {new_send}']
        if self.cursor.rowcount==0:return ['error: no order has been updated']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} order has been updated']
        else: return [f'{self.cursor.rowcount} orders have been updated']
    def delete(self,order_id:str='%',user_id:str='%',paid:str='%',send:str='%')->list:
        """
        public Method for delete order from database
        :param order_id: str - order id of the order to update (default is '%')
        :param user_id: str - user id of the order to update (default is '%')
        :param paid: str - paid status of the order to update (default is '%')
        :param send: str - send status of the order to update (default is '%')
        :return: list[str] - result of delete success or error
        """
        self.cursor.execute(OrderRowGateway.__DELETE_ORDER_SQL,(order_id,user_id,paid,send))
        if self.cursor.rowcount==0:return ['error: no order has been deleted']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} order has been deleted']
        else: return [f'{self.cursor.rowcount} orders have been deleted']
