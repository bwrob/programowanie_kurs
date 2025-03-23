import random
import time
from collections.abc import Callable

import matplotlib.pyplot as plt


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


def measure_time(func: Callable[[list[int]], int | None], data: list[int]) -> float:
    """Mierzy czas wykonania funkcji."""
    start_time = time.time()
    func(data)
    end_time = time.time()
    return end_time - start_time


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


def run_tests(data_types: list[str], str_lens: list[int] | None = None) -> None:
    """Uruchamia testy dla różnych typów danych."""
    list_sizes = [10, 100, 1000, 10000, 20000]

    for data_type in data_types:
        if data_type == "int":
            results = {
                "v1": [],
                "v2": [],
                "v3": [],
                "v4": [],
            }
            for size in list_sizes:
                data = generate_data(size, data_type)
                results["v1"].append(measure_time(find_min_v1, data))
                results["v2"].append(measure_time(find_min_v2, data))
                results["v3"].append(measure_time(find_min_v3, data))
                results["v4"].append(measure_time(find_min_v4, data))
            plot_results(
                results,
                list_sizes,
                "Czas działania algorytmów dla list liczb",
                "Długość listy",
            )
        elif data_type == "str":
            for str_len in str_lens:
                results = {
                    "v1": [],
                    "v2": [],
                    "v3": [],
                    "v4": [],
                }
                for size in list_sizes:
                    data = generate_data(size, data_type, str_len)
                    results["v1"].append(measure_time(find_min_v1, data))
                    results["v2"].append(measure_time(find_min_v2, data))
                    results["v3"].append(measure_time(find_min_v3, data))
                    results["v4"].append(measure_time(find_min_v4, data))
                plot_results(
                    results,
                    list_sizes,
                    f"Czas działania algorytmów dla list napisów o długości {str_len}",
                    "Długość listy",
                )

    list_sizes = [1000]
    str_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    for size in list_sizes:
        results = {
            "v1": [],
            "v2": [],
            "v3": [],
            "v4": [],
        }
        for str_len in str_sizes:
            data = generate_data(size, "str", str_len)
            results["v1"].append(measure_time(find_min_v1, data))
            results["v2"].append(measure_time(find_min_v2, data))
            results["v3"].append(measure_time(find_min_v3, data))
            results["v4"].append(measure_time(find_min_v4, data))
        plot_results(
            results,
            str_sizes,
            f"Czas działania algorytmów dla list o długości {size}",
            "Długość napisu",
        )


if __name__ == "__main__":
    run_tests(["int", "str"], [1, 32, 1024])
