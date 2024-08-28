import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import NotFound from "@/views/NotFound.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: NotFound
        },
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue'),
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue'),
        },
        {
            path: '/settings',
            name: 'settings',
            component: () => import('../views/SettingsView.vue'),
        },
        {
            path: '/reset-password',
            name: 'reset-password',
            component: () => import('../views/ResetPasswordView.vue'),
        },
        {
            path: '/check-email',
            name: 'check-email',
            component: () => import('../views/CheckEmailView.vue'),
        },
        {
            path: '/passport',
            name: 'passport',
            component: () => import('../views/PassportView.vue'),
        },
        {
            path: '/booking',
            name: 'booking',
            component: () => import('../views/BookingView.vue'),
        },
        {
            path: '/checkin',
            name: 'checkin',
            component: () => import('../views/CheckinView.vue'),
        },
        {
            path: '/ops',
            name: 'dashboard',
            component: () => import('../views/OpsCenter/Dashboard.vue')
        },
        {
            path: '/ops/dispatcher',
            name: 'dispatcher',
            component: () => import('../views/OpsCenter/Dispatcher.vue')
        },
        {
            path: '/ops/settings',
            name: 'pilot-settings',
            component: () => import('../views/OpsCenter/PilotSettings.vue')
        },
        {
            path: '/ops/flight/:flightNumber',
            name: 'flight',
            component: () => import('../views/OpsCenter/FlightManager.vue')
        },
    ],
});

export default router;
