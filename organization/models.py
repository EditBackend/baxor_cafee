from django.db import models
from django.contrib.auth.hashers import make_password

class Organization(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAYMENT_SOON = "payment_soon", "To‘lov yaqin"
        NOT_PAID = "not_paid", "To‘lov qilmagan"

    name = models.CharField(
        max_length=255,
        help_text="Tashkilot nomi"
    )

    logo = models.ImageField(
        upload_to="organization/logos/",
        null=True,
        blank=True,
        help_text="Tashkilot logotipi"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text="Tashkilot holati"
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        help_text="Telefon raqam (login sifatida ishlatiladi)"
    )

    password = models.CharField(
        max_length=255,
        help_text="Parol (hashlangan holda saqlanadi)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.name
