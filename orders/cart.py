
from books.models import Book


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("cart")

        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, book, quantity=1, override_quantity=False):

        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {"quantity": 0}

        if override_quantity:
            self.cart[book_id]["quantity"] = quantity
        else:
            self.cart[book_id]["quantity"] += quantity

        self.save()

    def remove(self, book):
        book_id = str(book.id)

        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session.pop("cart", None)
        self.cart = {}

    def __iter__(self):

        book_ids = self.cart.keys()

        books = Book.objects.filter(
            id__in=book_ids,
            is_active=True
        )

        for book in books:
            item = self.cart[str(book.id)].copy()

            item["book"] = book
            item["price"] = book.price
            item["total_price"] = book.price * item["quantity"]

            yield item

    def __len__(self):
        return sum(
            item["quantity"]
            for item in self.cart.values()
        )

    def get_total_price(self):

        return sum(
            item["book"].price * item["quantity"]
            for item in self
        )
