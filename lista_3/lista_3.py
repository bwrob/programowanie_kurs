#!/usr/bin/env python3

from rich import print


class SitoEratostenesaCache:
    def __init__(self) -> None:
        self._N_DLA_SITA = 2
        self._WYNIK_SITA = [2]
        self._SITO = [None, None, 2]

    def get_primes(self, N):
        if N == self._N_DLA_SITA:
            return self._WYNIK_SITA.copy()
        if N < self._N_DLA_SITA:
            return [x for x in self._WYNIK_SITA if x <= N]
        self._SITO += list(range(self._N_DLA_SITA + 1, N + 1))
        for p in self._SITO:
            if p is None:
                continue
            if p * p > N:
                break
            for x in range(max(p, (self._N_DLA_SITA // p + 1)) * p, N + 1, p):
                self._SITO[x] = None
        self._WYNIK_SITA = [x for x in self._SITO if x is not None]
        self._N_DLA_SITA = N
        return self._WYNIK_SITA.copy()


sito_cache = SitoEratostenesaCache()


def czyniki_pierwsze_cache(n):
    czynniki = {}
    for p in sito_cache.get_primes(n + 1):
        wykladnik = 0
        while n % p == 0:
            wykladnik += 1
            n //= p
        if wykladnik > 0:
            czynniki[p] = wykladnik
    return czynniki


def czyniki_pierwsze(n):
    czynniki = {}
    for p in sito_eratostenesa(n + 1):
        wykladnik = 0
        while n % p == 0:
            wykladnik += 1
            n //= p
        if wykladnik > 0:
            czynniki[p] = wykladnik
    return czynniki


def dzielniki(n):
    czynniki = czyniki_pierwsze_cache(n)
    dzielniki = [1]
    for p, k in czynniki.items():
        nowe_dzielniki = []
        for dzielnik in dzielniki:
            for i in range(1, k + 1):
                nowe_dzielniki.append(dzielnik * p**i)
        dzielniki.extend(nowe_dzielniki)
    return dzielniki


def suma_dzielnikow(n):
    return sum(dzielniki(n)[:-1])


def suma_dzielnikow_naiwna(n):
    suma = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            suma += i
            if i * i != n:
                suma += n // i
    return suma


def liczby_doskonale(N):
    doskonale = []
    for i in range(N, 2, -1):
        if suma_dzielnikow(i) == i:
            doskonale.append(i)
    return doskonale


def pary_zaprzyjaznione_cache(N):
    pary = []
    sumy = [0]*N
    for a in range(N):
        b = suma_dzielnikow(a)
        sumy[a] = b
        if b < a and sumy[b] == a:
            pary.append((a, b))
    return pary

def pary_zaprzyjaznione(N):
    pary = []
    for a in range(1, N):
        b = suma_dzielnikow(a)
        if a < b and suma_dzielnikow(b) == a and b < N:
            pary.append((a, b))
    return pary


def sito_eratostenesa(N):
    czy_pierwsza = [True] * N
    czy_pierwsza[0] = czy_pierwsza[1] = False
    for p in range(2, int(N**0.5) + 1):
        if czy_pierwsza[p]:
            for i in range(p * p, N, p):
                czy_pierwsza[i] = False
    return [p for p in range(2, N) if czy_pierwsza[p]]


def sito_sundarama(N):
    k = (N - 2) // 2
    liczby = [True] * (k + 1)
    for i in range(1, k + 1):
        for j in range(1, k + 1):
            liczba = i + j + 2 * i * j
            if liczba <= k:
                liczby[liczba] = False
    pierwsze = [2] + [2 * i + 1 for i in range(1, k) if liczby[i]]
    return [p for p in pierwsze if p < N]


def sito_sundarama2(N):
    k = (N - 2) // 2
    liczby = [True] * (k + 1)
    for i in range(1, int((k + 1) ** 0.5) + 1):  # Optimized range for i
        for j in range(i, (k - i) // (2 * i + 1) + 1):  # Optimized range for j
            liczby[i + j + 2 * i * j] = False
    pierwsze = [2] + [2 * i + 1 for i in range(1, k) if liczby[i]]
    return [p for p in pierwsze if p < N]


def zadanie_1() -> None:
    n = 10_000
    #print(czyniki_pierwsze(n))
    # print(dzielniki(n))
    #print(suma_dzielnikow(n))
    #print(suma_dzielnikow_naiwna(n))
    print(liczby_doskonale(n))


def zadanie_2() -> None:
    import time
    n = 10_000
    methods = [pary_zaprzyjaznione, pary_zaprzyjaznione_cache,]

    m = 5  # Number of repetitions
    padding = max(len(method.__name__) for method in methods)
    for method in methods:
        total_time = 0
        for _ in range(m):
            start = time.perf_counter_ns()
            _ = method(n)
            end = time.perf_counter_ns()
            total_time += end - start
        avg_time = total_time / m
        print(f"{method.__name__.ljust(padding)}: {str(avg_time).rjust(15)} ns")

    #print(pary_zaprzyjaznione(n))
    print(pary_zaprzyjaznione_cache(n))


def zadanie_3() -> None:
    import time

    n = 1_000
    methods = [sito_eratostenesa, sito_sundarama, sito_sundarama2]

    results = {}
    m = 100  # Number of repetitions
    padding = max(len(method.__name__) for method in methods)
    for method in methods:
        total_time = 0
        for _ in range(m):
            start = time.perf_counter_ns()
            results[method.__name__] = method(n)
            end = time.perf_counter_ns()
            total_time += end - start
        avg_time = total_time / m
        print(f"{method.__name__.ljust(padding)}: {str(avg_time).rjust(15)} ns")

    print(results[sito_eratostenesa.__name__] == results[sito_sundarama.__name__])
    print(results[sito_eratostenesa.__name__] == results[sito_sundarama2.__name__])


if __name__ == "__main__":
    zadanie_1()
    zadanie_2()
    zadanie_3()
