<template>
  <section class="page">
    <h1 class="title">Board Detail</h1>

    <div v-if="post" class="card">
      <div class="row">
        <span class="key">Title</span>
        <span class="value">{{ post.title }}</span>
      </div>
      <div class="row">
        <span class="key">Author</span>
        <span class="value">{{ post.user.username }}</span>
      </div>
      <div class="row">
        <span class="key">Created</span>
        <span class="value">{{ new Date(post.created_at).toLocaleString() }}</span>
      </div>
      <p class="desc">{{ post.content }}</p>

      <RouterLink class="link" to="/board">← Back to list</RouterLink>
    </div>
    <div v-else>
      Loading...
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
})

const post = ref(null)

const fetchPost = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/articles/${props.id}/`)
    post.value = response.data
  } catch (error) {
    console.error('Failed to fetch post:', error)
  }
}

onMounted(() => {
  fetchPost()
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
