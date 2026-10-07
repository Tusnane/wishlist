"""Модуль валидации входных данных вишлиста.

Иерархия классов:
    BaseValidator          - общий интерфейс (__call__), принцип DRY
    ├── TextValidator      - проверка и очистка текста желания
    └── DateValidator      - проверка даты

Все проверки поднимают ValueError, а возвращают уже очищенное значение.
Модуль не зависит от Django, поэтому тестируется обычным unittest.
"""
import datetime as dt
import re

_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


class BaseValidator:
    """Базовый класс валидаторов: вызов валидатора = вызов _check()."""

    def __call__(self, value):
        """Проверить значение и вернуть очищенный результат (или ValueError)."""
        return self._check(value)

    def _check(self, value):
        raise NotImplementedError("Подкласс должен реализовать _check()")


class TextValidator(BaseValidator):
    """Проверяет текст желания: тип, пустота, длина, управляющие символы."""

    def __init__(self, max_length=300):
        self.max_length = max_length  # идёт через сеттер ниже

    @property
    def max_length(self):
        """Максимальная длина текста (только положительное целое)."""
        return self._max_length

    @max_length.setter
    def max_length(self, value):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError("max_length должен быть целым числом >= 1")
        self._max_length = value

    def _check(self, value):
        if not isinstance(value, str):
            raise ValueError("Текст желания должен быть строкой")
        cleaned = _CONTROL_CHARS.sub(" ", value)
        cleaned = " ".join(cleaned.split())  # убираем лишние пробелы
        if not cleaned:
            raise ValueError("Текст желания не может быть пустым")
        if len(cleaned) > self._max_length:
            raise ValueError(f"Текст длиннее {self._max_length} символов")
        return cleaned


class DateValidator(BaseValidator):
    """Проверяет дату: строка ГГГГ-ММ-ДД или объект date, разумный диапазон лет."""

    def __init__(self, min_year=2000, max_year=2100):
        if min_year > max_year:
            raise ValueError("min_year не может быть больше max_year")
        self._min_year = min_year
        self._max_year = max_year

    @property
    def min_year(self):
        return self._min_year

    @property
    def max_year(self):
        return self._max_year

    def _check(self, value):
        if isinstance(value, dt.datetime):
            result = value.date()
        elif isinstance(value, dt.date):
            result = value
        elif isinstance(value, str):
            try:
                result = dt.date.fromisoformat(value.strip())
            except ValueError:
                raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД") from None
        else:
            raise ValueError("Дата должна быть строкой или date")
        if not self._min_year <= result.year <= self._max_year:
            raise ValueError(f"Год должен быть в диапазоне {self._min_year}-{self._max_year}")
        return result


# Готовые экземпляры для использования во views и моделях
clean_text = TextValidator()
clean_date = DateValidator()
