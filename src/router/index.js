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
      redirect: "/homepage",
      children: [
        {
          path: 'homepage',
          name: 'homepage',
          component: () => import('@/view/homepage.vue'),
        },
      ]
    },

  ]