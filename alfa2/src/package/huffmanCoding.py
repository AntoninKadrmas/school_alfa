import pickle, math
from queue import PriorityQueue
from package.xmlService import XMLService
from package.myEnum import Status,Mode

class Node():
    """
    Class Node is used to create Node tree that is user for encode and decode.
    """
    def __init__(self,frequency=None,left=None,right=None) -> None:
        """
        Constructor of class Node it creates object with attributes frequency, left adn right.

        :param frequency: is number means addition of left and right number of occurrence
        :param left: left param is children Node or EndNode object can not be None
        :param right: right param is children Node or EndNode object cant not be None
        """
        self.left:Node = left
        self.right:Node = right
        self.frequency:int = self.left.frequency+self.right.frequency \
            if frequency==None else frequency

    def __lt__(self, other):
        """
        Magic method lower then. Compare attribute frequency between objects.

        :param other: compered Node or EndNode object
        """
        return self.frequency < other.frequency


class EndNode(Node):
    """
    Class EndNode is represents as end node of Node object
    """
    def __init__(self, value:str,frequency:int) -> None:
        """
        Constructor of class EndNode inherited from Node it creates object with attributes frequency and value. Is it a last element of Nodes.

        :param value: is string character
        :param frequency: is number means number of occurrence of value
        :param left: right is set to None
        :param right: right is set to None
        """
        super().__init__(frequency)
        self.value:str = value


