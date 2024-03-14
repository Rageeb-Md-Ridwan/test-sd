from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("details/<int:id>/", views.DetailPostView.as_view(), name="detail_post"),
    path("details/<int:id>/purchase/", views.purchase_car, name="purchase_car"),
    path("details/<int:id>/purchase/", views.purchase_car, name="purchase_car"),
]
