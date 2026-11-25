from django.urls import path
from . import views

urlpatterns = [
    path("<int:order_id>/", views.payment_page, name="payment_page"),
    path("<int:order_id>/success/", views.payment_success, name="payment_success"),
    path("<int:order_id>/cancel/", views.cancel_order, name="cancel_order"),
]