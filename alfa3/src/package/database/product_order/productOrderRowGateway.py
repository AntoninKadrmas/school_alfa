import sys
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import RowGatewayInterface

class ProductOrderRowGateway(RowGatewayInterface):
    __INSERT_PRODUCT_ORDER_SQL = 'insert into `ProductOrder`(Order_idOrder,Product_idProduct,amount) values (%s,%s,%s)'
    __UPDATE_PRODUCT_ORDER_ID_ORDER_SQL = 'update `ProductOrder` set idOrder = %s where idProductOrder LIKE %s and Order_idOrder LIKE %s and Product_idProduct like %s'
    __UPDATE_PRODUCT_ORDER_ID_PRODUCT_SQL = 'update `ProductOrder` set idProduct = %s where idProductOrder LIKE %s and Order_idOrder LIKE %s and Product_idProduct like %s'
    __UPDATE_PRODUCT_ORDER_AMOUNT_SQL = 'update `ProductOrder` set amount = %s where idProductOrder LIKE %s and Order_idOrder LIKE %s and Product_idProduct like %s'
    __DELETE_PRODUCT_ORDER_SQL = 'delete from `ProductOrder` where idProductOrder LIKE %s and Order_idOrder LIKE %s and Product_idProduct like %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
    def insert(self,order_id:str,product_id:str,amount:str)->None:
        """
        public Method for insert product_order into database
        :param order_id: str - order id of the product_order
        :param product_id: str - product id of the product_order
        :param amount: str - amount of the product_order
        :return: list[str] - result of insert success or error
        """
        try:
            self.cursor.execute(ProductOrderRowGateway.__INSERT_PRODUCT_ORDER_SQL,(order_id,product_id,amount))
        except:
            return [f'error: order id {order_id} or product id {product_id} is incorrect and does not exits']
        return ['insert run correctly']   
    def update(self,new_order_id:str='',new_product_id:str='',new_amount:str='',product_order_id:str='%',order_id:str='%',product_id:str='%')->None:
        """
        public Method for update product_order in database
        :param new_order_id: str - new order id of the product_order (default is '')
        :param new_product_id: str - new product id of the product_order (default is '')
        :param new_amount: str - new amount of the product_order (default is '')
        :param product_order_id: str - id of the product_order to update (default is '%')
        :param order_id: str - order id of the product_order to update (default is '%')
        :param product_id: str - product id of the product_order to update (default is '%')
        :return: list[str] - result of update success or error
        """
        try:
            if new_order_id!='': self.cursor.execute(ProductOrderRowGateway.__UPDATE_PRODUCT_ORDER_ID_ORDER_SQL,(new_order_id,product_order_id,order_id,product_id))
        except:
            return [f'error: order id {new_order_id} is incorrect and does not exits']
        try:
            if new_product_id!='': self.cursor.execute(ProductOrderRowGateway.__UPDATE_PRODUCT_ORDER_ID_PRODUCT_SQL,(new_product_id,product_order_id,order_id,product_id))
        except:
            return [f'error: product id {new_product_id} is incorrect and does not exits']
        try:
            if new_amount!='': self.cursor.execute(ProductOrderRowGateway.__UPDATE_PRODUCT_ORDER_AMOUNT_SQL,(new_amount,product_order_id,order_id,product_id))
        except:
            return ['error: incorrect datatype']
        if self.cursor.rowcount==0:return ['error: no product_order has been updated']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} product_order has been updated']
        else: return [f'{self.cursor.rowcount} product_orders have been updated']
    def delete(self,product_order_id:str='%',order_id:str='%',product_id:str='%')->None:
        """
        public Method for delete brand from database
        :param product_order_id: str - id of the product_order to update (default is '%')
        :param order_id: str - order id of the product_order to update (default is '%')
        :param product_id: str - product id of the product_order to update (default is '%')
        :return: list[str] - result of delete success or error
        """
        self.cursor.execute(ProductOrderRowGateway.__DELETE_PRODUCT_ORDER_SQL,(product_order_id,order_id,product_id))
        if self.cursor.rowcount==0:return ['error: no product_order has been deleted']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} product_order has been deleted']
        else: return [f'{self.cursor.rowcount} product_orders have been deleted']
