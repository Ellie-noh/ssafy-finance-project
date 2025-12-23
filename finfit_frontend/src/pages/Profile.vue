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
          <div class="email-edit">
            <label for="email"><strong>이메일:</strong></label>
            <input
              id="email"
              v-model="editEmail"
              type="email"
              class="email-input"
              :disabled="!isEditing"
            />
            <button
              v-if="!isEditing"
              @click="startEdit"
              class="edit-btn"
            >
              수정
            </button>
            <button
              v-else
              @click="cancelEdit"
              class="cancel-btn"
            >
              취소
            </button>
            <button
              v-if="isEditing"
              @click="saveEmail"
              class="save-btn"
              :disabled="saving"
            >
              {{ saving ? '저장 중...' : '저장' }}
            </button>
          </div>
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
const isEditing = ref(false)
const editEmail = ref('')
const saving = ref(false)

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
    editEmail.value = response.data.user.email
  } catch (e) {
    error.value = '프로필을 불러오는데 실패했습니다.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit() {
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  editEmail.value = profile.value.user.email
}

async function saveEmail() {
  if (!editEmail.value.trim()) {
    alert('이메일을 입력해주세요.')
    return
  }

  saving.value = true
  try {
    const response = await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      email: editEmail.value
    }, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    })
    profile.value.user.email = response.data.email
    isEditing.value = false
    alert('이메일이 수정되었습니다.')
  } catch (e) {
    console.error('이메일 수정 실패:', e)
    alert('이메일 수정에 실패했습니다.')
  } finally {
    saving.value = false
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

.email-edit {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.email-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.email-input:disabled {
  background: #f9fafb;
  color: #6b7280;
}

.edit-btn, .cancel-btn, .save-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn {
  background: #3b82f6;
  color: white;
}

.edit-btn:hover {
  background: #2563eb;
}

.cancel-btn {
  background: #6b7280;
  color: white;
}

.cancel-btn:hover {
  background: #4b5563;
}

.save-btn {
  background: #10b981;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #059669;
}

.save-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
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
