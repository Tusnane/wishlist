"""Логика недель: понедельник-воскресенье по стандарту ISO 8601."""
import datetime as dt

DAY_NAMES = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


class WeekCalendar:
    """Неделя, в которой лежит заданная дата.

    Состояние хранится в приватном атрибуте _monday; снаружи доступны
    только чтение через свойства и безопасное изменение через set_anchor().
    """

    def __init__(self, anchor):
        self.set_anchor(anchor)

    def set_anchor(self, anchor):
        """Выбрать неделю, содержащую дату anchor (только date, не datetime)."""
        if isinstance(anchor, dt.datetime) or not isinstance(anchor, dt.date):
            raise ValueError("anchor должен быть датой (datetime.date)")
        self._monday = anchor - dt.timedelta(days=anchor.weekday())

    @property
    def monday(self):
        """Дата понедельника этой недели."""
        return self._monday

    @property
    def sunday(self):
        """Дата воскресенья этой недели."""
        return self._monday + dt.timedelta(days=6)

    @property
    def number(self):
        """Номер недели по ISO 8601 (1-53)."""
        return self._monday.isocalendar()[1]

    def dates(self):
        """Список из 7 дат недели, начиная с понедельника."""
        return [self._monday + dt.timedelta(days=i) for i in range(7)]

    def contains(self, day):
        """Входит ли дата в эту неделю."""
        return self._monday <= day <= self.sunday

    def shifted(self, weeks):
        """Новая неделя со сдвигом на weeks недель (можно отрицательное число)."""
        return WeekCalendar(self._monday + dt.timedelta(weeks=weeks))

    def __repr__(self):
        return f"WeekCalendar({self._monday.isoformat()}..{self.sunday.isoformat()})"
