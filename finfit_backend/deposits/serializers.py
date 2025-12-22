from rest_framework import serializers
from .models import DepositProduct, DepositOption

class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'

class DepositOptionSerializer(serializers.ModelSerializer):
    product = DepositProductSerializer(read_only=True)   # 옵션에 상품 정보 포함

    class Meta:
        model = DepositOption
        fields = '__all__'