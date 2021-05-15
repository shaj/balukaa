# Generated by Django 3.2 on 2021-04-11 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=128)),
                ("fullName", models.CharField(max_length=256)),
                ("is_active", models.BooleanField()),
            ],
            options={
                "verbose_name": "Счет",
                "verbose_name_plural": "План счетов",
            },
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("date", models.DateField()),
                ("summ", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_enter", models.BooleanField()),
                ("created_at", models.DateTimeField()),
                ("updates_at", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Проводка",
                "verbose_name_plural": "Бухгалтерские проводки",
            },
        ),
    ]
