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

      <!-- 댓글 목록 -->
      <section class="comments-section">
        <h3>댓글 {{ post.comments?.length || 0 }}개</h3>
        
        <!-- 댓글 작성 -->
        <div v-if="authStore.isLoggedIn" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="댓글을 작성하세요..."
            class="comment-input"
            rows="3"
          ></textarea>
          <button
            @click="createComment"
            :disabled="!newComment.trim() || creatingComment"
            class="comment-submit-btn"
          >
            {{ creatingComment ? '작성 중...' : '댓글 작성' }}
          </button>
        </div>
        <div v-else class="login-prompt">
          댓글을 작성하려면 <RouterLink to="/login">로그인</RouterLink>하세요.
        </div>

        <!-- 댓글 리스트 -->
        <div class="comments-list">
          <div
            v-for="comment in post.comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-header">
              <span class="comment-author">{{ comment.user.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              <div v-if="comment.user.id === currentUserId" class="comment-actions">
                <button @click="startEditComment(comment)" class="edit-btn">수정</button>
                <button @click="deleteComment(comment.id)" class="delete-btn">삭제</button>
              </div>
            </div>
            
            <!-- 댓글 내용 또는 수정 폼 -->
            <div v-if="editingCommentId !== comment.id" class="comment-content">
              {{ comment.content }}
            </div>
            <div v-else class="comment-edit-form">
              <textarea
                v-model="editCommentContent"
                class="comment-input"
                rows="3"
              ></textarea>
              <div class="edit-actions">
                <button @click="saveCommentEdit" class="save-btn">저장</button>
                <button @click="cancelCommentEdit" class="cancel-btn">취소</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <RouterLink class="link" to="/board">← Back to list</RouterLink>
    </div>
    <div v-else>
      Loading...
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
})

const authStore = useAuthStore()
const post = ref(null)

// 댓글 관련 상태
const newComment = ref('')
const creatingComment = ref(false)
const editingCommentId = ref(null)
const editCommentContent = ref('')

// 현재 사용자 ID (JWT 토큰에서 추출 또는 별도 API 호출)
const currentUserId = ref(null)

const fetchPost = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/articles/${props.id}/`)
    post.value = response.data
    
    // 현재 사용자 정보 가져오기 (프로필 API에서 사용자 ID 추출)
    if (authStore.isLoggedIn) {
      try {
        const profileResponse = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
          headers: {
            'Authorization': `Token ${authStore.token}`
          }
        })
        currentUserId.value = profileResponse.data.user.id
      } catch (e) {
        console.error('사용자 정보 조회 실패:', e)
      }
    }
  } catch (error) {
    console.error('Failed to fetch post:', error)
  }
}

// 댓글 작성
const createComment = async () => {
  if (!newComment.value.trim()) return
  
  creatingComment.value = true
  try {
    console.log('댓글 작성 시도:', {
      content: newComment.value,
      token: authStore.token,
      url: `http://127.0.0.1:8000/articles/articles/${props.id}/comments/`
    })
    
    const response = await axios.post(
      `http://127.0.0.1:8000/articles/articles/${props.id}/comments/`,
      { content: newComment.value },
      {
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      }
    )
    
    console.log('댓글 작성 성공:', response.data)
    post.value.comments.push(response.data)
    newComment.value = ''
  } catch (error) {
    console.error('댓글 작성 실패 상세 정보:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers,
      config: error.config
    })
    alert(`댓글 작성에 실패했습니다. (${error.response?.status || '네트워크 오류'})`)
  } finally {
    creatingComment.value = false
  }
}

// 댓글 수정 시작
const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
}

// 댓글 수정 취소
const cancelCommentEdit = () => {
  editingCommentId.value = null
  editCommentContent.value = ''
}

// 댓글 수정 저장
const saveCommentEdit = async () => {
  if (!editCommentContent.value.trim()) return
  
  try {
    const response = await axios.patch(
      `http://127.0.0.1:8000/articles/articles/${props.id}/comments/${editingCommentId.value}/`,
      { content: editCommentContent.value },
      {
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      }
    )
    
    // 댓글 목록 업데이트
    const commentIndex = post.value.comments.findIndex(c => c.id === editingCommentId.value)
    if (commentIndex !== -1) {
      post.value.comments[commentIndex] = response.data
    }
    
    editingCommentId.value = null
    editCommentContent.value = ''
  } catch (error) {
    console.error('댓글 수정 실패:', error)
    alert('댓글 수정에 실패했습니다.')
  }
}

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  
  try {
    await axios.delete(
      `http://127.0.0.1:8000/articles/articles/${props.id}/comments/${commentId}/`,
      {
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      }
    )
    
    // 댓글 목록에서 제거
    post.value.comments = post.value.comments.filter(c => c.id !== commentId)
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
    alert('댓글 삭제에 실패했습니다.')
  }
}

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('ko-KR')
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

/* 댓글 스타일 */
.comments-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.comments-section h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
}

.comment-form {
  margin-bottom: 24px;
}

.comment-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 8px;
}

.comment-submit-btn {
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.comment-submit-btn:hover:not(:disabled) {
  background: #2563eb;
}

.comment-submit-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.login-prompt {
  margin-bottom: 24px;
  padding: 12px;
  background: #fef3c7;
  border: 1px solid #f59e0b;
  border-radius: 6px;
  color: #92400e;
}

.login-prompt a {
  color: #dc2626;
  text-decoration: none;
  font-weight: 500;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #111827;
}

.comment-date {
  color: #6b7280;
  font-size: 12px;
}

.comment-actions {
  display: flex;
  gap: 8px;
}

.edit-btn, .delete-btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn {
  background: #f59e0b;
  color: white;
}

.edit-btn:hover {
  background: #d97706;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.delete-btn:hover {
  background: #dc2626;
}

.comment-content {
  color: #374151;
  line-height: 1.5;
}

.comment-edit-form {
  margin-top: 8px;
}

.edit-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.save-btn {
  padding: 6px 12px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.save-btn:hover {
  background: #059669;
}

.cancel-btn {
  padding: 6px 12px;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.cancel-btn:hover {
  background: #4b5563;
}
</style>
