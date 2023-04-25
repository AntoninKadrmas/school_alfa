import time, datetime
import os
import xml.etree.ElementTree as ET
from package.loadConfig import LoadConfig
from package.myEnum import Status

class XMLService():
    """
    Class XMLService that take car of xml read and write especially for logging results about program progress.
    """
    def __init__(self,mode,debug) -> None:
        """
        Constructor that load xml file and assigned all import parameters.

        :param mode: is param that decide in what mode is program going to run encode/decode
        :param debug: is param that decide if the result of program will be written into xml => true or not => false 
        """
        try:
            self.main = ET.parse('././logs/logs.xml')
        except:
            tree = ET.ElementTree(ET.Element('root'))
            tree.write('././logs/logs.xml',encoding='UTF-8',xml_declaration=True)
            self.main = ET.parse('././logs/logs.xml')
        self.config=None
        self.mode:str = mode
        self.debug:bool = debug
        try:
            self.config:LoadConfig = LoadConfig()
            self.from_file:str = self.config.from_file()
            self.to_file:str = self.config.to_file()
        except BaseException as e:
            self.config = str(e)
            if self.debug: self.log(Status.ERROR,str(e))
        if type(self.config)==str:
            raise Exception(self.config)

    def log(self,status:Status,error_message='') -> None:
        """
        public Method for logging results of program running into xml file.

        :param status: status parameter means in which way program ended SUCCESS/ERROR
        :param error_message: error_message contain error message if program end because of error
        """
        if not self.debug: return
        main = self.main.getroot()
        root = ET.SubElement(main,'log')
        ET.SubElement(root,'status').text = str(status.value)
        ET.SubElement(root,'mode').text = self.mode
        ET.SubElement(root,'executedTime').text = str(time.time())
        if status==Status.SUCCESS:
            data = ET.SubElement(root,'data')
            ET.SubElement(data,'fromFilePath').text = self.from_file
            ET.SubElement(data,'toFilePath').text = self.to_file
            ET.SubElement(data,'oldSize').text = str(os.path.getsize(self.from_file))
            ET.SubElement(data,'newSize').text = str(os.path.getsize(self.to_file))
        elif status==Status.ERROR:
            error = ET.SubElement(root,'error')
            ET.SubElement(error,'errorParameter').text = error_message.split(' ')[0]
            ET.SubElement(error,'errorMessage').text = error_message
        tree = ET.ElementTree(main)
        tree.write('././logs/logs.xml',encoding='UTF-8',xml_declaration=True)

    def _load_data(self) ->list:
        """
        private Method that loads data from xml file and convert it into list of dictionary's

        :return: list of dictionary's that contains key value pare of element tag and element text
        """
        root = self.main
        data =[]
        for log in root.iter('log'):
            log_dict={}
            for element in log:
                if element.tag in ['data','error']:
                    for sub_element in element:
                        log_dict[sub_element.tag] = sub_element.text
                else:log_dict[element.tag]=element.text
            data.append(log_dict)
        return data

    def get_all_data(self) -> list:
        """
        public Method returns all data

        :return: list of loaded dictionary's 
        """
        return self._load_data()

    def get_data_by_status(self,status:str) -> list:
        """
        public Method returns data filtered by status

        :param status: status parameter decide if method return data with error or success status
        :return: list of loaded dictionary's filtered by status parameter
        """
        return list(filter(lambda x:x['status']==str(status),self._load_data()))

    def get_data_by_date(self,from_date=None,to_date=None) -> list:
        """
        public Method returns data that have executedTime between from_date and to_date

        :param from_date: from_date parameter give lower limit of filtered time
        :param to_date: to_date parameter give higher limit of filtered time
        :return: list of loaded dictionary's filtered by parameters from_date and to_date
        """
        bad_format=False
        try:
            from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d_%H:%M:%S')
        except:
            try:
                from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d')
            except:
                bad_format=True
        if bad_format:
            raise Exception('Bad format of from_date format has to be "year-month-day hour:minute:second" or "year-month-day"')
        try:
            to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d_%H:%M:%S')
        except:
            try:
                to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d')
            except:
                bad_format=True
        if bad_format:
            raise Exception('Bad format of to_date format has to be "year-month-day hour:minute:second" or "year-month-day"')
        return list(filter(lambda x:time.mktime(from_date.timetuple())<=float(x['executedTime'])\
            <= time.mktime(to_date.timetuple()),self._load_data()))

    def get_data_by_mode(self,mode:str) -> list:
        """
        public Method returns data filtered by mode

        :param mode: mode parameter decide if method return data with encode or decode mode
        :return: list of loaded dictionary's filtered by mode parameter
        """
        return list(filter(lambda x:x['mode']==mode,self._load_data()))
