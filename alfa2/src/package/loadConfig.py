import json
import os
from package.myEnum import Mode

class LoadConfig():
    """
    Class that manage config.json file and test all parameters if they are valid.
    """
    def __init__(self) -> None:
        """
        Constructor that load and test all parameters in config.js file 
        """
        self.json_object = ''
        if not os.path.exists('././config/config.json'):
            raise Exception('config/config.json file does not exists please recreate it using readme.txt')
        try:
            with open('././config/config.json','r') as reader:
                self.json_object = json.load(reader)
        except:
            raise Exception('text in config/config.json is not json please recreate it using readme.txt')
        self._check_json()
        if not os.path.exists(self.json_object['config']['fromFile']):
            raise Exception('fromFile path attribute is not set up or incorrect \n!!please check fromFile value in config.json!!')
        if self.json_object['config']['overwrite']!=True and self.json_object['config']['overwrite']!=False:
            raise Exception('overwrite attribute is not set up or incorrect \n!!please check overwrite value in config.json!!') 
        if not os.path.isdir('/'.join(self.json_object['config']['toFile'].split('/')[0:len(self.json_object['config']['toFile'].split('/'))-1])):
            raise Exception('toFile path attribute is not set up or incorrect \n!!please check toFile value in config.json!!')
        elif os.path.exists(self.json_object['config']['toFile']) and not self.json_object['config']['overwrite']:
            raise Exception('overwrite attribute is not set up or incorrect because toFile path file exists\n!!please check overwrite value in config.json!!')

    def _check_json(self) -> None:
        """
        private Method that check if all parameters in json file are correctly spelled and exists.
        """
        try:
            self.json_object['config']
        except:
            raise Exception('config params is incorrect or missing please recreate it using readme.txt')
        important_params = ["toFile","fromFile","overwrite"]
        for param in important_params:
            try:
                self.json_object['config'][param]
            except:
                raise Exception(f'{param} params is incorrect or missing please recreate it using readme.txt')

    def from_file(self) -> str:
        """
        public Method that return from file path attribute.
        :return: return from file path attribute
        """
        return './'+self.json_object['config']['fromFile']
    def to_file(self) -> str:
        """
        public Method that return to file path attribute.
        :return: return to file path attribute
        """
        return './'+self.json_object['config']['toFile']
    def overwrite(self) -> bool:
        """
        public Method that return overwrite attribute.
        :return: return overwrite attribute
        """
        return self.json_object['config']['overwrite']