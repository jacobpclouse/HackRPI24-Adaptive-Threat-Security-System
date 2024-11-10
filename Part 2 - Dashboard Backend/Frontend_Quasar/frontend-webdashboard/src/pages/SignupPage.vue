<!-- http://localhost:9000/#/signup -->
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
      <q-btn label="Signup" @click="signup" />
      <p>{{ message }}</p>
      <router-link to="/login">Already have an account? Login here</router-link>
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
    async signup() {
      try {
        const response = await axios.post('http://localhost:5000/api/signup', {
          username: this.username,
          password: this.password
        });
        localStorage.setItem('token', response.data.access_token);
        this.message = 'Signup successful';
        this.$router.push('/');  // Redirect to dashboard after signup
        this.$root.isLoggedIn = true;  // Ensure global login state is updated
      } catch (error) {
        this.message = error.response.data.message || 'Signup failed';
      }
    }
  }
}
</script>
