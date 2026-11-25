
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from books.models import Book
from .cart import Cart


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

    book = get_object_or_404(
        Book,
        id=book_id,
        is_active=True
    )

    quantity = int(request.POST.get("quantity", 1))

    if quantity < 1 or quantity > book.stock:
        return redirect("cart_detail")

    cart.add(
        book=book,
        quantity=quantity
    )

    return redirect("cart_detail")


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