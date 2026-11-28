from django.db import models

# Create your models here.



from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
    
    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="books"
    )

    title = models.CharField(max_length=200, verbose_name = "عنوان")
    author = models.CharField(max_length=150)

    description = models.TextField()

    price = models.PositiveBigIntegerField(
        help_text="قیمت به تومان",
        verbose_name = "قیمت"
    )
    
    weight = models.PositiveIntegerField(
    default=500,
    verbose_name="وزن کتاب (گرم)",
    )

    stock = models.PositiveIntegerField(default=0)

    cover = models.ImageField(
        upload_to="books/covers/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True, verbose_name = "فعال / غیرفعال")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"

    def __str__(self):
        return self.title


class BookImage(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="books/gallery/")
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تصویر {self.book.title}"