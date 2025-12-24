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


# 💎 FinFit  
### AI 기반 맞춤형 금융 상품 추천 서비스  
> **당신의 자산 관리에 딱 맞는 옷을 입혀드립니다**

사용자의 금융 성향을 분석하는 **AI 챗봇**과  
**실시간 FX(금·은) 데이터 시각화**를 결합한  
**스마트 금융 큐레이션 플랫폼**

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Main_Stack-Django%20%7C%20Vue.js-41B883?style=flat-square"/>
  <img src="https://img.shields.io/badge/AI_Engine-OpenAI_GPT-orange?style=flat-square"/>
</p>

---

## 📖 Service Overview

**FinFit**은 수많은 예·적금 상품 속에서  
어떤 상품이 나에게 적합한지 판단하기 어려운 사용자를 위해 탄생했습니다.

단순한 나열식 금융 정보 제공에서 벗어나  
- 생성형 AI가 **사용자의 니즈와 상황을 이해하고**
- 최적의 금융 상품을 **이유와 함께 추천**하며
- 금·은 자산 시세를 **직관적인 차트로 시각화**합니다.

👉 정보 탐색이 아닌, **의사결정을 돕는 금융 서비스**를 목표로 합니다.

---

## 👥 Team & Roles

### 🧑‍💼 Backend  
**황효섭 (Team Leader)**

- **Architecture**
  - Django 기반 REST API 전체 구조 설계
  - 서버 아키텍처 및 프로젝트 구조화
- **Data Engineering**
  - Pandas를 활용한 예·적금 상품 데이터 전처리
  - FX(금·은) Excel 데이터 로딩 및 기간 필터링 로직 구현
- **System Integration**
  - AI 추천 및 챗봇 API 엔드포인트 구축
  - CORS 및 서버 환경 설정

---

### 🎨 Frontend  
**노유연 (Frontend Lead)**

- **UI/UX Design**
  - Vue.js 기반 반응형 웹 UI 설계
  - 사용자 흐름 중심의 화면 구성 및 컴포넌트 설계
- **Data Visualization**
  - 금·은 시세 변동 차트 구현
  - 금융 상품 리스트 및 필터링 UI 구현
- **AI Interface**
  - 플로팅 챗봇 UI 구현
  - 실시간 메시지 처리 및 사용자 인터랙션 구현

---

### 🤝 AI 기능 공동 수행
- AI 추천 시나리오 및 프롬프트 구조 공동 설계
- 추천 결과를 자연어로 설명하는 응답 로직 구성
- 사용자 질문 → 추천 → 설명까지 이어지는 흐름 협업

---

## ✨ Key Features

### 1️⃣ Intelligent Product Curation

- **Smart Filter**
  - 은행별, 금리별 필터링으로 원하는 상품을 빠르게 탐색
- **Interest TOP 5**
  - 우대금리 기준 상위 5개 상품 자동 추천
- **Detail Analysis**
  - 복잡한 가입 조건과 우대 조건을 핵심 정보 중심으로 제공

---

### 2️⃣ FX Market Visualizer

- **Gold & Silver Tracking**
  - Excel 기반 금·은 시세 데이터 조회
- **Period Selection**
  - 사용자가 선택한 기간에 따른 시세 흐름 시각화
- **Validation**
  - 선택 기간 내 데이터가 없을 경우 안내 메시지 제공

---

### 3️⃣ FinFit AI Chatbot

- **Natural Language Processing**
  - 자연어 질문을 통한 금융 상품 추천
- **Reasoning Service**
  - 단순 추천이 아닌, 추천 이유를 함께 설명
- **Interactive UI**
  - 플로팅 형태의 챗봇으로 언제든지 접근 가능

---

## ⚙️ Technology Stack

| Category | Tech Stack |
|--------|-----------|
| Backend | Django, Django REST Framework |
| Frontend | Vue.js, HTML, CSS |
| Data Processing | Pandas |
| AI | OpenAI GPT |
| Visualization | SVG 기반 차트 |
| Tooling | GitLab, Figma |

---

## 🔍 Recommendation Algorithm

FinFit의 금융 상품 추천은 다음 **4단계 프로세스**로 이루어집니다.

1. **Keyword Extraction**  
   - 사용자 질문에서 연령, 금액, 기간, 금융 성향 키워드 추출
2. **Candidate Filtering**  
   - 상품 데이터베이스에서 조건에 부합하는 후보군 생성
3. **Scoring & Ranking**  
   - 우대금리, 가입 기간에 가중치를 부여해 상품 정렬
4. **AI Response Generation**  
   - 최종 추천 상품을 기반으로 사용자 맞춤 설명 생성

---

## 💬 Project Retrospective

### “연결의 가치를 배우다”  
**황효섭**

> 프론트엔드와 백엔드가 데이터라는 공통 언어로 소통하며  
> 하나의 서비스를 완성해가는 과정에서  
> 협업과 구조 설계의 중요성을 깊이 체감했습니다.

---

### “사용자의 눈으로 바라보기”  
**노유연**

> 복잡한 금융 데이터를 어떻게 하면 더 직관적으로 전달할 수 있을지 고민하며  
> 기술 구현을 넘어 사용자 중심 설계의 중요성을 배울 수 있었습니다.

---

## 📌 GitLab Project Name

