<script setup>
import {ref} from 'vue';
import {usePage} from '@inertiajs/vue3';
import Navigation from "@/Layouts/Navigation.vue";

const auth = usePage().props.auth;
const content = ref();

defineProps({
    pilot: {
        type: Boolean,
        default: false
    }
});
</script>

<template>
    <div>
        <div class="min-h-screen">
            <div class="fixed w-full top-0 z-20">
                <Navigation :pilot="pilot"></Navigation>
            </div>
            <main>
                <header class="pt-24" v-if="$slots.header">
                    <slot name="header"/>
                </header>
                <slot/>
            </main>
        </div>
    </div>
</template>
