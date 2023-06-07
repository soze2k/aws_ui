<template>
    <div id="app">
      <img alt="Vue logo" src="./assets/logo.png">
      <h1>{{ message }}</h1>
    </div>
  </template>
  
  <script>
  export default {
    name: 'App',
    data() {
      return {
        message: 'Welcome to Your Vue.js App',
      };
    },
  };
  </script>
  
  <style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
  }
  </style>
  