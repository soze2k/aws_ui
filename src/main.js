import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Amplify from 'aws-amplify';
import AmplifyVue from '@aws-amplify/ui-vue';
import awsconfig from './aws-exports';
import '@aws-amplify/ui-vue/styles.css';

Amplify.configure(awsconfig);

createApp(App).use(router).mount('#app')

const app = createApp(App);
app.use(AmplifyVue);
app.mount('#app');