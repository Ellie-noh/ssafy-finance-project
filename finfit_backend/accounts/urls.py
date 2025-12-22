from django.urls import path, include
from .views import UserProfileView

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 비번 변경 등
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # 조회/수정
]