from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
from deposits.models import DepositProduct, DepositOption


# GMS에서 제공하는 OpenAI 호환 엔드포인트 사용
client = OpenAI(
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
    api_key=settings.OPENAI_API_KEY,
)

class ChatbotView(APIView):
    def post(self, request):
        user_message = request.data.get('message', '')

        if not user_message:
            return Response({"error": "메시지를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 예적금 상품 데이터 가져오기 (모든 상품, max_rate 기준 정렬)
            products = (
                DepositProduct.objects.filter(max_rate__isnull=False)
                .prefetch_related('options')
                .order_by('-max_rate')
            )
            product_data = []
            has_savings = False  # 적금 데이터 유무 확인
            for product in products:
                if '적금' in product.fin_prdt_nm:
                    has_savings = True
                options = product.options.all()
                option_info = []
                for opt in options:
                    option_info.append(f"기간: {opt.save_trm}개월, 기본금리: {opt.intr_rate}%, 최고금리: {opt.intr_rate2}%")
                product_data.append(f"상품명: {product.fin_prdt_nm}, 은행: {product.kor_co_nm}, 최고금리: {product.max_rate}%, 옵션: {'; '.join(option_info)}")
            
            product_context = "\n".join(product_data)
            
            # 시스템 프롬프트: 금융 상품 추천 챗봇
            system_prompt = f"""
            당신은 금융 상품 추천 전문 AI 어시스턴트입니다. 
            사용자의 상황에 맞춰 예금, 적금 상품을 추천해주세요.
            
            추천 시 고려사항:
            - 사용자의 연령, 소득, 목적에 맞춰 추천
            - 금리 우대 조건 설명
            - 위험도 안내 (예금은 안전)
            - 구체적인 상품명과 특징 언급
            - 답변은 핵심만 3줄 이내, 불릿 2-3개로 간결하게
            - 단락과 불릿을 명확히 분리해 가독성을 높이세요 (예: 섹션 제목 + 줄바꿈 + 불릿).
            - 문장은 한 줄씩 분리해 줄바꿈을 넣어주세요. 불릿/섹션별로 개행을 명확히 넣어 가독성을 높이세요.
            - 불릿은 반드시 새 줄에서 시작하세요. 한 줄에 문장 여러 개를 붙이지 말고, 예시처럼 줄바꿈을 충분히 사용하세요.
            - 이모티콘은 1-2개만 적게 사용하세요 (과하지 않게 😊 정도).
            - 먼저 필수 정보(나이대, 월 저축 가능액, 목적)가 없으면 3문항 이하의 초간단 설문으로 확인 후 추천하세요. 설문도 불릿 1줄씩, 짧게.
            - 사용자 조건(기간/목적/금액/연령)에 맞춰 상품을 골라주세요. 단순히 금리 상위만 반복하지 말고, 조건과 맞는 상품을 1-2개만 엄선하세요. 같은 상품을 반복 추천하지 마세요.
            - 추천 시에는 '상품명 / 은행 / 금리(최고)'를 명확히 쓰고, 사용자의 조건에 왜 맞는지 한 줄 이유를 덧붙이세요.
            친절하고 전문적인 tone으로 응답하세요. 불필요한 수사는 생략하고 요점만 전해주세요.
            
            현재 이용 가능한 예금 상품 데이터:
            {product_context}

            응답 형식:
            - 추천 상품 1-2개
            - 각 상품의 장점과 우대 조건
            - 주의사항
            """

            # 적금 요청인데 적금 데이터가 없으면 시스템 프롬프트에 미리 안내
            if ("적금" in user_message) and not has_savings:
                system_prompt += """
                현재 적금(적립식) 상품 데이터는 없습니다. 대신:
                - 일반적인 적금 선택 팁과 우대 조건을 짧게 안내하세요.
                - 제공된 예금 상품 중 금리가 높은 것을 적금 대안으로 1-2개 추천하세요.
                """

            try:
                completion = client.chat.completions.create(
                    model="gpt-4.1",  # GMS에서 지원되는 모델
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    max_tokens=256,
                )
                ai_message = completion.choices[0].message.content
            except Exception as api_error:
                print(f"GMS(OpenAI) 호출 실패: {str(api_error)}")
                # Fallback: 간단한 추천
                if "예금" in user_message or "적금" in user_message:
                    top_products = list(
                        DepositProduct.objects.filter(max_rate__isnull=False)
                        .order_by('-max_rate')[:2]
                    )
                    if top_products:
                        lines = []
                        for p in top_products:
                            options = "; ".join([
                                f"{opt.save_trm}개월 {opt.intr_rate2 or opt.intr_rate}%"
                                for opt in p.options.all()
                            ])
                            lines.append(f"- {p.fin_prdt_nm} / {p.kor_co_nm} / 최고 {p.max_rate}% (옵션: {options})")
                        ai_message = "추천 예금 상위 금리 상품:\n" + "\n".join(lines)
                    else:
                        ai_message = "현재 인기 있는 예금 상품으로는 상위 금리 상품을 추천드려요. 최고 금리 상품을 확인해보세요!"
                else:
                    ai_message = "금융 상품 추천에 대해 물어보세요. 예금이나 적금 상품을 추천해드릴게요!"
            
            return Response({"message": ai_message})
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")  # 디버깅용
            return Response({"error": f"AI 응답 생성 실패: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
