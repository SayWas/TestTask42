import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/userStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/',
      redirect: '/contracts'
    },
    {
      path: '/contracts',
      name: 'contracts',
      component: () => import('../views/Contracts.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/contracts/:id',
      name: 'contract_details',
      component: () => import('../views/ContractDetails.vue'),
      meta: { requiresAuth: true },
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!useUserStore().isAuthenticated) {
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
