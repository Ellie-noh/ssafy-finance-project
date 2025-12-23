from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('deposits/', include('deposits.urls')),
    path('goldsnsilvers/', include('goldsnsilvers.urls')),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
]
