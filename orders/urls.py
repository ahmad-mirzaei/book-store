from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:book_id>/", views.cart_add, name="cart_add"),
    path("remove/<int:book_id>/", views.cart_remove, name="cart_remove"),
    path("update/<int:book_id>/", views.cart_update, name="cart_update"),
    path("create-order/", views.create_order, name="create_order"),
    path("track/", views.track_order, name="track_order"),
    
]