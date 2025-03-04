from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="shop"),
	path("cart/", views.cart, name="cart"),
	path("load_items/", views.load_items, name="load_items"),
]
