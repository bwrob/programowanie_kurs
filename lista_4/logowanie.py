import datetime as dt 
import logging

from rich.logging import RichHandler

logger = logging.getLogger("programowanie")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    filename=f"log.txt",
    
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = RichHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Funkcje pomocnicze do zadania 3
def sortowanie_zliczanie_cyfra(lista, cyfra):
    klucze = list(range(10))
    wystapienia = dict.fromkeys(klucze, 0)
    for element in lista:
        cyfra_elementu = (element // 10**cyfra) % 10
        wystapienia[cyfra_elementu] += 1

    pozycje = {}
    poprzednia_suma = 0
    for klucz in klucze:
        pozycje[klucz] = poprzednia_suma
        poprzednia_suma += wystapienia[klucz]

    posortowana = [0] * len(lista)
    for element in lista:
        logger.debug(f"{posortowana}")
        cyfra_elementu = (element // 10**cyfra) % 10
        posortowana[pozycje[cyfra_elementu]] = element
        pozycje[cyfra_elementu] += 1
    return posortowana

def sortowanie_pozycyjne(lista):
    maksimum = max(lista)
    liczba_cyfr = len(str(maksimum))
    for cyfra in range(liczba_cyfr):
        logger.debug(f"Sortowanie cyfra: {cyfra}")
        lista = sortowanie_zliczanie_cyfra(lista, cyfra)
    return lista


def zadanie_3():
    logger.info("Zadanie 3 - Sortowanie pozycyjne")
    lista_pozycyjna = [170, 45, 75, 90, 802, 24, 2, 66]
    logger.info(
        f"Lista do posortowania: {lista_pozycyjna}",
    )
    posortowana = sortowanie_pozycyjne(lista_pozycyjna)
    logger.info(
        f"Posortowana lista: {posortowana}",
    )
if __name__ == "__main__":
    zadanie_3()
