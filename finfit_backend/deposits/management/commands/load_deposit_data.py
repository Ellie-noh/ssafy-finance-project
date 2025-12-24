from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from deposits.models import DepositProduct, DepositOption

API_KEY = settings.API_KEY
URL = 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

class Command(BaseCommand):
    help = 'Load deposit products from external API'

    def handle(self, *args, **options):
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
                self.stdout.write(self.style.ERROR('API 응답 형식이 올바르지 않습니다.'))
                return
            
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

            # 모든 옵션 저장 후 max_rate 계산 및 업데이트
            for product in DepositProduct.objects.all():
                options = product.options.all()
                if options:
                    max_rate = max([opt.intr_rate2 for opt in options if opt.intr_rate2 and opt.intr_rate2 > 0] or [0])
                    product.max_rate = max_rate if max_rate > 0 else None
                    product.save()

            self.stdout.write(self.style.SUCCESS(f'성공: {len(data["result"]["baseList"])}개 상품 저장'))
        
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'API 요청 실패: {str(e)}'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'JSON 파싱 실패: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'알 수 없는 오류: {str(e)}'))