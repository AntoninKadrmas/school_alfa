import unittest, json, sys, os, copy
sys.path.append('./')
from src.package.loadConfig import LoadConfig
class LoadConfigTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.previous_config=None
        with open('./config/config.json','r') as reader:    
            self.previous_config = json.load(reader)
        
    def test_basic_setup(self):
        load = LoadConfig()
        self.assertEqual(load.from_file(),"./data/forEncode/example.txt")
        self.assertEqual(load.to_file(),"./data/forDecode/example.txt")
        self.assertTrue(load.overwrite())

    def test_change_setup(self):
        self.save_json(self.change_config("./data/forDecode/example.txt","./data/forEncode/example.txt"))
        load = LoadConfig()
        self.assertEqual(load.to_file(),"./data/forEncode/example.txt")
        self.assertEqual(load.from_file(),"./data/forDecode/example.txt")
        self.save_json(self.previous_config)

    def test_error_json_file_problems(self):
        os.remove('./config/config.json')
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'config/config.json file does not exists please recreate it using readme.txt')

        self.save_json({"error":20})       
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'config params is incorrect or missing please recreate it using readme.txt')

        with open('./config/config.json','w')as writer:
            writer.write('error');       
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'text in config/config.json is not json please recreate it using readme.txt')
        self.save_json(self.previous_config)

        json_object = self.change_config()
        del json_object['config']['fromFile']
        self.save_json(json_object)
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'fromFile params is incorrect or missing please recreate it using readme.txt')
        self.save_json(self.previous_config)

        json_object = self.change_config()
        del json_object['config']['toFile']
        self.save_json(json_object)
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'toFile params is incorrect or missing please recreate it using readme.txt')
        self.save_json(self.previous_config)

        json_object = self.change_config()
        del json_object['config']['overwrite']
        self.save_json(json_object)
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'overwrite params is incorrect or missing please recreate it using readme.txt')
        self.save_json(self.previous_config)

    def test_incorrect_json_values(self):
        self.save_json(self.change_config(fromFile='/error/error.txt'))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'fromFile path attribute is not set up or incorrect \n!!please check fromFile value in config.json!!')
        self.save_json(self.previous_config)

        self.save_json(self.change_config(overwrite='ahoj'))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'overwrite attribute is not set up or incorrect \n!!please check overwrite value in config.json!!')
        self.save_json(self.previous_config)

        self.save_json(self.change_config(overwrite=False))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'overwrite attribute is not set up or incorrect because toFile path file exists\n!!please check overwrite value in config.json!!')
        self.save_json(self.previous_config)

        self.save_json(self.change_config(overwrite=False,toFile='./data/correct.txt'))
        load = LoadConfig()
        self.save_json(self.previous_config)

    
    def change_config(self,fromFile=None,toFile=None,overwrite=None):
        json_object = copy.deepcopy(self.previous_config)
        if fromFile!=None:json_object['config']['fromFile'] = fromFile
        if toFile!=None:json_object['config']['toFile'] = toFile
        if overwrite!=None:json_object['config']['overwrite'] = overwrite
        return json_object

    def save_json(self,json_data):
        with open('./config/config.json','w') as writer:
            json.dump(json_data,writer)
        