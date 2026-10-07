import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Wish",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(db_index=True, verbose_name="День")),
                ("text", models.CharField(max_length=300, verbose_name="Желание")),
                ("done", models.BooleanField(default=False, verbose_name="Выполнено")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="wishes", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "желание",
                "verbose_name_plural": "желания",
                "ordering": ["date", "done", "created"],
            },
        ),
    ]
