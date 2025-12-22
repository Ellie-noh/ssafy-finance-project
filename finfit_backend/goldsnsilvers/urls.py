from django.urls import path
from .views import AssetPriceView

urlpatterns = [
    path('api/asset-prices/', AssetPriceView.as_view(), name='asset-prices'),
]




"""
프론트 호출 예시

// 전체 금 데이터
axios.get('/api/asset-prices/?asset=gold')

// 특정 기간 은 데이터
axios.get('/api/asset-prices/?asset=silver&start_date=2025-01-01&end_date=2025-12-31')


선택 기간 내에 없을 때

if df.empty:
            return Response({
                "asset": asset_name,
                "message": "선택한 기간에 데이터가 없습니다.",
                "labels": [],
                "prices": []
            })

"""