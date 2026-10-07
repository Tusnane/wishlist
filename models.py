"""Модели вишлиста."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .validators import clean_text


class Wish(models.Model):
    """Одно желание пользователя, привязанное к конкретному дню."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishes")
    date = models.DateField("День", db_index=True)
    text = models.CharField("Желание", max_length=300)
    done = models.BooleanField("Выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "done", "created"]
        verbose_name = "желание"
        verbose_name_plural = "желания"

    def __str__(self):
        return f"{self.date}: {self.text}"

    def toggle(self):
        """Переключить статус «выполнено» и сохранить только это поле."""
        self.done = not self.done
        self.save(update_fields=["done"])

    def clean(self):
        """Нормализует и проверяет текст (вызывается из full_clean() и админки)."""
        try:
            self.text = clean_text(self.text)
        except ValueError as exc:
            raise ValidationError({"text": str(exc)}) from exc
