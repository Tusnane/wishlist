"""Тесты с Django: модель, представления, безопасность, изоляция пользователей."""
import datetime as dt

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Wish
from .weeks import WeekCalendar

User = get_user_model()
DAY = dt.date(2026, 10, 7)


class WishModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("anna", password="pw12345!")

    def make(self, **kw):
        data = {"user": self.user, "date": DAY, "text": "Купить книгу"}
        data.update(kw)
        return Wish.objects.create(**data)

    def test_str(self):
        self.assertEqual(str(self.make()), "2026-10-07: Купить книгу")

    def test_toggle_twice(self):
        wish = self.make()
        wish.toggle()
        wish.refresh_from_db()
        self.assertTrue(wish.done)
        wish.toggle()
        wish.refresh_from_db()
        self.assertFalse(wish.done)

    def test_clean_normalizes_text(self):
        wish = Wish(user=self.user, date=DAY, text="  a    b ")
        wish.clean()
        self.assertEqual(wish.text, "a b")

    def test_clean_rejects_empty_text(self):
        with self.assertRaises(ValidationError):
            Wish(user=self.user, date=DAY, text="   ").clean()

    def test_ordering_undone_before_done(self):
        done = self.make(text="сделано", done=True)
        todo = self.make(text="надо сделать")
        self.assertEqual(list(Wish.objects.all()), [todo, done])

    def test_deleting_user_deletes_wishes(self):
        self.make()
        self.user.delete()
        self.assertEqual(Wish.objects.count(), 0)


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("anna", password="pw12345!")
        self.other = User.objects.create_user("boris", password="pw12345!")
        self.client.force_login(self.user)

    def add(self, text="Тест", date="2026-10-07", client=None):
        return (client or self.client).post(reverse("add"), {"date": date, "text": text})

    def test_login_required_redirects(self):
        response = Client().get(reverse("week"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_login_page_opens(self):
        self.assertEqual(Client().get("/accounts/login/").status_code, 200)

    def test_week_page_has_seven_days(self):
        response = self.client.get(reverse("week"), {"d": "2026-10-07"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["days"]), 7)
        self.assertEqual(response.context["monday"], dt.date(2026, 10, 5))

    def test_bad_d_param_falls_back_to_current_week(self):
        response = self.client.get(reverse("week"), {"d": "garbage"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["monday"], WeekCalendar(timezone.localdate()).monday)

    def test_add_wish(self):
        response = self.add("Поехать в горы")
        self.assertEqual(response.status_code, 302)
        wish = Wish.objects.get()
        self.assertEqual((wish.user, wish.text, wish.date), (self.user, "Поехать в горы", DAY))

    def test_add_invalid_input_is_ignored(self):
        self.add("   ")
        self.add("ok", date="2026-99-99")
        self.add("a" * 301)
        self.add("ok", date="1900-01-01")
        self.assertEqual(Wish.objects.count(), 0)

    def test_add_boundary_300_chars(self):
        self.add("a" * 300)
        self.assertEqual(Wish.objects.count(), 1)

    def test_toggle_and_delete(self):
        self.add()
        wish = Wish.objects.get()
        self.client.post(reverse("toggle", args=[wish.pk]))
        wish.refresh_from_db()
        self.assertTrue(wish.done)
        self.client.post(reverse("delete", args=[wish.pk]))
        self.assertEqual(Wish.objects.count(), 0)

    def test_foreign_wish_is_protected(self):
        foreign = Wish.objects.create(user=self.other, date=DAY, text="секрет")
        self.assertEqual(self.client.post(reverse("toggle", args=[foreign.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("delete", args=[foreign.pk])).status_code, 404)
        foreign.refresh_from_db()
        self.assertFalse(foreign.done)

    def test_week_shows_only_own_wishes(self):
        Wish.objects.create(user=self.other, date=DAY, text="чужой секрет")
        Wish.objects.create(user=self.user, date=DAY, text="моё желание")
        response = self.client.get(reverse("week"), {"d": "2026-10-07"})
        self.assertContains(response, "моё желание")
        self.assertNotContains(response, "чужой секрет")

    def test_get_not_allowed_for_actions(self):
        wish = Wish.objects.create(user=self.user, date=DAY, text="x")
        for url in (reverse("add"), reverse("toggle", args=[wish.pk]), reverse("delete", args=[wish.pk])):
            self.assertEqual(self.client.get(url).status_code, 405)

    def test_csrf_is_enforced(self):
        strict = Client(enforce_csrf_checks=True)
        strict.force_login(self.user)
        response = strict.post(reverse("add"), {"date": "2026-10-07", "text": "x"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Wish.objects.count(), 0)

    def test_xss_is_escaped(self):
        self.add("<script>alert(1)</script>")
        response = self.client.get(reverse("week"), {"d": "2026-10-07"})
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;")

    def test_sql_injection_is_stored_as_plain_text(self):
        payload = "'; DROP TABLE wishes_wish; --"
        self.add(payload)
        self.assertEqual(Wish.objects.get().text, payload)

    def test_full_flow(self):
        self.add("Первое")
        self.add("Второе", date="2026-10-08")
        page = self.client.get(reverse("week"), {"d": "2026-10-07"})
        self.assertEqual(page.context["total"], 2)
        wish = Wish.objects.get(text="Первое")
        self.client.post(reverse("toggle", args=[wish.pk]))
        page = self.client.get(reverse("week"), {"d": "2026-10-07"})
        self.assertEqual((page.context["done"], page.context["total"]), (1, 2))
