<template>
  <div class="container mt-4">
    <h2>영상 상세</h2>
    <iframe width="560" height="315" :src="`https://www.youtube.com/embed/${videoId}`" frameborder="0" allowfullscreen></iframe>
    <h3 v-if="video">{{ video.snippet.title }}</h3>
    <p v-if="video">채널: {{ video.snippet.channelTitle }}</p>
    <p v-if="video">{{ video.snippet.description }}</p>
    <button v-if="!isSaved" class="btn btn-success" @click="saveVideo">나중에 볼 영상 저장</button>
    <button v-else class="btn btn-danger" @click="removeVideo">저장 취소</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      videoId: this.$route.params.id,
      video: null,
      savedVideos: []
    };
  },
  computed: {
    isSaved() {
      return this.savedVideos.some(v => v.id === this.videoId);
    }
  },
  async created() {
    await this.fetchVideoDetails();
    this.loadSavedVideos();
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
    loadSavedVideos() {
      this.savedVideos = JSON.parse(localStorage.getItem('savedVideos')) || [];
    },
    saveVideo() {
      const videoToSave = {
        id: this.videoId,
        title: this.video.snippet.title,
        thumbnail: this.video.snippet.thumbnails.medium.url
      };
      this.savedVideos.push(videoToSave);
      localStorage.setItem('savedVideos', JSON.stringify(this.savedVideos));
      this.loadSavedVideos(); // 업데이트
    },
    removeVideo() {
      this.savedVideos = this.savedVideos.filter(v => v.id !== this.videoId);
      localStorage.setItem('savedVideos', JSON.stringify(this.savedVideos));
      this.loadSavedVideos(); // 업데이트
    }
  }
};
</script>