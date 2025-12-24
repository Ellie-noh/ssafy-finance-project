import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import os

GOLD_FILE = os.path.join(settings.BASE_DIR, 'static', 'files', 'Gold_prices.xlsx')
SILVER_FILE = os.path.join(settings.BASE_DIR, 'static', 'files', 'Silver_prices.xlsx')

try:
    gold_df = pd.read_excel(GOLD_FILE)
    silver_df = pd.read_excel(SILVER_FILE)

    # print("Gold columns:", gold_df.columns.tolist())
    # print("Silver columns:", silver_df.columns.tolist())

    gold_df['Date'] = pd.to_datetime(gold_df['Date'])
    silver_df['Date'] = pd.to_datetime(silver_df['Date'])

    if 'Close/Last' in gold_df.columns:
        gold_df['Price'] = gold_df['Close/Last']
    elif 'Close' in gold_df.columns:
        gold_df['Price'] = gold_df['Close']

    if 'Close/Last' in silver_df.columns:
        silver_df['Price'] = silver_df['Close/Last']
    elif 'Close' in silver_df.columns:
        silver_df['Price'] = silver_df['Close']

    # Clean gold prices: remove commas and convert to float
    gold_df['Price'] = gold_df['Price'].str.replace(',', '').astype(float)

    # print("Gold Price sample:", gold_df['Price'].head())
    # print("Silver Price sample:", silver_df['Price'].head())

    # Remove NaN values
    gold_df = gold_df.dropna(subset=['Price'])
    silver_df = silver_df.dropna(subset=['Price'])

except Exception as e:
    print("Excel 파일 로드 실패:", e)
    gold_df = pd.DataFrame()
    silver_df = pd.DataFrame()

class AssetPriceView(APIView):
    def get(self, request):
        asset = request.query_params.get('asset', 'gold')  # gold or silver
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if asset == 'gold':
            df = gold_df.copy()
            asset_name = '금'
        elif asset == 'silver':
            df = silver_df.copy()
            asset_name = '은'
        else:
            return Response({"error": "asset 파라미터는 gold 또는 silver여야 합니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        if df.empty:
            return Response({"error": "데이터 로드에 실패했습니다. 파일 경로를 확인하세요."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 기간 필터링
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                df = df[df['Date'] >= start]
            except ValueError:
                return Response({"error": "start_date 형식은 YYYY-MM-DD여야 합니다."},
                                status=status.HTTP_400_BAD_REQUEST)

        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                df = df[df['Date'] <= end]
            except ValueError:
                return Response({"error": "end_date 형식은 YYYY-MM-DD여야 합니다."},
                                status=status.HTTP_400_BAD_REQUEST)

        if df.empty:
            return Response({
                "asset": asset_name,
                "message": "선택한 기간에 데이터가 없습니다.",
                "labels": [],
                "prices": []
            })

        df = df.sort_values('Date')
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        # NaN 값 제거
        df = df.dropna(subset=['Price'])

        data = {
            "asset": asset_name,
            "labels": df['Date'].tolist(),
            "prices": df['Price'].tolist() 
        }
        return Response(data)