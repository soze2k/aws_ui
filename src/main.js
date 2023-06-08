import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Amplify } from 'aws-amplify';
import AmplifyVue from '@aws-amplify/ui-vue';
import config from './aws-exports';

Amplify.configure(config);
Amplify.configure({
    Auth: {
        region: 'ap-southeast-2',
        userPoolId: 'ap-southeast-2_Sc8mVeVxo',
        userPoolWebClientId: '78acqta94st5tcnes8s3c66s94',
    }
});
const app = createApp(App);
app.use(router);
app.use(AmplifyVue);
app.mount('#app');
