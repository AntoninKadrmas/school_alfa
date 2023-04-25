import unittest,json 
from loadConfigTest import LoadConfigTest
from huffmanCodingTest import HuffmanCodingTest
from xmlSerivceTest import XMLServiceTest
if __name__ == '__main__':
    try:
        with open('./config/config.json','r') as reader:
            pervious = json.dump(reader)   
    except:
        json_object = {
            "config":{
                "fromFile":"./data/forEncode/example.txt",
                "toFile":"./data/forDecode/example.txt",
                "overwrite":True
            }
        }
        with open('./config/config.json','w') as writer:
            json.dump(json_object,writer)
    unittest.main()
 