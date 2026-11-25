from django.shortcuts import render
from .models import Book, Category
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


def home(request):
    books = Book.objects.filter(
        is_active=True,
        stock__gt=0
    ).select_related("category").order_by("-created_at")

    categories = Category.objects.all()

    context = {
        "books": books,
        "categories": categories,
    }

    return render(request, "books/home.html", context)



from django.shortcuts import render, get_object_or_404
from .models import Book


def home(request):
    books = Book.objects.filter(
        is_active=True,
        stock__gt=0
    ).order_by("-created_at")[:2]

    return render(request, "books/home.html", {
        "books": books
    })


def book_detail(request, pk):
    book = get_object_or_404(
        Book,
        pk=pk,
        is_active=True
    )

    return render(
        request,
        "books/detail.html",
        {"book": book}
    )
