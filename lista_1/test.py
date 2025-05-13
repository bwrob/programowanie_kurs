from random import choice, choices, randint

from rich import print

if __name__ == "__main__":
    n=20
    lista_int = [randint(0,10) for _ in range(n)]
    lista_abc = [choice("abc") for _ in range(n)]
    lista_ab = choices("ab", weights=[5,95], k=n)

    print(
        lista_int,
        lista_abc,
        lista_ab,
    )
