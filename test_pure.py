"""Модульные тесты без Django и без БД: валидаторы, недели, полиморфизм."""
import datetime as dt
import unittest

from wishes.validators import BaseValidator, DateValidator, TextValidator, clean_date, clean_text
from wishes.weeks import WeekCalendar


class TextValidatorTests(unittest.TestCase):
    def test_strips_and_collapses_spaces(self):
        self.assertEqual(clean_text("  Купить   книгу \n"), "Купить книгу")

    def test_empty_and_whitespace_rejected(self):
        for value in ("", "   ", "\n\t"):
            with self.assertRaises(ValueError):
                clean_text(value)

    def test_wrong_type_rejected(self):
        for value in (None, 123, ["a"], b"abc"):
            with self.assertRaises(ValueError):
                clean_text(value)

    def test_length_boundary(self):
        self.assertEqual(len(clean_text("a" * 300)), 300)
        with self.assertRaises(ValueError):
            clean_text("a" * 301)

    def test_control_chars_replaced_by_space(self):
        self.assertEqual(clean_text("a\x00b"), "a b")

    def test_custom_max_length(self):
        with self.assertRaises(ValueError):
            TextValidator(5)("123456")
        self.assertEqual(TextValidator(5)("12345"), "12345")

    def test_max_length_setter_validates(self):
        validator = TextValidator()
        for bad in (0, -1, "5", True, None, 2.5):
            with self.assertRaises(ValueError):
                validator.max_length = bad
        validator.max_length = 10
        self.assertEqual(validator.max_length, 10)


class DateValidatorTests(unittest.TestCase):
    def test_iso_string(self):
        self.assertEqual(clean_date("2026-10-07"), dt.date(2026, 10, 7))
        self.assertEqual(clean_date(" 2026-10-07 "), dt.date(2026, 10, 7))

    def test_date_and_datetime_objects(self):
        self.assertEqual(clean_date(dt.date(2026, 1, 1)), dt.date(2026, 1, 1))
        self.assertEqual(clean_date(dt.datetime(2026, 1, 1, 12, 30)), dt.date(2026, 1, 1))

    def test_invalid_strings(self):
        for value in ("2026-13-01", "abc", "", "31.12.2026", "2026-02-30"):
            with self.assertRaises(ValueError):
                clean_date(value)

    def test_wrong_type(self):
        for value in (None, 20261007, ["2026-10-07"]):
            with self.assertRaises(ValueError):
                clean_date(value)

    def test_year_boundaries(self):
        self.assertEqual(clean_date("2000-01-01").year, 2000)
        self.assertEqual(clean_date("2100-12-31").year, 2100)
        for value in ("1999-12-31", "2101-01-01"):
            with self.assertRaises(ValueError):
                clean_date(value)

    def test_bad_constructor(self):
        with self.assertRaises(ValueError):
            DateValidator(min_year=2100, max_year=2000)


class PolymorphismTests(unittest.TestCase):
    def test_subclasses_share_call_interface(self):
        cases = ((TextValidator(), "желание"), (DateValidator(), "2026-10-07"))
        for validator, good in cases:
            self.assertIsInstance(validator, BaseValidator)
            self.assertIsNotNone(validator(good))

    def test_same_call_different_behaviour(self):
        self.assertIsInstance(TextValidator()("2026-10-07"), str)
        self.assertIsInstance(DateValidator()("2026-10-07"), dt.date)

    def test_base_class_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            BaseValidator()("x")


class WeekCalendarTests(unittest.TestCase):
    def test_midweek_date(self):
        cal = WeekCalendar(dt.date(2026, 10, 7))  # среда
        self.assertEqual(cal.monday, dt.date(2026, 10, 5))
        self.assertEqual(cal.sunday, dt.date(2026, 10, 11))
        self.assertEqual(len(cal.dates()), 7)
        self.assertEqual(cal.dates()[0], cal.monday)
        self.assertEqual(cal.dates()[-1], cal.sunday)

    def test_monday_and_sunday_inputs_stay_in_same_week(self):
        self.assertEqual(WeekCalendar(dt.date(2026, 10, 5)).monday, dt.date(2026, 10, 5))
        self.assertEqual(WeekCalendar(dt.date(2026, 10, 11)).monday, dt.date(2026, 10, 5))

    def test_year_boundary_iso_week(self):
        cal = WeekCalendar(dt.date(2026, 1, 1))  # четверг
        self.assertEqual(cal.monday, dt.date(2025, 12, 29))
        self.assertEqual(cal.number, 1)

    def test_shifted_and_contains(self):
        cal = WeekCalendar(dt.date(2026, 10, 7))
        self.assertEqual(cal.shifted(1).monday, dt.date(2026, 10, 12))
        self.assertEqual(cal.shifted(-1).monday, dt.date(2026, 9, 28))
        self.assertTrue(cal.contains(dt.date(2026, 10, 11)))
        self.assertFalse(cal.contains(dt.date(2026, 10, 12)))

    def test_rejects_non_date(self):
        for value in (None, "2026-10-07", dt.datetime(2026, 10, 7), 5):
            with self.assertRaises(ValueError):
                WeekCalendar(value)

    def test_set_anchor_changes_week(self):
        cal = WeekCalendar(dt.date(2026, 10, 7))
        cal.set_anchor(dt.date(2026, 10, 20))
        self.assertEqual(cal.monday, dt.date(2026, 10, 19))


if __name__ == "__main__":
    unittest.main()
