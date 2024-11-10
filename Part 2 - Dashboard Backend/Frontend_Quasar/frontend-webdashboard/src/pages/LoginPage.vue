<!-- http://localhost:9000/#/login -->
<template>
  <q-page class="flex flex-center">
    <div>
      <img
      alt="eye logo"
      src="eye1.svg"
      style="width: 200px; height: 200px"
    >
      <q-input v-model="username" label="Username" />
      <q-input v-model="password" label="Password" type="password" />
      <q-btn label="Login" @click="login" />
      <p>{{ message }}</p>
      <router-link to="/signup">Don't have an account? Signup here</router-link>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      message: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/api/login', {
          username: this.username,
          password: this.password
        });
        const token = response.data.access_token;
        localStorage.setItem('token', token);  // Store JWT token in localStorage
        this.message = 'Login successful';
        this.$router.push('/');  // Redirect to dashboard after login
        this.$root.isLoggedIn = true;  // Ensure global login state is updated
      } catch (error) {
        this.message = error.response.data.message || 'Login failed';
      }
    }
  }
}
</script>
