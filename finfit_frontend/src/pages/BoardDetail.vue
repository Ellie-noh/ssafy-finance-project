<template>
  <section class="page">
    <h1 class="title">Board Detail</h1>

    <div class="card">
      <div class="row">
        <span class="key">Post ID</span>
        <span class="value">{{ id }}</span>
      </div>

      <p class="desc">
        지금은 더미 상세 화면입니다. 나중에 API 붙이면 id로 글 가져오면 끝.
      </p>

      <RouterLink class="link" to="/board">← Back to list</RouterLink>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
})
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.title { font-size: 24px; font-weight: 700; }
.card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; max-width: 640px; display: flex; flex-direction: column; gap: 12px; }
.row { display: flex; justify-content: space-between; }
.key { color: #6b7280; }
.value { font-weight: 600; }
.desc { color: #4b5563; margin: 0; }
.link { text-decoration: none; color: #111827; font-weight: 600; }
</style>
