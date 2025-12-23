from django.urls import path, include
from rest_framework_nested import routers
from .views import ArticleViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)

articles_router = routers.NestedDefaultRouter(router, r'articles', lookup='article')
articles_router.register(r'comments', CommentViewSet, basename='article-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(articles_router.urls)),
]