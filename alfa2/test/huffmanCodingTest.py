import unittest, os, json, copy, time,sys
sys.path.append('./')
from src.package.huffmanCoding import HuffmanCoding

class HuffmanCodingTest(unittest.TestCase):
    
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.previous_config=None
        with open('./config/config.json','r') as reader:    
            self.previous_config = json.load(reader)
    def test_encode_decode(self):
        from_path = "./data/forEncode/example.txt"
        new_from_path = './data/forEncode/temp_example.txt'
        to_path = "./data/forDecode/temp_example.txt"
        self.save_json(self.change_config(from_path,to_path,True))
        coding = HuffmanCoding('encode',False)
        coding.encode()
        self.assertTrue(os.path.exists(to_path))
        self.assertLess(os.path.getsize(to_path),os.path.getsize(from_path))

        coding = HuffmanCoding('decode',False)
        with self.assertRaises(Exception) as error:
            coding.decode()
        self.assertEqual(str(error.exception),'file is not binary try to add in config.json as value of parameter fromFile path to some encoded file by method encode()')

        self.save_json(self.change_config(to_path,new_from_path,True))
        coding = HuffmanCoding('decode',False)
        coding.decode()
        self.assertTrue(os.path.exists(new_from_path))
        self.assertLess(os.path.getsize(to_path),os.path.getsize(new_from_path))

        coding = HuffmanCoding('encode',False)
        with self.assertRaises(Exception) as error:
            coding.decode()
        self.assertEqual(str(error.exception),'file is not raw text (txt) try to add in config.json as value of parameter fromFile path to some txt file')
        
        os.remove(new_from_path)
        os.remove(to_path)
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