from django.db import models
from books.models import Book
import uuid
import secrets
import string


def generate_tracking_code():
    characters = string.ascii_uppercase + string.digits

    while True:
        code = ''.join(
            secrets.choice(characters)
            for _ in range(12)
        )

        if not Order.objects.filter(tracking_code=code).exists():
            return code


class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("cancelled", "لغو شده"),
    ]
    full_name = models.CharField(
    max_length=150,
    verbose_name="نام و نام خانوادگی"
)

    phone = models.CharField(
        max_length=15,
        verbose_name="شماره تماس"
    )

    address = models.TextField(
        verbose_name="آدرس کامل"
    )

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="کد پستی"
    )
    tracking_code = models.CharField(
        max_length=12,
        default=generate_tracking_code,
        unique=True,
        editable=False,
        verbose_name="کد پیگیری"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return f"سفارش شماره {self.id}"

    def get_total_price(self):
        return sum(
            item.price * item.quantity
            for item in self.items.all()
        )


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT
    )

    price = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.book.title