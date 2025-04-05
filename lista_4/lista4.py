import gc
import random
from itertools import repeat
from random import (
    getstate,
    randrange,
    seed,
    setstate,  # Dodane importy
    shuffle,
)
from time import perf_counter


# Funkcje pomocnicze do zadania 1
def inwersje(L):
    inwersje_lista = []
    n = len(L)
    for i in range(n):
        for j in range(i + 1, n):
            if L[i] > L[j]:
                inwersje_lista.append((L[i], L[j]))
    return inwersje_lista


def rangi(L):
    S = sorted(L)
    rangi_lista = []
    for element in L:
        rangi_lista.append(S.index(element))
    return rangi_lista


def zadanie_1():
    L = [1, 5, 2, -1]
    print("Zadanie 1 - Inwersje:", inwersje(L))
    print("Zadanie 1 - Rangi:", rangi(L))


# Funkcje pomocnicze do zadania 2
def sortowanie_zliczanie(
    lista,
    klucze,
):
    wystapienia = dict.fromkeys(klucze, 0)
    for element in lista:
        wystapienia[element] += 1

    pozycje = {}
    poprzednia_suma = 0
    for klucz in klucze:
        pozycje[klucz] = poprzednia_suma
        poprzednia_suma += wystapienia[klucz]

    posortowana = [0] * len(lista)
    for element in lista:
        posortowana[pozycje[element]] = element
        pozycje[element] += 1
    return posortowana


def sortowanie_bąbelkowe(lista, relacja=lambda x, y: x <= y):
    n = len(lista)
    dalej = True
    i = 0
    while dalej:
        dalej = False
        for j in range(n - 1 - i):
            if not relacja(lista[j], lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                dalej = True
        i += 1


def sortowanie_wstawianie(lista, relacja=lambda x, y: x <= y):
    for i in range(1, len(lista)):
        li = lista[i]
        j = i
        while j > 0 and not relacja(lista[j - 1], li):
            lista[j] = lista[j - 1]
            j -= 1
        lista[j] = li


def sortowanie_wybieranie(lista, relacja=lambda x, y: x <= y):
    n = len(lista)
    for i in range(n - 1):
        j = i
        for k in range(i + 1, n):
            if not relacja(lista[j], lista[k]):
                j = k
        if j != i:
            lista[i], lista[j] = lista[j], lista[i]


def sortowanie_scalanie(
    lista,
    relacja=lambda x, y: x <= y,
):
    def scal(lista1, lista2):
        wynik = []
        n1 = len(lista1)
        n2 = len(lista2)
        i1 = 0
        i2 = 0
        while i1 < n1 and i2 < n2:
            if relacja(lista1[i1], lista2[i2]):
                wynik.append(lista1[i1])
                i1 += 1
            else:
                wynik.append(lista2[i2])
                i2 += 1
        return wynik + lista1[i1:] + lista2[i2:]

    n = len(lista)
    if n <= 1:
        return lista.copy()
    k = n // 2
    l1, l2 = lista[:k], lista[k:]
    l1 = sortowanie_scalanie(l1)
    l2 = sortowanie_scalanie(l2)
    return scal(l1, l2)


def zmierz_raz_sortowanie(
    algorytm,
    lista,
    min_time=0.2,
):
    czas = 0
    ile_teraz = 1
    stan_gc = gc.isenabled()
    gc.disable()
    while czas < min_time:
        kopie_list = [lista.copy() for _ in repeat(None, ile_teraz)]
        if ile_teraz == 1:
            start = perf_counter()
            algorytm(kopie_list.pop())
            stop = perf_counter()
        else:
            iterator = repeat(None, ile_teraz)
            start = perf_counter()
            for _ in iterator:
                algorytm(kopie_list.pop())
            stop = perf_counter()
        czas = stop - start
        ile_teraz *= 2
    if stan_gc:
        gc.enable()
    return czas / ile_teraz


def zmierz_min_sortowanie(
    algorytm,
    lista,
    serie_min=5,
    min_time=0.2,
):
    pomiary = []
    generator = getstate()
    seed()
    my_seed = randrange(1000)
    for _ in repeat(None, serie_min):
        seed(my_seed)
        pomiary.append(zmierz_raz_sortowanie(algorytm, lista, min_time=min_time))
    setstate(generator)
    return min(pomiary)


def zmierz_sortowanie(
    algorytm,
    lista,
    serie_median=10,
    serie_min=5,
    min_time=0.2,
):
    pomiary = []
    lista = lista.copy()
    for _ in repeat(None, serie_median):
        shuffle(lista)
        pomiary.append(
            zmierz_min_sortowanie(
                algorytm,
                lista,
                serie_min=serie_min,
                min_time=min_time,
            ),
        )
    pomiary.sort()
    if serie_median % 2 == 0:
        return (pomiary[serie_median // 2 - 1] + pomiary[serie_median // 2]) / 2
    return pomiary[serie_median // 2]


def zadanie_2():
    lista_losowa = [random.choice(range(10)) for _ in range(1000)]
    klucze = list(range(10))

    czas_zliczanie = zmierz_sortowanie(
        lambda l: sortowanie_zliczanie(l, klucze),
        lista_losowa,
    )
    czas_babelkowe = zmierz_sortowanie(lambda l: sortowanie_bąbelkowe(l), lista_losowa)
    czas_wstawianie = zmierz_sortowanie(
        lambda l: sortowanie_wstawianie(l),
        lista_losowa,
    )
    czas_wybieranie = zmierz_sortowanie(
        lambda l: sortowanie_wybieranie(l),
        lista_losowa,
    )
    czas_scalanie = zmierz_sortowanie(lambda l: sortowanie_scalanie(l), lista_losowa)

    print("Zadanie 2 - Czas sortowania przez zliczanie:", czas_zliczanie)
    print("Zadanie 2 - Czas sortowania bąbelkowego:", czas_babelkowe)
    print("Zadanie 2 - Czas sortowania przez wstawianie:", czas_wstawianie)
    print("Zadanie 2 - Czas sortowania przez wybieranie:", czas_wybieranie)
    print("Zadanie 2 - Czas sortowania przez scalanie:", czas_scalanie)


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
        cyfra_elementu = (element // 10**cyfra) % 10
        posortowana[pozycje[cyfra_elementu]] = element
        pozycje[cyfra_elementu] += 1
    return posortowana


def sortowanie_pozycyjne(lista):
    maksimum = max(lista)
    liczba_cyfr = len(str(maksimum))
    for cyfra in range(liczba_cyfr):
        lista = sortowanie_zliczanie_cyfra(lista, cyfra)
    return lista


def zadanie_3():
    lista_pozycyjna = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Zadanie 3 - Posortowana lista:", sortowanie_pozycyjne(lista_pozycyjna))


if __name__ == "__main__":
    zadanie_1()
    zadanie_2()
    zadanie_3()
