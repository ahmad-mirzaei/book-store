from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from books.models import Book
from .cart import Cart
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderCreateForm


def cart_detail(request):
    cart = Cart(request)

    return render(
        request,
        "orders/cart.html",
        {"cart": cart}
    )


@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id, is_active=True)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        return redirect("book_detail", pk=book.id)

    current_quantity = cart.cart.get(str(book.id), {}).get("quantity", 0)

    if quantity < 1 or current_quantity + quantity > book.stock:
        return redirect("book_detail", pk=book.id)

    cart.add(book=book, quantity=quantity)
    messages.success(request, f"کتاب «{book.title}» با موفقیت به سبد خرید اضافه شد.")

    return redirect("book_detail", pk=book.id)


@require_POST
def cart_remove(request, book_id):

    cart = Cart(request)

    book = get_object_or_404(Book, id=book_id)

    cart.remove(book)

    return redirect("cart_detail")


@require_POST
def cart_update(request, book_id):
    cart = Cart(request)

    book = get_object_or_404(
        Book,
        id=book_id,
        is_active=True
    )

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        return redirect("cart_detail")

    if quantity < 1 or quantity > book.stock:
        return redirect("cart_detail")

    if str(book_id) not in cart.cart:
        return redirect("cart_detail")

    cart.add(
        book=book,
        quantity=quantity,
        override_quantity=True
    )

    return redirect("cart_detail")



def create_order(request):
    cart = Cart(request)
    pending_order_id = request.session.get("pending_order_id")
    if pending_order_id:
        pending_order = Order.objects.filter(
            id=pending_order_id,
            status="pending"
        ).first()

        if pending_order:
            return redirect("payment_page", order_id=pending_order.id)

        request.session.pop("pending_order_id", None)

    if len(cart) == 0:
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect("cart_detail")

    form = OrderCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        with transaction.atomic():
            cart_items = []

            for book_id, item in cart.cart.items():
                book = Book.objects.select_for_update().filter(
                    id=book_id,
                    is_active=True
                ).first()

                if book is None or item["quantity"] > book.stock:
                    messages.error(
                        request,
                        "موجودی یکی از کتاب‌ها کافی نیست."
                    )
                    return redirect("cart_detail")

                cart_items.append((book, item["quantity"]))

            order = form.save(commit=False)
            order.save()
            request.session["pending_order_id"] = order.id

            for book, quantity in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    price=book.price,
                    quantity=quantity
                )

        return redirect("payment_page", order_id=order.id)

    return render(
        request,
        "orders/checkout.html",
        {"form": form, "cart": cart}
    )


def track_order(request):
    order = None
    error = None

    if request.method == "POST":
        tracking_code = request.POST.get("tracking_code", "").strip().upper()
        phone = request.POST.get("phone", "").strip()

        order = Order.objects.filter(
            tracking_code=tracking_code,
            phone=phone
        ).first()

        if order is None:
            error = "کد پیگیری یا شماره تماس اشتباه است."

    return render(
        request,
        "orders/track_order.html",
        {"order": order, "error": error}
    )