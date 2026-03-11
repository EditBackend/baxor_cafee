from django.db import models
import uuid
from django.utils import timezone
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils.timezone import now
import random
from datetime import date


class Order(models.Model):
    TYPE_DINE_IN = 'dine_in' # shu joyda ovqatlanadi.
    TYPE_TAKEAWAY = 'takeaway' # olib ketadi
    TYPE_DELIVERY = 'delivery'  # yetkazib beradi


    class Status(models.TextChoices):
        NEW = "NEW", "Yangi"
        COOKING = "COOKING", "Tayyorlanmoqda"
        READY = "READY", "Tayyor"
        CLOSED = "CLOSED", "Yopildi"

    ORDER_TYPE_CHOICES = [
        (TYPE_DINE_IN, 'Dine in (zalda)'),
        (TYPE_TAKEAWAY, 'Takeaway (olib ketish)'),
        (TYPE_DELIVERY, 'Delivery (yetkazib berish)'),
    ]

    STATUS_DRAFT = 'draft'
    STATUS_SENT_TO_KITCHEN = 'sent_to_kitchen'
    STATUS_COOKING = 'cooking'
    STATUS_READY = 'ready'
    STATUS_SERVED = 'served'
    STATUS_PAYMENT_PENDING = 'payment_pending'
    STATUS_PAID = 'paid'
    STATUS_CLOSED = 'closed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SENT_TO_KITCHEN, 'Oshxonaga yuborildi'),
        (STATUS_COOKING, 'Tayyorlanmoqda'),
        (STATUS_READY, 'Tayyor'),
        (STATUS_SERVED, 'Berildi'),
        (STATUS_PAYMENT_PENDING, 'To‘lov kutilmoqda'),
        (STATUS_PAID, 'To‘lov olindi'),
        (STATUS_CLOSED, 'Yopildi'),
        (STATUS_CANCELLED, 'Bekor qilindi'),
    ]

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.PROTECT,
        related_name='orders',
        help_text="Buyurtma qaysi tashkilotga tegishli.",blank=True, null=True
    )

    branch = models.ForeignKey(
        'branch.Branch',
        on_delete=models.PROTECT,
        related_name='orders',
        help_text="Buyurtma qaysi filialga tegishli."
    )

    table = models.ForeignKey(
        'table.Table',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        help_text="Stol (agar dine-in bo‘lsa)."
    )

    type = models.CharField(
        max_length=20,
        choices=ORDER_TYPE_CHOICES,
        # default= zalda
        help_text="Buyurtma turi (zal, takeaway, delivery)."
    )

    number = models.CharField(
        max_length=20,
        help_text="Buyurtma raqami (unikal)."
    )

    def save(self, *args, **kwargs):
        if not self.number:
            today = date.today()
            # Bugungi barcha mavjud raqamlarni olish
            existing_numbers = Order.objects.filter(created_at=today).values_list('number', flat=True)

            while True:
                # 3-xonali raqam yaratish (001-999)
                rand_number = f"{random.randint(1, 999):03}"
                if rand_number not in existing_numbers:
                    self.number = rand_number
                    break

        # Asl save metodini chaqirish
        super().save(*args, **kwargs)
