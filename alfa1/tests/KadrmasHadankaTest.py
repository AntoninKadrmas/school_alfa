import unittest
import time
import sys
import os
sys.path.append('../alfa')
from package.KadrmasHadanka import PovolenaSlova, KadrmasovaHadanka, KadrmasovaHra


proces = 'PROCES_AMOUNT'
timeout = 'TIMEOUT'
word = 'WORD_LENGTH'
file = 'USED_FILE'
# default setup
os.environ[proces] = 'auto'
os.environ[timeout] = 'infinite'
os.environ[word] = 'infinite'
os.environ[file] = 'small'


class PovolenaSlovaTest(unittest.TestCase):
    def test_povolena_slova_init(self):
        previous = os.getenv(word)

        os.environ[word] = 'infinite'
        planovana = PovolenaSlova()
        self.assertTrue('staphylococcus' in planovana.slova)
        self.assertTrue('the' in planovana.slova)
        self.assertFalse('asdiubuicviyg' in planovana.slova)

        os.environ[word] = '5'
        planovana = PovolenaSlova()
        self.assertTrue('am' in planovana.slova)
        self.assertTrue('hello' in planovana.slova)
        self.assertFalse('paints' in planovana.slova)
        self.assertFalse('neighbour' in planovana.slova)
        self.assertFalse('aglem' in planovana.slova)

        os.environ[word] = 'error'
        with self.assertRaises(BaseException):
            planovana = PovolenaSlova()

        os.environ[word] = previous

    def test_vyber_souboru_init(self):
        previous = os.getenv(file)

        os.environ[file] = 'small'
        planovana = PovolenaSlova()
        self.assertLessEqual(len(planovana.slova), 370000)

        os.environ[file] = 'big'
        planovana = PovolenaSlova()
        self.assertGreater(len(planovana.slova), 370000)

        del os.environ[file]
        planovana = PovolenaSlova()
        self.assertLessEqual(len(planovana.slova), 370000)

        os.environ[file] = 'error'
        with self.assertRaises(BaseException):
            planovana = PovolenaSlova()

        os.environ[file] = previous

    def test_existuje_slovo(self):
        planovana = PovolenaSlova()
        self.assertTrue(planovana.existuje_slovo('welcome'))
        self.assertTrue(planovana.existuje_slovo('WeLcoME'))
        self.assertFalse(planovana.existuje_slovo('welc@#$ome'))
        self.assertFalse(planovana.existuje_slovo('welcomee'))


class KadrmasovaHadankaTest(unittest.TestCase):
    def test_kadrmasova_hadanka_init(self):
        veta = 'he just want some friends'
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertEqual(hadanka.veta, veta)
        self.assertEqual(
            hadanka.slova, ['he', 'just', 'want', 'some', 'friends'])

        veta = "i love     you"
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertEqual(hadanka.veta, 'i love you')
        self.assertEqual(hadanka.slova, ['i', 'love', 'you'])

        veta = 'he is looong'
        with self.assertRaises(BaseException):
            hadanka = KadrmasovaHadanka(veta, PovolenaSlova())

        veta = ''
        with self.assertRaises(BaseException):
            hadanka = KadrmasovaHadanka(veta, PovolenaSlova())

    def test_pocet_slov(self):
        veta = 'he just want some friends'
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertEqual(hadanka.pocet_slov(), 5)

        veta = "i love     you"
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertEqual(hadanka.pocet_slov(), 3)

        veta = 'the'
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertEqual(hadanka.pocet_slov(), 1)

    def test_hadej_slovo(self):
        veta = 'he just want some friends some'
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertEqual(hadanka.hadej_slovo('he'), [0])
        self.assertEqual(hadanka.hadej_slovo('some'), [3, 5])
        self.assertEqual(hadanka.hadej_slovo('WanT'), [2])
        self.assertEqual(hadanka.hadej_slovo('wan'), [])
        self.assertEqual(hadanka.hadej_slovo('every'), [])
        with self.assertRaises(BaseException):
            hadanka.hadej_slovo('wantt')
        with self.assertRaises(BaseException):
            hadanka.hadej_slovo('just@')
    
    def test_hadej_vetu(self):
        veta = 'he just want some friends some'
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertTrue(hadanka.hadej_vetu('he just want some friends some'))
        self.assertTrue(hadanka.hadej_vetu('he jUSt wANt SOme fRieNds sOme'))
        self.assertTrue(hadanka.hadej_vetu('      he just want some friends some     '))
        self.assertFalse(hadanka.hadej_vetu('he just want some friends'))
        self.assertFalse(hadanka.hadej_vetu('he  just  want  some  friends  some'))
        with self.assertRaises(BaseException): hadanka.hadej_vetu('he just want some friends some.')

    def test_kontrola(self):
        previous = os.getenv(word)
        veta = 'he'
        hadanka = KadrmasovaHadanka(veta, PovolenaSlova())
        self.assertFalse(hadanka.kontrola(['gun'])[0])
        self.assertTrue(hadanka.kontrola(['   gUn ','In',' school  '])[0])
        self.assertTrue(hadanka.kontrola(['gun','in','schoolalole'])[0])
        self.assertEqual(hadanka.kontrola(['gun','in','schoolalole'])[1][0],'schoolalole')
        self.assertEqual(hadanka.kontrola(['gun','in','schoolalole'])[1][1],-1)
        os.environ[word] = str(3)
        self.assertFalse(hadanka.kontrola(['gun','in','hit'])[0])
        self.assertEqual(hadanka.kontrola(['gun','in','playground'])[1][0],'playground')
        self.assertEqual(hadanka.kontrola(['gun','in','playground'])[1][1],3)
        os.environ[word] = previous

class KadrmasovaHraTest(unittest.TestCase):

    def test_kadrmasova_hra_init(self):
        hra = KadrmasovaHra()
        self.assertIsNone(hra.hadanka)
        self.assertIsNotNone(hra.hadana_slova)
    def test_hraj(self):
        hra = KadrmasovaHra()
        hra.hraj(KadrmasovaHadanka('hi',hra.hadana_slova))
        self.assertEqual(hra.hadanka.veta,'hi')
        with self.assertRaises(BaseException):
            hra.hraj(None)
    def test_hadej(self):
        previous = os.getenv(timeout)
        hra = KadrmasovaHra()
        hra.hraj(KadrmasovaHadanka('hi',hra.hadana_slova))
        reseni:dict[int,str] = dict()
        with self.assertRaises(BaseException):
            hra.hadej_paralelne(reseni,[])
        with self.assertRaises(BaseException):
            hra.hadej_paralelne(None,['hi'])
        hra.hadej_paralelne(reseni,['ho'])
        self.assertEqual(len(reseni),0)
        hra.hadej_paralelne(reseni,['hi'])
        self.assertEqual(len(reseni),1)
        self.assertEqual(reseni[0],'hi')
        os.environ[timeout] = str(2)
        reseni:dict[int,str] = dict()
        zacatek = time.time()
        hra.hadej_paralelne(reseni,hra.hadana_slova.slova[2000:30000])
        konec = time.time()
        self.assertEqual(round(konec-zacatek),int(os.getenv(timeout)))
        self.assertEqual(len(reseni),0)
        os.environ[timeout] = previous