from rich import print

from dual_numbers import DualNumber, epsilon

funcje_zaimplementowane = True

# Utwórz kilka liczb dualnych
a = DualNumber(2, 3)  # 2 + 3ε
b = DualNumber(1, 4)  # 1 + 4ε
c = DualNumber(5, 0)  # 5 + 0ε (odpowiednik liczby rzeczywistej 5)
d = 1 + 2 * epsilon  # 1 + 2ε

# Wypisz liczby dualne
print("Liczba dualna a:", a)
print("Liczba dualna b:", b)
print("Epsilon:", epsilon)

# Podstawowe operacje arytmetyczne
print("Dodawanie:", a + b)
print("Odejmowanie:", a - b)
print("Mnożenie:", a * b)
print("Dzielenie:", a / b)
print("Potęgowanie:", a**2)
print("Negacja", -a)

# Operacje prawostronne
print("Dodawanie prawe:", 1 + a)
print("Odejmowanie prawe:", 5 - a)
print("Mnożenie prawe:", 2 * a)
print("Dzielenie prawe:", 10 / a)
print("Potęgowanie prawe", 2**a)

# Operacje porównania
print("Równość:", a == b)
print("Nierówność:", a != b)
print("Równość:", a == DualNumber(2, 3))

# Konwersja na int i float
print("Konwersja na int:", int(a))
print("Konwersja na float:", float(a))

# Opcjonalne funkcje na liczbach dualnych
if funcje_zaimplementowane:
    print("Pierwiastek kwadratowy z a:", DualNumber.sqrt(a))
    print("Funkcja wykładnicza z a:", DualNumber.exp(a))
    print("Sinus z a:", DualNumber.sin(a))
    print("Cosinus z a:", DualNumber.cos(a))
