from package.database.connection import Connection
from package.database.myEnum import UserType
from package.database.userLogin import User,UserSingleton
from typing import Generator
class View():
    __SELECT_PRODUCT_AND_BRAND_SQL = 'select * from view_product_brand'
    __SELECT_VIEW_ORDER_SQL = 'select * from view_order_products where User_idUser LIKE %s'
    __SELECT_FINAL_PRICE_SQL = 'select * from view_final_price where User_idUser LIKE %s and idOrder LIKE %s'
    def __init__(self,user_type:UserType=None) -> None:
        """
        constructor make connection to db
        :param user_type: type of privileges for database connection
        """
        self.user:User = UserSingleton.getUser()
        self.connection = Connection.getConnection(user_type)
        self.cursor = self.connection.cursor()
    def product_and_brand(self)->Generator:
        """
        public Method that return join of product and brand table
        :return: yield of serialized data brands and their products
        """
        to_string = ['product id','product name','weight in KG','price','brand name','residence']
        self.cursor.execute(View.__SELECT_PRODUCT_AND_BRAND_SQL)
        yield [True] + to_string
        for results in self.cursor:
            yield [False] + list(results)
    def order_and_products(self)->Generator:
        """
        public Method that return join of product and order table
        :return: yield of serialized data orders and theirs products
        """
        to_string = ['order id','create date','paid','send','final price','product name','brand name','price','amount']
        price=[]
        for result in self.order_final_price():
            price.append(result)
        print(self.user.id)
        self.cursor.execute(View.__SELECT_VIEW_ORDER_SQL,(self.user.id,))
        previous = None
        count=0
        for results in self.cursor:
            if previous!= results[0]:#return new order
                yield [True]+to_string[:5]
                yield [False] + list(results[:2]+(int(results[2])==1,int(results[3])==1)) + [price[count]]
                yield [True] + list(to_string[5:])
                count+=1
                previous=results[0]
            yield [False]+list(results[4:8])#return product
        if count==0: return ['error: no order found']
    def order_final_price(self,order:str='%')->Generator:
        """
        public Method that return counted price for specific order
        :param order: string that specify order number
        :return: yield of float number as price or error
        """
        try:
            self.cursor.execute(View.__SELECT_FINAL_PRICE_SQL,(str(self.user.id),order))
        except :
            yield 'error: order id is incorrect'
        else:
            for result in self.cursor:
                yield float(result[0])
