from django.db import models

class KitchenTicket(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "Yangi"
        COOKING = "COOKING", "Tayyorlanmoqda"
        READY = "READY", "Tayyor"
        CANCELLED = "CANCELLED", "Bekor qilindi"


    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="kitchen_tickets",
        help_text="Ticket qaysi tashkilotga tegishli.",blank=True, null=True
    )


    branch = models.ForeignKey(
        'branch.Branch',
        on_delete=models.CASCADE,
        related_name="kitchen_tickets",
        help_text="Ticket qaysi filialga tegishli."
    )

    # Buyurtma bilan bog‘lash
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.CASCADE,
        related_name="kitchen_tickets",
        help_text="Bog‘langan buyurtma."
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        help_text="Oshxona jarayon holati."
    )

    sent_by = models.ForeignKey(
        'employee.Employee',
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_tickets",
        help_text="Ticketni yuborgan xodim."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Ticket yaratilgan vaqt (avtomatik)."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Ticket oxirgi yangilangan vaqt (avtomatik)."
    )

    def __str__(self):
        return f"Ticket #{self.id} ({self.status})"



# Manashu uchun put metod yozish kerak. endpoint berasiz bunda faqat status yangilandi holos boshqa narsa ozgarmaydi.