import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Signup from '@/pages/Signup.vue'
import Products from '@/pages/Products.vue'
import ProductDetail from '@/pages/ProductDetail.vue'
import Fx from '@/pages/Fx.vue'
import BankMap from '@/pages/BankMap.vue'
import BoardList from '@/pages/BoardList.vue'
import BoardDetail from '@/pages/BoardDetail.vue'
import BoardCreate from '@/pages/BoardCreate.vue'
import Profile from '@/pages/Profile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: Home },

    { path: '/login', name: 'Login', component: Login },
    { path: '/signup', name: 'Signup', component: Signup },

    { path: '/products', name: 'Products', component: Products },
    { path: '/products/:fin_prdt_cd', name: 'ProductDetail', component: ProductDetail, props: true },
    { path: '/fx', name: 'Fx', component: Fx },
    { path: '/banks', name: 'BankMap', component: BankMap },

    { path: '/board', name: 'BoardList', component: BoardList },
    { path: '/board/new', name: 'BoardCreate', component: BoardCreate },
    { path: '/board/:id', name: 'BoardDetail', component: BoardDetail, props: true },

    { path: '/profile', name: 'Profile', component: Profile },

    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

export default router
