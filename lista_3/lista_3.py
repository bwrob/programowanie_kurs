def suma_dzielnikow(n):
    suma = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            suma += i
            if i * i != n:
                suma += n // i
    return suma


def liczby_doskonale(N):
    doskonale = []
    for i in range(2, N):
        if suma_dzielnikow(i) == i:
            doskonale.append(i)
    return doskonale


def pary_zaprzyjaznione(N):
    pary = []
    for a in range(1, N):
        b = suma_dzielnikow(a)
        if a < b and suma_dzielnikow(b) == a and b < N:
            pary.append((a, b))
    return len(pary)


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
    liczby = list(range(1, k + 1))
    wykreslone = set()
    for i in range(1, k + 1):
        for j in range(i, k + 1):
            liczba = i + j + 2 * i * j
            if liczba <= k:
                wykreslone.add(liczba)
    pierwsze = [2] + [2 * i + 1 for i in liczby if i not in wykreslone]
    return [p for p in pierwsze if p < N]


def sito_sundarama2(N):
    k = (N - 2) // 2
    liczby = list(range(1, k + 1))
    wykreslone = set()
    for i in range(1, k + 1):
        j = i
        while i + j + 2 * i * j <= k:
            wykreslone.add(i + j + 2 * i * j)
            j += 1
    pierwsze = [2] + [2 * i + 1 for i in liczby if i not in wykreslone]
    return [p for p in pierwsze if p < N]


def zadanie_1():
    print(liczby_doskonale(100))


def zadanie_2():
    print(pary_zaprzyjaznione(10_000))


def zadanie_3():
    import time

    N = 100_000
    start = time.time()
    eratosthenes_primes = sito_eratostenesa(N)
    end = time.time()
    print(f"Sito Eratostenesa: {end - start:.4f} s")

    start = time.time()
    sundaram_primes = sito_sundarama(N)
    end = time.time()
    print(f"Sito Sundarama: {end - start:.4f} s")

    start = time.time()
    sundaram_primes2 = sito_sundarama2(N)
    end = time.time()
    print(f"Sito Sundarama z optymalizacją: {end - start:.4f} s")


if __name__ == "__main__":
    zadanie_1()
    zadanie_2()
    zadanie_3()
