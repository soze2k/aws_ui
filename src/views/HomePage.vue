<template>
  <div>
    <h1>Home Page</h1>
    <p>Welcome to the home page!</p>
    <button class="btn" @click="logout">Logout</button>
  </div>
</template>

<script>
import { Auth } from 'aws-amplify';

export default {
  methods: {
    async logout() {
      try {
        await Auth.signOut();
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.btn {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #009688;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #00695c;
}
</style>