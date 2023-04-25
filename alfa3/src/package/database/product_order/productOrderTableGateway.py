import sys
from typing import Generator
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import TableGatewayInterface

class ProductOrderTableGateway(TableGatewayInterface):
    __GET_PRODUCT_ORDER_SQL = 'select * from `ProductOrder` where idProductOrder LIKE %s and Order_idOrder LIKE %s and Product_idProduct like %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
        self.to_string=['product order id','order id','product id','amount']
    def select(self,product_order_id:str='%',order_id:str='%',product_id:str='%')->Generator:
        """
        public Method select return result of select query
        :param product_order_id: str - product_order id of the product_order to select(default %)
        :param order_id: str - order id of the product_order to select(default %)
        :param product_id: str - product id of the product_order to select(default %)
        :return: yield resulted data from sql query 
        """
        self.cursor.execute(ProductOrderTableGateway.__GET_PRODUCT_ORDER_SQL,(product_order_id,order_id,product_id))
        for value in self.cursor:
            yield value

