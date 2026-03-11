from django.db import models
from django.core.validators import RegexValidator

class Employee(models.Model):
    class Role(models.TextChoices):
        OFITSIANT = "OFITSIANT", "Ofitsiant"
        OSHPAZ = "OSHPAZ", "Oshpaz"
        KASSIR = "KASSIR", "Kassir"
        MENEJER = "MENEJER", "Menejer"
        ADMIN = "ADMIN", "Administrator"


    organization = models.ForeignKey(
        'organization.Organization',  # Organization modeli
        on_delete=models.CASCADE,
        related_name="employees",
        help_text="Xodim ishlaydigan tashkilot.",null=True, blank=True
    )

    branch = models.ForeignKey(
        'branch.Branch',
        on_delete=models.CASCADE,
        related_name="employees",
        help_text="Xodim ishlaydigan filial."
    )

    name = models.CharField(
        max_length=255,
        help_text="Xodimning to‘liq ismi."
    )
    password = models.CharField(
        max_length=4,
        default = '',
        validators=[RegexValidator(r'^\d{4}$', 'Parol 4 xonali bo‘lishi kerak')]
    )

    face_password = models.CharField(
        max_length=4,
         default = '',
        validators=[RegexValidator(r'^\d{4}$', 'Face password 4 xonali bo‘lishi kerak')]
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        help_text="Telefon raqami (unikal bo‘lishi kerak)."
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        help_text="Xodim lavozimi."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Xodim faol yoki yo‘qligi."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Yozuv yaratilgan vaqt (avtomatik)."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Oxirgi yangilanish vaqti (avtomatik)."
    )

    def __str__(self):
        return f"{self.name} ({self.role})"