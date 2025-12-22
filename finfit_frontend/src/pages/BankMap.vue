<template>
  <section class="page">
    <h1 class="title">은행 찾기</h1>

    <div class="card">
      <input
        v-model="keyword"
        class="input"
        placeholder="은행명 또는 지역 검색"
      />

      <div class="list">
        <div
          v-for="bank in filteredBanks"
          :key="bank.id"
          class="item"
        >
          <div class="name">{{ bank.name }}</div>
          <div class="addr">{{ bank.address }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const keyword = ref('')

const banks = [
  { id: 1, name: '국민은행 강남점', address: '서울 강남구 테헤란로' },
  { id: 2, name: '신한은행 역삼점', address: '서울 강남구 역삼동' },
  { id: 3, name: '우리은행 삼성점', address: '서울 강남구 삼성로' },
  { id: 4, name: '하나은행 서초점', address: '서울 서초구 서초대로' },
]

const filteredBanks = computed(() =>
  banks.filter(
    b =>
      b.name.includes(keyword.value) ||
      b.address.includes(keyword.value)
  )
)
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.title {
  font-size: 24px;
  font-weight: 700;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  max-width: 520px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px 12px;
  outline: none;
}

.list {
  display: flex;
  flex-direction: column;
}

.item {
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
}

.item:last-child {
  border-bottom: none;
}

.name {
  font-weight: 600;
}

.addr {
  font-size: 13px;
  color: #6b7280;
}
</style>
