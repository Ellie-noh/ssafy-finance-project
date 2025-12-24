<template>
  <div class="container mt-4">
    <h2>나중에 볼 영상</h2>
    <div v-if="savedVideos.length > 0" class="row">
      <div v-for="video in savedVideos" :key="video.id" class="col-md-4 mb-3">
        <div class="card">
          <img :src="video.thumbnail" class="card-img-top" alt="Thumbnail">
          <div class="card-body">
            <h5 class="card-title">{{ video.title }}</h5>
            <router-link :to="`/video/${video.id}`" class="btn btn-primary">보기</router-link>
            <button class="btn btn-danger ms-2" @click="removeVideo(video.id)">삭제</button>
          </div>
        </div>
      </div>
    </div>
    <p v-else>등록된 영상이 없습니다.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      savedVideos: []
    };
  },
  created() {
    this.loadSavedVideos();
  },
  methods: {
    loadSavedVideos() {
      this.savedVideos = JSON.parse(localStorage.getItem('savedVideos')) || [];
    },
    removeVideo(id) {
      this.savedVideos = this.savedVideos.filter(v => v.id !== id);
      localStorage.setItem('savedVideos', JSON.stringify(this.savedVideos));
    }
  }
};
</script>