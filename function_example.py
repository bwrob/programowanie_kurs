import math

from rich import print

from function_hierarchy import (
    DifferentiableFunction,
    ExponentialFunction,
    PolynomialFunction,
    SineFunction,
)

# Przykłady użycia

# Funkcja wielomianowa: 3x^2 - 2x + 1
p = PolynomialFunction([3, -2, 1], name="Wielomian Kwadratowy")
print(p)
print(p(2))
pochodna_p = p.derivative()
print(pochodna_p)
print(pochodna_p(2))

# Funkcja sinus: 2*sin(0.5*x + 0.3)
s = SineFunction(amplitude=2, frequency=0.5, phase=0.3, name="Funkcja Sinus")
print(s)
print(s(math.pi))
pochodna_s = s.derivative()
print(pochodna_s)
print(pochodna_s(math.pi))

# Funkcja eksponencjalna: 2^x
e = ExponentialFunction(base=2, name="Funkcja Eksponencjalna")
print(e)
print(e(3))
pochodna_e = e.derivative()
print(pochodna_e(3))


# Przykład użycia DifferentiableFunction z funkcją lambda
def f(x):
    return x**2 + 2 * x + 1


df = DifferentiableFunction(f, name="Funkcja kwadratowa")
print(df(3))  # Wypisze 16
pochodna_df = df.derivative()
print(pochodna_df(3))  # Wypisze przybliżoną wartość pochodnej f(x) w x=3, czyli 8
