<!-- this is the old dashboard page, use the index instead -->
<template>
  <q-page class="flex flex-center">
    <img alt="Quasar logo" src="eye1.svg" style="width: 200px; height: 200px" />
    <div>
      <h1>BACKUP Dashboard Page!!</h1>
      <div v-if="videos.length">
        <q-card v-for="video in videos" :key="video.id" class="q-mb-md">
          <q-card-section>
            <div class="text-h6">
              <!-- <a @click="goToVideoPage(video.video_url)" class="text-primary cursor-pointer"> -->
              <a @click="goToVideoPage(video.id)" class="text-primary cursor-pointer">
                {{ video.camera_name }} - {{ video.location }}
              </a>
            </div>
            <div>Start: {{ video.start_time }} | Stop: {{ video.stop_time }}</div>
            <div>Video filename: {{ video.video_filename }}</div>
            <div>Video Id: {{ video.id }}</div>
          </q-card-section>

          <q-card-section>
            <video width="320" height="240" controls>
              <source :src="video.video_url" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </q-card-section>
        </q-card>
      </div>
      <div v-else>
        <p>Loading videos...</p>
      </div>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      videos: []
    };
  },
  methods: {
    async fetchVideos() {
      try {
        const response = await axios.get('http://localhost:5000/api/videos');
        this.videos = response.data;
      } catch (error) {
        console.error('Error fetching video data:', error);
      }
    },
    goToVideoPage(videoId) {
      // this.$router.push({ name: 'video', params: { id: videoId } });
      this.$router.push({ name: 'video', params: { id: videoId } });
    }
  },
  mounted() {
    this.fetchVideos();
  }
};
</script>

