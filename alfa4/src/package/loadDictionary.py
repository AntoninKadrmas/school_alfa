import json, os, re

class LoadDictionary():
    """
    Class that manage dictionary.json file and test all parameters if they are valid.
    """
    def __init__(self) -> None:
        """
        Constructor that load and test all parameters from dictionary.json file 
        """
        self.json_object = ''
        if not os.path.exists('.././config/dictionary.json'):
            raise Exception('config/dictionary.json file does not exists please recreate it using readme.txt')
        error=False
        try:
            with open('.././config/dictionary.json','r') as reader:
                self.json_object = json.load(reader)
        except:error=True
        finally:
            if error:raise Exception('text in config/dictionary.json is not json please recreate it using readme.txt')
        self._check_json()
    def _check_json(self) -> None:
        """
        private Method that check if all parameters in json file are correctly spelled and exists.
        """
        try:
            self.json_object['dictionary']
        except:
            raise Exception('config params is incorrect or missing please recreate it using readme.txt')
        length = len(self.json_object['dictionary'])
        if length!=5:raise Exception(f'number of translated words has to be exactly 5 you have {length}')
        for index,element in enumerate(self.json_object['dictionary']):
            if len(element)!=2:raise Exception(f'{index+1}. element in dictionary field have {len(element)} and expected are just 2 one english one czech')
    def dictionary(self) -> list:
        """
        public Method that return dictionary.
        :return: return dictionary attribute
        """
        return self.json_object['dictionary']

class LoadDictionarySingleton():
    """
    Dictionary singleton that make sure that only one copy of dictionary exists
    """
    __confInstance:LoadDictionary = None
    @staticmethod
    def getDictionary():
        """
        static Method that create new dictionary if no dictionary exists or return existing one.
        """
        if LoadDictionarySingleton.__confInstance==None:
            LoadDictionarySingleton()
        return LoadDictionarySingleton.__confInstance
    def __init__(self) -> None:
        """
        Constructor that made one dictionary instance 
        """
        if LoadDictionarySingleton.__confInstance!=None: raise Exception('load dictionary is exists')
        LoadDictionarySingleton.__confInstance = LoadDictionary()
