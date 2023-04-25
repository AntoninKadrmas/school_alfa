Pro supštěni programu spusťte soubor KadrmasAlfa.py.
Program vas an začátku vyzve pro zadání věty ktrou bude počítač hádat.
Pravidla zadané věty:
1. Mouhou se zadávat pouze anglická slova.
2. nesmí se používat zkrácené výrazy jako je I'am nebo can'ta
3. ve větě se nesmí použít žádná interpunkce nebo jiné speciální znaky
3.1. to znamená že jsou povoleny pouze pismena a-z
4. slova ve větě nejsou case sensitive 
5. věta musí obsahovat alespoň jedno slovo
6. program nepropustí slova která nezná (slova se do slovníku dají přidávat)
Poté co je zadána věta splňující všechny požadavky program se spustí a začne hadat větu.

Konfigurace v souboru .env
    TIMEOUT => povinný parametr
        - parametr timeout určuje dobu za jak dlouho (v sekundách) počítač vzdá hledání výsledné věty
        - může nabívat hodnotu přirozeného čísla nebo hodnotu 'infinite' (př: TIMEOUT=infinite,TIMEOUT=10)
    WORD_LENGTH => povinný parametr
        - parametr určuje maximální hodnotu jednotlivých slov použitých v hádance
        - může nabívat hodnotu přirozeného čísla nebo hodnotu 'infinite' (př: WORD_LENGTH=infinite,WORD_LENGTH=10)
    USED_FILE => nepoviný parametr (defaultní hodnota = small)
        - parametr určuje jaký z dvou souboru se bude používat pro hádání věty
        - může nabývat hodnoty 'small'(30000 slov) a 'big' (370000 slov) (př: USED_FILE=big,USED_FILE=small)
    PROCES_AMOUNT => nepoviný parametr (defaultní hodnota = auto)
        - parametr určuje kolik procesu program spustí asinchroně v jednom poolu
        - může nabívat hodnotu přirozeného čísla nebo hodnotu 'auto' ('auto' => maximální počet procesů)
        - hodnota nemůže být vězší jak maximální počet procesů (př: PROCES_AMOUNT=auto,PROCES_AMOUNT=4)

pro spuštění testů je potřeba ve složce /test spustit soubor test.py


textové soubory jsou knihovny seznami stažené z git repositářů
https://github.com/derekchuank/high-frequency-vocabulary used 30k dictionary
https://github.com/dwyl/english-words/blob/master/words_alpha.txt used 370k dictionary
