<template>
  <section class="hero">
    <div class="hero-left">
      <p class="badge">FinFit • 한 곳에서 금융 비교</p>
      <h1 class="title">
        금융 상품 추천과 현물 정보, 은행 정보를
        <br />
        한 번에 확인하세요
      </h1>
      <p class="subtitle">
        지금은 프론트 UI 단계예요. 나중에 백엔드 API만 연결하면
        추천/게시판/현물 데이터를 실시간으로 보여줄 수 있어요.
      </p>

      <div class="cta">
        <RouterLink to="/products" class="btn primary">상품 둘러보기</RouterLink>
        <RouterLink to="/fx" class="btn ghost">현물 정보 보기</RouterLink>
        <RouterLink to="/banks" class="btn ghost">은행 찾기</RouterLink>
      </div>

      <div class="stats">
        <div class="stat">
          <p class="stat-num">3</p>
          <p class="stat-label">핵심 기능</p>
        </div>
        <div class="stat">
          <p class="stat-num">1</p>
          <p class="stat-label">플랫폼</p>
        </div>
        <div class="stat">
          <p class="stat-num">∞</p>
          <p class="stat-label">확장 가능</p>
        </div>
      </div>
    </div>

    <div class="hero-right">
      <div class="mock-card">
        <p class="mock-title">오늘의 추천</p>

        <div class="mock-item">
          <div class="dot"></div>
          <div class="mock-text">
            <p class="mock-name">예적금 Top3</p>
            <p class="mock-desc">금리, 기간, 혜택 기준으로 한눈에</p>
          </div>
        </div>

        <div class="mock-item">
          <div class="dot"></div>
          <div class="mock-text">
            <p class="mock-name">현물 알림</p>
            <p class="mock-desc">금/은 가격 변동 체크</p>
          </div>
        </div>

        <div class="mock-item">
          <div class="dot"></div>
          <div class="mock-text">
            <p class="mock-name">가까운 은행</p>
            <p class="mock-desc">지도 기반으로 빠르게 찾기</p>
          </div>
        </div>

        <RouterLink to="/board" class="mock-link">커뮤니티 보러가기 →</RouterLink>
      </div>
    </div>
  </section>

  <section class="grid">
    <article class="card">
      <h2 class="card-title">금융 상품</h2>
      <p class="card-desc">
        예적금/대출 등 상품을 비교하고, 추천 기준을 확장할 수 있어요.
      </p>
      <RouterLink to="/products" class="card-link">Products →</RouterLink>
    </article>

    <article class="card">
      <h2 class="card-title">현물 정보</h2>
      <p class="card-desc">
        금/은 현물 가격과 변동 추이를 한 화면에서 볼 수 있게 구성할 수 있어요.
      </p>
      <RouterLink to="/fx" class="card-link">Fx →</RouterLink>
    </article>

    <article class="card">
      <h2 class="card-title">은행 찾기</h2>
      <p class="card-desc">
        지도 API 연동 후 위치 기반 검색으로 확장할 수 있어요.
      </p>
      <RouterLink to="/banks" class="card-link">BankMap →</RouterLink>
    </article>

    <article class="card">
      <h2 class="card-title">게시판</h2>
      <p class="card-desc">
        커뮤니티로 후기/질문을 공유하고, 로그인 연동도 쉽게 붙일 수 있어요.
      </p>
      <RouterLink to="/board" class="card-link">Board →</RouterLink>
    </article>
  </section>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
  align-items: center;
  padding: 24px 0 8px;
}

.hero-left {
  padding: 12px 0;
}

.badge {
  display: inline-block;
  font-size: 13px;
  padding: 6px 10px;
  border-radius: 999px;
  background: #f3f4f6;
  color: #111827;
  margin-bottom: 12px;
}

.title {
  font-size: 36px;
  line-height: 1.2;
  margin: 0 0 10px;
  color: #111827;
}

.subtitle {
  margin: 0 0 18px;
  color: #4b5563;
  line-height: 1.6;
}

.cta {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  border: 1px solid #e5e7eb;
  color: #111827;
  background: #fff;
}

.btn.primary {
  background: #111827;
  color: #fff;
  border-color: #111827;
}

.btn.ghost:hover {
  background: #f9fafb;
}

.stats {
  display: flex;
  gap: 18px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.stat {
  min-width: 110px;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
}

.stat-num {
  font-size: 22px;
  font-weight: 800;
  margin: 0;
  color: #111827;
}

.stat-label {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.hero-right {
  display: flex;
  justify-content: flex-end;
}

.mock-card {
  width: 100%;
  max-width: 360px;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 16px;
  background: #ffffff;
}

.mock-title {
  font-weight: 800;
  margin: 0 0 12px;
  color: #111827;
}

.mock-item {
  display: flex;
  gap: 10px;
  padding: 10px;
  border-radius: 12px;
  background: #f9fafb;
  margin-bottom: 10px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  margin-top: 6px;
  background: #111827;
}

.mock-name {
  margin: 0;
  font-weight: 700;
  color: #111827;
}

.mock-desc {
  margin: 4px 0 0;
  font-size: 13px;
  color: #6b7280;
}

.mock-link {
  display: inline-block;
  margin-top: 6px;
  text-decoration: none;
  color: #111827;
  font-weight: 700;
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 18px 0 10px;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 14px;
  background: #fff;
}

.card-title {
  margin: 0 0 8px;
  font-size: 16px;
  color: #111827;
}

.card-desc {
  margin: 0 0 12px;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.card-link {
  text-decoration: none;
  font-weight: 700;
  color: #111827;
}

@media (max-width: 960px) {
  .hero {
    grid-template-columns: 1fr;
  }
  .hero-right {
    justify-content: flex-start;
  }
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 520px) {
  .title {
    font-size: 28px;
  }
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
