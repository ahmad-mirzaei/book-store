
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import F
from django.contrib import messages
from django.views.decorators.http import require_POST
from orders.models import Order
from books.models import Book


def payment_page(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        status="pending"
    )

    if request.session.get("pending_order_id") != order.id:
        return redirect("cart_detail")

    return render(
        request,
        "payments/payment.html",
        {"order": order}
    )


def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.session.get("pending_order_id") != order.id:
        return redirect("cart_detail")

    if request.method == "POST":
        try:
            with transaction.atomic():
                # فقط یک بار اجازه پرداخت سفارش را می‌دهیم.
                changed = Order.objects.filter(
                    id=order.id,
                    status="pending"
                ).update(status="paid")

                if not changed:
                    order.refresh_from_db()
                    if order.status == "paid":
                        return redirect("payment_success", order_id=order.id)
                    return redirect("cart_detail")

                # کاهش موجودی هر کتاب
                for item in order.items.all():
                    updated = Book.objects.filter(
                        id=item.book_id,
                        stock__gte=item.quantity
                    ).update(
                        stock=F("stock") - item.quantity
                    )

                    if not updated:
                        raise ValueError(
                            "موجودی یکی از کتاب‌ها کافی نیست."
                        )

        except ValueError:
            messages.error(
                request,
                "موجودی کافی نیست. سفارش پرداخت نشد."
            )
            return redirect("cart_detail")

        # خالی کردن سبد خرید پس از پرداخت موفق
        request.session.pop("cart", None)

        return redirect("payment_success", order_id=order.id)

    if order.status == "paid":
        return render(
            request,
            "payments/success.html",
            {"order": order}
        )

    return redirect("payment_page", order_id=order.id)



@require_POST
def cancel_order(request, order_id):
    if request.session.get("pending_order_id") != order_id:
        return redirect("cart_detail")

    order = get_object_or_404(
        Order,
        id=order_id,
        status="pending"
    )

    order.status = "cancelled"
    order.save(update_fields=["status"])

    request.session.pop("pending_order_id", None)

    messages.success(request, "سفارش شما با موفقیت لغو شد.")

    return redirect("cart_detail")