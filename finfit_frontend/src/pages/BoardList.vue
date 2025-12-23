<template>
  <section class="page">
    <div class="header">
      <h1 class="title">Board</h1>
      <RouterLink class="btn" to="/board/new">New</RouterLink>
    </div>

    <div class="list">
      <div v-for="post in posts" :key="post.id" class="item" @click="goDetail(post.id)">
        <div class="item-title">{{ post.title }}</div>
        <div class="item-meta">{{ post.user.username }} · {{ new Date(post.created_at).toLocaleDateString() }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const posts = ref([])

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/articles/articles/')
    posts.value = response.data
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  }
}

onMounted(() => {
  fetchPosts()
})

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
