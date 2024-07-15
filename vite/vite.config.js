import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
// noinspection JSUnusedGlobalSymbols
export default defineConfig({
    plugins: [
        vue({
            template: {
                compilerOptions: {
                    isCustomElement: isCustomElement
                }
            }
        }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
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
            }
        }
    },
});

function isCustomElement(tag) {
    return tag.startsWith('form-') ||
        tag === 'layer' ||
        tag === 'inwrapper' ||
        tag === 'outwrapper';
}
