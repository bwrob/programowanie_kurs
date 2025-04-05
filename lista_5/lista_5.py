from collections import Counter

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
__MESSAGE = """CNJRYVTNJRYJWRQALZFGNYVQBZH
CNJRYANTBEMRNTNJRYANQBYR
CNJRYFCBXBWALAVRJNQMVYAVXBZH
TNJRYANWQMVXFMRJLZLFYNYFJNJBYR
PVNTYRCBYBJNYCBFJBVZCBXBWH
GBCVRFGBMNWNPZVRQMLFGBYLFGBYXV
TBAVYHPVRXNYJLJENPNYXBMVBYXV
FGEMRYNYVGENOVYVXEMLPMNYQBMABWH"""


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


def test_koduj():
    assert koduj("A") == "B"
    assert koduj("Z") == "A"
    assert koduj("ALAMAKOTA", 12) == "MXMYMWAFM"
    print("Wszystkie testy przeszły pomyślnie.")


def test_dekoduj():
    assert dekoduj("B") == "A"
    assert dekoduj("A") == "Z"
    assert dekoduj("MXMYMWAFM", 12) == "ALAMAKOTA"
    print("Wszystkie testy przeszły pomyślnie.")


def porównaj(freq1, freq2):
    delta = 0
    for litera, częstość in freq1.items():
        if litera not in freq2:
            delta += częstość
        else:
            delta += abs(częstość - freq2[litera])
    for litera, częstość in freq2.items():
        if litera not in freq1:
            delta += częstość
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


def zad_1():
    odleglosci_dict = odległości_dla_kluczy(__MESSAGE)
    print("Odległości dla kluczy:")
    for k, v in odleglosci_dict.items():
        print(f"Klucz {k}: {v}")
    print("Najmniejsza odległość:")
    min_key = min(odleglosci_dict, key=odleglosci_dict.get)
    print(f"Klucz {min_key}: {odleglosci_dict[min_key]}")
    print("Zdekodowana wiadomość:")
    print(dekoduj(__MESSAGE, min_key))


if __name__ == "__main__":
    test_koduj()
    test_dekoduj()
    zad_1()
