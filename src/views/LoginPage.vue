<template>
    <div>
      <h1>Login</h1>
      <a :href="loginURL">Go to Login</a>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        loginURL: 'https://cloudsnapgroup15.auth.ap-southeast-2.amazoncognito.com',
      };
    },
    mounted() {
      
      const script = document.createElement('script');
      script.src = 'https://cdn.cognitoforms.com/scripts/xxxxxx/xxxxxx.js'; 
      script.async = true;
      document.body.appendChild(script);
    },
  };
  </script>
  