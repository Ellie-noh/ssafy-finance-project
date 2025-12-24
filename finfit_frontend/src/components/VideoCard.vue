<template>
  <div class="video-card">
    <div class="thumbnail-container">
      <img :src="video.snippet.thumbnails.medium.url" class="thumbnail" :alt="video.snippet.title">
      <div class="play-overlay">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="white">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </div>
    </div>
    <div class="video-info">
      <h3 class="video-title">{{ video.snippet.title }}</h3>
      <p class="channel-name">{{ video.snippet.channelTitle }}</p>
      <p class="upload-date">{{ formatDate(video.snippet.publishedAt) }}</p>
      <p class="video-description">{{ truncateDescription(video.snippet.description) }}</p>
      <router-link :to="`/video/${video.id.videoId}`" class="watch-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" class="play-icon">
          <path d="M8 5v14l11-7z"/>
        </svg>
        시청하기
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    video: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 1) {
        return '오늘';
      } else if (diffDays === 2) {
        return '어제';
      } else if (diffDays <= 7) {
        return `${diffDays - 1}일 전`;
      } else if (diffDays <= 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks}주 전`;
      } else if (diffDays <= 365) {
        const months = Math.floor(diffDays / 30);
        return `${months}개월 전`;
      } else {
        const years = Math.floor(diffDays / 365);
        return `${years}년 전`;
      }
    },
    truncateDescription(description) {
      if (description.length > 100) {
        return description.substring(0, 100) + '...';
      }
      return description;
    }
  }
};
</script>

<style scoped>
.video-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-bottom: 16px;
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.thumbnail-container {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.video-card:hover .play-overlay {
  opacity: 1;
}

.video-info {
  padding: 16px;
}

.video-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.channel-name {
  font-size: 14px;
  color: #606060;
  margin: 0 0 4px 0;
  font-weight: 500;
}

.upload-date {
  font-size: 12px;
  color: #909090;
  margin: 0 0 8px 0;
}

.video-description {
  font-size: 14px;
  color: #606060;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.watch-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #111827;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.watch-btn:hover {
  background: #1f2937;
  color: white;
}

.play-icon {
  flex-shrink: 0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .video-card {
    margin-bottom: 12px;
  }

  .thumbnail-container {
    height: 160px;
  }

  .video-info {
    padding: 12px;
  }

  .video-title {
    font-size: 14px;
  }

  .channel-name,
  .video-description {
    font-size: 13px;
  }

  .watch-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .thumbnail-container {
    height: 140px;
  }

  .video-info {
    padding: 10px;
  }

  .video-title {
    font-size: 13px;
  }

  .watch-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
