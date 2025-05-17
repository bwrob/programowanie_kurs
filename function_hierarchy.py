#!/usr/bin/env python3
"""Implementacja funkcji rzeczywistych w Pythonie."""

import math
from collections.abc import Callable


class RealFunction:
    """Klasa bazowa reprezentująca funkcję rzeczywistą."""

    def __init__(self, func: Callable[[float], float], name: str | None = None):
        self.func = func
        self.name = name

    def __call__(self, x: float) -> float:
        return self.func(x)

    def __str__(self) -> str:
        return self.name if self.name else "Anonimowa funkcja"


class DifferentiableFunction(RealFunction):
    """Klasa reprezentująca funkcję różniczkowalną."""

    def __init__(self, func: Callable[[float], float], name: str | None = None):
        super().__init__(func, name)

    def derivative(self, h: float = 1e-7) -> "RealFunction":
        """Oblicza pochodną funkcji w punkcie x przy użyciu różnic centralnych."""
        return RealFunction(
            lambda x: (self.func(x + h) - self.func(x - h)) / (2 * h),
            name=f"Pochodna {self.name}" if self.name else None,
        )


class PolynomialFunction(DifferentiableFunction):
    """Klasa reprezentująca funkcję wielomianową."""

    def __init__(self, coefficients: list[float], name: str | None = None):
        super().__init__(lambda x: self._evaluate_polynomial(x, coefficients), name)
        self.coefficients = coefficients

    def _evaluate_polynomial(self, x: float, coeffs: list[float]) -> float:
        """Oblicza wartość wielomianu dla danego x używając schematu Hornera."""
        result = 0
        for coeff in coeffs:
            result = result * x + coeff
        return result

    def __str__(self) -> str:
        terms = []
        for i, coeff in enumerate(self.coefficients):
            power = len(self.coefficients) - 1 - i
            if coeff:
                term = (
                    f"{'+' if coeff > 0 and i > 0 else ''}"
                    f" {'-' if coeff < 0 else ''}"
                )
                if abs(coeff) != 1 or power == 0:
                    term += str(abs(coeff))
                if power > 0:
                    term += "x" + (f"^{power}" if power > 1 else "")
                terms.append(term)
        return "".join(terms) or "0"

    def derivative(self) -> "PolynomialFunction":
        """Oblicza pochodną wielomianu i zwraca nowy obiekt PolynomialFunction."""
        if not self.coefficients:
            return PolynomialFunction([])
        derivative_coeffs = []
        for i, coeff in enumerate(self.coefficients[:-1]):
            derivative_coeffs.append(coeff * (len(self.coefficients) - 1 - i))
        return PolynomialFunction(
            derivative_coeffs,
            name=f"Pochodna {self.name}" if self.name else None,
        )


class SineFunction(DifferentiableFunction):
    """Klasa reprezentująca funkcję sinus."""

    def __init__(
        self,
        amplitude: float = 1.0,
        frequency: float = 1.0,
        phase: float = 0.0,
        name: str | None = None,
    ):
        super().__init__(lambda x: amplitude * math.sin(frequency * x + phase), name)
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def __str__(self) -> str:
        amplitude = f"{self.amplitude} * " if self.amplitude != 1 else ""
        s = f"{amplitude}sin({self.frequency}*x"
        if self.phase != 0:
            s += f"+{self.phase}"
        s += ")"
        return s

    def derivative(self) -> "SineFunction":
        """Oblicza pochodną funkcji sinus i zwraca nowy obiekt SineFunction."""
        # Pochodna amplitude * sin(frequency * x + phase)
        # to amplitude * frequency * cos(frequency * x + phase)
        return SineFunction(
            amplitude=self.amplitude * self.frequency,
            frequency=self.frequency,
            phase=self.phase + math.pi / 2,
            name=f"Pochodna {self.name}" if self.name else None,
        )


class ExponentialFunction(DifferentiableFunction):
    """Klasa reprezentująca funkcję eksponencjalną."""

    def __init__(
        self,
        base: float = math.e,
        scalar: float = 1.0,
        name: str | None = None,
    ):
        super().__init__(lambda x: scalar * base**x, name)
        self.base = base
        self.scalar = scalar

    def __str__(self) -> str:
        return (
            f"{self.scalar} * {self.base} ^ x"
            if self.scalar != 1.0
            else f"{self.base} ^ x"
        )

    def derivative(self) -> "ExponentialFunction":
        """Oblicza pochodną funkcji eksponencjalnej."""
        return ExponentialFunction(
            base=self.base,
            scalar=self.scalar * math.log(self.base),
            name=f"Pochodna {self.name}" if self.name else None,
        )
