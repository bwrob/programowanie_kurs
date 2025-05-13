#!/usr/bin/env python3
"""Provide functions for encoding and decoding messages using a Caesar cipher.

Calculate Levenshtein distance and guess the most similar string from a list.
"""

import time
from collections import Counter
from itertools import permutations
from logging import INFO, Formatter, getLogger

import numpy as np
from rich.logging import RichHandler

log = getLogger(__name__)

# Add a RichHandler to the logger
handler = RichHandler(show_time=False)  # Disable timestamp in RichHandler
handler.setFormatter(Formatter("%(message)s"))
log.addHandler(handler)

__FREQ = {
    "A": 0.099,
    "B": 0.0147,
    "C": 0.0436,
    "D": 0.0325,
    "E": 0.0877,
    "F": 0.003,
    "G": 0.0142,
    "H": 0.0108,
    "I": 0.0821,
    "J": 0.0228,
    "K": 0.0351,
    "L": 0.0392,
    "M": 0.028,
    "N": 0.0572,
    "O": 0.086,
    "P": 0.0313,
    "Q": 0.0014,
    "R": 0.0469,
    "S": 0.0498,
    "T": 0.0398,
    "U": 0.025,
    "V": 0.004,
    "W": 0.0465,
    "X": 0.0002,
    "Y": 0.0376,
    "Z": 0.0653,
}
__CESEAR_MESSAGE = """CNJRYVTNJRYJWRQALZFGNYVQBZH
CNJRYANTBEMRNTNJRYANQBYR
CNJRYFCBXBWALAVRJNQMVYAVXBZH
TNJRYANWQMVXFMRJLZLFYNYFJNJBYR
PVNTYRCBYBJNYCBFJBVZCBXBWH
GBCVRFGBMNWNPZVRQMLFGBYLFGBYXV
TBAVYHPVRXNYJLJENPNYXBMVBYXV
FGEMRYNYVGENOVYVXEMLPMNYQBMABWH"""

__KEYWORDS = {
    "kalafior",
    "rower",
    "krowa",
    "pieczarka",
    "prezydent",
    "usa",
    "pi",
    "sigma",
    "python",
    "naleśniki",
}

__PARALLEL_MESSAGE = "uslppiapniepyrtswczehazdoyrkcnadvientjqlkjeogijpzxczx"

__TEST_MESSAGE = "amaurtcheobwuksa"
__TEST_KEYWORDS = {
    "marchewka",
    "autobus",
}


def koduj(napis: str, klucz: int = 1) -> str:
    start = ord("A")
    letters = ord("Z") - start + 1
    if klucz == 0:
        return napis
    return "".join(
        [chr((ord(litera) - start + klucz) % letters + start) for litera in napis],
    )


def dekoduj(napis: str, klucz: int = 1) -> str:
    return koduj(napis, -klucz)


def test_koduj() -> None:
    assert koduj("A") == "B"
    assert koduj("Z") == "A"
    assert koduj("ALAMAKOTA", 12) == "MXMYMWAFM"
    log.debug("Wszystkie testy przeszły pomyślnie.")


def test_dekoduj() -> None:
    assert dekoduj("B") == "A"
    assert dekoduj("A") == "Z"
    assert dekoduj("MXMYMWAFM", 12) == "ALAMAKOTA"
    log.debug("Wszystkie testy przeszły pomyślnie.")


def porównaj(freq1, freq2):
    delta = 0
    for litera, czestosc in freq1.items():
        if litera not in freq2:
            delta += czestosc
        else:
            delta += abs(czestosc - freq2[litera])
    for litera, czestosc in freq2.items():
        if litera not in freq1:
            delta += czestosc
    return delta


def odległości_dla_kluczy(napis: str) -> dict[int, float]:
    """Funkcja oblicza odległości dla kluczy od 0 do 25."""

    def czestosc_dla_klucza(k: int) -> dict[str, float]:
        """Funkcja oblicza częstości dla danego klucza."""
        counter = Counter(dekoduj(napis, k))
        total = sum(counter.values())
        return {k: v / total for k, v in counter.items()}

    return {
        k: porównaj(
            czestosc_dla_klucza(k),
            __FREQ,
        )
        for k in range(26)
    }


def zad_1() -> None:
    test_koduj()
    test_dekoduj()

    odleglosci_dict = odległości_dla_kluczy(__CESEAR_MESSAGE)
    log.debug("Najmniejsza odległość:")
    min_key = min(odleglosci_dict, key=odleglosci_dict.get)
    log.debug("Klucz %s: %s", min_key, odleglosci_dict[min_key])
    log.info("Zdekodowana wiadomość:")
    log.info(dekoduj(__CESEAR_MESSAGE, min_key))


