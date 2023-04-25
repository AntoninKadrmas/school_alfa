import unittest, json, sys
sys.path.append('../src')
from package.command import Command
class CommandTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        with open('../config/config.json','r') as reader:    
            self.previous_config = json.load(reader)
        with open('./data/testConfig.json','r') as reader:    
            self.new_test_conf = json.load(reader)
        with open('../config/dictionary.json','r') as reader:    
            self.previous_dictionary = json.load(reader)
        with open('./data/testDictionary.json','r') as reader:    
            self.new_test_dict = json.load(reader)

    def test_run_ping(self):
        self._rewrite_config(self.new_test_conf)
        command = Command()
        server_name=self.new_test_conf['server']['name']
        self.assertEqual(command.run('TRANSLATEPING"value"'),f'TRANSLATEPONG"{server_name}"')

    def test_error_input_run(self):
        command = Command()
        self.assertIsNone(command.run(''))
        self.assertIsNone(command.run('TRANSLATELOCL'))

    def test_recreate_config(self):
        self._rewrite_config(self.previous_config)
        self._rewrite_dictionary(self.previous_dictionary)
        with open('../config/config.json','r') as reader:    
            actual_conf = json.load(reader)
        self._rewrite_config(self.previous_config)
        with open('../config/dictionary.json','r') as reader:    
            actual_dict = json.load(reader)
        self.assertEqual(actual_conf,self.previous_config)
        self.assertEqual(actual_dict,self.previous_dictionary)

    def _rewrite_config(self,config):
        with open('../config/config.json','w') as writer:    
            json.dump(config,writer)

    def _rewrite_dictionary(self,dictionary):
        with open('../config/dictionary.json','w') as writer:    
            json.dump(dictionary,writer)
