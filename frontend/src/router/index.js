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
            path: '/auth',
            name: 'Authentication', 
            component: () => import('../views/AuthView.vue'),
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