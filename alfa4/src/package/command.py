import socket, struct, re, multiprocessing, subprocess,os, logging
from multiprocessing import Pool
from functools import partial
from itertools import chain
from package.loadDictionary import LoadDictionary,LoadDictionarySingleton
from package.loadConfig import LoadConfig,LoadConfigSingleton
class Command():
    def __init__(self) -> None:
        """
        Constructor of command class hold dictionary of commands
        """
        self.word_dictionary:LoadDictionary = LoadDictionarySingleton.getDictionary()
        self.value = ''
        self._command_dictionary = {
            "TRANSLATEPING":(self._pong,"TRANSLATEPONG"),
            "TRANSLATELOCL":(self._translate,"TRANSLATEDSUC","TRANSLATEDERR"),
            "TRANSLATESCAN":(self._scan,)
        }
        self.well_know_ip =[]
    def run(self,value:str)->str:
        """
        public Method run call specific method from dictionary by user input
        :param value: string param that contains user input
        :return: return one of the three command result from command_dictionary or None if input is incorrect
        """
        try:
            command = value[:13]
            self.value=value.split('"')[1]
            if command in self._command_dictionary.keys():
                return self._command_dictionary[command][0]() #call specific method from _command_dictionary
            else:return #incorrect command
        except:return 
    def _translate(self)->str:
        """
        private Method that translate english word into czech if the word exists in the _command_dictionary
        :return: translation of the english word if it exist in dictionary else error
        """
        found = list(filter(lambda x:x[0] == self.value,self.word_dictionary.dictionary()))
        if len(found)==0:
            settings:LoadConfig = LoadConfigSingleton.getConfig()
            result = self._command_dictionary['TRANSLATELOCL'][2]
            return f'{result}"{settings.error()}"'
        else:
            result = self._command_dictionary['TRANSLATELOCL'][1]
            return f'{result}"{found[0][1]}"'
    def _pong(self)->str:
        """
        private Method that respond with the program name
        :return: response with program name from config.json
        """
        settings:LoadConfig = LoadConfigSingleton.getConfig()
        result = self._command_dictionary['TRANSLATEPING'][1]
        return f'{result}"{settings.name()}"'
    def _scan(self) -> str:
        """
        private Method ask for translations for all ip addresses and for every port in port range
        :return: correct translation if the pears know answer else his error message 
        """
        settings:LoadConfig = LoadConfigSingleton.getConfig()
        port_ranges = list(chain(*[list(range(port_range[0],port_range[0]+1)) if len(port_range)==1 else list(range(port_range[0],port_range[1]+1)) for port_range in settings.port_range()])) #add all ports into one list
        result = self._find_answer(port_ranges)
        if result!=None:return result
        new_pool = []
        ip_ranges = list(chain(*[address_range if len(address_range)==1 else self._generate_ip_range(address_range[0],address_range[1]) for address_range in settings.address_range()])) #add all ip addresses in one list
        with Pool(multiprocessing.cpu_count()) as pool_thread:
            for result in pool_thread.imap_unordered(self._check_connection,ip_ranges):
                if not result[1] and result[0] in self.well_know_ip: self.well_know_ip.remove(result[0])
                elif result[1] and result[0] not in self.well_know_ip:
                    self.well_know_ip.append(result[0])
                    new_pool.append(result[0])
        logging.basicConfig(filename='alfa4.log',format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info(f'find {len(new_pool)} new active ip addresses to connect')
        result = self._find_answer(port_ranges,new_pool)
        if result!=None:return result
        else: return self._translate()#rno result find return local error
    def _find_answer(self,port_ranges,ip_ranges=None):
        """
        private Method that collected responses from each ip address and port pair and then return result
        :param port_ranges: is range of port from config.json that is peer going to connect
        :param ip_ranges: is range of ipv4 addresses from config.json that is peer going to connect
        :return: return correct answer if it's found or None if it's not
        """
        ip_ranges = ip_ranges if ip_ranges!=None else self.well_know_ip
        with Pool(multiprocessing.cpu_count()) as pool_thread:
            for address in ip_ranges:
                part = partial(self._connect_guess,address)
                for result in pool_thread.imap_unordered(part,port_ranges):
                    if result==None:continue
                    else:return result
            else:return None
    def _connect_guess(self,address:str,port:int):
        """
        private Method that trying to get response from pear on specific ip address and port
        :param address: specific ip address that is used to connect to
        :param port: specific port that is used to connect to
        :return: return None if can't connect to the peer or if the peer does not know the translation word 
        else correct response
        """
        logging.basicConfig(filename='alfa4.log',format='%(asctime)s - %(message)s', level=logging.INFO)
        try:
            settings:LoadConfig = LoadConfigSingleton.getConfig()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(settings.connection_timeout())
                s.connect((address, port)) #try to connect
                data=None
                server_name = f'TRANSLATEPING"{settings.name()}"'
                s.send(bytes(server_name,'utf-8')) #send translateping to check if peer communicate on the same protocol
                try:
                    s.settimeout(settings.response_timeout())
                    while True:
                        data =s.recv(2048).decode() #wait for response
                        break
                    if self._command_dictionary['TRANSLATEPING'][1] in data: 
                        logging.info(f'connected to the functional peer {address}:{port}')
                        translate = f'TRANSLATELOCL"{self.value}"'
                        s.send(bytes(translate,'utf-8')) #send translatelocl request into connected server
                        try:
                            s.settimeout(settings.response_timeout())
                            while True:
                                data =s.recv(2048).decode() #wait for response
                                break
                            if self._command_dictionary['TRANSLATELOCL'][1] in data:
                                logging.info(f'from {address}:{port} got response {data}')
                                return data #return response if it is correct
                        except: pass
                except: pass
        except: pass #can\t connect to the server
    def _generate_ip_range(self,first:str, last:str) -> list:
        """
        private Method that returns all ip address from input range
        :param first: first lower ip address from range
        :param last: last higher ip address from range
        :return: list of all ip address between first and last included
        """
        first = struct.unpack('>I', socket.inet_aton(first))[0]
        last = struct.unpack('>I', socket.inet_aton(last))[0]
        return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(first, last)]
    def _check_connection(self,address:str) -> tuple:
        """
        private Method that ping address and find out if the address response or not
        :param address: is tested ip address
        :return: is combination of address and boolean variable that said if the address exists True or dose not exists False
        """
        try:
            if os.name == 'nt':response= subprocess.run(['ping','-n','2',address],capture_output=True)#on windows
            else:response= subprocess.run(['ping','-c','2',address],capture_output=True)#on different device than windows like linux
        except:
            response=0
        if 'destination host unreachable' in str(response).lower():response=1
        elif 'request timed out' in str(response).lower():response=1
        else:
            response=0
        logging.info(f'Get answer frm address {address} => {not response}')
        return (address,True if not response else False)     