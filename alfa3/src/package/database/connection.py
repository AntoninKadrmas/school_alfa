import mysql.connector
from package.database.myEnum import UserType
from package.loadConfig import LoadConfigSingleton

class Connection():
    """
    Connection singleton that make sure that only one copy of db connection exists
    """
    __dbInstance = None
    @staticmethod
    def getConnection(user_type:UserType=None):
        """
        static Method that create new db connection if no connection exists or return existing one.
        :param user_type: attribute that decide in what privileges mode is db connection created 
        """
        if Connection.__dbInstance==None:
            if user_type==None:raise Exception('When creating first instance user type can not be null')
            Connection(user_type)
        return Connection.__dbInstance
    def __init__(self,user_type:UserType) -> None:
        """
        Constructor that made one database connection 
        :param user_type: attribute that decide in what privileges mode is db connection created 
        """
        if Connection.__dbInstance!=None: raise Exception('db connection is exists')
        Connection.__dbInstance = self.__connection(user_type)

    @staticmethod
    def close() -> None:
        """
        static Method for close connection and clean dbInstance
        """
        Connection.__dbInstance.close()
        Connection.__dbInstance =None
    def __connection(self,type:UserType):
        """
        private Method for create connection into database
        :param type: type of user privileges 
        :return: return connection to mysql database
        """
        config= LoadConfigSingleton.getConfig()
        try:
            connection =  mysql.connector.connect(
                host=config.address(),
                database=config.database(),
                user="public_user",
                password="password",
            ) if type == UserType.USER else\
            mysql.connector.connect(
                host=config.address(),
                database=config.database(),
                user="admin",
                password="password",
            )
        except Exception as e:print(e)
        else:
            return connection
        raise Exception('Error in database connection check database name and ip address in config.json in config file')