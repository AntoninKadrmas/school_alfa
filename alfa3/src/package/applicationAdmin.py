from package.database.myEnum import OrderState
from package.database.user import userRowGateway,userTableGateway
from package.database.brand import brandRowGateway,brandTableGateway
from package.database.product import productRowGateway,productTableGateway
from package.database.order import orderRowGateway,orderTableGateway
from package.loadConfig import LoadConfigSingleton
from typing import Generator
import csv

class ApplicationAdmin():
    """
    Class ApllicationUser take care of the admin actions.
    """
    def __init__(self) -> None:
        """
        Constructor of application admin creates command dictionary.
        """
        self.options = {
            "Create user":userRowGateway.UserRowGateway().execute_insert,
            "View users":userTableGateway.UserTableGateway().execute_select,
            "Delete user":userRowGateway.UserRowGateway().execute_delete,
            "Create product":productRowGateway.ProductRowGateway().execute_insert,
            "View products":productTableGateway.ProductTableGateway().execute_select,
            "Delete product":productRowGateway.ProductRowGateway().execute_delete,
            "Create brand":brandRowGateway.BrandRowGateway().execute_insert,
            "View brands":brandTableGateway.BrandTableGateway().execute_select,
            "Delete brand":brandRowGateway.BrandRowGateway().execute_delete,
            "View paid orders":self.__view_paid_orders,
            "Send paid order":self.__send_paid_order,
            "Import data into brand":self.__import_brand,
            "Import data into products":self.__import_products,
            "Exit":self.__exit
        }
    def __view_paid_orders(self)->Generator:
        """
        private Method that show orders which paid status is true
        :return: return all orders that are paid serialized for table
        """
        to_string =['order id','create date','user id','paid','send']
        yield [True]+to_string
        for results in orderTableGateway.OrderTableGateway().select(paid=OrderState.SEND_PAID.value):
            yield [False]+list(results)
    def __send_paid_order(self)-> list:
        """
        private Method that updates paid order status of send to true
        :return: return result of updating success or error
        """
        try:
            choseOrder = int(input('Chose order id to send:'))
            if choseOrder<=0:raise Exception
        except Exception: return ['error: order id is lower or equal 0']
        except: return ['error: in order id wrong datatype']
        else:
            for result in orderTableGateway.OrderTableGateway().select(order_id=choseOrder):
                if int(result[3])==OrderState.NOT_SEND_PAID.value:return['error: not paid orders can not be send']
            result = orderRowGateway.OrderRowGateway().update(new_send=str(OrderState.SEND_PAID.value),order_id=str(choseOrder))
            if str(result[0]).split()[0]=='error:': return result
            return ['send correctly']
    def __import_brand(self)->list:
        """
        private Method that take care of importing into brand table.
        :return: return result of importing success or error
        """
        config = LoadConfigSingleton.getConfig()#get config
        if type(config.import_path())==list:return config.import_path()
        with open(config.import_path(),'r') as reader:
            error=False
            try:result = csv.reader(reader,delimiter=config.delimiter())#read data as csv
            except:error=True
            finally:
                if error:return ['error: some problem with converting to csv']
            for index,line in enumerate(result):
                error=False
                for word in line:#check if there is no data that are empty
                    if word.strip()=='':return[f'error: on line {index+1} you have empty value']
                try:result = brandRowGateway.BrandRowGateway().insert(*line)#insert into brand
                except:error=True
                else:
                    if 'error' in result[0]: return [f'{result[0]} on line {index+1}']#error during inserting
                finally:
                    if error: return [f'error: bad amount of arguments in line {index+1} number of arguments actual {len(line)} expected 2']       
        return ['all data correctly imported']
    def __import_products(self)->list:
        """
        private Method that take care of importing into product table.
        :return: return result of importing success or error
        """
        config = LoadConfigSingleton.getConfig()#get config
        if type(config.import_path())==list:return config.import_path()
        with open(config.import_path(),'r') as reader:
            error=False
            try:result = csv.reader(reader,delimiter=config.delimiter())#read data as csv
            except:error=True
            finally:
                if error:return ['error: some problem with converting to csv']
            for index,line in enumerate(result):
                for word in line:#check if there is no data that are empty
                    if word.strip()=='': return[f'error: on line {index+1} you have empty value']
                try: id = int(line[3].strip())
                except:
                    id = None
                    for result in brandTableGateway.BrandTableGateway().select(brand_name=line[3].strip()):#found id of brand by name
                       id = result[0]
                       break
                    else: return[f'error: brand with name {line[3]} on line {index+1} does not exists']
                finally:
                    try: 
                        line[3]=id#update id so now it is totally number
                        result = productRowGateway.ProductRowGateway().insert(*line)#insert product
                    except:error=True
                    else:
                        if 'error' in result[0]: return [f'{result[0]} on line {index+1}']#some error while inserting
                    finally:
                        if error: return [f'error: bad amount of arguments in line {index+1} number of arguments actual {len(line)} expected 4'] 
        return ['all data correctly imported']
    def __exit(self):
        """
        private Method that end program
        """
        exit()