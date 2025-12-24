<template>
  <div class="chatbot-container">
    <button @click="toggleChat" class="chat-toggle">
      💬
    </button>
    
    <div
      v-if="isOpen"
      class="chat-window"
      :style="{ width: chatWidth + 'px', height: chatHeight + 'px' }"
    >
      <div class="chat-header">
        <h3>AI 금융 상담</h3>
        <button @click="toggleChat" class="close-btn">×</button>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message', msg.sender === 'user' ? 'user' : 'bot']"
        >
          <pre>{{ msg.text }}</pre>
        </div>
        <div v-if="isTyping" class="message bot typing">
          AI가 답변 중...
        </div>
      </div>

      <div class="step-prompts">
        <div class="prompt-section">
          <div class="prompt-title">나이대</div>
          <div class="prompt-buttons">
            <button
              v-for="opt in ageOptions"
              :key="opt"
              :class="['prompt-btn', selected.age === opt ? 'selected' : '']"
              @click="selectOption('age', opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>
        <div class="prompt-section">
          <div class="prompt-title">월 저축 가능 금액</div>
          <div class="prompt-buttons">
            <button
              v-for="opt in amountOptions"
              :key="opt"
              :class="['prompt-btn', selected.amount === opt ? 'selected' : '']"
              @click="selectOption('amount', opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>
        <div class="prompt-section">
          <div class="prompt-title">저축 목적</div>
          <div class="prompt-buttons">
            <button
              v-for="opt in purposeOptions"
              :key="opt"
              :class="['prompt-btn', selected.purpose === opt ? 'selected' : '']"
              @click="selectOption('purpose', opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>
        <div class="prompt-actions">
          <button class="reset-btn" @click="resetSelection">선택 초기화</button>
          <button class="send-btn filled" :disabled="!isSelectionComplete" @click="sendSelection">
            선택한 정보로 추천받기
          </button>
        </div>
      </div>

      <div class="chat-input">
        <input 
          v-model="userInput" 
          @keyup.enter="sendMessage" 
          placeholder="궁금한 걸 물어보세요..." 
          class="input-field"
        >
        <button @click="sendMessage" class="send-btn">보내기</button>
      </div>

      <div class="resize-handle" @mousedown.prevent="startResize"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, computed, onBeforeUnmount } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const userInput = ref('')
const messages = ref([])
const isTyping = ref(false)
const messagesContainer = ref(null)
const chatWidth = ref(350)
const chatHeight = ref(620)
const isResizing = ref(false)
const resizeStart = { x: 0, y: 0, width: 0, height: 0 }

const ageOptions = ['20대', '30대', '40대', '50대', '60세 이상']
const amountOptions = ['30만원 이하', '100만원 이하', '1000만원 이하', '1000만원 이상']
const purposeOptions = ['여행', '교육', '장기', '단기', '기타']
const selected = ref({ age: null, amount: null, purpose: null })

const isSelectionComplete = computed(() => selected.value.age && selected.value.amount && selected.value.purpose)

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && messages.value.length === 0) {
    addMessage(
      'bot',
      '안녕하세요! 😊\n예금이나 적금 상품 추천을 도와드릴까요?\n아래 단계별 선택 버튼으로 나이대, 월 저축 가능액, 저축 목적을 선택해주세요.'
    )
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return
  const message = userInput.value.trim()
  userInput.value = ''
  await sendMessageWithText(message)
}

const sendMessageWithText = async (text) => {
  if (!text.trim()) return
  addMessage('user', text.trim())
  isTyping.value = true
  try {
    const response = await axios.post('http://127.0.0.1:8000/chatbot/chat/', {
      message: text.trim()
    })
    addMessage('bot', response.data.message)
  } catch (error) {
    console.error('챗봇 에러:', error)
    addMessage('bot', '잠시 후 다시 시도해주세요. 문제가 계속되면 관리자에게 문의해주세요.')
  } finally {
    isTyping.value = false
  }
}

