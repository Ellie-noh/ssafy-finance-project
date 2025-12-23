<template>
  <div class="page">
    <h1>마이페이지</h1>

    <div v-if="loading" class="state">불러오는 중…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <div v-else-if="profile">
      <!-- 탭 메뉴 -->
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: activeTab === 'profile' }"
          @click="activeTab = 'profile'"
        >
          프로필 편집
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'products' }"
          @click="activeTab = 'products'"
        >
          가입 상품
        </button>
      </div>

      <!-- 프로필 편집 탭 -->
      <div v-if="activeTab === 'profile'" class="tab-content">
        <section class="section">
          <h2>회원 정보</h2>
          <div v-if="!isEditing" class="info">
            <p><strong>사용자명:</strong> {{ profile.user.username }}</p>
            <p><strong>이메일:</strong> {{ profile.user.email }}</p>
            <button @click="startEditing" class="btn edit-btn">수정하기</button>
          </div>
          <form v-else @submit.prevent="updateProfile" class="edit-form">
            <div class="form-group">
              <label for="username">사용자명:</label>
              <input
                id="username"
                v-model="editForm.username"
                type="text"
                required
              />
            </div>
            <div class="form-group">
              <label for="email">이메일:</label>
              <input
                id="email"
                v-model="editForm.email"
                type="email"
                required
              />
            </div>
            <div class="form-actions">
              <button type="submit" class="btn save-btn" :disabled="saving">저장</button>
              <button type="button" @click="cancelEditing" class="btn cancel-btn">취소</button>
            </div>
          </form>
        </section>
      </div>

      <!-- 가입 상품 탭 -->
      <div v-if="activeTab === 'products'" class="tab-content">
        <section class="section">
          <h2>가입한 상품</h2>
          <div v-if="profile.joined_products.length === 0" class="empty">가입한 상품이 없습니다.</div>
          <div v-else>
            <div class="grid">
              <div v-for="product in profile.joined_products" :key="product.fin_prdt_cd" class="card">
                <h3>{{ product.fin_prdt_nm }}</h3>
                <p>{{ product.kor_co_nm }}</p>
                <p v-if="product.max_rate">최대 우대금리: {{ product.max_rate }}%</p>
              </div>
            </div>

            <!-- 금리 그래프 -->
            <div class="chart-section">
              <h3>가입 상품 금리 비교</h3>
              <div class="chart-container">
                <Bar :data="chartData" :options="chartOptions" />
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- 내 게시글 (항상 표시) -->
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
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import ChartDataLabels from 'chartjs-plugin-datalabels'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ChartDataLabels)

const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')
const profile = ref(null)
const activeTab = ref('profile')
const isEditing = ref(false)
const saving = ref(false)
const editForm = ref({
  username: '',
  email: ''
})

// 차트 데이터
const chartData = computed(() => {
  if (!profile.value || !profile.value.joined_products.length) {
    return {
      labels: [],
      datasets: []
    }
  }

  const products = profile.value.joined_products
  return {
    labels: products.map(p => p.fin_prdt_nm.length > 15 ? p.fin_prdt_nm.substring(0, 15) + '...' : p.fin_prdt_nm),
    datasets: [{
      label: '최대 우대금리 (%)',
      data: products.map(p => p.max_rate || 0),
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: '가입 상품 금리 비교'
    },
    datalabels: {
      anchor: 'end',
      align: 'top',
      formatter: (value) => value > 0 ? `${value}%` : '',
      font: {
        weight: 'bold'
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '금리 (%)'
      }
    }
  }
}

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

function startEditing() {
  isEditing.value = true
  editForm.value = {
    username: profile.value.user.username,
    email: profile.value.user.email
  }
}

function cancelEditing() {
  isEditing.value = false
  editForm.value = { username: '', email: '' }
}

async function updateProfile() {
  saving.value = true
  try {
    const response = await axios.put('http://127.0.0.1:8000/accounts/profile/', editForm.value, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    })
    profile.value.user = response.data.user
    isEditing.value = false
    alert('프로필이 업데이트되었습니다.')
  } catch (e) {
    error.value = '프로필 업데이트에 실패했습니다.'
    console.error(e)
  } finally {
    saving.value = false
  }
}

onMounted(fetchProfile)
</script>

<style scoped>
.page {
  padding: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.section {
  margin-bottom: 32px;
}

.tabs {
  display: flex;
  margin-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.tab {
  padding: 12px 24px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  color: #6b7280;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.tab:hover {
  color: #374151;
}

.tab.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
}

.tab-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.info {
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
  position: relative;
}

.edit-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.edit-btn:hover {
  background: #2563eb;
}

.edit-form {
  background: #f9fafb;
  padding: 24px;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 16px;
}

.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.save-btn, .cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-btn {
  background: #10b981;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #059669;
}

.save-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.cancel-btn {
  background: #6b7280;
  color: white;
}

.cancel-btn:hover {
  background: #4b5563;
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
  margin-bottom: 32px;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-section {
  margin-top: 32px;
  padding: 24px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-section h3 {
  margin-bottom: 16px;
  color: #374151;
}

.chart-container {
  height: 400px;
}

.empty {
  color: #6b7280;
  font-style: italic;
  text-align: center;
  padding: 48px;
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
