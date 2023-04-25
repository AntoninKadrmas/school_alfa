import json, os, re

class LoadConfig():
    """
    Class that manage config.json file and test all parameters if they are valid.
    """
    def __init__(self) -> None:
        """
        Constructor that load and test all parameters in config.json file 
        """
        self.json_object = ''
        if not os.path.exists('.././config/config.json'):
            raise Exception('config/config.json file does not exists please recreate it using readme.txt')
        error=False
        try:
            with open('.././config/config.json','r') as reader:
                self.json_object = json.load(reader)
        except:error=True
        finally:
            if error:raise Exception('text in config/config.json is not json please recreate it using readme.txt')
        self._check_json()
        self._check_variables()
        self._check_address_range()
        self._check_port_range()
    def _check_json(self) -> None:
        """
        private Method that check if all parameters in json file are correctly spelled and exists.
        """
        try:
            self.json_object['server']
        except:
            raise Exception('server params is incorrect or missing please recreate it using readme.txt')
        important_params = ["address","port","name","error","connection_timeout","response_timeout","client_timeout"]
        for param in important_params:
            try:
                self.json_object['server'][param]
            except:
                raise Exception(f'{param} params is incorrect or missing please recreate it using readme.txt')
        try:
            self.json_object['scan']
        except:
            raise Exception('scan params is incorrect or missing please recreate it using readme.txt')
        important_params = ["address","port"]
        for param in important_params:
            try:
                self.json_object['scan'][param]
            except:
                raise Exception(f'{param} params is incorrect or missing please recreate it using readme.txt')
    def _check_variables(self)->None:
        """
        private Method check all server part variables from config.json are correct
        """
        ip =  self.json_object['server']['address'] if not re.fullmatch(r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}',self.json_object['server']['address']) else 'localhost'
        if ip!='localhost': raise Exception('Error in address parameter look at the readme documentations')
        try:
            port = int(self.json_object['server']['port'])
        except:
            raise Exception('port parameter in config.json has to be integer')
        else:
            if(port<0):raise Exception("port parameter in config.json can't be lower then zero")
        for timeout in ['response_timeout','connection_timeout','client_timeout']:
            try:
                port = float(self.json_object['server'][f'{timeout}'])
            except:
                raise Exception(f'{timeout} parameter in config.json has to be decimal')
            else:
                if(port<=0):raise Exception(f"{timeout} parameter in config.json can't be lower then zero")
        if(self.json_object['server']['name']==''): raise Exception("name parameter of the server can't be empty")
        if(self.json_object['server']['error']==''): raise Exception("error parameter of the server can't be empty")
    def _check_address_range(self):
        """
        private Method that check if ip address ranges from scan part of the config.json are set correctly set
        """
        if len(self.json_object['scan']['address'])==0: raise Exception('in the scan address missing address/es to scan edit it by using readme.txt')
        for index, ip_range in enumerate(self.json_object['scan']['address']):
            if len(ip_range)!=1 and len(ip_range)!=2: raise Exception(f'{index+1}. have incorrect number of ip address actual {len(ip_range)} expected 1 or 2 edit it by using readme.txt')
            for address in ip_range:
                if re.fullmatch(r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}',address) or address=='localhost':pass
                else: raise Exception(f'{index+1}. field have ip address that is incorrect in each position of four can be number from 0 to 255')
            if len(ip_range)==1 or ip_range[0]=='localhost':continue
            else:
                first_address=ip_range[0].split('.')
                last_address = ip_range[1].split('.')
                for x in range(4):
                    if int(first_address[x])<int(last_address[x]):break
                    elif int(first_address[x])==int(last_address[x]):continue
                    else:raise Exception(f'{index+1}. field have incorrect ip address range left side is bigger then right side')
    def _check_port_range(self):
        """
        private Method that check if port ranges from scan part of the config.json are set correctly set
        """
        if len(self.json_object['scan']['port'])==0: raise Exception('in the scan port missing port/s to scan edit it by using readme.txt')
        for index, ports in enumerate(self.json_object['scan']['port']):
            if len(ports)!=1 and len(ports)!=2: raise Exception(f'{index+1}. have incorrect number of ports actual {len(ports)} expected 1 or 2 edit it by using readme.txt')
            error=0
            try:
                port=int(ports[0])
                if port<0: error=1
                if len(ports)==2:
                    port=int(ports[1])
                    if port<0 and error==0:error=2
            except:error=3
            finally:
                if error==3:raise Exception(f'{index+1}. field have to contains just integer values edit it by using readme.txt')
                if error==2:raise Exception(f'{index+1}. field have second port below the zero edit it by using readme.txt')
                if error==1:raise Exception(f'{index+1}. field have first port below the zero edit it by using readme.txt')

            if len(ports)==1:continue
            else:
                if int(ports[0])>int(ports[1]):raise Exception(f'{index+1}. field have left port bigger then right incorrect range edit it by using readme.txt')

    def address(self) -> str:
        """
        public Method that return ip address.
        :return: return ip address attribute
        """
        return self.json_object['server']['address']
    def port(self) -> int:
        """
        public Method that return port.
        :return: return port attribute
        """
        return int(self.json_object['server']['port'])
    def response_timeout(self) -> float:
        """
        public Method that return response timeout.
        :return: return response timeout attribute
        """
        return float(self.json_object['server']['response_timeout'])
    def connection_timeout(self) -> float:
        """
        public Method that return server connection timeout.
        :return: return server connection timeout attribute
        """
        return float(self.json_object['server']['connection_timeout'])
    def client_timeout(self) -> float:
        """
        public Method that return client connection timeout.
        :return: return client connection timeout attribute
        """
        return float(self.json_object['server']['client_timeout'])
    def name(self) -> str:
        """
        public Method that return name.
        :return: return name attribute
        """
        return self.json_object['server']['name']
    def error(self) -> str:
        """
        public Method that return error.
        :return: return error attribute
        """
        return self.json_object['server']['error']
    def address_range(self) -> list:
        """
        public Method that return ip address range.
        :return: return ip address range attribute
        """
        return self.json_object['scan']['address']
    def port_range(self) -> list:
        """
        public Method that return port range.
        :return: return port range attribute
        """
        return self.json_object['scan']['port']

class LoadConfigSingleton():
    """
    Config singleton that make sure that only one copy of config exists
    """
    __confInstance:LoadConfig = None
    @staticmethod
    def getConfig():
        """
        static Method that create new config if no config exists or return existing one.
        """
        if LoadConfigSingleton.__confInstance==None:
            LoadConfigSingleton()
        return LoadConfigSingleton.__confInstance
    def __init__(self) -> None:
        """
        Constructor that made one config instance 
        """
        if LoadConfigSingleton.__confInstance!=None: raise Exception('load config is exists')
        LoadConfigSingleton.__confInstance = LoadConfig()