const addMessage = (sender, text) => {
  messages.value.push({
    id: Date.now(),
    sender,
    text
  })
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const selectOption = (type, value) => {
  selected.value = { ...selected.value, [type]: value }
}

const resetSelection = () => {
  selected.value = { age: null, amount: null, purpose: null }
}

const sendSelection = async () => {
  if (!isSelectionComplete.value) return
  const text = `나이대: ${selected.value.age}, 월 저축 가능 금액: ${selected.value.amount}, 저축 목적: ${selected.value.purpose} — 이 조건에 맞는 예금/적금 상품을 추천해줘`
  await sendMessageWithText(text)
}

const startResize = (event) => {
  isResizing.value = true
  resizeStart.x = event.clientX
  resizeStart.y = event.clientY
  resizeStart.width = chatWidth.value
  resizeStart.height = chatHeight.value
  document.addEventListener('mousemove', onResize)
  document.addEventListener('mouseup', stopResize)
}

const onResize = (event) => {
  if (!isResizing.value) return
  const dx = resizeStart.x - event.clientX
  const dy = resizeStart.y - event.clientY
  chatWidth.value = Math.max(320, Math.min(600, resizeStart.width + dx))
  chatHeight.value = Math.max(420, Math.min(800, resizeStart.height + dy))
}

const stopResize = () => {
  if (!isResizing.value) return
  isResizing.value = false
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
}

onBeforeUnmount(() => {
  stopResize()
})
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0ea5e9, #2563eb);
  color: #fff;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35);
  transition: all 0.3s ease;
}

.chat-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 32px rgba(14, 165, 233, 0.4);
}

.chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 620px;
  background: linear-gradient(145deg, #f8fafc, #eef2ff);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 16px 48px rgba(15, 23, 42, 0.18);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: linear-gradient(135deg, #2563eb, #0ea5e9);
  color: #fff;
  padding: 16px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 15px;
  letter-spacing: 0.2px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-messages {
  flex: 1;
  padding: 18px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: #f8fafc;
}

.message {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 13.5px;
  line-height: 1.4;
  white-space: pre-wrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.message pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: inherit;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #2563eb, #0ea5e9);
  color: #fff;
}

.message.bot {
  align-self: flex-start;
  background: #ffffff;
  color: #1f2937;
  border: 1px solid #e5e7eb;
}

.message.typing {
  font-style: italic;
  color: #9ca3af;
}

.step-prompts {
  padding: 14px 16px;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #f4f7fb, #eef2ff);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.prompt-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.prompt-title {
  font-size: 12px;
  color: #4b5563;
  font-weight: 600;
}

.prompt-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.prompt-btn {
  padding: 6px 10px;
  border: 1px solid #dbeafe;
  border-radius: 14px;
  background: #fff;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
  color: #1f2937;
}

.prompt-btn.selected {
  background: linear-gradient(135deg, #2563eb, #0ea5e9);
  color: #fff;
  border-color: #2563eb;
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);
}

.prompt-btn:hover {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}

.prompt-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  align-items: center;
  margin-top: 4px;
}

.reset-btn {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 14px;
  background: white;
  cursor: pointer;
  font-size: 12px;
}

.chat-input {
  padding: 14px 16px;
  border-top: 1px solid #e5e7eb;
  background: #f8fafc;
  display: flex;
  gap: 8px;
}

.input-field {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #dbeafe;
  border-radius: 16px;
  outline: none;
  font-size: 14px;
}

.input-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.send-btn {
  padding: 8px 16px;
  background: linear-gradient(135deg, #2563eb, #0ea5e9);
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.send-btn.filled:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.send-btn:hover {
  background: #1d4ed8;
}

.resize-handle {
  position: absolute;
  left: 8px;
  bottom: 8px;
  width: 16px;
  height: 16px;
  border-radius: 4px;
  background: #cbd5e1;
  cursor: nwse-resize;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.resize-handle:hover {
  opacity: 1;
  background: #94a3b8;
}

@media (max-width: 480px) {
  .chat-window {
    width: calc(100vw - 40px);
    height: calc(100vh - 140px);
    bottom: 80px;
    right: 20px;
  }
}
</style>
