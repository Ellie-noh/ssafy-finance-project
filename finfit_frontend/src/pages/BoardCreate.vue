<template>
  <section class="page">
    <h1 class="title">New Post</h1>

    <form class="card" @submit.prevent="onSubmit">
      <label class="label">
        <span>Title</span>
        <input v-model="title" class="input" type="text" placeholder="제목" />
      </label>

      <label class="label">
        <span>Content</span>
        <textarea v-model="content" class="textarea" placeholder="내용"></textarea>
      </label>

      <button class="btn" type="submit">Save</button>

      <RouterLink class="link" to="/board">Cancel</RouterLink>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

const router = useRouter()
const title = ref('')
const content = ref('')

const onSubmit = () => {
  // 나중에 API 붙일 자리
  console.log('create', { title: title.value, content: content.value })
  router.push('/board')
}
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.title { font-size: 24px; font-weight: 700; }
.card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 12px; max-width: 640px; }
.label { display: flex; flex-direction: column; gap: 6px; font-size: 14px; }
.input { border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 12px; outline: none; }
.textarea { border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 12px; min-height: 140px; outline: none; resize: vertical; }
.btn { border: 1px solid #111827; background: #111827; color: #fff; border-radius: 10px; padding: 10px 12px; cursor: pointer; }
.link { text-decoration: none; color: #111827; font-weight: 600; width: fit-content; }
</style>
