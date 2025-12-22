from rest_framework import serializers
from .models import CustomUser
from products.serializers import ProductSerializer  # 가입 상품 Serializer (F03 가정)

class CustomUserSerializer(serializers.ModelSerializer):
    joined_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'joined_products']
        read_only_fields = ['id']

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user