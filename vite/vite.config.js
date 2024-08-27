import { fileURLToPath, URL } from 'node:url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import Components from 'unplugin-vue-components/vite'
import {BootstrapVueNextResolver} from "bootstrap-vue-next";

// https://vitejs.dev/config/
// noinspection JSUnusedGlobalSymbols
export default defineConfig({
    plugins: [
        vue({
            template: {
                compilerOptions: {
                    isCustomElement: isCustomElement,
                },
            },
        }),
        Components({
            resolvers: [BootstrapVueNextResolver({
                aliases: {
                    // BInput: 'BFormInput',
                }
            })],
        }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
    server: {
        port: 8080,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/static': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
        },
    },
});

function isCustomElement(tag) {
    return (
        tag.startsWith('form-') ||
        tag === 'layer' ||
        tag === 'inwrapper' ||
        tag === 'outwrapper' ||
        tag === 'na-splitflapdisplay'
    );
}
