from django.db import models
from django.utils.timezone import now

# =========================
# TABLE
# =========================
class Table(models.Model):

    class Status(models.TextChoices):
        FREE = "FREE", "Bo‘sh"
        BUSY = "BUSY", "Band"
        PAYMENT = "PAYMENT", "Hisob jarayonida"
        CLOSED = "CLOSED", "Yopilgan"

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="tables",
        help_text="Stol qaysi tashkilotga tegishli.", blank=True, null=True
    )

    branch = models.ForeignKey(
        'branch.Branch',
        on_delete=models.CASCADE,
        related_name="tables",
        help_text="Stol qaysi filialga tegishli."
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Stol nomi yoki qo‘shimcha belgi (ixtiyoriy)."
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.FREE,
        help_text="Stolning joriy holati."
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Stol faol yoki yo‘qligi."
    )

    created_at = models.DateTimeField(
        default=now,
        help_text="Yaratilgan vaqt."
    )

    class Meta:
        unique_together = ("branch", "name")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["branch", "name"]),
        ]

    def __str__(self):
        branch_name = getattr(self.branch, "name", "Branch")
        return f"{branch_name} - {self.name}"


# =========================
# CATEGORY
# =========================
class Category(models.Model):

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="categories",
        help_text="Kategoriya qaysi tashkilotga tegishli."
    )

    branch = models.ForeignKey(
        'branch.Branch',
        on_delete=models.CASCADE,
        related_name="categories",
        help_text="Kategoriya qaysi filialga tegishli."
    )

    name = models.CharField(
        max_length=255,
        help_text="Kategoriya nomi."
    )

    created_at = models.DateTimeField(
        default=now,
        help_text="Yaratilgan vaqt."
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("branch", "name")
        indexes = [
            models.Index(fields=["branch", "name"]),
        ]

    def __str__(self):
        return self.name


# =========================
# PRODUCT
# =========================
class Product(models.Model):

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="products",
        help_text="Mahsulot qaysi tashkilotga tegishli."
    )

    branch = models.ForeignKey(
        'branch.Branch',
        on_delete=models.CASCADE,
        related_name="products",
        help_text="Mahsulot qaysi filialga tegishli."
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        help_text="Mahsulot kategoriyasi."
    )

    name = models.CharField(
        max_length=255,
        help_text="Mahsulot nomi."
    )

    kitchen_name = models.CharField(
        max_length=255,
        help_text="Oshxonada ishlatiladigan nom."
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Mahsulot narxi."
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Mahsulot sotuvda faol yoki yo‘qligi."
    )

    created_at = models.DateTimeField(
        default=now,
        help_text="Yaratilgan vaqt."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Oxirgi yangilanish vaqti."
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("branch", "name")
        indexes = [
            models.Index(fields=["branch", "category"]),
        ]

    def __str__(self):
        return self.name