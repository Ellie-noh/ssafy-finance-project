from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer
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
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': '잘못된 자격 증명'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': '로그아웃 성공'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_profile(request):
    if not request.user.is_authenticated:
        return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
    user = request.user
    joined_products = user.joined_products.all()
    from deposits.serializers import DepositProductSerializer
    products_data = DepositProductSerializer(joined_products, many=True).data
    from articles.models import Article
    from articles.serializers import ArticleSerializer
    user_articles = Article.objects.filter(user=user)
    articles_data = ArticleSerializer(user_articles, many=True).data
    return Response({
        "user": UserSerializer(user).data,
        "joined_products": products_data,
        "user_articles": articles_data
    })

@api_view(['POST'])
def join_product(request, fin_prdt_cd):
    if not request.user.is_authenticated:
        return Response({"detail": "로그인 후 이용 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
    try:
        product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        request.user.joined_products.add(product)
        return Response({"message": "가입 성공"})
    except DepositProduct.DoesNotExist:
        return Response({"error": "상품을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
