<template>
  <div class="search-view">
    <div class="search-header">
      <h1 class="search-title">영상 검색</h1>
      <p class="search-subtitle">관심 있는 금융 관련 영상을 검색해보세요</p>
    </div>

    <form @submit.prevent="searchVideos" class="search-form">
      <div class="search-input-group">
        <input
          v-model="query"
          type="text"
          class="search-input"
          placeholder="예: 주식 투자, 부동산, 예금 금리..."
          required
        >
        <button type="submit" class="search-btn" :disabled="loading">
          <svg v-if="loading" class="loading-icon" width="20" height="20" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" stroke-dasharray="31.416" stroke-dashoffset="31.416">
              <animate attributeName="stroke-dashoffset" values="31.416;0" dur="1s" repeatCount="indefinite"/>
            </circle>
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
          검색
        </button>
      </div>
    </form>

    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>영상을 검색하는 중...</p>
    </div>

    <div v-else-if="videos.length > 0" class="videos-grid">
      <VideoCard
        v-for="video in videos"
        :key="video.id.videoId"
        :video="video"
        class="video-item"
      />
    </div>

    <div v-else-if="searched" class="empty-state">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
        <circle cx="11" cy="11" r="8"/>
        <path d="m21 21-4.35-4.35"/>
      </svg>
      <h3>검색 결과가 없습니다</h3>
      <p>다른 키워드로 검색해보세요</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VideoCard from '../components/VideoCard.vue';

export default {
  components: { VideoCard },
  data() {
    return {
      query: '',
      videos: [],
      loading: false,
      searched: false
    };
  },
  methods: {
    async searchVideos() {
      if (!this.query.trim()) return;

      this.loading = true;
      this.searched = false;

      try {
        const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY;
        const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(this.query)}&type=video&maxResults=12&key=${apiKey}`;

        const response = await axios.get(url);
        this.videos = response.data.items || [];
        this.searched = true;
      } catch (error) {
        console.error('API 호출 오류:', error);
        this.videos = [];
        this.searched = true;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.search-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  text-align: center;
  margin-bottom: 40px;
}

.search-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.search-subtitle {
  font-size: 18px;
  color: #606060;
  margin: 0;
}

.search-form {
  max-width: 600px;
  margin: 0 auto 40px;
}

.search-input-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 16px 20px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  background: #111827;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  white-space: nowrap;
}

.search-btn:hover:not(:disabled) {
  background: #1f2937;
}

.search-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #606060;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #111827;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.video-item {
  transition: transform 0.2s ease;
}

.video-item:hover {
  transform: translateY(-4px);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  color: #606060;
}

.empty-state svg {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #1a1a1a;
}

.empty-state p {
  font-size: 16px;
  margin: 0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .search-view {
    padding: 16px;
  }

  .search-title {
    font-size: 24px;
  }

  .search-subtitle {
    font-size: 16px;
  }

  .search-input-group {
    flex-direction: column;
    gap: 12px;
  }

  .search-input {
    width: 100%;
  }

  .search-btn {
    width: 100%;
    justify-content: center;
  }

  .videos-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .search-title {
    font-size: 20px;
  }

  .search-input,
  .search-btn {
    padding: 12px 16px;
    font-size: 14px;
  }
}
</style>
