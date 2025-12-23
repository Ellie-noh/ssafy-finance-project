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

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외
        data = response.json()
        
        if 'result' not in data:
            return Response({"error": "API 응답 형식이 올바르지 않습니다.", "response": data}, status=400)
        
        # 기존 데이터 삭제 (선택사항)
        DepositProduct.objects.all().delete()
        DepositOption.objects.all().delete()
        
        for base in data['result']['baseList']:
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

        for option in data['result']['optionList']:
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

        return Response({"message": f"성공: {len(data['result']['baseList'])}개 상품 저장"})
    
    except requests.exceptions.RequestException as e:
        return Response({"error": f"API 요청 실패: {str(e)}"}, status=500)
    except ValueError as e:
        return Response({"error": f"JSON 파싱 실패: {str(e)}"}, status=500)
    except Exception as e:
        return Response({"error": f"알 수 없는 오류: {str(e)}"}, status=500)


@api_view(['GET'])
def deposit_products(request):
    products = DepositProduct.objects.all()
    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_options(request, fin_prdt_cd):
    product = get_object_or_404(DepositProduct, fin_prdt_cd=fin_prdt_cd)
    options = product.options.all()
    serializer = DepositOptionSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, fin_prdt_cd):
    product = get_object_or_404(DepositProduct, fin_prdt_cd=fin_prdt_cd)
    serializer = DepositProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def top_rates(request):
    top_options = DepositOption.objects.order_by('-intr_rate2')[:5]
    data = []
    for option in top_options:
        data.append({
            **DepositProductSerializer(option.product).data,
            "save_trm": option.save_trm,
            "intr_rate_type_nm": option.intr_rate_type_nm,
            "intr_rate": option.intr_rate,
            "intr_rate2": option.intr_rate2,
        })
    return Response(data)