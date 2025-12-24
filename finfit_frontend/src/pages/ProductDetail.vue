<template>
  <section class="wrap">
    <div class="top">
      <button class="back" @click="router.back()">←</button>
      <div>
        <h1>{{ product?.fin_prdt_nm || "상품 상세" }}</h1>
        <p class="sub">{{ product?.kor_co_nm }}</p>
      </div>
    </div>

    <div v-if="loading" class="state">불러오는 중...</div>
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

        <div v-if="isLoggedIn" class="actions">
          <button
            v-if="!isJoined"
            class="btn primary"
            type="button"
            @click="joinProduct"
          >
            가입하기
          </button>
          <button
            v-else
            class="btn danger"
            type="button"
            @click="cancelJoin"
          >
            가입 취소
          </button>
        </div>
        <p v-else class="hint">로그인 후 가입할 수 있어요.</p>
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
import axios from "axios";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { isLoggedIn } = storeToRefs(authStore);

const loading = ref(false);
const error = ref("");
const product = ref(null);
const isJoined = ref(false);


function joinProduct() {
  if (!isLoggedIn.value) return;
  const finPrdtCd = route.params.fin_prdt_cd;
  axios
    .post(`http://127.0.0.1:8000/accounts/join-product/${finPrdtCd}/`, {}, {
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
    .then(() => {
      alert("가입 성공");
      isJoined.value = true;
    })
    .catch((error) => {
      console.error("가입 실패:", error);
      alert("가입 실패");
    });
}

function cancelJoin() {
  if (!isLoggedIn.value) return;
  if (!confirm("가입을 취소할까요?")) return;
  const finPrdtCd = route.params.fin_prdt_cd;
  axios
    .delete(`http://127.0.0.1:8000/accounts/join-product/${finPrdtCd}/`, {
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
    .then(() => {
      alert("가입 취소 완료");
      isJoined.value = false;
    })
    .catch((error) => {
      console.error("가입 취소 실패:", error);
      alert("가입 취소 실패");
    });
}

async function fetchJoinStatus() {
  try {
    const response = await axios.get("http://127.0.0.1:8000/accounts/profile/", {
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    });
    const joined = response.data?.joined_products || [];
    isJoined.value = joined.some(
      (p) => p.fin_prdt_cd === route.params.fin_prdt_cd
    );
  } catch (e) {
    console.error("가입 여부 조회 실패:", e);
  }
}

async function fetchDetail() {
  loading.value = true;
  error.value = "";

  try {
    const finPrdtCd = route.params.fin_prdt_cd;
    const productResponse = await axios.get(
      `http://127.0.0.1:8000/deposits/deposit-product/${finPrdtCd}/`
    );
    const optionsResponse = await axios.get(
      `http://127.0.0.1:8000/deposits/deposit-product-options/${finPrdtCd}/`
    );
    product.value = { ...productResponse.data, options: optionsResponse.data };
    if (isLoggedIn.value) {
      await fetchJoinStatus();
    }
  } catch (e) {
    error.value = "상품 정보를 불러오는 데 실패했습니다.";
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function formatRate(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "정보 없음";
  }
  return `${Number(value).toFixed(2)}%`;
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

.actions { display: flex; gap: 8px; flex-wrap: wrap; }
.actions .btn { width: 100%; }

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
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
}
.btn.primary:hover { background: #1d4ed8; }
.btn.danger {
  background: #fff;
  border-color: #e5e7eb;
  color: #111827;
}
.btn.danger:hover { background: #f3f4f6; }
.btn.ghost:hover { background: #f9fafb; }

.hint {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
}
</style>
