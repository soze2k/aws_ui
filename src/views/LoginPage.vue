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
        loginURL: 'https://cloudsnapgroup15.auth.ap-southeast-2.amazoncognito.com/login?client_id=78acqta94st5tcnes8s3c66s94&response_type=token&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Flogged_in.html',
      };
    },
    mounted() {
      const script = document.createElement('script');
      script.src = 'https://cloudsnapgroup15.auth.ap-southeast-2.amazoncognito.com/login?client_id=78acqta94st5tcnes8s3c66s94&response_type=token&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Flogged_in.html';
      script.async = true;
      document.body.appendChild(script);
    },
  };
  </script>
  