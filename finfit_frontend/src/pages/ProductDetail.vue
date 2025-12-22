<template>
  <section class="wrap">
    <div class="top">
      <button class="back" @click="router.back()">←</button>
      <div>
        <h1>{{ product?.fin_prdt_nm || "상품 상세" }}</h1>
        <p class="sub">{{ product?.kor_co_nm }}</p>
      </div>
    </div>

    <div v-if="loading" class="state">불러오는 중…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <div v-else-if="product" class="grid">
      <article class="card">
        <h3>가입 정보</h3>

        <div class="row">
          <span>가입대상</span><span>{{ product.join_member || "정보 없음" }}</span>
        </div>
        <div class="row">
          <span>가입방법</span><span>{{ product.join_way || "정보 없음" }}</span>
        </div>
        <div class="row">
          <span>가입제한</span><span>{{ product.join_deny }}</span>
        </div>
        <div class="row">
          <span>우대조건</span><span>{{ product.spcl_cnd || "정보 없음" }}</span>
        </div>
        <p class="note" v-if="product.etc_note">{{ product.etc_note }}</p>

        <!-- ✅ 요구사항: 로그인된 사용자에게만 가입하기 버튼 표시 -->
        <button
          v-if="isLoggedIn"
          class="btn primary"
          type="button"
          @click="joinProduct"
        >
          가입하기
        </button>

        <!-- (선택) 로그인 안 된 경우 안내 문구 -->
        <p v-else class="hint">
          로그인 후 가입할 수 있어요.
        </p>

        <!-- (선택) 테스트용 로그인 토글: 제출 시 빼도 됨 -->
        <button class="btn ghost" type="button" @click="toggleLogin">
          (테스트) 로그인 상태: {{ isLoggedIn ? "ON" : "OFF" }}
        </button>
      </article>

      <article class="card">
        <h3>금리 옵션</h3>
        <div v-if="(product.options || []).length === 0" class="empty">옵션 정보가 없어요</div>

        <div v-else class="table">
          <div class="th">기간</div>
          <div class="th">유형</div>
          <div class="th">기본</div>
          <div class="th">우대</div>

          <template v-for="(o, idx) in product.options" :key="idx">
            <div class="td">{{ o.save_trm }}개월</div>
            <div class="td">{{ o.intr_rate_type_nm }}</div>
            <div class="td">{{ formatRate(o.intr_rate) }}</div>
            <div class="td strong">{{ formatRate(o.intr_rate2) }}</div>
          </template>
        </div>
      </article>
    </div>

    <div v-else class="state">상품을 찾지 못했어요</div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const loading = ref(false);
const error = ref("");
const product = ref(null);

const API_URL = import.meta.env.VITE_API_URL || "";

/** ✅ (임시) 로그인 상태: 나중에 store/백엔드 붙이면 여기만 교체 */
const isLoggedIn = ref(false);

function toggleLogin() {
  isLoggedIn.value = !isLoggedIn.value;
}

/** ✅ 요구사항: 가입하기 클릭 시 가입목록에 추가
 * 지금은 더미로 localStorage에 저장해두면 "추가됐다"를 증명하기 좋음
 */
function joinProduct() {
  if (!product.value) return;

  const key = "joined_products";
  const prev = JSON.parse(localStorage.getItem(key) || "[]");

  // 중복 방지
  const exists = prev.some((x) => x.fin_prdt_cd === product.value.fin_prdt_cd);
  if (!exists) {
    prev.push({
      fin_prdt_cd: product.value.fin_prdt_cd,
      fin_prdt_nm: product.value.fin_prdt_nm,
      kor_co_nm: product.value.kor_co_nm,
      joined_at: new Date().toISOString().slice(0, 10),
    });
    localStorage.setItem(key, JSON.stringify(prev));
  }

  alert(exists ? "이미 가입한 상품이에요 (더미)" : "가입 완료! (더미로 저장됨)");
}

/** ===== 상세 데이터 로드 ===== */
async function fetchDetail() {
  loading.value = true;
  error.value = "";

  try {
    const fin_prdt_cd = route.params.fin_prdt_cd;
    const res = await fetch(`${API_URL}/api/deposits/${fin_prdt_cd}/`, {
      credentials: "include",
    });
    if (!res.ok) throw new Error("API 응답 오류");
    product.value = await res.json();
  } catch (e) {
    product.value = dummyDetail(route.params.fin_prdt_cd);
    error.value = "";
  } finally {
    loading.value = false;
  }
}

function dummyDetail(fin_prdt_cd) {
  return {
    fin_prdt_cd,
    kor_co_nm: "테스트은행",
    fin_prdt_nm: "미니멀 정기예금",
    etc_note: "백엔드 연결 전 더미 상세입니다.",
    join_deny: 1,
    join_member: "개인",
    join_way: "영업점/모바일",
    spcl_cnd: "급여이체",
    options: [
      { intr_rate_type_nm: "단리", save_trm: "6", intr_rate: 2.1, intr_rate2: 2.8 },
      { intr_rate_type_nm: "단리", save_trm: "12", intr_rate: 2.3, intr_rate2: 3.0 },
    ],
  };
}

function formatRate(v) {
  if (v === null || v === undefined || Number.isNaN(Number(v))) return "—";
  return `${Number(v).toFixed(2)}%`;
}

onMounted(fetchDetail);
</script>

<style scoped>
.wrap { padding: 8px 0; }
.top { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.back { border: 1px solid #e5e7eb; background: #fff; border-radius: 12px; padding: 8px 10px; cursor: pointer; }
h1 { margin: 0; font-size: 22px; letter-spacing: -0.3px; }
.sub { margin: 4px 0 0; color: #6b7280; font-size: 14px; }

.state { padding: 24px; border: 1px solid #e5e7eb; border-radius: 14px; background: #fff; color: #374151; }
.state.error { color: #b91c1c; border-color: #fecaca; background: #fff5f5; }

.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
@media (max-width: 840px) { .grid { grid-template-columns: 1fr; } }

.card { border: 1px solid #e5e7eb; border-radius: 16px; padding: 14px; background: #fff; display: flex; flex-direction: column; gap: 12px; }
.card h3 { margin: 0; font-size: 16px; }

.row { display: flex; justify-content: space-between; gap: 12px; padding: 8px 0; border-bottom: 1px solid #f3f4f6; font-size: 14px; }
.row span:first-child { color: #6b7280; }

.note { margin: 0; color: #6b7280; font-size: 13px; line-height: 1.5; }

.table { display: grid; grid-template-columns: 1.1fr 1fr 1fr 1fr; gap: 8px; align-items: center; }
.th { font-size: 12px; color: #6b7280; padding-bottom: 6px; border-bottom: 1px solid #f3f4f6; }
.td { font-size: 14px; padding: 6px 0; }
.strong { font-weight: 800; color: #111827; }
.empty { color: #6b7280; font-size: 14px; }

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background: #fff;
  cursor: pointer;
  font-weight: 800;
}
.btn.primary {
  background: #111827;
  border-color: #111827;
  color: #fff;
}
.btn.primary:hover { opacity: 0.92; }
.btn.ghost:hover { background: #f9fafb; }

.hint {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
}
</style>
