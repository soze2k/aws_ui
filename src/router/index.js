import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/Index.vue'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
    {
      path: '/',
      name: 'index',
      component: index,
      redirect: "/homePage",
      children: [
        {
          path: 'homePage',
          name: 'HomePage',
          component: () => import('@/views/HomePage.vue'),
        },
      ]
    },

  ]
  const router = new VueRouter({
    mode: 'history',
    scrollBehavior(to, from, savedPosition) {
      
      if (savedPosition) {
      
        return savedPosition
      } else {
        return { x: 0, y: 0 }
      }
    },
    base: process.env.BASE_URL,
    routes
  })
  
export default router
