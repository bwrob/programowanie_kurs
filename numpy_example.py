import numpy as np


def numpy_example():
    # Utwórz tablicę 1D
    tablica_1d = np.array([1, 2, 3, 4, 5])
    print("Tablica 1D:", tablica_1d)

    # Utwórz tablicę 2D
    tablica_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print("Tablica 2D:\n", tablica_2d)

    # Utwórz tablice z zerami, jedynkami i zakresem wartości
    tablica_zer = np.zeros((2, 3))
    tablica_jedynek = np.ones((2, 3))
    tablica_zakres = np.arange(0, 10, 2)
    print("Tablica zer:\n", tablica_zer)
    print("Tablica jedynek:\n", tablica_jedynek)
    print("Tablica zakresu:", tablica_zakres)

    # Zmień kształt tablicy
    tablica_przeksztalcona = tablica_1d.reshape((5, 1))
    print("Przekształcona tablica:\n", tablica_przeksztalcona)

    # Podstawowe operacje arytmetyczne
    tablica_sumy = tablica_1d + 5
    tablica_iloczynu = tablica_1d * 2
    print("Tablica sumy:", tablica_sumy)
    print("Tablica iloczynu:", tablica_iloczynu)

    # Operacje element-po-elemencie
    suma_elementow = tablica_1d + tablica_1d
    iloczyn_elementow = tablica_1d * tablica_1d
    print("Suma elementów:", suma_elementow)
    print("Iloczyn elementów:", iloczyn_elementow)

    # Mnożenie macierzy
    iloczyn_macierzy = np.dot(tablica_2d, tablica_2d.T)
    print("Iloczyn macierzy:\n", iloczyn_macierzy)

    # Operacje statystyczne
    srednia_wartosc = np.mean(tablica_1d)
    suma_wartosci = np.sum(tablica_1d)
    maksymalna_wartosc = np.max(tablica_1d)
    print("Średnia wartość:", srednia_wartosc)
    print("Suma wartości:", suma_wartosci)
    print("Maksymalna wartość:", maksymalna_wartosc)

    # Indeksowanie i wycinanie
    wycieta_tablica = tablica_1d[1:4]
    print("Wycieta tablica:", wycieta_tablica)

    # Dwuwymiarowe wycinanie
    wycieta_tablica_2d = tablica_2d[1:, 1:]
    print("Wycieta tablica 2D:\n", wycieta_tablica_2d)

    # Indeksowanie logiczne
    tablica_indeksowana_logicznie = tablica_1d[tablica_1d > 2]
    print("Tablica indeksowana logicznie:", tablica_indeksowana_logicznie)

    # Operacje logiczne
    wszystkie_wieksze_od_zera = np.all(tablica_1d > 0)
    jakikolwiek_wiekszy_od_czterech = np.any(tablica_1d > 4)
    print("Wszystkie elementy większe od zera:", wszystkie_wieksze_od_zera)
    print("Jakikolwiek element większy od czterech:", jakikolwiek_wiekszy_od_czterech)


if __name__ == "__main__":
    numpy_example()
