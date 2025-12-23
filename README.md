# SSAFY 맞춤 금융상품 추천 서비스 FinFit

> **서울 6반 4조** - 금융 상품 비교·추천 + 환율 + 근처 은행 찾기까지 한 번에!  
> 금융감독원·한국수출입은행·카카오맵 API를 활용한 사용자 맞춤형 금융 웹 서비스

## 서비스 개요

- 금융 상품 가입 및 마이페이지 관리
- 사용자에게 **맞춤형 정기예금 상품 추천**
- 실시간 **환율 조회·계산·차트**
- 위치 기반 **근처 은행 지도 검색**
- 자유로운 금융 정보 공유를 위한 **커뮤니티 게시판**

## 주요 기능

| 기능                  | 설명                                                                  |
|-----------------------|----------------------------------------------------------------------|
| 회원가입 / 로그인      | 사용자 인증 회원관리 시스템                                               |
| 금융상품 목록 & 검색   | 금융감독원 API 연동 → 정기예금 상품 조회·검색                               |
| 금리 TOP5 추천        | 최고 금리 기준 상위 5개 상품 추천                                          |
| 상품 가입 신청        | 관심 상품에 바로 가입 신청                                                 |
| 환율 계산기 & 차트     | 한국수출입은행 API → 환율 계산 및 기간별 차트                               |
| 근처 은행 찾기        | Kakao Map API 연동 → 위치 기준 은행 마커 표시                              | 
| 커뮤니티 게시판       | CRUD 완비, 작성자만 수정/삭제 가능                                         |
| 마이페이지            | 가입한 상품, 나의 게시글 조회, 회원정보 수정, 탈퇴                           |

## 작업 분해 및 계획

![WBS](assets/WBS.JPG)


## 프로젝트 구조
### ERD (Entity Relationship Diagram)

![ERD](assets/ERD.png)

### UCD (Use Case Diagram)

![UCD](assets/UCD.png)

# 화면설계

- figma 링크
https://www.figma.com/design/hVRARKTw7g033STaYzLGvy/%EC%A0%9C%EB%AA%A9-%EC%97%86%EC%9D%8C?node-id=0-1&t=TphFpSBO6CFi0nbf-1

- 화면 목록
홈페이지 / 금융 상품 목록 / 환율 / 은행 지도 / 게시판 / 개인 프로필 / 로그인 / 회원 가입

### 상세 이미지

#### 홈페이지 
![HOMEPAGE](assets/홈페이지.png)

#### 금융 상품 목록 
![LIST](assets/금융상품목록화면.png)

#### 환율 
![EXCHANGE](assets/환율.png)

#### 은행 지도 
![MAP](assets/은행지도.png)

#### 게시판
![ARTICLE](assets/게시판.png)

#### 개인 프로필 
![PROFILE](assets/개인프로필.png)

#### 로그인
![LOGIN](assets/로그인.png)


#### 회원 가입 
![SIGNUP](assets/회원가입.png)

💎 FinFit: AI 기반 맞춤형 금융 상품 추천 서비스

"당신의 자산 관리에 딱 맞는 옷을 입혀드립니다." > 사용자의 성향을 분석하는 AI 챗봇과 실시간 FX 데이터 시각화를 결합한 스마트 금융 큐레이션 플랫폼

<p align="center">

<img src="https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square">

<img src="https://img.shields.io/badge/Main_Stack-Django_%7C_Vue.js-41B883?style=flat-square">

<img src="https://img.shields.io/badge/AI_Engine-OpenAI_GPT-orange?style=flat-square">

</p>

📖 Service Overview

FinFit은 복잡한 금융 상품들 속에서 길을 잃은 사용자를 위해 탄생했습니다.

단순한 나열식 정보 제공에서 벗어나, 생성형 AI가 사용자의 니즈를 파악하고 최적의 예적금 상품을 추천하며, 금·은 자산 시세 흐름을 한눈에 파악할 수 있도록 돕습니다.

👥 Team & Roles

[Backend]

황효섭 (Team Leader)

Architecture: Django 기반 REST API 총괄 설계 및 서버 구조화.

Data Engineering: Pandas를 활용한 금융 상품 및 FX(금/은) 데이터 전처리 로직 구현.

System Integration: 추천 시스템 백엔드 엔드포인트 구축 및 CORS/인증 보안 설정.

[Frontend]

노유연 (Frontend Lead)

UI/UX Design: Vue.js 기반의 반응형 웹 디자인 및 사용자 중심 UX 설계.

Data Visualization: Chart.js를 활용한 시세 변동 그래프 및 상품 필터링 시스템 구현.

AI Interface: 대화형 챗봇 UI 및 실시간 메시지 스트리밍 인터렉션 개발.

✨ Key Features

1️⃣ Intelligent Product Curation

Smart Filter: 은행별, 금리별 맞춤 필터링으로 원하는 상품을 1초 만에 검색.

Interest TOP 5: 현재 시장에서 가장 유리한 우대금리 상품 상위 5개를 자동으로 추출하여 추천.

Detail Analysis: 가입 제한, 우대 조건 등 복잡한 약관을 핵심 정보 위주로 요약 제공.

2️⃣ FX Market Visualizer

Gold & Silver Tracking: 엑셀 데이터 기반의 정밀한 시세 데이터 조회.

Period Selection: 사용자가 원하는 기간을 설정하여 과거부터 현재까지의 시세 흐름을 차트로 확인.

3️⃣ FinFit AI Chatbot

Natural Language Processing: 자연어 질의를 통해 "사회초년생을 위한 월 50만 원 적금" 같은 구체적 상황 대응.

Reasoning Service: 단순 추천을 넘어 '왜 이 상품이 사용자에게 적합한지'에 대한 논리적 이유 제공.

⚙️ Technology Stack

CategoryTech StackBackendFrontendDatabase/Tool🔍 Recommendation Algorithm

FinFit은 4단계의 고도화된 추천 프로세스를 거칩니다.

Keyword Extraction: 사용자 질문에서 연령, 금액, 성향 키워드 추출.

Candidate Filtering: 상품 데이터베이스에서 조건에 부합하는 후보군 생성.

Scoring & Ranking: 우대금리 및 기간 가중치를 적용하여 최적의 상품 정렬.

AI Response Generation: 최종 선정된 데이터를 바탕으로 사용자 맞춤형 설명문 생성.

💬 Project Retrospective

"연결의 가치를 배우다" > 황효섭: API 설계부터 환경 설정까지, 프론트엔드와 백엔드가 데이터라는 언어로 소통하며 하나의 완성된 서비스를 만드는 과정에서 협업의 중요성을 깊이 체감했습니다.

"사용자의 눈으로 바라보기" > 노유연: 복잡한 금융 데이터를 어떻게 하면 더 직관적으로 전달할 수 있을지 고민하며, 기술적 구현을 넘어 사용자 관점의 설계(User-Centered Design) 능력을 기를 수 있었습니다.

FinFit이 마음에 드셨다면 상단의 ⭐ Star를 눌러주세요!
