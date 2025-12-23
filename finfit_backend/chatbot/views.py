from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatbotView(APIView):
    def post(self, request):
        user_message = request.data.get('message', '')
        
        if not user_message:
            return Response({"error": "메시지를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 시스템 프롬프트: 금융 상품 추천 챗봇
            system_prompt = """
            당신은 금융 상품 추천 전문 AI 어시스턴트입니다. 
            사용자의 상황에 맞춰 예금, 적금 상품을 추천해주세요.
            
            추천 시 고려사항:
            - 사용자의 연령, 소득, 목적에 맞춰 추천
            - 금리 우대 조건 설명
            - 위험도 안내
            - 구체적인 상품명과 특징 언급
            
            친절하고 전문적인 tone으로 응답하세요.
            """
            
            # 임시: 더미 응답으로 테스트
            # 간단한 응답으로 테스트
            if "예금" in user_message or "적금" in user_message:
                ai_message = "현재 인기 있는 예금 상품으로는 '코드K 정기예금'이 있습니다. 최고 연 4.0% 금리로, 1년 만기 시 우대금리가 적용됩니다. 더 자세한 추천을 원하시면 구체적인 상황을 알려주세요!"
            elif "안녕" in user_message:
                ai_message = "안녕하세요! 저는 AI 금융 추천 봇입니다. 예금, 적금 상품 추천을 도와드릴게요. 무엇을 도와드릴까요?"
            else:
                ai_message = f"'{user_message}'에 대해 물어보셨네요. 저는 금융 상품 추천 전문 봇입니다. 예금이나 적금에 대해 물어보세요!"
            
            return Response({"message": ai_message})
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")  # 디버깅용
            return Response({"error": f"AI 응답 생성 실패: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
