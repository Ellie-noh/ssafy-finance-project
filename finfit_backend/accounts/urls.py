from django.urls import path
from .views import SignupView, LoginView, LogoutView, join_product, user_profile

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('join-product/<str:fin_prdt_cd>/', join_product, name='join_product'),
    path('profile/', user_profile, name='user_profile'),
]