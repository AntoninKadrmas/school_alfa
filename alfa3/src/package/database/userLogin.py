class User():
    """
    User object that handle all important information about user
    """
    def __init__(self,user:tuple) -> None:
        self.id = user[0]
        self.type = user[1]
        self.name = user[2]
        self.cash = user[3]
        
class UserSingleton():
    """
    User singleton that make sure that only one copy of user exists
    """
    __userInstance:User = None
    @staticmethod
    def getUser(user:tuple=None):
        """
        static Method that return create new user if no user exists or return existing one.
        """
        if UserSingleton.__userInstance==None:
            if user==None:raise Exception('When creating first instance user type can not be null')
            UserSingleton(user)
        return UserSingleton.__userInstance
    def __init__(self,user:tuple) -> None:
        """
        Constructor that made one user instance 
        """
        if UserSingleton.__userInstance!=None: raise Exception('User exists')
        UserSingleton.__userInstance = User(user)