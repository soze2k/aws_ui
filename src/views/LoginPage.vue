<template>
    <div>
      <h1>Login</h1>
      <button class="btn" @click="login">Go to Login</button>
    </div>
  </template>
  
  <script>
  import { Auth } from 'aws-amplify';
  
  export default {
    methods: {
      async login() {
        try {
          await Auth.federatedSignIn({ provider: 'Cognito' });
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
  