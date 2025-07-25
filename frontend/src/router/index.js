import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginPage.vue'

const routes = [
  { path: '/',      redirect: '/login' }, //the main page redirects to the login
  { path: '/login', component: LoginPage },
  { path: '/forgot',  component: () => import('@/views/ForgotPassword.vue') },
  { path: '/reset',   component: () => import('@/views/ResetPassword.vue') },
  { path: '/signup', component: () => import('@/views/SignUpPage.vue') },
]


export default createRouter({
  history: createWebHistory(),
  routes
})
