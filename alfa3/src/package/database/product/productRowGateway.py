import sys
from typing import Union
sys.path.append('../')
from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.interfaceDB import RowGatewayInterface

class ProductRowGateway(RowGatewayInterface):
    __INSERT_PRODUCT_SQL = 'insert into product(nameProduct,weightKG,price,Brand_idBrand) values (%s,%s,%s,%s)'
    __UPDATE_PRODUCT_NAME_SQL = 'update product set nameProduct = %s where idProduct LIKE %s and nameProduct LIKE %s and Brand_idBrand like %s'
    __UPDATE_PRODUCT_WEIGHT_SQL = 'update product set weightKG = %s where idProduct LIKE %s and nameProduct LIKE %s and Brand_idBrand like %s'
    __UPDATE_PRODUCT_PRICE_SQL = 'update product set price = %s where idProduct LIKE %s and nameProduct LIKE %s and Brand_idBrand like %s'
    __UPDATE_PRODUCT_BRAND_SQL = 'update product set Brand_idBrand = %s where idProduct LIKE %s and nameProduct LIKE %s and Brand_idBrand like %s'
    __DELETE_PRODUCT_SQL = 'delete from product where idProduct LIKE %s and nameProduct LIKE %s and Brand_idBrand like %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db and create to_string for print out
        :param user_type: type of privileges for database connection
        """
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor(buffered=True)
    def insert(self,product_name:str,weight:str,price:str,brand_id:str)->list:
        """
        public Method for insert product into database
        :param product_name: str - name of the product
        :param weight: str - weight of the product (have to be convertible to decimal number)
        :param price: str - price of the product (have to be convertible to decimal number)
        :param brand_id: str - brand id of the product
        :return: list[str] - result of insert success or error
        """
        if self.__it_is_number(weight,'weight')!=None:return self.__it_is_number(weight,'weight')
        if self.__it_is_number(price,'price')!=None:return self.__it_is_number(price,'price')
        try:
            self.cursor.execute(ProductRowGateway.__INSERT_PRODUCT_SQL,(product_name,weight,price,brand_id))
        except:
            return [f'error: brand with id {brand_id} does not exists']
        return ['insert run correctly']
    def update(self,new_product_name:str='',new_weight:str='',new_price:str='',new_brand_id:str='',product_id:str='%',product_name:str='%',brand_id:str='%')->list:
        """
        public Method for update product in database
        :param new_product_name: str - new name of the product (default is '')
        :param new_weight: str - new weight of the product (default is '')
        :param new_price: str - new price of the product (default is '')
        :param new_brand_id: str - new brand id of the product (default is '')
        :param product_id: str - id of the product to update (default is '%')
        :param product_name: str - name of the product to update (default is '%')
        :param brand_id: str - brand id of the product to update (default is '%')
        :return: list[str] - result of update success or error
        """
        if self.__it_is_number(new_weight,'weight')!=None:return self.__it_is_number(new_weight,'weight')
        if self.__it_is_number(new_price,'price')!=None:return self.__it_is_number(new_price,'price')
        try:
            if new_product_name!='': self.cursor.execute(ProductRowGateway.__UPDATE_PRODUCT_NAME_SQL,(new_product_name,product_id,product_name,brand_id))
        except:
            return [f'error: incorrect datatype {new_product_name}']
        try:
            if new_brand_id!='': self.cursor.execute(ProductRowGateway.__UPDATE_PRODUCT_BRAND_SQL,(new_brand_id,product_id,product_name,brand_id))
        except:
            return [f'error: brand with id {new_brand_id}  does not exists']
        try:
            if new_weight!='': self.cursor.execute(ProductRowGateway.__UPDATE_PRODUCT_WEIGHT_SQL,(new_weight,product_id,product_name,brand_id))
        except:
            return [f'error: incorrect datatype {new_weight}']
        try:
            if new_price!='': self.cursor.execute(ProductRowGateway.__UPDATE_PRODUCT_PRICE_SQL,(new_price,product_id,product_name,brand_id))
        except:
            return [f'error: incorrect datatype {new_price}']
        if self.cursor.rowcount==0:return ['error: no product has been updated']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} product has been updated']
        else: return [f'{self.cursor.rowcount} products have been updated']
    def delete(self,product_id:str='%',product_name:str='%',brand_id:str='%')->list:
        """
        public Method for delete product from database
        :param product_id: str - id of the product to update (default is '%')
        :param product_name: str - name of the product to update (default is '%')
        :param brand_id: str - brand id of the product to update (default is '%')
        :return: list[str] - result of delete success or error
        """
        self.cursor.execute(ProductRowGateway.__DELETE_PRODUCT_SQL,(product_id,product_name,brand_id))
        if self.cursor.rowcount==0:return ['error: no product has been deleted']
        elif self.cursor.rowcount==1: return [f'{self.cursor.rowcount} product has been deleted']
        else: return [f'{self.cursor.rowcount} products have been deleted']
    def __it_is_number(self,value:str,name:str)->Union[None,list]:
        """
        private Method check if the value is decimal number
        :param value: str - value that would be tested
        :param name: str - name of the variable that is tested
        :return: list[str] if found some problem in value else None
        """
        try:
            float(value)
            if float(value)<=0:raise ZeroDivisionError()
        except ZeroDivisionError:
            return [f'error: {name} is lower or equal zerorror: {name} is lower or equal zero'] 
        except:
            return [f'error: {name} is not a number']