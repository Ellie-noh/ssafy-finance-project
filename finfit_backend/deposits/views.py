from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests

from .models import DepositProduct, DepositOption
from .serializers import DepositProductSerializer, DepositOptionSerializer

API_KEY = settings.API_KEY
URL = 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'


@api_view(['GET'])
def save_deposit_products(request):
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',   # 은행만
        'pageNo': '1',
    }

    response = requests.get(URL, params=params).json()

    for base in response['result']['baseList']:
        product_data = {
            'fin_prdt_cd': base['fin_prdt_cd'],
            'kor_co_nm': base['kor_co_nm'],
            'fin_prdt_nm': base['fin_prdt_nm'],
            'etc_note': base.get('etc_note', ''),
            'join_deny': int(base['join_deny']),
            'join_member': base.get('join_member', ''),
            'join_way': base.get('join_way', ''),
            'spcl_cnd': base.get('spcl_cnd', ''),
        }

        product, _ = DepositProduct.objects.update_or_create(
            fin_prdt_cd=base['fin_prdt_cd'],
            defaults=product_data
        )

    for option in response['result']['optionList']:
        try:
            product = DepositProduct.objects.get(fin_prdt_cd=option['fin_prdt_cd'])
        except DepositProduct.DoesNotExist:
            continue

        intr_rate = option.get('intr_rate')
        if intr_rate is None:
            intr_rate = -1
        intr_rate2 = option.get('intr_rate2')
        if intr_rate2 is None:
            intr_rate2 = -1

        option_data = {
            'product': product,
            'intr_rate_type_nm': option['intr_rate_type_nm'],
            'save_trm': option['save_trm'],
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
        }

        DepositOption.objects.update_or_create(
            product=product,
            save_trm=option['save_trm'],
            defaults=option_data
        )

    return Response({"message": "okay"})


@api_view(['GET'])
def deposit_products(request):
    products = DepositProduct.objects.all()
    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_product(request):
    serializer = DepositProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message": "데이터 삽입 성공"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def product_options(request, fin_prdt_cd):
    product = get_object_or_404(DepositProduct, fin_prdt_cd=fin_prdt_cd)
    options = product.options.all()
    serializer = DepositOptionSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_rate(request):
    top_option = DepositOption.objects.order_by('-intr_rate2').first()
    if not top_option:
        return Response({"message": "데이터 없음"})
    data = {
        **DepositProductSerializer(top_option.product).data,
        "save_trm": top_option.save_trm,
        "intr_rate_type_nm": top_option.intr_rate_type_nm,
        "intr_rate": top_option.intr_rate,
        "intr_rate2": top_option.intr_rate2,
    }
    return Response(data)