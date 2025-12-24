<template>
  <section class="page">
    <h1 class="title">게시글 상세</h1>

    <div v-if="post" class="card">
      <div class="row">
        <span class="key">제목</span>
        <span v-if="!isEditingPost" class="value">{{ post.title }}</span>
        <input v-else v-model="editPostTitle" class="post-input" />
      </div>
      <div class="row">
        <span class="key">작성자</span>
        <span class="value">{{ post.user.username }}</span>
      </div>
      <div class="row">
        <span class="key">작성일</span>
        <span class="value">{{ new Date(post.created_at).toLocaleString() }}</span>
      </div>

      <div v-if="isOwner" class="post-actions">
        <button v-if="!isEditingPost" @click="startEditPost" class="edit-btn">수정</button>
        <button v-if="!isEditingPost" @click="deletePost" class="delete-btn">삭제</button>
        <button v-else @click="savePostEdit" class="save-btn">저장</button>
        <button v-if="isEditingPost" @click="cancelPostEdit" class="cancel-btn">취소</button>
      </div>

      <p v-if="!isEditingPost" class="desc">{{ post.content }}</p>
      <textarea v-else v-model="editPostContent" class="post-textarea" rows="6"></textarea>

      <section class="comments-section">
        <h3>댓글 {{ post.comments?.length || 0 }}개</h3>

        <div v-if="isLoggedIn" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="댓글을 작성해주세요..."
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

        <div class="comments-list">
          <div
            v-for="comment in post.comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-header">
              <span class="comment-author">{{ comment.user.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              <div v-if="isCommentOwner(comment)" class="comment-actions">
                <button @click="startEditComment(comment)" class="edit-btn">수정</button>
                <button @click="deleteComment(comment.id)" class="delete-btn">삭제</button>
              </div>
            </div>

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

      <RouterLink class="link" to="/board">← 목록으로</RouterLink>
    </div>
    <div v-else class="state">Loading...</div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
})

const authStore = useAuthStore()
const { isLoggedIn, token } = storeToRefs(authStore)
const router = useRouter()
const post = ref(null)

const newComment = ref('')
const creatingComment = ref(false)
const editingCommentId = ref(null)
const editCommentContent = ref('')

const isEditingPost = ref(false)
const editPostTitle = ref('')
const editPostContent = ref('')

const currentUserId = ref(null)
const isOwner = computed(() => {
  if (!post.value || currentUserId.value === null) return false
  return String(currentUserId.value) === String(post.value.user.id)
})

const isCommentOwner = (comment) => {
  if (!comment?.user) return false
  return String(comment.user.id) === String(currentUserId.value)
}

const fetchCurrentUser = async () => {
  try {
    const profileResponse = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    currentUserId.value = profileResponse.data.user.id
  } catch (e) {
    console.error('사용자 정보 조회 실패:', e)
  }
}

const fetchPost = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/articles/${props.id}/`)
    post.value = response.data

    if (isLoggedIn.value) {
      await fetchCurrentUser()
    }
  } catch (error) {
    console.error('Failed to fetch post:', error)
  }
}

const startEditPost = () => {
  isEditingPost.value = true
  editPostTitle.value = post.value.title
  editPostContent.value = post.value.content
}

const cancelPostEdit = () => {
  isEditingPost.value = false
  editPostTitle.value = ''
  editPostContent.value = ''
}

const savePostEdit = async () => {
  if (!editPostTitle.value.trim() || !editPostContent.value.trim()) return

  try {
    const response = await axios.patch(
      `http://127.0.0.1:8000/articles/articles/${props.id}/`,
      { title: editPostTitle.value, content: editPostContent.value },
      {
        headers: {
          Authorization: `Token ${token.value}`
        }
      }
    )
    post.value = { ...post.value, ...response.data }
    isEditingPost.value = false
  } catch (error) {
    console.error('게시글 수정 실패:', error)
    alert('게시글 수정에 실패했습니다.')
  }
}

const deletePost = async () => {
  if (!confirm('게시글을 삭제할까요?')) return

  try {
    await axios.delete(`http://127.0.0.1:8000/articles/articles/${props.id}/`, {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    router.push('/board')
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
    alert('게시글 삭제에 실패했습니다.')
  }
}

const createComment = async () => {
  if (!isLoggedIn.value || !newComment.value.trim()) return

  creatingComment.value = true
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/articles/articles/${props.id}/comments/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${token.value}`
        }
      }
    )

    post.value.comments.push(response.data)
    newComment.value = ''
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert(`댓글 작성에 실패했습니다. (${error.response?.status || '네트워크 오류'})`)
  } finally {
    creatingComment.value = false
  }
}

const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
}

const cancelCommentEdit = () => {
  editingCommentId.value = null
  editCommentContent.value = ''
}

const saveCommentEdit = async () => {
  if (!editCommentContent.value.trim()) return

  try {
    const response = await axios.patch(
      `http://127.0.0.1:8000/articles/articles/${props.id}/comments/${editingCommentId.value}/`,
      { content: editCommentContent.value },
      {
        headers: {
          Authorization: `Token ${token.value}`
        }
      }
    )

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

const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return

  try {
    await axios.delete(
      `http://127.0.0.1:8000/articles/articles/${props.id}/comments/${commentId}/`,
      {
        headers: {
          Authorization: `Token ${token.value}`
        }
      }
    )

    post.value.comments = post.value.comments.filter(c => c.id !== commentId)
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
    alert('댓글 삭제에 실패했습니다.')
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('ko-KR')
}

onMounted(() => {
  fetchPost()
})

watch(isLoggedIn, (value) => {
  if (value) {
    fetchCurrentUser()
  } else {
    currentUserId.value = null
  }
})
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.title { font-size: 24px; font-weight: 700; }
.card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; max-width: 720px; display: flex; flex-direction: column; gap: 12px; }
.row { display: flex; justify-content: space-between; gap: 12px; align-items: center; }
.key { color: #6b7280; min-width: 64px; }
.value { font-weight: 600; }
.desc { color: #4b5563; margin: 0; white-space: pre-wrap; }
.link { text-decoration: none; color: #111827; font-weight: 600; }
.state { padding: 24px; border: 1px solid #e5e7eb; border-radius: 12px; background: #fff; }

.post-input {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.post-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
}

.post-actions {
  display: flex;
  gap: 8px;
}

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
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.comment-submit-btn:hover:not(:disabled) {
  background: #1d4ed8;
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
  gap: 12px;
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

.edit-btn, .delete-btn, .save-btn, .cancel-btn {
  padding: 6px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
  background: #fff;
  color: #111827;
}

.edit-btn:hover,
.delete-btn:hover,
.cancel-btn:hover {
  background: #f3f4f6;
}

.save-btn {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.save-btn:hover {
  background: #1d4ed8;
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
</style>
