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

    def list(self, request, *args, **kwargs):
        # 읽기: 모두 허용
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # 읽기: 모두 허용 (댓글 포함)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # 작성자 자동 설정 (PK 자동 할당)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:  # PK 비교로 본인 확인
            return Response({"detail": "본인 게시글만 수정 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:  # PK 비교로 본인 확인
            return Response({"detail": "본인 게시글만 삭제 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['parent_lookup_article'])

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = Article.objects.get(pk=self.kwargs['parent_lookup_article'])
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:  # PK 비교로 본인 확인
            return Response({"detail": "본인 댓글만 수정 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        if instance.user.pk != request.user.pk:  # PK 비교로 본인 확인
            return Response({"detail": "본인 댓글만 삭제 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)