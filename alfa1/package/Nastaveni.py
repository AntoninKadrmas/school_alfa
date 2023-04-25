import os
from dotenv import load_dotenv
import multiprocessing


class Nastaveni:
    load_dotenv()
    def get_pouzit_soubor():
        """
        Metoda pro urceni jaky ze dvou souboru by se mel pri hadani pouzit.
        Pro rozhodnuti vyuziva enviroment hodnotu USED_FILE nastavenou v souboru .env

        :return: vraci hodnoty 'small' pro soubor s 30000 slov a 'big' pro soubor s 370000 slov
        """
        if os.getenv('USED_FILE') == None:
            return 'small'  # neexistuje paramter
        pouzit_soubor = os.getenv('USED_FILE').lower().strip()
        if pouzit_soubor != 'small' and pouzit_soubor != 'big':
            raise Exception(
                'V souobru .env je chybne nastavena hodnota parametru USED_FILE')
        else:
            return pouzit_soubor

    def get_delka_slova():
        """
        Metoda pro urceni maximalni delky jednotlivych zadavanych/hadanych slov.
        Pro rozhodnuti vyuziva enviroment hodnotu WORD_LENGTH nastavenou v souboru .env

        :return: vraci hodnotu nezaporneho zakladniho cisla predstavujic maximalni delku nebo 
        hodnotu -1 pomoci niz se maximalni delka slova v programu nebude brat v potaz
        """
        delka_slova = os.getenv('WORD_LENGTH').lower().strip()
        try:
            if delka_slova != 'infinite':
                int(delka_slova)
        except:
            raise Exception(
                'V souobru .env je chybne nastavena hodnota parametru WORD_LENGTH')
        if delka_slova == 'infinite':
            return -1
        elif int(delka_slova) <= 0:
            return -1
        else:
            return int(delka_slova)

    def get_casovy_limit():
        """
        Metoda pro urceni maximalni delky behu algoritmu od zacatku hledani.
        Pro rozhodnuti vyuziva enviroment hodnotu TIMEOUT nastavenou v souboru .env

        :return: vraci hodnotu nezaporneho zakladniho cisla predstavujic maximalni delku nebo 
        hodnotu -1 pomoci niz se maximalni delka behu programu nebude brat v potaz
        """
        casovy_limit = os.getenv('TIMEOUT').lower().strip()
        try:
            if casovy_limit != 'infinite':
                int(casovy_limit)
        except:
            raise Exception(
                'V souobru .env je chybne nastavena hodnota parametru TIMEOUT')
        if casovy_limit == 'infinite':
            return -1
        elif int(casovy_limit) <= 0:
            return -1
        else:
            return int(casovy_limit)

    def get_pocet_procesu():
        """
        Metoda pro urceni poctu procesu na kterych se bude asynchrone hadat.
        Pro rozhodnuti vyuziva enviroment hodnotu PROCES_AMOUNT nastavenou v souboru .env

        :return: vraci hodnotu zakladniho cisla, ktere je mensi nebo rovno poctu cpu v pocitaci
        """
        max_pocet_procesu = multiprocessing.cpu_count()
        if os.getenv('PROCES_AMOUNT') == None:
            return max_pocet_procesu  # neexistuje parametr
        pocet_procesu = os.getenv('PROCES_AMOUNT').lower().strip()
        try:
            if pocet_procesu != 'auto':
                int(pocet_procesu)
        except:
            raise Exception(
                'V souboru .env je chybne nasatvena hodnota parametru PROCES_COUNT')
        if pocet_procesu == 'auto':
            return max_pocet_procesu
        elif int(pocet_procesu) > max_pocet_procesu or int(pocet_procesu) <= 0:
            return max_pocet_procesu
        else:
            return int(pocet_procesu)