#1️⃣ Superuser kiradi → saqlaydi → ishlaydi ✅
#2️⃣ Oddiy admin kiradi → saqlamoqchi bo‘ladi → xatolik chiqadi ❌

    # number ni avtomatik ravishda yaratish kerak, qaytarilmas bo'lsin. 3-xona bo'lsin qaytarilmas bo'lsin.
    # random orqali qiling. bir kundan keyin yana o'sha raqamlarni ishlatish mumkin.
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        help_text="Buyurtma joriy holati."
    )

    guests_count = models.PositiveIntegerField(
        default=1,
        help_text="Mehmonlar soni."
    )

    assigned_waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='assigned_orders',
        help_text="Mas’ul ofitsiant."
    )

    note = models.TextField(
        blank=True,
        help_text="Buyurtmaga umumiy izoh."
    )

    service_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Servis haqi."
    )

    # 🔹 Bu yerda saqlash vaqtida tekshiruv qilamiz
    # Agar request superuser bo'lmasa -> saqlashga ruxsat bermaymiz
    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)

        # Agar request bor va user superuser emas bo'lsa
        if request and not request.user.is_superuser:
            raise PermissionDenied("Sizda servis narxini o'zgartirishga ruxsat yo'q!")

        # Aks holda oddiy saqlash ishlaydi
        super().save(*args, **kwargs)

    def __str__(self):
        return self.type


    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Yakuniy to‘lanadigan summa."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        # Ovqatlar summasi (narx * soni)
        items_total = self.items.aggregate(
            total=Coalesce(
                Sum(F("price") * F("quantity"), output_field=DecimalField()),
                0
            )
        )["total"]

        # Boshqa mahsulotlar summasi
        other_total = self.other_items.aggregate(
            total=Coalesce(Sum("price"), 0)
        )["total"]

        return items_total + other_total + self.service_fee

    def save(self, *args, **kwargs):
        # Agar bu eski object bo‘lsa (update bo‘layotgan bo‘lsa)
        if self.pk:
            old = OrderItem.objects.get(pk=self.pk)

            # Agar status NEW dan COOKING ga o‘zgarsa
            if old.status != self.status and self.status == self.Status.COOKING and not self.sent_to_kitchen_at:
                self.sent_to_kitchen_at = timezone.now()
        # Agar yangi object bo‘lib to‘g‘ridan COOKING bo‘lib yaratilsa
        elif self.status == self.Status.COOKING:
            self.sent_to_kitchen_at = timezone.now()

        # Avval saqlaymiz (PK kerak bo‘lishi uchun)
        super().save(*args, **kwargs)

        # Totalni hisoblaymiz va update qilamiz
        total = self.calculate_total()
        if self.total_amount != total:
            self.total_amount = total
            super().save(update_fields=["total_amount"])
    ready_at = models.DateTimeField(
        null=True, blank=True, help_text="Tayyor bo‘lgan vaqt."
    )
    # avtomatik bo'ladi. ready ga otgan payti vaqt avtomatik belgilanadi. statusga qarab.
    closed_at = models.DateTimeField(
        null=True, blank=True, help_text="Yopilgan vaqt."
    )
    # avtomatik belgiladi. statusga qarab

    def save(self, *args, **kwargs):

        now = timezone.now()

        if self.pk:
            old = OrderItem.objects.get(pk=self.pk)

            # 🔥 Oshxonaga yuborilganda vaqt yozish
            if (
                old.status != self.status
                and self.status == self.Status.COOKING
                and not self.sent_to_kitchen_at
            ):
                self.sent_to_kitchen_at = now

            # 🔥 Yopilgan vaqt (READY yoki CANCELLED bo‘lsa)
            if (
                old.status != self.status
                and self.status in [self.Status.READY, self.Status.CANCELLED]
                and not self.closed_at
            ):
                self.closed_at = now

        else:
            # Yangi create bo‘lib darhol COOKING bo‘lsa
            if self.status == self.Status.COOKING:
                self.sent_to_kitchen_at = now

            # Yangi create bo‘lib READY yoki CANCELLED bo‘lsa
            if self.status in [self.Status.READY, self.Status.CANCELLED]:
                self.closed_at = now

        super().save(*args, **kwargs)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Yaratilgan vaqt."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Oxirgi yangilanish vaqti."
    )

    def __str__(self):
        return f"{self.number} ({self.get_status_display()})"


class OrderItem(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "Yangi"
        COOKING = "COOKING", "Tayyorlanmoqda"
        READY = "READY", "Tayyor"
        CANCELLED = "CANCELLED", "Bekor qilindi"

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.PROTECT,
        related_name='order_items',
        help_text="Buyurtma elementi qaysi tashkilotga tegishli.",blank=True, null=True
    )

    order = models.ForeignKey(
        'order.Order',
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Qaysi buyurtmaga tegishli."
    )
    
    product = models.ForeignKey(
        'table.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        help_text="Mahsulot (o‘chirilgan bo‘lsa NULL)."
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Bir dona narxi."
    )

    qty = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Soni/miqdori."
    )

    line_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Umumiy summa (unit_price x qty)."
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        help_text="Hozirgi holati."
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Yaratilgan vaqti."
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product} x {self.qty}"

