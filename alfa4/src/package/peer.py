import socket, time, multiprocessing, logging, threading
from package.command import Command
from package.loadConfig import LoadConfig,LoadConfigSingleton
from package.loadDictionary import LoadDictionarySingleton
class Peer():
    def __init__(self) -> None:
        """
        Constructor that check correction of both configuration file and create tcp peer
        """
        try:
            self.settings:LoadConfig = LoadConfigSingleton.getConfig()#create first instance that check if all data in config.json are correct
            LoadDictionarySingleton.getDictionary()#create first instance that check if all data in dictionary.json are correct
            logging.basicConfig(filename='alfa4.log',format='%(asctime)s - %(message)s', level=logging.INFO)
            error=False
            try:
                self.peer_inet_address = (self.settings.address(), self.settings.port())
                self.peer_socket = socket.socket()
                self.peer_socket.bind(self.peer_inet_address)
            except:
                error=True
            finally:
                if error:raise Exception(f'Cant create peer, peer with address {self.settings.address()} and port {self.settings.port()} could be in use already')
            self.peer_socket.listen()
            self.connections =[] 
            logging.info("peer is running on "+str(self.peer_inet_address[0])+":"+str(self.peer_inet_address[1]))
            while True:
                connection, client_inet_address = self.peer_socket.accept()#wait for the user
                logging.info(f'new peer with ip address {client_inet_address[0]} and port {client_inet_address[1]} connected to the peer')
                process = threading.Thread(target=self._await_user,args=(connection,client_inet_address))
                process.start()
                self.connections.append((connection,process))#create thread for new user so peer can wait for another user
        except Exception as e:
            print(e)
            logging.exception(str(e))
        finally:
            logging.info('peer has been stopped')
            self.close()
    def _await_user(self,connection,address):
        """
        private Method that serve every one client or peer wait for user input and then 
        execute run method of command class
        :param connection: user connection that is used from sending and receiving data
        :param address: contains connected device ip address and port
        """
        try:
            command = Command()  
            logging.basicConfig(filename='alfa4.log',format='%(asctime)s - %(message)s', level=logging.INFO)
            connection.settimeout(self.settings.client_timeout())
            while True:
                response = connection.recv(1024).decode('utf-8').strip().replace('\r\n','')
                response = command.run(response)
                if response!=None:
                    if '\r\n' in response:response = response.replace('\r\n','')
                    connection.send(bytes(f'{str(response)}\r\n','utf-8'))
                else:connection.send(bytes('\r','utf-8'))# check if the connection is still running
                time.sleep(0.01)
        except socket.timeout:logging.info(f'connected peer with ip address {address[0]} and port {address[1]} get connection timeout')
        except:logging.info(f'connected peer with ip address {address[0]} and port {address[1]} interrupted connection')
        finally:
            connection.close()
    def close(self):
        """
        public Method that close peer and all it's connections
        """
        try:
            for connection in self.connections:
                connection[0].close()
                connection[1].terminate()
            self.peer_socket.close()
        except:pass
