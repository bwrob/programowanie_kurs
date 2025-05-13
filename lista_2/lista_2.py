from math import gcd

import numpy as np


def algorytm_euklidesa(a: int, b: int) -> int:
    """Oblicz największy wspólny dzielnik a i b za pomocą algorytmu Euklidesa.

    :param a: Pierwsza liczba całkowita
    :param b: Druga liczba całkowita
    :return: Największy wspólny dzielnik a i b
    """
    while b != 0:
        a, b = b, a % b
    return a


def symbol_newtona(n: int, k: int) -> int:
    """Oblicz współczynnik Newtona (n po k) za pomocą podejścia rekurencyjnego.

    :param n: Całkowita liczba elementów
    :param k: Liczba elementów do wybrania
    :return: Współczynnik Newtona (n po k)
    """
    if k in (0, n):
        return 1
    return symbol_newtona(n - 1, k - 1) + symbol_newtona(n - 1, k)


def symbol_newtona_pascal(n: int, k: int) -> int:
    """Oblicz współczynnik Newtona (n po k) za pomocą trójkąta Pascala.

    :param n: Całkowita liczba elementów
    :param k: Liczba elementów do wybrania
    :return: Współczynnik Newtona (n po k)
    """
    pascal = np.zeros((n + 1, n + 1), dtype=int)
    for i in range(n + 1):
        pascal[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            pascal[i][j] = pascal[i - 1][j - 1] + pascal[i - 1][j]
    return int(pascal[n][k])


def symbol_newtona_silnia(n: int, k: int) -> int:
    """Oblicz współczynnik Newtona (n po k) za pomocą silni.

    :param n: Całkowita liczba elementów
    :param k: Liczba elementów do wybrania
    :return: Współczynnik Newtona (n po k)
    """

    def silnia(n: int) -> int:
        """Oblicz silnię n.

        :param n: Liczba całkowita
        :return: Silnia n
        """
        if n == 0:
            return 1
        return n * silnia(n - 1)

    return silnia(n) // (silnia(k) * silnia(n - k))


def xgcd(a: int, b: int) -> tuple[int, int, int]:
    """Rozszerzony algorytm Euklidesa do znalezienia największego wspólnego dzielnika a i b.

    Zwraca NWD oraz współczynniki x i y takie, że ax + by = NWD(a, b).

    :param a: Pierwsza liczba całkowita
    :param b: Druga liczba całkowita
    :return: Krotka zawierająca NWD(a, b), x i y
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def xgcd_rekurencyjnie(a: int, b: int) -> tuple[int, int, int]:
    """Rekurencyjna implementacja rozszerzonego algorytmu Euklidesa.

    :param a: Pierwsza liczba całkowita
    :param b: Druga liczba całkowita
    :return: Krotka zawierająca NWD(a, b), x i y
    """
    if b == 0:
        return a, 1, 0
    d, x, y = xgcd_rekurencyjnie(b, a % b)
    return d, y, x - (a // b) * y


def rownanie_diofantyczne(a: int, b: int, c: int) :
    """Rozwiąż równanie diofantyczne ax + by = c.

    Używając rozszerzonego algorytmu Euklidesa.

    :param a: Pierwszy współczynnik
    :param b: Drugi współczynnik
    :param c: Stała
    :return: Krotka zawierająca x i y
    """
    d, x, y = xgcd(a, b)
    if c % d != 0:
        return None
    return x * c // d, y * c // d


def diofantyczne_nieujemne(a: int, b: int, c: int) -> set[tuple[int, int]]:
    """Rozwiąż równanie diofantyczne ax + by = c z nieujemnymi rozwiązaniami.

    Używając rozszerzonego algorytmu Euklidesa.

    :param a: Pierwszy współczynnik
    :param b: Drugi współczynnik
    :param c: Stała
    :return: Zbiór krotek zawierających wszystkie nieujemne rozwiązania (x, y)
    """
    rozwiazanie = rownanie_diofantyczne(a, b, c)
    if rozwiazanie is None:
        return set()
    x, y = rozwiazanie
    d = algorytm_euklidesa(a, b)
    return {
        (x + k * (b // d), y - k * (a // d))
        for k in range((c // d) + 1)
        if x + k * (b // d) >= 0 and y - k * (a // d) >= 0
    }


def skoczek_alfred(cel: int) -> tuple[str, int]:
    """Określ, czy Alfred może dotrzeć do celu, używając skoków o długości 84 cm lub 228 cm.

    :param cel: Odległość do celu w centymetrach
    :return: Krotka zawierająca cel ("dom" lub "kolega") i minimalną liczbę skoków, lub None, jeśli nie może dotrzeć do celu
    """
    skoki = [84, 228]
    rozwiazania = diofantyczne_nieujemne(skoki[0], skoki[1], cel)
    if rozwiazania:
        min_skoki = min(sum(rozwiazanie) for rozwiazanie in rozwiazania)
        return "dom" if cel == 430 else "kolega", min_skoki
    return None


def lcm(a: int, b: int) -> int:
    """Oblicz najmniejszą wspólną wielokrotność dwóch liczb całkowitych."""
    return a * b // gcd(a, b)


def min_land_parts(k: int) -> int:
    """Oblicz minimalną liczbę części, na które należy podzielić ziemię."""
    result = 1
    for i in range(1,k+1):
        result = lcm(result, i)
    return result


if __name__ == "__main__":
    print(algorytm_euklidesa(10, 5))
    cel_home = 430
    cel_friend = 432

    wynik_home = skoczek_alfred(cel_home)
    wynik_friend = skoczek_alfred(cel_friend)

    if wynik_home:
        print(f"Alfred może dotrzeć do domu w {wynik_home[1]} skokach.")
    elif wynik_friend:
        print(f"Alfred może dotrzeć do kolegi w {wynik_friend[1]} skokaPch.")
    else:
        print("Alfred będzie musiał spać pod gołym niebem.")

    k = 5  # Przykładowa wartość dla k
    print(
        f"Minimalna liczba części, na które należy podzielić ziemię dla {k} dzieci, to: {min_land_parts(k)}",
    )
