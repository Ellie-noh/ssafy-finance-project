from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, LoginSerializer, CustomUserSerializer
from deposits.models import DepositProduct


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out.'}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'DELETE':
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        request.user.delete()
        return Response({'message': 'Account deleted.'}, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    joined_products = user.joined_products.all()
    from deposits.serializers import DepositProductSerializer
    products_data = DepositProductSerializer(joined_products, many=True).data
    from articles.models import Article
    from articles.serializers import ArticleSerializer
    user_articles = Article.objects.filter(user=user)
    articles_data = ArticleSerializer(user_articles, many=True).data
    return Response({
        'user': CustomUserSerializer(user).data,
        'joined_products': products_data,
        'user_articles': articles_data
    })


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def join_product(request, fin_prdt_cd):
    product = get_object_or_404(DepositProduct, fin_prdt_cd=fin_prdt_cd)
    if request.method == 'DELETE':
        request.user.joined_products.remove(product)
        return Response({'message': 'Join canceled.'})

    request.user.joined_products.add(product)
    return Response({'message': 'Joined.'})
