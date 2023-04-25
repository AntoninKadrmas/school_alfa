from package.database.myEnum import OrderState,UserType
from package.database.order import orderRowGateway,orderTableGateway
from package.database.product_order import productOrderRowGateway
from package.database.user import userRowGateway,userTableGateway
from package.database.view.view import View
from package.database.userLogin import UserSingleton, User
from typing import Generator
class ApplicationUser():
    """
    Class ApllicationUser take care of the user actions.
    """
    def __init__(self) -> None:
        """
        Constructor of application user creates command dictionary.
        """
        self.user:User = UserSingleton.getUser()
        self.order:dict=dict() 
        self.options = {
            "View my account":self.__view_account,
            "Create order":self.__create_order,
            "View orders":View().order_and_products,
            "Delete order":self.__delete_order,
            "Paid order":self.__paid_order,
            "View products":View().product_and_brand,
            "Add product to bin":self.__add_product,
            "Remove product from bin":self.__remove_product,
            "View product in bin":self.__view_product,
            "Add cash":self.__add_cash,
            "Exit":self.__exit
        }
    def __create_order(self)->list:
        """
        private Method that create with all her products. In dictionary of products have to be one or more products.
        :return: return result of creating success or error
        """
        if len(self.order.keys())==0:return ['error: add some product into bin to create order']
        orderRowGateway.OrderRowGateway().insert(self.user.id)
        for order in orderTableGateway.OrderTableGateway().select(user_id=self.user.id):
            order_id = order[0]
            break;
        for id,amount in self.order.items():
            result = productOrderRowGateway.ProductOrderRowGateway().insert(str(order_id),str(id),str(amount))
            if 'error:' in str(result[0]): return[f'error: in product id => {id}, check your bin']
        self.order=dict()
        return ['order create correctly']
    def __delete_order(self)->list:
        """
        private Method that delete order by id user input. Can not delete paid orders.
        :return: return result of deleting success or error
        """
        while True:
            try:
                choseOrder = int(input('Chose order id to delete:'))
                if choseOrder<=0:raise Exception
            except Exception:
                return ['error: order id is lower or equal 0']
            except:
                return ['error: in order id wrong datatype']  
            else:
                for result in orderTableGateway.OrderTableGateway().select(order_id=str(choseOrder),user_id=str(self.user.id)):
                    if int(result[3])==OrderState.SEND_PAID.value:return['error: paid orders can not be deleted']
                return orderRowGateway.OrderRowGateway().delete(order_id=str(choseOrder),user_id=str(self.user.id))
    def __add_product(self)->list:
        """
        private Method that add id product and his amount into dictionary user input.
        If id in dictionary exist just increase it's amount.
        :return: return result of adding success or error
        """
        try:
            choseProduct = int(input('Chose product id to add:'))
            if choseProduct<=0:raise Exception
        except Exception:
            return ['error: product id is lower or equal 0']
        except:
            return ['error: in product id wrong datatype']
        else:     
            try:
                choseAmount = int(input('Chose amount:'))
                if choseAmount<=0:raise Exception
            except Exception:
                return ['error: amount is lower or equal 0']
            except:
                return ['error: in product wrong datatype']  
            else:
                if choseProduct in self.order.keys():self.order[choseProduct] += choseAmount
                else:self.order[choseProduct] = choseAmount
                return ['product added']
    def __remove_product(self)->list:
        """
        private Method that remove products from dictionary by id user input
        :return: return result of removing success or error
        """
        try:
            choseProduct = int(input('Chose product id to add:'))
            if choseProduct<=0:raise Exception
        except Exception:
            return ['error: product id is lower or equal 0']
        except:
            return ['error: in product id wrong datatype']   
        else:     
            if choseProduct in self.order.keys():del self.order[choseProduct]
            else:return ['error: product does not exist in bin']
            return ['product removed']
    def __view_product(self)->Generator:
        """
        private Method that show what products are now in the dictionary.
        :return: return id of product and it's amount serialized for table
        """
        yield [True,'id','amount']
        for key,value in self.order.items():
            yield [False,key,value]
    def __add_cash(self)->list:
        """
        private Method that add more cash to user account.
        :return: return result of adding success or error
        """
        try:
            cashInput = float(input('Add cash:'))
            if cashInput<=0:raise Exception
        except Exception:
            return ['error: cash is lower or equal 0']
        except:
            return ['error: in cash is used wrong datatype']   
        else:
            new_cash = float(self.user.cash)+cashInput
            result = userRowGateway.UserRowGateway().update(new_cash=str(new_cash),user_id=str(self.user.id))
            if 'error:' in str(result[0]):return result
            self.user.cash =new_cash
            return['cash added to your account']
    def __paid_order(self)->list:
        """
        private Method that set status of user inputted order to true and remove amount of money corresponding with price of inputted order.
        :return: return result of transferring money and changing paid status success or error
        """
        try:
            choseOrder = int(input('Chose order id to paid:'))
            if choseOrder<=0:raise Exception
        except Exception:
            return ['error: order id is lower or equal 0']
        except:
            return ['error: in order id wrong datatype']
        else:
            for price in View().order_final_price(str(choseOrder)):
                product_price = price
                if str(product_price).split()[0]=='error:':return [product_price]
                break
            else:return [f'error: order with id {choseOrder} does not exists']
            if float(product_price)>float(self.user.cash): return['error: dont have enough cash']
            new_cash = float(self.user.cash)-float(product_price)
            result = userRowGateway.UserRowGateway().update(new_cash=str(new_cash),user_id=str(self.user.id))#decrease user cash balance
            if str(result[0]).split()[0]=='error:': return result
            for result in userTableGateway.UserTableGateway().select(nick_name=UserType.ADMIN.value):#get admin previous cash
                old_cash = float(result[3])
            result = userRowGateway.UserRowGateway().update(new_cash=str(old_cash+product_price),nick_name=UserType.ADMIN.value)#increase admin cash balance
            if 'error:' in str(result[0]): return result
            result = orderRowGateway.OrderRowGateway().update(new_paid=str(OrderState.SEND_PAID.value),user_id=str(self.user.id),order_id=str(choseOrder))#update order status
            if 'error:' in str(result[0]): return result
            self.user.cash = new_cash
            return ['paid correctly']
    def __view_account(self)->Generator:
        """
        private Method that show what account information's
        :return: return user information serialized for table
        """
        yield [True,'user id','nickname','type','cash'] 
        yield [False,self.user.id,self.user.name,self.user.type,self.user.cash]
    def __exit(self):
        """
        private Method that end program
        """
        exit()