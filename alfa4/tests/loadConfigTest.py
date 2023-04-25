import unittest, json, sys, os, copy
sys.path.append('../')
from src.package.loadConfig import LoadConfigSingleton ,LoadConfig
class LoadConfigTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.previous_config=None
        with open('../config/config.json','r') as reader:    
            self.previous_config = json.load(reader)
        with open('./data/testConfig.json','r') as reader:    
            self.new_test = json.load(reader)

    def _rewrite_config(self,config):
        with open('../config/config.json','w') as writer:    
            json.dump(config,writer)

    def test_basic_setup(self):
        self._rewrite_config(self.new_test)
        load = LoadConfig()
        self.assertEqual(load.address(),'localhost')
        self.assertEqual(load.port(),65530)
        self.assertEqual(load.connection_timeout(),1)
        self.assertEqual(load.response_timeout(),2)
        self.assertEqual(load.client_timeout(),4)
        self.assertEqual(load.name(),"server name")
        self.assertEqual(load.error(),"server error")
        self.assertEqual(len(load.address_range()),2)
        self.assertEqual(len(load.address_range()[0]),1)
        self.assertEqual(load.address_range()[0],["localhost"])
        self.assertEqual(len(load.address_range()[1]),2)
        self.assertEqual(load.address_range()[1],["192.168.0.1","192.168.0.5"])
        self.assertEqual(len(load.port_range()),2)
        self.assertEqual(len(load.port_range()[0]),2)
        self.assertEqual(load.port_range()[0],[8080,8085])
        self.assertEqual(load.port_range()[1],[65535])

    def test_error_json_file_problems(self):
        os.remove('../config/config.json')
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'config/config.json file does not exists please recreate it using readme.txt')

        with open('../config/config.json','w')as writer:
            writer.write('error');       
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'text in config/config.json is not json please recreate it using readme.txt')
        
        new_json = copy.deepcopy(self.new_test)
        del new_json['server']
        self._rewrite_config(new_json)
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'server params is incorrect or missing please recreate it using readme.txt')
        
        for param in ["address","port","name","error","connection_timeout","response_timeout","client_timeout"]:
            new_json = copy.deepcopy(self.new_test)
            del new_json['server'][param]
            self._rewrite_config(new_json)
            with self.assertRaises(Exception) as error:
                LoadConfig()
            self.assertEqual(str(error.exception),f'{param} params is incorrect or missing please recreate it using readme.txt')
        
        new_json = copy.deepcopy(self.new_test)
        del new_json['scan']
        self._rewrite_config(new_json)
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'scan params is incorrect or missing please recreate it using readme.txt')

        for param in ["address","port"]:
            new_json = copy.deepcopy(self.new_test)
            del new_json['scan'][param]
            self._rewrite_config(new_json)
            with self.assertRaises(Exception) as error:
                LoadConfig()
            self.assertEqual(str(error.exception),f'{param} params is incorrect or missing please recreate it using readme.txt')
    
    def test_correction_attributes_server_part(self):
        self._rewrite_config(self._change_config('server','address',"250"))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'Error in address parameter look at the readme documentations')
        
        self._rewrite_config(self._change_config('server','port',"error"))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'port parameter in config.json has to be integer')

        self._rewrite_config(self._change_config('server','port',-50))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'port parameter in config.json can\'t be lower then zero')

        for timeout in ['response_timeout','connection_timeout','client_timeout']:
            self._rewrite_config(self._change_config('server',timeout,"error"))
            with self.assertRaises(Exception) as error:
                LoadConfig()
            self.assertEqual(str(error.exception),f'{timeout} parameter in config.json has to be decimal')
            self._rewrite_config(self._change_config('server',timeout,0))
            with self.assertRaises(Exception) as error:
                LoadConfig()
            self.assertEqual(str(error.exception),f"{timeout} parameter in config.json can't be lower then zero")

        self._rewrite_config(self._change_config('server',"name",""))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),"name parameter of the server can't be empty")

        self._rewrite_config(self._change_config('server',"error",""))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),"error parameter of the server can't be empty")

    def test_correction_attributes_scan_part_address_range(self):
        self._rewrite_config(self._change_config('scan',"address",[]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'in the scan address missing address/es to scan edit it by using readme.txt')
        
        self._rewrite_config(self._change_config('scan',"address",[[]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. have incorrect number of ip address actual 0 expected 1 or 2 edit it by using readme.txt')
        
        self._rewrite_config(self._change_config('scan',"address",[['','','']]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. have incorrect number of ip address actual 3 expected 1 or 2 edit it by using readme.txt')

        self._rewrite_config(self._change_config('scan',"address",[["192.168"]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. field have ip address that is incorrect in each position of four can be number from 0 to 255')

        self._rewrite_config(self._change_config('scan',"address",[["192.168.1.1","192.168.0.1"]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. field have incorrect ip address range left side is bigger then right side')

    def test_correction_attributes_scan_part_port_range(self):
        self._rewrite_config(self._change_config('scan',"port",[]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'in the scan port missing port/s to scan edit it by using readme.txt')
        
        self._rewrite_config(self._change_config('scan',"port",[[]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. have incorrect number of ports actual 0 expected 1 or 2 edit it by using readme.txt')
        
        self._rewrite_config(self._change_config('scan',"port",[['','','']]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. have incorrect number of ports actual 3 expected 1 or 2 edit it by using readme.txt')

        self._rewrite_config(self._change_config('scan',"port",[["error"]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. field have to contains just integer values edit it by using readme.txt')

        self._rewrite_config(self._change_config('scan',"port",[[-50]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. field have first port below the zero edit it by using readme.txt')

        self._rewrite_config(self._change_config('scan',"port",[[150,-50]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. field have second port below the zero edit it by using readme.txt')

        self._rewrite_config(self._change_config('scan',"port",[[1050,880]]))
        with self.assertRaises(Exception) as error:
            LoadConfig()
        self.assertEqual(str(error.exception),'1. field have left port bigger then right incorrect range edit it by using readme.txt')
    
    def test_recreate_config(self):
        self._rewrite_config(self.previous_config)
        with open('../config/config.json','r') as reader:    
            actual = json.load(reader)
        self.assertEqual(actual,self.previous_config)

    def _change_config(self,first_parameter:str,second_parameter:str,new_value:any):
        json_object = copy.deepcopy(self.new_test)
        json_object[first_parameter][second_parameter] = new_value
        return json_object
class LoadConfigSingletonTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_singleton_cooperation(self):
        first =LoadConfigSingleton.getConfig()
        second =LoadConfigSingleton.getConfig()
        self.assertEqual(first,second)
        with self.assertRaises(Exception) as error:
            LoadConfigSingleton()
        self.assertEqual(str(error.exception),'load config is exists')  