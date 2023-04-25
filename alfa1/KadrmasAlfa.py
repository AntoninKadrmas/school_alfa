from functools import partial
from package.Nastaveni import Nastaveni
from package.KadrmasHadanka import KadrmasovaHadanka, KadrmasovaHra
import multiprocessing

if __name__ == "__main__":
    print('Vytejte v hadance kde napisete vetu kterou pocitac nasledne uhodne.')
    print('Veta muze obsahovat pouze anglicka slova (program muzete ucit slova ktera nezna).')
    print('Veta nesmi obsahovat zadne specialni znaky. Nerozlisuji se velka a mala pismena.')
    hra = KadrmasovaHra()
    while (True):
        veta = input('Zadejte hadanou vetu: ')
        try:
            hadanka = KadrmasovaHadanka(veta, hra.hadana_slova)
            hra.hraj(hadanka)
            break
        except Exception as e:
            vyjmka = str(e).split(' ')
            if(vyjmka[3]=='' or len(vyjmka[3])==0):
                print('Veta musi obsahovat nejake slova')
            else:
                print(e)
                if vyjmka[-3] == 'neexistuje':
                    odpoved = ''
                    while odpoved.lower().strip() != 'a' and odpoved.lower().strip() != 'n':
                        odpoved = input(
                            f'Chcete slovo {vyjmka[3]} pridat do slovniku a/n (a => ano/n => ne):')
                    else:
                        if odpoved == 'a':
                            hra.hadana_slova.zapis_nove_slovo(vyjmka[3])

    pocet_procesu = Nastaveni.get_pocet_procesu()
    manager = multiprocessing.Manager()
    reseni = manager.dict()
    pool = multiprocessing.Pool(pocet_procesu)

    paralelni_funcke = partial(hra.hadej_paralelne, reseni)
    pool.map(paralelni_funcke, [hra.hadana_slova.slova[len(hra.hadana_slova.slova)//pocet_procesu *
             x:len(hra.hadana_slova.slova)//pocet_procesu*(x+1)] for x in range(pocet_procesu)])

    if (len(reseni.values()) != len(hra.hadanka.slova)):
        raise Exception(
            'Casovy limit vyprsel a program nestihl uhodnout vsechny slova hadanky.')
    vysledna_veta = ' '.join([reseni[pozice]
                             for pozice in range(len(reseni.values()))])
    print(f"Pocet slov: {len(reseni)}/{len(reseni)}")
    print(f"{hra.hadanka.veta} <== Zadana veta")
    print(f"{vysledna_veta} <== Vysledna veta")
    print(f"Rovna se vysledna veta zadane vete => {hra.hadanka.hadej_vetu(vysledna_veta)}")
