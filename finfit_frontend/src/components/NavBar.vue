<template>
  <nav class="nav">
    <RouterLink to="/" class="brand">Finfit</RouterLink>

    <div class="links">
      <RouterLink to="/" class="link">Home</RouterLink>
      <RouterLink to="/products" class="link">Products</RouterLink>
      <RouterLink to="/fx" class="link">Fx</RouterLink>
      <RouterLink to="/banks" class="link">Banks</RouterLink>
      <RouterLink to="/board" class="link">Board</RouterLink>
      <RouterLink to="/search" class="link">Videos</RouterLink>
    </div>

    <div class="actions">
      <template v-if="!isLoggedIn">
        <RouterLink to="/login" class="btn ghost">Login</RouterLink>
        <RouterLink to="/signup" class="btn primary">Signup</RouterLink>
      </template>
      <template v-else>
        <button @click="handleLogout" class="btn ghost">Logout</button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isLoggedIn = authStore.isLoggedIn

const handleLogout = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/accounts/logout/', {}, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    })
  } catch (error) {
    console.error('Logout failed:', error)
  } finally {
    authStore.logout()
    router.push('/')
  }
}
</script>

<style scoped>
.nav {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid #e5e7eb;
  backdrop-filter: blur(8px);
}

.brand {
  font-weight: 800;
  text-decoration: none;
  color: #111827;
  letter-spacing: -0.2px;
}

.links {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.link {
  text-decoration: none;
  color: #374151;
  padding: 6px 10px;
  border-radius: 10px;
}

.link:hover {
  background: #f9fafb;
  color: #111827;
}

.link.router-link-active {
  color: #111827;
  font-weight: 700;
  background: #f3f4f6;
}

.actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
}

.btn.ghost {
  background: #fff;
  color: #111827;
}

.btn.ghost:hover {
  background: #f9fafb;
}

.btn.primary {
  background: #111827;
  color: #fff;
  border-color: #111827;
}

.btn.primary:hover {
  opacity: 0.92;
}
</style>
