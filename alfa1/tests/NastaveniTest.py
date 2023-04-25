import multiprocessing
import unittest
import sys
import os
sys.path.append('../alfa')
from package.Nastaveni import Nastaveni

proces = 'PROCES_AMOUNT'
timeout = 'TIMEOUT'
word = 'WORD_LENGTH'
file = 'USED_FILE'
# default setup
os.environ[proces] = 'auto'
os.environ[timeout] = 'infinite'
os.environ[word] = 'infinite'
os.environ[file] = 'small'

class NastaveniTest(unittest.TestCase):
    def test_get_pouzit_soubor(self):
        previous = os.getenv(file)
        del os.environ[file]
        self.assertEqual(Nastaveni.get_pouzit_soubor(),'small')
        os.environ[file] = 'small'
        self.assertEqual(Nastaveni.get_pouzit_soubor(),'small')
        os.environ[file] = '  small  ' 
        self.assertEqual(Nastaveni.get_pouzit_soubor(),'small')
        os.environ[file] = 'big'
        self.assertEqual(Nastaveni.get_pouzit_soubor(),'big')
        os.environ[file] = 'BIG'
        self.assertEqual(Nastaveni.get_pouzit_soubor(),'big')
        os.environ[file] = 'error'
        with self.assertRaises(BaseException):
            Nastaveni.get_pouzit_soubor()
        os.environ[file] = previous

    def test_get_delka_slova(self):
        previous = os.getenv(word)
        del os.environ[word]
        with self.assertRaises(BaseException):
            Nastaveni.get_delka_slova()
        os.environ[word] = 'infinite'
        self.assertEqual(Nastaveni.get_delka_slova(),-1)
        os.environ[word] = str(0)
        self.assertEqual(Nastaveni.get_delka_slova(),-1)
        os.environ[word] = str(-10)
        self.assertEqual(Nastaveni.get_delka_slova(),-1)
        os.environ[word] = str(5)
        self.assertEqual(Nastaveni.get_delka_slova(),5)
        os.environ[word] = 'error'
        with self.assertRaises(BaseException):
            Nastaveni.get_delka_slova()
        os.environ[word] = previous

    def test_get_casovy_limit(self):
        previous = os.getenv(timeout)
        del os.environ[timeout]
        with self.assertRaises(BaseException):
            Nastaveni.get_casovy_limit()
        os.environ[timeout] = 'infinite'
        self.assertEqual(Nastaveni.get_casovy_limit(),-1)
        os.environ[timeout] = str(0)
        self.assertEqual(Nastaveni.get_casovy_limit(),-1)
        os.environ[timeout] = str(-10)
        self.assertEqual(Nastaveni.get_casovy_limit(),-1)
        os.environ[timeout] = str(10)
        self.assertEqual(Nastaveni.get_casovy_limit(),10)
        os.environ[timeout] = 'error'
        with self.assertRaises(BaseException):
            Nastaveni.get_casovy_limit()
        os.environ[timeout] = previous

    def test_get_pocet_procesu(self):
        previous = os.getenv(proces)
        max_pocet_procesu = multiprocessing.cpu_count()
        del os.environ[proces]
        self.assertEqual(Nastaveni.get_pocet_procesu(),max_pocet_procesu)
        os.environ[proces] = 'auto'
        self.assertEqual(Nastaveni.get_pocet_procesu(),max_pocet_procesu)
        os.environ[proces] = str(0)
        self.assertEqual(Nastaveni.get_pocet_procesu(),max_pocet_procesu)
        os.environ[proces] = str(-10)
        self.assertEqual(Nastaveni.get_pocet_procesu(),max_pocet_procesu)
        os.environ[proces] = str(1000)
        self.assertEqual(Nastaveni.get_pocet_procesu(),max_pocet_procesu)
        os.environ[proces] = str(1)
        self.assertEqual(Nastaveni.get_pocet_procesu(),1)
        os.environ[proces] = str(2)
        self.assertEqual(Nastaveni.get_pocet_procesu(),2)
        os.environ[proces] = 'error'
        with self.assertRaises(BaseException):
            Nastaveni.get_pocet_procesu()
        os.environ[proces] = previous