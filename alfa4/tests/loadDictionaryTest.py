import unittest, json, sys, os, copy
sys.path.append('../')
from src.package.loadDictionary import LoadDictionarySingleton ,LoadDictionary
class LoadDictionaryTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.previous_dictionary=None
        with open('../config/dictionary.json','r') as reader:    
            self.previous_dictionary = json.load(reader)
        with open('./data/testDictionary.json','r') as reader:    
            self.new_test = json.load(reader)

    def _rewrite_dictionary(self,dictionary):
        with open('../config/dictionary.json','w') as writer:    
            json.dump(dictionary,writer)

    def test_basic_setup(self):
        self._rewrite_dictionary(self.new_test)
        dict = LoadDictionary()
        self.assertEqual(len(dict.dictionary()),5)
        for pairs in dict.dictionary():
            self.assertEqual(len(pairs),2)
            self.assertNotEqual(pairs[0],'')
            self.assertNotEqual(pairs[1],'')
    def test_error_json_file_problems(self):
        os.remove('../config/dictionary.json')
        with self.assertRaises(Exception) as error:
            LoadDictionary()
        self.assertEqual(str(error.exception),'config/dictionary.json file does not exists please recreate it using readme.txt')

        with open('../config/dictionary.json','w')as writer:
            writer.write('error');       
        with self.assertRaises(Exception) as error:
            LoadDictionary()
        self.assertEqual(str(error.exception),'text in config/dictionary.json is not json please recreate it using readme.txt')
        
        self._rewrite_dictionary({});  
        with self.assertRaises(Exception) as error:
            LoadDictionary()
        self.assertEqual(str(error.exception),'config params is incorrect or missing please recreate it using readme.txt')

        self._rewrite_dictionary({"dictionary":[[],[],[],[]]});  
        with self.assertRaises(Exception) as error:
            LoadDictionary()
        self.assertEqual(str(error.exception),'number of translated words has to be exactly 5 you have 4')

        self._rewrite_dictionary({"dictionary":[[],[],[],[],[],[]]});  
        with self.assertRaises(Exception) as error:
            LoadDictionary()
        self.assertEqual(str(error.exception),'number of translated words has to be exactly 5 you have 6')

        new_dict = copy.deepcopy(self.new_test)
        del new_dict['dictionary'][2][0]
        self._rewrite_dictionary(new_dict)
        with self.assertRaises(Exception) as error:
            LoadDictionary()
        self.assertEqual(str(error.exception),'3. element in dictionary field have 1 and expected are just 2 one english one czech')
    
        new_dict = copy.deepcopy(self.new_test)
        new_dict['dictionary'][4].append('error')
        self._rewrite_dictionary(new_dict)
        with self.assertRaises(Exception) as error:
            LoadDictionary()
        self.assertEqual(str(error.exception),'5. element in dictionary field have 3 and expected are just 2 one english one czech')
        
    def test_recreate_config(self):
        self._rewrite_dictionary(self.previous_dictionary)
        with open('../config/dictionary.json','r') as reader:    
            actual = json.load(reader)
        self.assertEqual(actual,self.previous_dictionary)
class LoadDictionarySingletonTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_singleton_cooperation(self):
        first =LoadDictionarySingleton.getDictionary()
        second =LoadDictionarySingleton.getDictionary()
        self.assertEqual(first,second)
        with self.assertRaises(Exception) as error:
            LoadDictionarySingleton()
        self.assertEqual(str(error.exception),'load dictionary is exists')  
