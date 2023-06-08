<template>
    <div>
      <h1>Login</h1>
      <a :href="loginURL" @click="redirectToLogin">Go to Login</a>
    </div>
</template>

<script>
export default {
  data() {
    return {
        loginURL: 'https://cloudsnapgroup15.auth.ap-southeast-2.amazoncognito.com/login?response_type=code&client_id=78acqta94st5tcnes8s3c66s94&redirect_uri=http://localhost:8000/',
    };
  },
  methods: {
    redirectToLogin() {
      window.location.href = this.loginURL;
    },
  },
};
</script>

