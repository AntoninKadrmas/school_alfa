import sys
from typing import Generator
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import TableGatewayInterface

class ProductTableGateway(TableGatewayInterface):
    __GET_PRODUCT_SQL = 'select * from product where idProduct LIKE %s and nameProduct LIKE %s and Brand_idBrand like %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
        self.to_string=['product id','product name','weight in KG','price','brand id']
    def select(self,product_id:str='%',product_name:str='%',brand_id:str='%')->Generator:
        """
        public Method select return result of select query
        :param product_id: str - product id of the product to select(default %)
        :param product_name: str - product name of the product to select(default %)
        :param brand_id: str - brand of the product to select(default %)
        :return: yield resulted data from sql query 
        """
        self.cursor.execute(ProductTableGateway.__GET_PRODUCT_SQL,(product_id,product_name,brand_id))
        for value in self.cursor:
            yield value

