from package.Template import Hadanka, Hra
from package.Nastaveni import Nastaveni
from multiprocessing import Lock
import os

import random
import time


class PovolenaSlova:
    def __init__(self) -> None:
        """
        Konstruktor ma z ukol nacist z souboru slovnik dovolenych slov.
        """
        if Nastaveni.get_pouzit_soubor() == 'big':
            self.slova = [line.replace('\n', '') for line in open('data/chunk_words.txt')]  # 370000 slov
        else:
            self.slova = [line.replace('\n', '') for line in open('data/words.txt')]  # 30000 slova
        if int(Nastaveni.get_delka_slova()) != -1:
            self.slova = list(filter(lambda x: len(
                x) <= int(Nastaveni.get_delka_slova()), self.slova))

    def existuje_slovo(self, slovo: str) -> bool:
        """
        Metoda ma zaukol zkontrolovat zdali slovo existuje v slovniku dovolenych slov

        :param slovo: slovo ktere se hleda v slovniku
        :return: true pokud slovo existuje false pokud slovo neexistuje
        """
        return True if slovo.lower() in self.slova else False

    def zapis_nove_slovo(self, slovo: str):
        """
        Metoda ma za ukol zapsat nove slovo do souboru pouzivaneho slovniku.
        
        :param slovo: slovo ktere se zapisuje do slovniku
        """
        if Nastaveni.get_pouzit_soubor() == 'big':
            with open('data/chunk_words.txt', 'at') as soubor:
                soubor.write(slovo.lower().strip()+'\n')
        else:
            with open('data/words.txt', 'at') as soubor:
                soubor.write(slovo.lower().strip()+'\n')


class KadrmasovaHadanka(Hadanka):
    def __init__(self, veta: str, povolena_slova:PovolenaSlova) -> None:
        """
        Konstruktor ma za ukol zkontrolovat spravnost slov ve vete, rozelati vetu na slova
        a ulozit pouzivana slova.

        :param veta: veta hadanky kterou bude pocitac hadat
        :param povolena_slova: viz PovolenaSlova
        """
        veta = veta.lower().strip()
        self.povolena_slova: PovolenaSlova = povolena_slova
        self.slova = list(filter(lambda x: x != "", veta.split(' ')))
        if len(self.slova)==0:raise Exception('Veta musi obsahovat alespon jendno slovo.')
        self.veta = ' '.join(self.slova)
        self.hadej_vetu(self.veta)

    def pocet_slov(self) -> list:
        """
        Metoda ma za ukol vratit pocet slov ve vete.

        :return: cislo reprezentujici pocet slov ve vete
        """
        return len(self.slova)

    def hadej_slovo(self, slovo: str) -> list[int]:
        """
        Metoda ma za ukol vratit vsechny viskyty hadaneho slova.

        :param slovo: hadane slovo
        :return: list cisel reprezentujici vsechna mista (indexy) na kterych se slovo ve vete vyskytuje
        """
        slovo = slovo.lower().strip()
        vysledek = self.kontrola([slovo])
        if vysledek[0]:
            raise Exception(f"Slovo {vysledek[1][0]} je chybne")
        indexy_slov = []
        try:
            index = self.slova.index(slovo)
            while (True):
                indexy_slov.append(index)
                index = self.slova.index(
                    slovo, indexy_slov[len(indexy_slov)-1]+1)
        except:
            return indexy_slov

    def hadej_vetu(self, veta: str) -> bool:
        """
        Metoda ma za ukol porovnat hadanou vetu se zadanou vetou.

        :param veta: hadana veta
        :return: True pokud se hadana veta a zadana veta rovnaji False v opacnem pripade
        """
        veta = veta.lower().strip()
        vysledek = self.kontrola(list(filter(lambda x: x != "", veta.split(' '))))
        if vysledek[0]:
            if vysledek[1][1] != -1 and len(vysledek[1][0]) > vysledek[1][1]:
                raise Exception(
                    f"Veta obshuje slovo {vysledek[1][0]} ktere prekracuje limit ({vysledek[1][1]}) delky slova")
            else:
                raise Exception(
                    f"Veta obshuje slovo {vysledek[1][0]} ktere neexistuje v slovniku")
        return True if veta == self.veta else False

    def kontrola(self, slova:list[str]) -> bool:
        """
        Metoda ma za ukol zkontrolovat zdali vsechna slova splnuji vsechny podminky:
        1. delka slova odpovida limitu
        2. slovo existuje ve slovniku

        :param slova: list hadanych slov
        :return: True pokud se mezi hadanymi slov nenasla chyba False v opacnem pripade
        """
        for slovo in slova:
            if not self.povolena_slova.existuje_slovo(slovo) or \
                    (len(slovo) > Nastaveni.get_delka_slova() and Nastaveni.get_delka_slova() != -1):
                return (True, [slovo, Nastaveni.get_delka_slova()])
        else:
            return (False,)


class KadrmasovaHra(Hra):
    def __init__(self) -> None:
        """
        Konstruktor ma za ukol zalozit instanci PovolenaSlova a popripade z ni vyfiltrovat
        slova ktera neodpovidaji limitu.
        """
        self.hadana_slova = PovolenaSlova()
        self.hadanka: KadrmasovaHadanka = None

    def hraj(self, hadanka: KadrmasovaHadanka) -> None:
        """
        Metoda ma za ukol priradit parametru tridy hodnotu instance tridy KadrmasovaHadanka.

        :param hadanka: instance tridy KadrmasovaHadanka
        """
        if not isinstance(hadanka,KadrmasovaHadanka):raise Exception('Hadanka musi byt instance tridy kadrmasova hadanka')
        self.hadanka = hadanka

    def hadej_paralelne(self, reseni: dict[int,str], slova: list[str]) -> None:
        """
        Metoda ma za ukol nahodne hadat slova za pomoci kolekce slova. Metoda skonci ve chvili kdy
        se pocet prvku v reseni bude rovnat poctu slov v hadance nebo ve chvili kdy prekroci casovy limit.

        :param reseni: dictionary do ktere se ukladaji uhodnuta slova(value) a jejich pozice(key)
        :param slova: list obsahujici slova z kterych bude pocitac hadat hadanku    
        """
        if len(slova) == 0:raise Exception('List hadanych slov nesmi byt prazdny')
        start_time = time.time()
        limit = Nastaveni.get_casovy_limit()
        for x in range(len(slova)):
            if len(reseni) == self.hadanka.pocet_slov() or \
                    (time.time()-start_time >= limit and limit != -1):
                return
            print(f"Pocet slov: {len(reseni)}/{self.hadanka.pocet_slov()}")
            nahodne_cislo = random.randint(0, len(slova)-1)
            hadane_slovo = slova[nahodne_cislo]
            vysledeky = self.hadanka.hadej_slovo(hadane_slovo)
            lock = Lock()
            lock.acquire()
            for vysledek in vysledeky:
                reseni[vysledek] = hadane_slovo
            lock.release()
            del slova[nahodne_cislo]

