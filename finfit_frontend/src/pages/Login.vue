<template>
  <section class="page">
    <h1 class="title">Login</h1>

    <form class="card" @submit.prevent="onSubmit">
      <label class="label">
        <span>Email</span>
        <input v-model="email" class="input" type="email" placeholder="email@example.com" />
      </label>

      <label class="label">
        <span>Password</span>
        <input v-model="password" class="input" type="password" placeholder="••••••••" />
      </label>

      <button class="btn" type="submit">Login</button>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const onSubmit = () => {
  // 나중에 API 붙일 자리
  console.log('login', { email: email.value, password: password.value })
}
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.title { font-size: 24px; font-weight: 700; }
.card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 12px; max-width: 420px; }
.label { display: flex; flex-direction: column; gap: 6px; font-size: 14px; }
.input { border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 12px; outline: none; }
.btn { border: 1px solid #111827; background: #111827; color: #fff; border-radius: 10px; padding: 10px 12px; cursor: pointer; }
</style>
