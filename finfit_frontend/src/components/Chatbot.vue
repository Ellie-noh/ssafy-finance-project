<template>
  <div class="chatbot-container">
    <button @click="toggleChat" class="chat-toggle">
      💬
    </button>
    
    <div v-if="isOpen" class="chat-window">
      <div class="chat-header">
        <h3>AI 금융 추천</h3>
        <button @click="toggleChat" class="close-btn">×</button>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="msg in messages" :key="msg.id" 
             :class="['message', msg.sender === 'user' ? 'user' : 'bot']">
          {{ msg.text }}
        </div>
        <div v-if="isTyping" class="message bot typing">
          AI가 입력 중...
        </div>
      </div>
      
      <div class="chat-input">
        <input 
          v-model="userInput" 
          @keyup.enter="sendMessage" 
          placeholder="금융 상품 추천을 물어보세요..."
          class="input-field"
        >
        <button @click="sendMessage" class="send-btn">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const userInput = ref('')
const messages = ref([])
const isTyping = ref(false)
const messagesContainer = ref(null)

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && messages.value.length === 0) {
    addMessage('bot', '안녕하세요! 저는 AI 금융 추천 봇입니다. 예금, 적금 상품 추천을 도와드릴게요. 무엇을 도와드릴까요?')
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return
  
  const message = userInput.value.trim()
  userInput.value = ''
  
  addMessage('user', message)
  isTyping.value = true
  
  try {
    const response = await axios.post('http://127.0.0.1:8000/chatbot/chat/', {
      message: message
    })
    
    addMessage('bot', response.data.message)
  } catch (error) {
    console.error('챗봇 에러:', error)
    addMessage('bot', '죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.')
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
  background: #2563eb;
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.chat-toggle:hover {
  transform: scale(1.1);
  background: #1d4ed8;
}

.chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: #2563eb;
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
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
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.4;
}

.message.user {
  align-self: flex-end;
  background: #2563eb;
  color: white;
}

.message.bot {
  align-self: flex-start;
  background: #f3f4f6;
  color: #374151;
}

.message.typing {
  font-style: italic;
  color: #9ca3af;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}

.input-field {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 20px;
  outline: none;
  font-size: 14px;
}

.input-field:focus {
  border-color: #2563eb;
}

.send-btn {
  padding: 8px 16px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.send-btn:hover {
  background: #1d4ed8;
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