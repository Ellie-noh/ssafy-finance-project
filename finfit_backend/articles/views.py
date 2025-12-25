from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_nested.viewsets import NestedViewSetMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleCreateSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
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
        article_id = self._get_article_id()
        if not article_id:
            return Response({'detail': 'Missing article id.'}, status=400)

        article = get_object_or_404(Article, pk=article_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=201)
