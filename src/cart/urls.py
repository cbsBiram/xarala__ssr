from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:course_id>/", views.cart_add, name="cart_add"),
    path(
        "add-to-cart/<str:course_slug>/",
        views.add_course_to_cart,
        name="add_course_to_cart",
    ),
    path("remove/<int:course_id>/", views.cart_remove, name="cart_remove"),
]
