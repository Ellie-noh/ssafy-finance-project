<template>
  <div class="page">
    <h1>마이페이지</h1>

    <div v-if="loading" class="state">불러오는 중…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <div v-else-if="profile">
      <section class="section">
        <h2>회원 정보</h2>
        <div class="info">
          <p><strong>사용자명:</strong> {{ profile.user.username }}</p>
          <p><strong>이메일:</strong> {{ profile.user.email }}</p>
        </div>
      </section>

      <section class="section">
        <h2>가입한 상품</h2>
        <div v-if="profile.joined_products.length === 0" class="empty">가입한 상품이 없습니다.</div>
        <div v-else class="grid">
          <div v-for="product in profile.joined_products" :key="product.fin_prdt_cd" class="card">
            <h3>{{ product.fin_prdt_nm }}</h3>
            <p>{{ product.kor_co_nm }}</p>
          </div>
        </div>
      </section>

      <section class="section">
        <h2>내 게시글</h2>
        <div v-if="profile.user_articles.length === 0" class="empty">작성한 게시글이 없습니다.</div>
        <div v-else class="grid">
          <div v-for="article in profile.user_articles" :key="article.id" class="card">
            <h3>{{ article.title }}</h3>
            <p>{{ article.content.substring(0, 100) }}...</p>
            <small>{{ new Date(article.created_at).toLocaleDateString() }}</small>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')
const profile = ref(null)

async function fetchProfile() {
  if (!authStore.isLoggedIn) {
    error.value = '로그인이 필요합니다.'
    return
  }
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    })
    profile.value = response.data
  } catch (e) {
    error.value = '프로필을 불러오는데 실패했습니다.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchProfile)
</script>

<style scoped>
.page {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.section {
  margin-bottom: 32px;
}

.info {
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  background: #fff;
}

.empty {
  color: #6b7280;
  font-style: italic;
}

.state {
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  text-align: center;
}

.state.error {
  color: #b91c1c;
  border-color: #fecaca;
  background: #fff5f5;
}
</style>
