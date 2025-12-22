<template>
  <section class="wrap">
    <header class="head">
      <div>
        <h1>Products</h1>
        <p class="sub">예적금 상품을 은행별로 빠르게 비교해요</p>
      </div>

      <div class="controls">
        <select v-model="selectedBank" class="select">
          <option value="">전체 은행</option>
          <option v-for="b in bankOptions" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>
    </header>

    <div v-if="loading" class="state">불러오는 중…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <div v-else class="grid">
      <!-- ✅ 카드 자체를 RouterLink로: 어디 눌러도 상세로 이동 -->
      <RouterLink
        v-for="p in filteredProducts"
        :key="p.fin_prdt_cd"
        class="card"
        :to="`/products/${p.fin_prdt_cd}`"
      >
        <div class="top">
          <div class="bank">{{ p.kor_co_nm }}</div>
          <div class="badge">상품</div>
        </div>

        <h3 class="title">{{ p.fin_prdt_nm }}</h3>

        <div class="meta">
          <div class="meta-item">
            <span class="label">최대 우대금리</span>
            <span class="value">{{ formatRate(getMaxRate2(p)) }}</span>
          </div>
          <div class="meta-item">
            <span class="label">기간</span>
            <span class="value">{{ getTermsText(p) }}</span>
          </div>
        </div>

        <p class="note" v-if="p.etc_note">{{ p.etc_note }}</p>
        <p class="note" v-else>상세에서 가입조건과 금리옵션을 확인할 수 있어요</p>

        <div class="arrow">자세히 보기 →</div>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

const loading = ref(false);
const error = ref("");
const products = ref([]);

const API_URL = import.meta.env.VITE_API_URL || "";

async function fetchProducts() {
  loading.value = true;
  error.value = "";

  try {
    const res = await fetch(`${API_URL}/api/deposits/`, { credentials: "include" });
    if (!res.ok) throw new Error("API 응답 오류");
    const data = await res.json();
    products.value = Array.isArray(data) ? data : [];
  } catch (e) {
    products.value = dummyProducts;
  } finally {
    loading.value = false;
  }
}

const selectedBank = ref("");

const bankOptions = computed(() => {
  const set = new Set(products.value.map((p) => p.kor_co_nm).filter(Boolean));
  return Array.from(set).sort();
});

const filteredProducts = computed(() => {
  if (!selectedBank.value) return products.value;
  return products.value.filter((p) => p.kor_co_nm === selectedBank.value);
});

function getMaxRate2(p) {
  const opts = p.options || [];
  const nums = opts.map((o) => Number(o.intr_rate2)).filter((n) => !Number.isNaN(n));
  if (nums.length === 0) return null;
  return Math.max(...nums);
}

function getTermsText(p) {
  const opts = p.options || [];
  const terms = opts.map((o) => o.save_trm).filter(Boolean);
  const uniq = Array.from(new Set(terms)).sort((a, b) => Number(a) - Number(b));
  if (uniq.length === 0) return "정보 없음";
  if (uniq.length <= 3) return uniq.map((t) => `${t}개월`).join(", ");
  return `${uniq[0]}~${uniq[uniq.length - 1]}개월`;
}

function formatRate(v) {
  if (v === null || v === undefined) return "정보 없음";
  return `${Number(v).toFixed(2)}%`;
}

onMounted(fetchProducts);

// ✅ 더미 데이터 (Django 모델명 그대로)
const dummyProducts = [
  {
    fin_prdt_cd: "DP001",
    kor_co_nm: "테스트은행",
    fin_prdt_nm: "미니멀 정기예금",
    etc_note: "우대조건 충족 시 금리 상승",
    join_deny: 1,
    join_member: "개인",
    join_way: "영업점/모바일",
    spcl_cnd: "급여이체",
    options: [
      { intr_rate_type_nm: "단리", save_trm: "6", intr_rate: 2.1, intr_rate2: 2.8 },
      { intr_rate_type_nm: "단리", save_trm: "12", intr_rate: 2.3, intr_rate2: 3.0 },
    ],
  },
  {
    fin_prdt_cd: "DP002",
    kor_co_nm: "샘플저축은행",
    fin_prdt_nm: "깔끔 적금 플랜",
    etc_note: "",
    join_deny: 1,
    join_member: "개인",
    join_way: "모바일",
    spcl_cnd: "자동이체",
    options: [
      { intr_rate_type_nm: "복리", save_trm: "12", intr_rate: 2.6, intr_rate2: 3.2 },
      { intr_rate_type_nm: "복리", save_trm: "24", intr_rate: 2.8, intr_rate2: 3.5 },
    ],
  },
];
</script>

<style scoped>
/* 너가 쓰던 스타일 그대로 + 링크 카드용 2줄만 추가 */
.wrap { padding: 8px 0; }
.head { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-bottom: 16px; }
h1 { margin: 0; font-size: 28px; letter-spacing: -0.4px; }
.sub { margin: 6px 0 0; color: #6b7280; font-size: 14px; }
.controls { display: flex; gap: 8px; align-items: center; }
.select { border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 12px; background: #fff; color: #111827; }
.state { padding: 24px; border: 1px solid #e5e7eb; border-radius: 14px; background: #fff; color: #374151; }
.state.error { color: #b91c1c; border-color: #fecaca; background: #fff5f5; }
.grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
@media (max-width: 980px) { .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 640px) { .head { flex-direction: column; align-items: flex-start; } .grid { grid-template-columns: 1fr; } }

/* ✅ RouterLink라서 밑줄 제거 + 글색 유지 */
.card { text-decoration: none; color: inherit; }

.card { border: 1px solid #e5e7eb; border-radius: 16px; padding: 14px; background: #fff; transition: transform 0.05s ease, box-shadow 0.15s ease; }
.card:hover { transform: translateY(-1px); box-shadow: 0 10px 30px rgba(17, 24, 39, 0.06); }
.top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.bank { font-size: 13px; color: #374151; font-weight: 600; }
.badge { font-size: 12px; padding: 4px 8px; border-radius: 999px; border: 1px solid #e5e7eb; color: #111827; background: #f9fafb; }
.title { margin: 0 0 12px; font-size: 16px; letter-spacing: -0.2px; }
.meta { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
.meta-item { border: 1px solid #f3f4f6; border-radius: 12px; padding: 10px; background: #fcfcfd; }
.label { display: block; font-size: 12px; color: #6b7280; margin-bottom: 4px; }
.value { font-size: 14px; font-weight: 700; color: #111827; }
.note { margin: 0; color: #6b7280; font-size: 13px; line-height: 1.4; min-height: 36px; }
.arrow { margin-top: 12px; font-size: 13px; color: #111827; font-weight: 700; }
</style>
