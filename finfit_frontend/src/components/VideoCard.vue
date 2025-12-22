<template>
  <div class="card">
    <img :src="video.snippet.thumbnails.medium.url" class="card-img-top" alt="Thumbnail">
    <div class="card-body">
      <h5 class="card-title">{{ video.snippet.title }}</h5>
      <p class="card-text">{{ video.snippet.channelTitle }}</p>
      <router-link :to="`/video/${video.id.videoId}`" class="btn btn-primary">상세 보기</router-link>
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
  }
};
</script>