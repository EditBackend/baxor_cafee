from django.db import models
from organization.models import Organization



class Branch(models.Model):
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="branches",
        help_text="Ushbu filial qaysi tashkilotga tegishli ekanligini ko‘rsatadi.",
        blank=True,null=True)

    name = models.CharField(
        max_length=255,
        help_text="Filialning to‘liq nomi. Masalan: 'Chilonzor filiali' yoki 'Main Office'. Bu nom tizim bo‘ylab filialni aniqlash uchun ishlatiladi."
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Filial faol yoki faol emasligini bildiradi. Agar False bo‘lsa, filial tizimda o‘chirilgan emas, lekin vaqtincha ishlamaydi."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Filial yozuvi yaratilgan sana va vaqt. Bu maydon avtomatik ravishda to‘ldiriladi va o‘zgartirilmaydi."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Filial ma’lumotlari oxirgi marta qachon yangilanganini ko‘rsatadi. Har safar saqlanganda avtomatik yangilanadi."
    )

    def __str__(self):
        return self.name
