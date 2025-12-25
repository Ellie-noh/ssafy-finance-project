from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.conf import settings
import requests

from .models import DepositProduct, DepositOption
from .serializers import DepositProductSerializer, DepositOptionSerializer

API_KEY = settings.API_KEY
DEPOSIT_URL = 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SAVING_URL = 'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'


def _fetch_products_page(url, page_no):
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': str(page_no),
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if 'result' not in data:
        raise ValueError('Invalid API response')

    base_list = data['result'].get('baseList', [])
    option_list = data['result'].get('optionList', [])
    return base_list, option_list


def _save_products(base_list):
    created_count = 0

    for base in base_list:
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

        _, created = DepositProduct.objects.get_or_create(
            fin_prdt_cd=base['fin_prdt_cd'],
            defaults=product_data,
        )
        if created:
            created_count += 1

    return created_count


def _save_options(option_list):
    for option in option_list:
        product = DepositProduct.objects.filter(fin_prdt_cd=option['fin_prdt_cd']).first()
        if not product:
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
            defaults=option_data,
        )


def _update_max_rates():
    for product in DepositProduct.objects.all():
        options = product.options.all()
        if options:
            max_rate = max(
                [opt.intr_rate2 for opt in options if opt.intr_rate2 and opt.intr_rate2 > 0] or [0]
            )
            product.max_rate = max_rate if max_rate > 0 else None
            product.save()


def _load_products(target_total=100, max_pages=50):
    if not API_KEY:
        return False, {'error': 'API key is missing.'}, status.HTTP_500_INTERNAL_SERVER_ERROR

    created_total = 0
    page_no = 1

    while page_no <= max_pages and DepositProduct.objects.count() < target_total:
        new_on_page = 0
        has_data = False

        for url in (DEPOSIT_URL, SAVING_URL):
            base_list, option_list = _fetch_products_page(url, page_no)
            if base_list:
                has_data = True
            new_on_page += _save_products(base_list)
            _save_options(option_list)

        if not has_data:
            break

        if new_on_page == 0:
            break

        created_total += new_on_page
        page_no += 1

    _update_max_rates()

    return True, {
        'message': 'Loaded deposit and saving products.',
        'created': created_total,
        'total': DepositProduct.objects.count(),
        'pages': page_no - 1,
    }, status.HTTP_200_OK


@api_view(['GET'])
@permission_classes([IsAdminUser])
def save_deposit_products(request):
    try:
        success, payload, code = _load_products()
        return Response(payload, status=code)
    except requests.exceptions.RequestException as e:
        return Response({'error': f'API request failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValueError as e:
        return Response({'error': f'JSON parse failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': f'Unknown error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def deposit_products(request):
    if not DepositProduct.objects.exists():
        try:
            success, payload, code = _load_products()
            if not success:
                return Response(payload, status=code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'API request failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({'error': f'JSON parse failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'Unknown error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    products = DepositProduct.objects.all()
    bank = request.query_params.get('bank') or request.query_params.get('kor_co_nm')
    if bank:
        products = products.filter(kor_co_nm=bank)

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
    seen_products = set()
    data = []

    for option in DepositOption.objects.order_by('-intr_rate2'):
        product_id = option.product_id
        if product_id in seen_products:
            continue
        seen_products.add(product_id)

        data.append({
            **DepositProductSerializer(option.product).data,
            'save_trm': option.save_trm,
            'intr_rate_type_nm': option.intr_rate_type_nm,
            'intr_rate': option.intr_rate,
            'intr_rate2': option.intr_rate2,
        })

        if len(data) >= 5:
            break

    return Response(data)
