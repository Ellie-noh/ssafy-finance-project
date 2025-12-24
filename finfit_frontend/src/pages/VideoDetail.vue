<template>
  <div class="video-detail">
    <div class="video-container">
      <iframe
        width="100%"
        height="500"
        :src="`https://www.youtube.com/embed/${videoId}`"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>

    <div class="video-info" v-if="video">
      <h1 class="video-title">{{ video.snippet.title }}</h1>
      <div class="video-meta">
        <span class="channel-name">{{ video.snippet.channelTitle }}</span>
        <span class="separator">•</span>
        <span class="upload-date">{{ formatDate(video.snippet.publishedAt) }}</span>
      </div>
      <div class="video-description">
        <p>{{ video.snippet.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      videoId: this.$route.params.id,
      video: null
    };
  },
  async created() {
    await this.fetchVideoDetails();
  },
  methods: {
    async fetchVideoDetails() {
      const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY;
      const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${this.videoId}&key=${apiKey}`;
      try {
        const response = await axios.get(url);
        this.video = response.data.items[0];
      } catch (error) {
        console.error('API 호출 오류:', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.video-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.video-container {
  margin-bottom: 24px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.video-container iframe {
  display: block;
  width: 100%;
  height: 500px;
}

.video-info {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.video-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 16px 0;
  line-height: 1.3;
}

.video-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #606060;
}

.channel-name {
  font-weight: 600;
  color: #1a1a1a;
}

.separator {
  color: #909090;
}

.upload-date {
  color: #909090;
}

.video-description {
  font-size: 16px;
  line-height: 1.6;
  color: #404040;
}

.video-description p {
  margin: 0;
  white-space: pre-wrap;
}

@media (max-width: 768px) {
  .video-detail {
    padding: 16px;
  }

  .video-container iframe {
    height: 250px;
  }

  .video-info {
    padding: 16px;
  }

  .video-title {
    font-size: 20px;
  }
}
</style>