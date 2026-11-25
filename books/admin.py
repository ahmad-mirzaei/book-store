from django.contrib import admin
from .models import Category, Book, BookImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "price",
        "stock",
        "is_active",
    )

    list_filter = ("category", "is_active")
    search_fields = ("title", "author")
    list_editable = ("price", "stock", "is_active")

    inlines = [BookImageInline]