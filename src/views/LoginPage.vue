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
      loginURL: 'https://cloudsnapgroup15.auth.ap-southeast-2.amazoncognito.com/login?client_id=78acqta94st5tcnes8s3c66s94&response_type=token&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F',
    };
  },
  methods: {
    redirectToLogin() {
      window.location.href = this.loginURL;
    },
  },
};
</script>
