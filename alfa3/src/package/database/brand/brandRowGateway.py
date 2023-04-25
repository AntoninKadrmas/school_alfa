import sys
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import RowGatewayInterface

class BrandRowGateway(RowGatewayInterface):
    __INSERT_BRAND_SQL = 'insert into brand(nameBrand,residence) values(%s,%s)'
    __UPDATE_BRAND_NAME_SQL = 'update brand set nameBrand = %s where idBrand LIKE %s and nameBrand LIKE %s and residence LIKE %s'
    __UPDATE_BRAND_RESIDENCE_SQL = 'update brand set residence = %s where idBrand LIKE %s and nameBrand LIKE %s and residence LIKE %s'
    __DELETE_BRAND_SQL = 'delete from brand where idBrand LIKE %s and nameBrand LIKE %s and residence LIKE %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
    def insert(self,brand_name:str,residence:str)->list:
        """
        public Method for insert brand into database
        :param brand_name: str - name of the brand
        :param residence: str - residence of the brand
        :return: list[str] - result of insert success or error
        """
        try:
            self.cursor.execute(BrandRowGateway.__INSERT_BRAND_SQL,(brand_name,residence))
        except:
            return [f'error: name {brand_name} already exists']
        else:
            return [f'insert run correctly']
    def update(self,new_brand_name:str='',new_residence:str='',brand_id:str='%',brand_name:str='%',residence:str='%')->list:
        """
        public Method for update brand in database
        :param new_brand_name: str - new name of the brand (default is '')
        :param new_residence: str - new residence of the brand (default is '')
        :param brand_id: str - id of the brand to update (default is '%')
        :param brand_name: str - name of the brand to update (default is '%')
        :param residence: str - residence of the brand to update (default is '%')
        :return: list[str] - result of update success or error
        """
        try:
            if new_brand_name!='': self.cursor.execute(BrandRowGateway.__UPDATE_BRAND_NAME_SQL,(new_brand_name,brand_id,brand_name,residence))
        except:
            return [f'error: name {brand_name} already exists']
        try:
            if new_residence!='': self.cursor.execute(BrandRowGateway.__UPDATE_BRAND_RESIDENCE_SQL,(new_residence,brand_id,brand_name,residence))
        except:
            return [f'error: some error in {new_residence}']
        if self.cursor.rowcount==0:return ['error: no brand has been updated']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} brand has been updated']
        else: return [f'{self.cursor.rowcount} brands have been updated']
    def delete(self,brand_id:str='%',brand_name:str='%',residence:str='%')->list:
        """
        public Method for delete brand from database
        :param brand_id: str - id of the brand to update (default is '%')
        :param brand_name: str - name of the brand to update (default is '%')
        :param residence: str - residence of the brand to update (default is '%')
        :return: list[str] - result of delete success or error
        """
        self.cursor.execute(BrandRowGateway.__DELETE_BRAND_SQL,(brand_id,brand_name,residence))
        if self.cursor.rowcount==0:return ['error: no brand has been deleted']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} brand has been deleted']
        else: return [f'{self.cursor.rowcount} brands have been deleted']