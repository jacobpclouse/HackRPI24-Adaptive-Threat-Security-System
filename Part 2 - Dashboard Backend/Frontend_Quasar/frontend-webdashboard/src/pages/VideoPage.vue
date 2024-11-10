<template>
    <q-page class="flex flex-center">
      <div v-if="video">
        <h1>{{ video.camera_name }} - {{ video.location }}</h1>
        <div>Start: {{ video.start_time }}</div>
        <div>Stop: {{ video.stop_time }}</div>
        <div>IP: {{ video.camera_ip }}</div>
        <div>Camera: {{ video.camera_name }} | Location: {{ video.location }}</div>

        
        <video width="100%" height="auto" controls>
          <source :src="video.video_url" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
  
        <div class="q-pa-md">
          <q-btn label="Invert Colors" @click="applyTransformation('invert')" color="primary" />
          <q-btn label="Increase Contrast" @click="applyTransformation('contrast')" color="primary" />
          <!-- Add more buttons for other transformations -->
        </div>
  
        <q-btn label="Return to Main Dashboard" @click="goBack" color="secondary" />
      </div>
      <div v-else>
        <p>Loading video...</p>
      </div>
    </q-page>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        video: null
      };
    },
    methods: {
      async fetchVideo() {
        try {
          const response = await axios.get(`http://localhost:5000/api/video/${this.$route.params.id}`);
          this.video = response.data;
        } catch (error) {
          console.error('Error fetching video:', error);
        }
      },
      applyTransformation(transformation) {
        // Send a request to Flask to apply the transformation
        axios.post(`http://localhost:5000/api/video/${this.$route.params.id}/transform`, { transformation })
          .then(response => {
            this.video.video_url = response.data.video_url; // Update URL if needed
          })
          .catch(error => {
            console.error('Error applying transformation:', error);
          });
      },
      goBack() {
        this.$router.push({ name: 'index' });
      }
    },
    mounted() {
      this.fetchVideo();
    }
  };
  </script>
  