<template>
  <div class="container mt-4">
    <h2>영상 검색</h2>
    <form @submit.prevent="searchVideos">
      <div class="input-group mb-3">
        <input v-model="query" type="text" class="form-control" placeholder="키워드 입력" required>
        <button class="btn btn-primary" type="submit">검색</button>
      </div>
    </form>
    <div v-if="videos.length > 0" class="row">
      <div v-for="video in videos" :key="video.id.videoId" class="col-md-4 mb-3">
        <VideoCard :video="video" />
      </div>
    </div>
    <p v-else>검색 결과가 없습니다.</p>
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
      videos: []
    };
  },
  methods: {
    async searchVideos() {
      const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY;
      const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${this.query}&type=video&key=${apiKey}`;
      try {
        const response = await axios.get(url);
        this.videos = response.data.items;
      } catch (error) {
        console.error('API 호출 오류:', error);
      }
    }
  }
};
</script>