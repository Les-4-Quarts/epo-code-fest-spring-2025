import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // Redirect root path to analyze view
      path: '/',
      name: 'home',
      redirect: '/analyze'
    },
    {
      path: '/analyze',
      name: 'analyze',
      component: () => import('../views/AnalyzeView.vue')
    },
    {
      path: '/analyzed/:id',
      name: 'analyzed',
      component: () => import('../views/AnalyzedViewByPatentNumber.vue'),
    },
    {
      path: '/explore',
      name: 'explore',
      component: () => import('../views/ExploreView.vue')
    },
  ]
})

export default router
