from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_nested.viewsets import NestedViewSetMixin
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleCreateSerializer, CommentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateSerializer
        return ArticleSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    parent_lookup_kwargs = {'article_pk': 'article_id'}

    def _get_article_id(self):
        return (
            self.kwargs.get('parent_lookup_article')
            or self.kwargs.get('article_pk')
            or self.kwargs.get('article_id')
        )

    def get_queryset(self):
        article_id = self._get_article_id()
        if not article_id:
            return Comment.objects.none()
        return Comment.objects.filter(article_id=article_id)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)

        article_id = self._get_article_id()
        if not article_id:
            return Response({'detail': 'Missing article id.'}, status=status.HTTP_400_BAD_REQUEST)

        article = Article.objects.filter(pk=article_id).first()
        if not article:
            return Response({'detail': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
