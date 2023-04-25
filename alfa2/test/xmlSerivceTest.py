import unittest, sys, time, datetime
import xml.etree.ElementTree as ET

sys.path.append('./')
from src.package.xmlService import XMLService
from src.package.myEnum import Status,Mode
class XMLServiceTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.previous_xml = ET.parse('./logs/logs.xml')
    def test_create_XML_object(self):
        xml = XMLService(Mode.ENCODE.value,False)
        self.assertFalse(xml.debug)
        self.assertEqual(xml.mode,'encode')
        self.assertEqual(xml.from_file,"./data/forEncode/example.txt")
        self.assertEqual(xml.to_file,"./data/forDecode/example.txt")
        xml = XMLService(Mode.DECODE.value,True)
        self.assertTrue(xml.debug)
        self.assertEqual(xml.mode,'decode')
    def test_log(self):
        self.clean_xml()
        xml = XMLService(Mode.ENCODE.value,True)
        self.assertEqual(xml.get_all_data(),[])
        xml.log(Status.ERROR,'error message test')
        self.assertEqual(xml.get_all_data()[0]['status'],Status.ERROR.value)
        self.assertEqual(xml.get_all_data()[0]['errorMessage'],'error message test')
        self.assertEqual(len(xml.get_data_by_status(Status.ERROR.value)),1)
        self.assertEqual(len(xml.get_data_by_status(Status.SUCCESS.value)),0)
        self.assertEqual(len(xml.get_data_by_mode(Mode.ENCODE.value)),1)
        self.assertEqual(len(xml.get_data_by_mode(Mode.DECODE.value)),0)

        xml.log(Status.ERROR,'error message test')
        self.assertEqual(len(xml.get_all_data()),2)
        self.assertEqual(len(xml.get_data_by_status(Status.ERROR.value)),2)
        self.assertEqual(len(xml.get_data_by_status(Status.SUCCESS.value)),0)
        self.clean_xml()
        xml = XMLService(Mode.DECODE.value,True)
        start_time = str(datetime.datetime.fromtimestamp(round(time.time()))).replace(' ','_')
        time.sleep(1)
        xml.log(Status.SUCCESS)
        time.sleep(1)
        end_time = str(datetime.datetime.fromtimestamp(round(time.time()))).replace(' ','_')
        self.assertEqual(len(xml.get_all_data()),1)
        self.assertEqual(len(xml.get_data_by_status(Status.ERROR.value)),0)
        self.assertEqual(len(xml.get_data_by_status(Status.SUCCESS.value)),1)
        self.assertEqual(len(xml.get_data_by_mode(Mode.ENCODE.value)),0)
        self.assertEqual(len(xml.get_data_by_mode(Mode.DECODE.value)),1)
        self.assertEqual(xml.get_data_by_date(start_time,end_time)[0]['status'],Status.SUCCESS.value)
        self.assertEqual(len(xml.get_data_by_date(start_time,end_time)),1)
        self.assertEqual(len(xml.get_data_by_date(start_time.split('_')[0],\
            str(datetime.datetime.fromtimestamp(round(time.time()+100000))).replace(' ','_'))),1)

        self.previous_xml.write('./logs/logs.xml',encoding='UTF-8',xml_declaration=True)
    def test_log_error(self):
        self.clean_xml()
        xml = XMLService(Mode.DECODE.value,False)
        xml.log(Status.ERROR,'error message')
        xml.log(Status.SUCCESS)
        self.assertEqual(len(xml.get_all_data()),0)
        self.assertEqual(len(xml.get_data_by_status(Status.ERROR.value)),0)
        self.assertEqual(len(xml.get_data_by_status(Status.SUCCESS.value)),0)
        xml = XMLService(Mode.DECODE.value,True)
        start_time = str(datetime.datetime.fromtimestamp(round(time.time()))).replace(' ','_')
        xml.log(Status.SUCCESS)
        with self.assertRaises(Exception) as error:
            xml.get_data_by_date('','end time')
        self.assertEqual(str(error.exception),'Bad format of from_date format has to be "year-month-day hour:minute:second" or "year-month-day"')
        with self.assertRaises(Exception) as error:
            xml.get_data_by_date(start_time,'')
        self.assertEqual(str(error.exception),'Bad format of to_date format has to be "year-month-day hour:minute:second" or "year-month-day"')
        self.previous_xml.write('./logs/logs.xml',encoding='UTF-8',xml_declaration=True)


    def clean_xml(self):
        tree = ET.ElementTree(ET.Element('root'))
        tree.write('./logs/logs.xml',encoding='UTF-8',xml_declaration=True)