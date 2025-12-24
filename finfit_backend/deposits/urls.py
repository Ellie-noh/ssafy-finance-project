from django.urls import path
from . import views

urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.product_options),
    path('deposit-product/<str:fin_prdt_cd>/', views.product_detail),
    path('top-rates/', views.top_rates),
]
