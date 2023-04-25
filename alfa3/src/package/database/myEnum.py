from enum import Enum

class UserType(Enum):
    """
        Enum for different privilege type connections.
    """
    USER='user'
    ADMIN='admin'

class CostumerType(Enum):
    """
        Enum for different user types.
    """
    CUSTOMER='customer'
    EMPLOYEE='emplo'
    
class OrderState(Enum):
    """
        Enum for different status of paid and send.
    """
    SEND_PAID=1
    NOT_SEND_PAID=0
