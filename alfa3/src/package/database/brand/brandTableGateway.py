import sys
from typing import Generator
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import TableGatewayInterface

class BrandTableGateway(TableGatewayInterface):
    __GET_BRAND_SQL = 'select * from brand where idBrand LIKE %s and nameBrand LIKE %s and residence LIKE %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
        self.to_string=['brand id','brand name','residence']
    def select(self,id_brand:str='%',brand_name:str='%',residence:str='%')->Generator:
        """
        public Method select return result of select query
        :param id_brand: str - brand id of the brand to select(default %)
        :param brand_name: str - brand name of the brand to select(default %)
        :param residence: str - residence of the brand to select(default %)
        :return: yield resulted data from sql query 
        """
        self.cursor.execute(BrandTableGateway.__GET_BRAND_SQL,(id_brand,brand_name,residence))
        for value in self.cursor:
            yield value 
