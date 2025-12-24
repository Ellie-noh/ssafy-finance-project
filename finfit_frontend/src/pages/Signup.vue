<template>
  <section class="page">
    <h1 class="title">Signup</h1>

    <form class="card" @submit.prevent="onSubmit">
      <label class="label">
        <span>Username</span>
        <input v-model="username" class="input" type="text" placeholder="username" />
      </label>

      <label class="label">
        <span>Email</span>
        <input v-model="email" class="input" type="email" placeholder="email@example.com" />
      </label>

      <label class="label">
        <span>Password</span>
        <input v-model="password" class="input" type="password" placeholder="••••••••" />
      </label>

      <label class="label">
        <span>Confirm Password</span>
        <input v-model="password2" class="input" type="password" placeholder="••••••••" />
      </label>

      <button class="btn" type="submit">Create Account</button>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')

const onSubmit = async () => {
  if (password.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }
  try {
    const response = await axios.post('http://127.0.0.1:8000/accounts/signup/', {
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value
    })
    authStore.setToken(response.data.token)
    router.push('/')
  } catch (error) {
    console.error('Signup failed:', error)
    alert('회원가입 실패')
  }
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
