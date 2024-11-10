<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        
        <q-toolbar-title>
          <q-avatar>
              <img src="eye_white.svg">
            </q-avatar>
          CRIME CATCHER
        </q-toolbar-title>
        <!-- Show logout button only when user is logged in -->
        <q-btn outline @click="logout" v-if="isLoggedIn">Logout</q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const isLoggedIn = ref(!!localStorage.getItem('token'));

    const logout = () => {
      localStorage.removeItem('token');  // Remove the JWT token from localStorage
      isLoggedIn.value = false;  // Update the login state
      // Redirect to the login page
      window.location.href = '/login';  // Force a redirect to the login page
    };

    return {
      isLoggedIn,
      logout
    };
  },
  watch: {
    // Watch for changes in localStorage and update the login state accordingly
    '$route'() {
      this.isLoggedIn = !!localStorage.getItem('token');
    }
    
  }
}
</script>

