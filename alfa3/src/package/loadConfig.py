import json, os, re
from typing import Union

class LoadConfig():
    """
    Class that manage config.json file and test all parameters if they are valid.
    """
    def __init__(self) -> None:
        """
        Constructor that load and test all parameters in config.js file 
        """
        self.json_object = ''
        if not os.path.exists('.././config/config.json'):
            raise Exception('config/config.json file does not exists please recreate it using readme.txt')
        error=False
        try:
            with open('.././config/config.json','r') as reader:
                self.json_object = json.load(reader)
        except:error=True
        finally:
            if error:raise Exception('text in config/config.json is not json please recreate it using readme.txt')
        self._check_json()
        ip =  self.json_object['db_config']['address'] if not re.fullmatch(r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}',self.json_object['db_config']['address']) else 'localhost'
        if ip!='localhost': raise Exception('Error in address parameter look at the readme documentations')
        if self.json_object['db_config']['database']=='':raise Exception('Error in database name parameter is empty')
    def _check_json(self) -> None:
        """
        private Method that check if all parameters in json file are correctly spelled and exists.
        """
        try:
            self.json_object['db_config']
        except:
            raise Exception('config params is incorrect or missing please recreate it using readme.txt')
        important_params = ["address","database"]
        for param in important_params:
            try:
                self.json_object['db_config'][param]
            except:
                raise Exception(f'{param} params is incorrect or missing please recreate it using readme.txt')
    def address(self) -> str:
        """
        public Method that return ip address.
        :return: return ip address attribute
        """
        return self.json_object['db_config']['address']
    def database(self) -> str:
        """
        public Method that return database name
        :return: return database name attribute
        """
        return self.json_object['db_config']['database']
    def import_path(self)->Union[str,list]:
        """
        public Method that return and check import path
        :return: return import path
        """
        error=False
        try:self.json_object['import']
        except:error=True
        finally:
            if error:return ['error: import param is incorrect or missing please recreate it using readme.txt']
        try:path = self.json_object['import']['path']
        except:error=True
        finally:
            if error:return['error: import path param is incorrect or missing please recreate it using readme.txt']
        if '.csv' not in self.json_object['import']['path']:return['error: file does not have .csv ending']
        if not os.path.exists(path):return['error: file does not exists']
        return path
    def delimiter(self)->str:
        """
        public Method that return delimiter if exists or ;
        :return: return delimiter
        """
        try:self.json_object['import']
        except:return ';'
        try:delimiter = self.json_object['import']['delimiter']
        except:return ';'
        return delimiter if len(delimiter)==1 else ';'

class LoadConfigSingleton():
    """
    Config singleton that make sure that only one copy of config exists
    """
    __confInstance:LoadConfig = None
    @staticmethod
    def getConfig():
        """
        static Method that create new config if no config exists or return existing one.
        """
        if LoadConfigSingleton.__confInstance==None:
            LoadConfigSingleton()
        return LoadConfigSingleton.__confInstance
    def __init__(self) -> None:
        """
        Constructor that made one config instance 
        """
        if LoadConfigSingleton.__confInstance!=None: raise Exception('load config is exists')
        LoadConfigSingleton.__confInstance = LoadConfig()
