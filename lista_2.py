import rich


def algorytm_euklidesa(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def symbol_newtona(n: int, k: int) -> int:
    if k == 0 or k == n:
        return 1
    return symbol_newtona(n - 1, k - 1) + symbol_newtona(n - 1, k)


def symbol_newtona_pascal(n: int, k: int) -> int:
    pascal = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        pascal[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            pascal[i][j] = pascal[i - 1][j - 1] + pascal[i - 1][j]
    rich.print(pascal)
    return pascal[n][k]


def symbol_newtona_silnia(n: int, k: int) -> int:
    def silnia(n: int) -> int:
        if n == 0:
            return 1
        return n * silnia(n - 1)

    return silnia(n) // (silnia(k) * silnia(n - k))


if __name__ == "__main__":
    print(algorytm_euklidesa(10, 5))
    print(algorytm_euklidesa(14, 7))
    print(algorytm_euklidesa(21, 14))

    for newton in [symbol_newtona, symbol_newtona_pascal, symbol_newtona_silnia]:
        print(newton(4, 2))
        print(newton(5, 2))
        print(newton(7, 3))
        print(newton(10, 5))
