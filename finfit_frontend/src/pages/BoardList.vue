<template>
  <section class="page">
    <div class="header">
      <h1 class="title">Board</h1>
      <RouterLink class="btn" to="/board/new">New</RouterLink>
    </div>

    <div class="list">
      <div v-for="post in posts" :key="post.id" class="item" @click="goDetail(post.id)">
        <div class="item-title">{{ post.title }}</div>
        <div class="item-meta">{{ post.author }} · {{ post.created_at }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()

const posts = [
  { id: 1, title: '첫 글입니다', author: 'admin', created_at: '2025-12-22' },
  { id: 2, title: '환율 정보 어디서 보나요?', author: 'user1', created_at: '2025-12-22' },
  { id: 3, title: '예금 추천 부탁', author: 'user2', created_at: '2025-12-21' },
  { id: 4, title: '적금 금리 비교', author: 'user3', created_at: '2025-12-21' },
  { id: 5, title: '프로젝트 진행 공유', author: 'user4', created_at: '2025-12-20' },
]

const goDetail = (id) => {
  router.push(`/board/${id}`)
}
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 24px; font-weight: 700; }
.btn { border: 1px solid #111827; background: #111827; color: #fff; border-radius: 10px; padding: 8px 12px; text-decoration: none; }
.list { display: flex; flex-direction: column; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; }
.item { padding: 12px 14px; cursor: pointer; border-bottom: 1px solid #e5e7eb; }
.item:last-child { border-bottom: none; }
.item-title { font-weight: 600; }
.item-meta { font-size: 12px; color: #6b7280; margin-top: 4px; }
</style>
