<template>
  <q-page class="flex flex-center">

    <!-- Left Drawer for Filtering -->
    <q-drawer v-model="drawerOpen" side="left" width="250" bordered>
      <q-list padding>
        <q-item-label header>Filter Videos</q-item-label>
        
        <!-- Filter by Index Order -->
        <q-item>
          <q-item-section>
            <q-select
              v-model="filters.indexOrder"
              :options="['Ascending', 'Descending']"
              label="Index Order"
              dense
              outlined
            />
          </q-item-section>
        </q-item>

        <!-- Filter by Camera Name -->
        <q-item>
          <q-item-section>
            <q-input
              v-model="filters.name"
              label="Camera Name"
              dense
              outlined
            />
          </q-item-section>
        </q-item>

        <!-- Filter by Start Date/Time -->
        <q-item>
          <q-item-section>
            <q-input
              v-model="filters.startTime"
              label="Start Date/Time"
              type="datetime-local"
              dense
              outlined
            />
          </q-item-section>
        </q-item>

        <!-- Filter by Stop Date/Time -->
        <q-item>
          <q-item-section>
            <q-input
              v-model="filters.stopTime"
              label="Stop Date/Time"
              type="datetime-local"
              dense
              outlined
            />
          </q-item-section>
        </q-item>

        <!-- Additional Filters -->
        <q-item v-for="(filterLabel, filterKey) in additionalFilters" :key="filterKey">
          <q-item-section>
            <q-input
              v-model="filters[filterKey]"
              :label="filterLabel"
              dense
              outlined
            />
          </q-item-section>
        </q-item>

        <!-- Apply Filters and Clear Filters Buttons (stacked vertically) -->
        <q-item class="q-mt-md">
          <q-item-section class="column">
            <q-btn label="Clear Filters" color="negative" @click="clearFilters" class="q-mb-sm full-width" />
            <q-btn label="Apply Filters" color="primary" @click="applyFilters" class="full-width" />
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <!-- Main Content -->
    <div class="q-pa-md">
      <h1>Index Camera Dashboard</h1>
      <div v-if="filteredVideos.length">
        <q-card v-for="video in filteredVideos" :key="video.id" class="q-mb-md">
          <q-card-section>
            <div class="text-h6">{{ video.camera_name }} - {{ video.location }}</div>
            <div>Start: {{ video.start_time }} | Stop: {{ video.stop_time }}</div>
            <div>Camera: {{ video.camera_name }} | IP: {{ video.camera_ip }} | Location: {{ video.location }}</div>
            <div>Video filename: {{ video.video_filename }}</div>
          </q-card-section>
          <q-card-section>
            <video width="320" height="240" controls>
              <source :src="video.video_url" type="video/mp4">
              Your browser does not support the video tag.
            </video>
          </q-card-section>
          <q-card-actions align="left">
            <q-btn label="View Video" color="primary" @click="goToVideoPage(video.id)" />
          </q-card-actions>
        </q-card>
      </div>
      <div v-else>
        <p>Loading videos...</p>
      </div>
    </div>

    <!-- Footer with Drawer Toggle Icon -->
    <q-footer class="bg-grey-3 text-black q-pa-sm" elevated>
      <div class="row justify-between items-center">
        <div>
          <q-icon name="filter_list" size="24px" color="primary" />
          <span class="text-caption q-ml-xs">Filter Options</span>
        </div>
        <q-btn flat icon="menu" @click="drawerOpen = !drawerOpen" color="primary" />
      </div>
    </q-footer>
    
  </q-page>
</template>



<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      drawerOpen: false,
      videos: [],
      filters: {
        indexOrder: '',
        name: '',
        startTime: '',
        stopTime: '',
        cameraIp: '',
        cameraName: '',
        location: ''
      },
      additionalFilters: {
        length: 'Length of Video',
        cameraIp: 'Camera IP',
        cameraName: 'Camera Name',
        location: 'Location'
      }
    };
  },
  computed: {
    filteredVideos() {
      let filtered = [...this.videos];
      if (this.filters.indexOrder) {
        filtered.sort((a, b) => this.filters.indexOrder === 'Ascending' ? a.id - b.id : b.id - a.id);
      }
      if (this.filters.name) {
        filtered = filtered.filter(video => video.camera_name.includes(this.filters.name));
      }
      if (this.filters.startTime) {
        filtered = filtered.filter(video => video.start_time >= this.filters.startTime);
      }
      if (this.filters.stopTime) {
        filtered = filtered.filter(video => video.stop_time <= this.filters.stopTime);
      }
      if (this.filters.cameraIp) {
        filtered = filtered.filter(video => video.camera_ip.includes(this.filters.cameraIp));
      }
      if (this.filters.cameraName) {
        filtered = filtered.filter(video => video.camera_name.includes(this.filters.cameraName));
      }
      if (this.filters.location) {
        filtered = filtered.filter(video => video.location.includes(this.filters.location));
      }
      return filtered;
    }
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
    applyFilters() {
      this.drawerOpen = false;
    },
    clearFilters() {
      this.filters = {
        indexOrder: '',
        name: '',
        startTime: '',
        stopTime: '',
        cameraIp: '',
        cameraName: '',
        location: ''
      };
    },
    goToVideoPage(videoId) {
      this.$router.push({ name: 'video', params: { id: videoId } });
    }
  },
  mounted() {
    this.fetchVideos();
  }
};
</script>
