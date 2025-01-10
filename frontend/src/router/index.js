import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'IndexPage',
            component: () => import('../views/IndexView.vue'),
        },
        {
            path: '/auth/login',
            name: 'LoginPage',
            component: () => import('../views/AuthView.vue'),
            props: { initialForm: 'login' }, // Передаем форму логина
        },
        {
            path: '/auth/register',
            name: 'RegisterPage',
            component: () => import('../views/AuthView.vue'),
            props: { initialForm: 'register' }, // Передаем форму регистрации
        },
        {
            path: '/workspace',
            name: 'Workspace', 
            component: () => import('../views/WorkspaceView.vue'),
        }, 
        {
            path: '/profile',
            name: 'Profile',
            component: () => import('../views/ProfileView.vue'),
        }
    ]
})

export default router