class HuffmanCoding():
    """
    Class HuffmanCoding take care about decode and encode algorithms.
    """
    def __init__(self,mode,debug) -> None:
        """
        Constructor of class HuffmanCoding that do all logic around compress and decompress txt files.

        :param mode: is param that decide in what mode is program going to run encode/decode
        :param debug: is param that decide if the result of program will be written into xml => true or not => false 
        """
        self.xml:XMLService = XMLService(mode,debug)
        self.frequency_dict:dict[str:int] ={}
        self.binary_dict:dict[str:str] ={}
        self.tree:Node = None
        self.data = None

    def encode(self) -> None:
        """
        public Method for encode text data into binary and then write the created binary data composed of 
        binary to char dictionary, first ignore characters length and encoded binary data into the file.
        """
        self._load_data()
        self._create_tree()
        binary_result=''
        appears = 0
        write_progress = -1
        for x,letter in enumerate(self.data):
            binary_result+=self.binary_dict[letter]
            appears+=.00005
            if appears>=4:appears,write_progress=0,-1
            self._progress(write_progress,appears,x)
            if(write_progress<math.floor(appears)):write_progress=math.floor(appears)
        print(f'ENCODE progress: 100%/100%')
        final_binary:bytearray = self._convert_binary_str_to_bytearray(binary_result)
        bin_text_length = int(8*(math.ceil(len(binary_result)/8))-len(binary_result)).\
            to_bytes(1,'big')
        with open(self.xml.to_file,'wb')as file:
            file.write(pickle.dumps([
                pickle.dumps(self.frequency_dict),
                bin_text_length,
                final_binary
                ]))
        self.xml.log(Status.SUCCESS)

    def decode(self) -> None:
        """
        public Method for decode binary data composed of binary to char dictionary, first ignore characters length 
        and encoded binary data and then write the created text data into the file.
        """
        self._load_data()
        self.frequency_dict = pickle.loads(self.data[0])
        self._create_tree()
        ignore_first_x = int.from_bytes(self.data[1],'big')
        compressed_data = ''
        appears = 0
        write_progress = -1
        for index,number in enumerate(self.data[2]):
            compressed_data+=f'{number:08b}'
            appears+=.00005
            if appears>=4:appears,write_progress=0,-1
            self._progress(write_progress,appears,index)
            if(write_progress<math.floor(appears)):write_progress=math.floor(appears)
        print(f'DECODE progress: 100%/100%')
        with open(self.xml.to_file,'wt') as writer:
            writer.write(self._decode_bin(self.tree,compressed_data[ignore_first_x:]))
        self.xml.log(Status.SUCCESS)

    def _progress(self,write_progress,appears,index) -> None:
        """
        private Method for printing out progress of encoding or decoding.

        :param write_progress: is integer number that indicate when the progress should be printed 
        :param appears: parameter that is increasing every time of for loop if it is bigger than write_progress progress is printed
        :param index: how much elements was already encoded/decoded
        :param encoded: parameter that adapt print for encoding
        """
        length = len(self.data[2])
        mode = 'DECODE'
        if self.xml.mode==Mode.ENCODE.value:
            mode = 'ENCODE'
            length=len(self.data)
        if(write_progress<math.floor(appears)):
            print(f'{mode} progress: {int(index*100/length)}%/{100}%')

    def _load_data(self) -> None:
        """
        private Method that loads binary or text data from file and store is.

        :param encode: decide if the data is gonna be binary (false) or text (true) in true case it also generate frequency dictionary
        """
        if self.xml.mode==Mode.ENCODE.value:
            self.data=''
            error=False
            try:    
                with open(self.xml.from_file,'rt') as reader:
                    temp_read = reader.read(10000)
                    while temp_read!='':
                        self.data+=temp_read
                        temp_read = reader.read(10000)
            except:
                error = True
            if error: 
                error='file is not raw text (txt) try to add in config.json as value of parameter fromFile path to some txt file'
                self.xml.log(Status.ERROR,error)
                raise Exception(error)
            for i in self.data:
                if i in self.frequency_dict:
                    self.frequency_dict[i]+=1
                else:
                    self.frequency_dict[i]=1
        else:
            self.data = []
            with open(self.xml.from_file,'rb') as reader:
                error = False
                try:
                    self.data = pickle.loads(reader.read())
                except:
                    error=True
                if error:
                    error='file is not binary try to add in config.json as value of parameter fromFile path to some encoded file by method encode()'
                    self.xml.log(Status.ERROR,error)
                    raise Exception(error)
                    
    def _convert_binary_str_to_bytearray(self,binary_result:str) -> bytearray:
        """
        private Method for converting string combined by 0 and 1 to bytearray. 
        Method append on beginning so many zeros so the length of the string is divisible by 8

        :binary_result: is string parameter combined only by characters 0 and 1
        :return: return byte array of all numbers created by converted every eight 0 and 1 character to number
        """
        final_binary_array= []
        binary_result='0'*(8*(math.ceil(len(binary_result)/8))-len(binary_result))\
            + binary_result
        for x in range(0,math.ceil(len(binary_result)/8)):
            num = int(binary_result[8*x:8*(x+1)],2)
            final_binary_array.append(num)
        return bytearray(final_binary_array)

    def _generate_bin_dict(self,node:Node,text:str) -> None:
        """
        private Method generate dictionary with text and binary (key and value) by using given Node object and recursion.

        :param node: parameter is Node object used for generate dictionary
        :param text: parameter that is used to store encoding of each character
        """
        if type(node)==EndNode:
            self.binary_dict[node.value] = text
            return
        self._generate_bin_dict(node.left,text+'0')
        self._generate_bin_dict(node.right,text+'1')

    def _decode_bin(self,node:Node,data:str) -> str:
        """
        private Method for decode given data string to original text by using Node object.

        :param node: is object node parameter that is used there for decoding the data
        :param data: is string composed of 0 and 1
        :return: return decoded text 
        """
        text = ''
        current:Node = node
        for bit in data:
            current = current.right if bit=='1' else current.left
            if(type(current)==EndNode):
                text+=current.value
                current = node
        return text

    def _create_tree(self) -> None:
        """
        private Method that create one Node by combined elements of frequency dictionary converted to EndNode objects.
        """
        node_list = PriorityQueue()
        for key,value in self.frequency_dict.items():
           node_list.put(EndNode(key,value))
        while node_list.qsize()>1:
            self.tree = Node(
                left=node_list.get(),
                right=node_list.get()
            )
            node_list.put(self.tree)
        self._generate_bin_dict(self.tree,'') 