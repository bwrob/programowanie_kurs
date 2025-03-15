import math
import random
from time import perf_counter_ns

import matplotlib.pyplot as plt
import numpy as np


def find_min_v1(data: list[int]) -> int | None:
    """Wersja 1: Iteracja po liście i porównywanie z aktualnym minimum."""
    if not data:
        return None
    min_val = data[0]
    for item in data:
        min_val = min(min_val, item)
    return min_val


def find_min_v2(data: list[int]) -> int | None:
    """Wersja 2: Iteracja z użyciem indeksów."""
    if not data:
        return None
    min_val = data[0]
    for i in range(1, len(data)):
        min_val = min(min_val, data[i])
    return min_val


def find_min_v3(data: list[int]) -> int | None:
    """Wersja 3: Użycie 'while'."""
    if not data:
        return None
    min_val = data[0]
    i = 1
    while i < len(data):
        min_val = min(min_val, data[i])
        i += 1
    return min_val


def find_min_v4(data: list[int]) -> int | None:
    """Wersja 4: Użycie enumerate."""
    if not data:
        return None
    min_val = data[0]
    for index, item in enumerate(data):
        if index == 0:
            continue
        min_val = min(min_val, item)
    return min_val


def measure_time(func, repeat=1):
    """Mierzy czas wykonania funkcji."""

    def worker(*args, **kwargs):
        start_time = perf_counter_ns()
        for _ in range(repeat):
            func(*args, **kwargs)
        end_time = perf_counter_ns()
        return (end_time - start_time) / repeat

    return worker


def generate_data(size: int, data_type: str, str_len: int = 1) -> list:
    """Generuje dane testowe."""
    if data_type == "int":
        return [random.randint(0, size) for _ in range(size)]
    if data_type == "str":
        return [
            "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=str_len))
            for _ in range(size)
        ]


def plot_results(
    results: dict[str, list[float]],
    x_values: list[int],
    title: str,
    x_label: str,
    y_label: str = "Czas [s]",
) -> None:
    """Rysuje wykres wyników."""
    plt.figure(figsize=(10, 6))
    for func_name, times in results.items():
        plt.plot(x_values, times, label=func_name)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


def atan_minus_1(x):
    return math.atan(x) - 1


def bisection(func, a: float, b: float, tol=1e-9, max_iter=1000):
    """Znajduje miejsce zerowe funkcji f metodą bisekcji.

    Args:
        a: Lewy koniec przedziału.
        b: Prawy koniec przedziału.
        tol: Tolerancja (dokładność).
        max_iter: Maksymalna liczba iteracji.

    Returns:
        Przybliżone miejsce zerowe lub None, jeśli nie znaleziono.

    """
    if func(a) * func(b) >= 0:
        return None  # Brak gwarancji istnienia miejsca zerowego

    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(func(c)) < tol:
            return c
        if func(c) * func(a) < 0:
            b = c
        else:
            a = c
    return None


def sasiedztwo(A: np.ndarray, r: int, i: int, j: int) -> np.ndarray:
    """Zwraca elementy należące do sąsiedztwa elementu A[i, j] o promieniu r.

    Args:
        A: Dwuwymiarowa tablica NumPy.
        r: Promień sąsiedztwa.
        i: Indeks wiersza elementu.
        j: Indeks kolumny elementu.

    Returns:
        Wycinek tablicy A zawierający sąsiedztwo elementu A[i, j].

    """
    n, m = A.shape
    i_min = max(0, i - r)
    i_max = min(n, i + r + 1)
    j_min = max(0, j - r)
    j_max = min(m, j + r + 1)
    return A[i_min:i_max, j_min:j_max]


def maksima_lokalne_wycinki(A: np.ndarray) -> list[tuple[int, int]]:
    """Znajduje wszystkie maksima lokalne w tablicy A, używając wycinków tablicy.

    Args:
        A: Dwuwymiarowa tablica NumPy.

    Returns:
        Lista par współrzędnych maksimów lokalnych.

    """
    n, m = A.shape
    maksima = []
    for i in range(n):
        for j in range(m):
            sasiedzi = sasiedztwo(A, 1, i, j)
            if np.all(A[i, j] >= sasiedzi):
                maksima.append((i, j))
    return maksima


def czy_jednomodalna(A: np.ndarray) -> bool:
    """Sprawdza, czy tablica A jest jednomodalna.

    Args:
        A: Dwuwymiarowa tablica NumPy.

    Returns:
        True, jeśli tablica jest jednomodalna, False w przeciwnym razie.

    """
    maksima = maksima_lokalne_wycinki(A)
    return len(maksima) == 1
