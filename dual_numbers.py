from __future__ import annotations

import math


class DualNumber:
    """Reprezentuje liczbę dualną postaci a + bε."""

    def __init__(self, real: float = 0.0, dual: float = 0.0) -> None:
        """Inicjalizuje liczbę dualną.

        Args:
            real: Część rzeczywista (a). Domyślnie 0.0.
            dual: Część dualna (b). Domyślnie 0.0.

        """
        self.real = float(real)
        self.dual = float(dual)

    def __str__(self) -> str:
        """Zwraca liczbę dualną jako czytelny napis."""
        sign = "+" if self.dual >= 0 else "-"
        return f"{self.real} {sign} {abs(self.dual)}ε"

    def __repr__(self) -> str:
        """Zwraca oficjalną reprezentację liczby dualnej."""
        return f"DualNumber({self.real}, {self.dual})"

    def __add__(self, other: DualNumber | float) -> DualNumber:
        """Dodaje dwie liczby dualne lub liczbę dualną i liczbę rzeczywistą."""
        if isinstance(other, DualNumber):
            return DualNumber(self.real + other.real, self.dual + other.dual)
        if isinstance(other, int | float):
            return DualNumber(self.real + other, self.dual)
        return NotImplemented

    def __radd__(self, other: DualNumber | float) -> DualNumber:
        """Obsługuje dodawanie z liczbą rzeczywistą po lewej stronie."""
        return self + other

    def __sub__(self, other: DualNumber | int | float) -> DualNumber:
        """Odejmuje dwie liczby dualne lub liczbę dualną i liczbę rzeczywistą."""
        if isinstance(other, DualNumber):
            return DualNumber(self.real - other.real, self.dual - other.dual)
        if isinstance(other, (int, float)):
            return DualNumber(self.real - other, self.dual)
        return NotImplemented

    def __rsub__(self, other: float) -> DualNumber:
        """Obsługuje odejmowanie z liczbą rzeczywistą po lewej stronie."""
        return DualNumber(other - self.real, -self.dual)

    def __mul__(self, other: DualNumber | float) -> DualNumber:
        """Mnoży dwie liczby dualne lub liczbę dualną i liczbę rzeczywistą."""
        if isinstance(other, DualNumber):
            real_part = self.real * other.real
            dual_part = (self.real * other.dual) + (self.dual * other.real)
            return DualNumber(real_part, dual_part)
        if isinstance(other, int | float):
            return DualNumber(self.real * other, self.dual * other)
        return NotImplemented

    def __rmul__(self, other: float) -> DualNumber:
        """Obsługuje mnożenie z liczbą rzeczywistą po lewej stronie."""
        return self * other

    def __truediv__(self, other: DualNumber | float) -> DualNumber:
        """Dzieli dwie liczby dualne lub liczbę dualną i liczbę rzeczywistą."""
        if isinstance(other, DualNumber):
            if other.real == 0:
                raise ZeroDivisionError("Dzielenie przez zero")
            real_part = self.real / other.real
            dual_part = (self.dual * other.real - self.real * other.dual) / (
                other.real**2
            )
            return DualNumber(real_part, dual_part)
        if isinstance(other, int | float):
            if other == 0:
                raise ZeroDivisionError("Dzielenie przez zero")
            return DualNumber(self.real / other, self.dual / other)
        return NotImplemented

    def __rtruediv__(self, other: float) -> DualNumber:
        """Obsługuje dzielenie z liczbą rzeczywistą po lewej stronie."""
        if self.real == 0:
            raise ZeroDivisionError("Dzielenie przez zero")
        real_part = other / self.real
        dual_part = (0 - other * self.dual) / (self.real**2)
        return DualNumber(real_part, dual_part)

    def __pow__(self, n: float) -> DualNumber:
        """Podnosi liczbę dualną do potęgi n.

        (n jest liczbą całkowitą lub zmiennoprzecinkową).
        """
        if isinstance(n, int | float):
            real_part = self.real**n
            dual_part = n * (self.real ** (n - 1)) * self.dual
            return DualNumber(real_part, dual_part)
        return NotImplemented

    def __rpow__(self, other: float) -> DualNumber:
        """Obsługuje przypadek, gdy liczba rzeczywista jest podnoszona do potęgi liczby dualnej."""
        if isinstance(other, int | float):
            real_part = other**self.real
            dual_part = real_part * math.log(other) * self.dual
            return DualNumber(real_part, dual_part)
        return NotImplemented

    def __neg__(self) -> DualNumber:
        """Zwraca negację liczby dualnej."""
        return DualNumber(-self.real, -self.dual)

    def __eq__(self, other: DualNumber) -> bool:
        """Sprawdza, czy dwie liczby dualne są równe."""
        if isinstance(other, DualNumber):
            return self.real == other.real and self.dual == other.dual
        return False

    def __ne__(self, other: DualNumber) -> bool:
        """Sprawdza, czy dwie liczby dualne nie są równe."""
        return not self == other

    def __int__(self) -> int:
        """Konwertuje liczbę dualną na liczbę całkowitą.

        Zwraca część rzeczywistą.
        """
        return int(self.real)

    def __float__(self) -> float:
        """Konwertuje liczbę dualną na liczbę zmiennoprzecinkową.

        Zwraca część rzeczywistą.
        """
        return float(self.real)

    @staticmethod
    def sqrt(z: DualNumber) -> DualNumber:
        """Oblicza pierwiastek kwadratowy z liczby dualnej."""
        if z.real < 0:
            msg = (
                "Pierwiastek kwadratowy z ujemnej części rzeczywistej nie jest "
                "zdefiniowany dla liczb dualnych w tej implementacji"
            )
            raise ValueError(msg)
        real_part = math.sqrt(z.real)
        dual_part = z.dual / (2 * real_part) if real_part != 0 else 0
        return DualNumber(real_part, dual_part)

    @staticmethod
    def exp(z: DualNumber) -> DualNumber:
        """Oblicza funkcję wykładniczą liczby dualnej."""
        real_part = math.exp(z.real)
        dual_part = real_part * z.dual
        return DualNumber(real_part, dual_part)

    @staticmethod
    def sin(z: DualNumber) -> DualNumber:
        """Oblicza sinus liczby dualnej."""
        real_part = math.sin(z.real)
        dual_part = math.cos(z.real) * z.dual
        return DualNumber(real_part, dual_part)

    @staticmethod
    def cos(z: DualNumber) -> DualNumber:
        """Oblicza cosinus liczby dualnej."""
        real_part = math.cos(z.real)
        dual_part = -math.sin(z.real) * z.dual
        return DualNumber(real_part, dual_part)


epsilon = DualNumber(0, 1)  # Nieskończenie mała jednostka epsilon