def levenshtein(napis1: str, napis2: str) -> int:
    """Funkcja oblicza odległość Levenshteina między dwoma napisami."""
    len1, len2 = len(napis1), len(napis2)
    macierz = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        macierz[i][0] = i
    for j in range(len2 + 1):
        macierz[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if napis1[i - 1] == napis2[j - 1]:
                macierz[i][j] = macierz[i - 1][j - 1]
            else:
                macierz[i][j] = min(
                    macierz[i - 1][j] + 1,  # Usunięcie
                    macierz[i][j - 1] + 1,  # Wstawienie
                    macierz[i - 1][j - 1] + 2,  # Zamiana
                )
    log.debug("Macierz:\n%s", np.array(macierz))
    log.debug("Odległość Levenshteina: %s", macierz[len1][len2])
    return macierz[len(napis1)][len(napis2)]


def levenshtein_2(napis1: str, napis2: str) -> int:
    """Funkcja oblicza odległość Levenshteina między dwoma napisami."""
    len1, len2 = len(napis1), len(napis2)
    macierz = np.zeros((len1 + 1, len2 + 1), dtype=int)

    macierz[:, 0] = np.arange(len1 + 1)
    macierz[0, :] = np.arange(len2 + 1)

    for i, j in np.ndindex(len1, len2):
        koszt = 0 if napis1[i] == napis2[j] else 2
        macierz[i + 1, j + 1] = min(
            macierz[i, j + 1] + 1,  # Usunięcie
            macierz[i + 1, j] + 1,  # Wstawienie
            macierz[i, j] + koszt,  # Zamiana
        )

    log.debug("Macierz:\n%s", macierz)
    log.debug(f"Odległość Levenshteina: {macierz[len1, len2]}")

    return macierz[len1, len2]


def guess(napis: str, lista: list[str]) -> str:
    """Funkcja zgaduje, który z napisów jest najbardziej podobny do podanego."""
    odleglosci = [(levenshtein(napis, slowo), slowo) for slowo in lista]
    odleglosci.sort()
    log.debug(f"Odległości: {odleglosci}")

    min_odleglosci = odleglosci[0][0]
    return [slowo for odleglosc, slowo in odleglosci if odleglosc == min_odleglosci]


def zad_2(*, perf_test: int = False) -> None:
    """Funkcja testująca odległość Levenshteina."""
    napis_1 = "Ala ma kota."
    napis_2 = "Olek ma psa."

    if perf_test:
        iterations = 100
        level = log.level
        log.setLevel(INFO)
        # Measure performance of levenshtein
        times_levenshtein = []
        for _ in range(iterations):
            start = time.perf_counter_ns()
            levenshtein(napis_1, napis_2)
            end = time.perf_counter_ns()
            times_levenshtein.append(end - start)

        # Measure performance of levenshtein_2
        times_levenshtein_2 = []
        for _ in range(iterations):
            start = time.perf_counter_ns()
            levenshtein_2(napis_1, napis_2)
            end = time.perf_counter_ns()
            times_levenshtein_2.append(end - start)
        log.setLevel(level)
        log.info("\nPorównanie wydajności:")
        log.info(
            "Levenshtein - Średni czas: %ss, Minimalny czas: %ss",
            np.mean(times_levenshtein),
            np.min(times_levenshtein),
        )
        log.info(
            "Levenshtein_2 - Średni czas: %ss, Minimalny czas: %ss",
            np.mean(times_levenshtein_2),
            np.min(times_levenshtein_2),
        )

    log.info(
        "Odległość Levenshteina między '%s' a '%s':\n%s\n%s",
        napis_1,
        napis_2,
        levenshtein(napis_1, napis_2),
        levenshtein_2(napis_1, napis_2),
    )

    log.info("\nZgadnij, który z napisów jest najbardziej podobny do 'Ala':")
    lista = ["Olek", "Ola", "Ala ma kota"]
    log.info("Lista: %s", lista)
    log.info("Najbardziej podobne napisy:")
    podobne_napisy = guess("Ala", lista)
    log.info(podobne_napisy)


def odplatanie(msg: str, slowa: set[str]) -> list[str]:
    msg_counter = Counter(msg)
    mozliwe_slowa = sorted(
        (slowo for slowo in slowa if Counter(slowo) <= msg_counter),
        key=lambda x: len(x),
    )
    log.info(
        "Słowa po odfiltorwaniu %s %s\n%s",
        len(slowa),
        len(mozliwe_slowa),
        mozliwe_slowa,
    )

    msg_list = list(msg)
    log.info("Wiadomość %s : %s", len(msg_list), msg_list)

    slowa_chars = {char for slowo in mozliwe_slowa for char in slowo}
    log.debug("Litery: %s", slowa_chars)

    msg_list = [litera for litera in msg_list if litera in slowa_chars]
    log.info("Wiadomość po odfiltrowaniu %s : %s", len(msg_list), msg_list)

    results = []
    max_current = 0

    for per in permutations(mozliwe_slowa):
        per_list = msg_list.copy()
        result = []

        for slowo in per:
            slowo_list = per_list.copy()
            for litera in slowo:
                if litera not in slowo_list:
                    break
                slowo_list[slowo_list.index(litera)] = None
            else:
                per_list = slowo_list
                result.append(slowo)

        log.debug("Znalezione slowa: %s", result)
        log.debug("Pozostałe litery: %s", per_list)

        log.debug(sum(len(slowo) for slowo in result))

        assert sum(len(slowo) for slowo in result) == len(
            [c for c in per_list if c is None],
        )

        if len(result) > max_current:
            max_current = len(result)
            log.info("Znaleziono nowy maks %s: %s", max_current, result)
            log.info("Pozostałe litery: %s", per_list)

        results.append(result)
        result = []

    max_slow = max(len(result) for result in results)
    return {tuple(sorted(result)) for result in results if len(result) == max_slow}


def zad_3() -> None:
    znalezione = odplatanie(__PARALLEL_MESSAGE, slowa=__KEYWORDS)
    log.info(
        "znaleziono %s rozwiazań dlugości %s :\n%s",
        len(znalezione),
        len(next(iter(znalezione))) if znalezione else 0,
        znalezione,
    )


if __name__ == "__main__":
    log.setLevel(DEBUG)
    for zadanie in [zad_3]:
        log.info("Zadanie %s".center(20), zadanie.__name__)
        start = time.perf_counter()
        zadanie()
        end = time.perf_counter()
        log.info("Czas wykonania: %s. \n\n\n", round(end - start, 4))
