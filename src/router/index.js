import { createRouter, createWebHistory } from 'vue-router'
import { Auth } from 'aws-amplify';
import HomePage from '../views/HomePage.vue'
import ImagePage from '../views/ImagePage.vue'
import LoginPage from '../views/LoginPage.vue' 

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: true }, 
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/image',
    name: 'Image',
    component: ImagePage,
    meta: { requiresAuth: true }, 
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})


router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const currentUser = await Auth.currentUserInfo();

  if (requiresAuth && !currentUser) {
    next('/login');
  } else {
    next();
  }
});

export default router
