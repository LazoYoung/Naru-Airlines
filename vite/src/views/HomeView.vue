<script setup>
import Navigation from "@/components/Navigation.vue";
import { reactive } from 'vue';
import { ref } from 'vue';

const props = defineProps({
    isAdmin: {
        type: Boolean,
        default: false,
    },
    mapApiKey: {
        type: String,
        default: null,
    },
});

const modal = reactive({
    airport: false,
});
const quotes = [
    'Only the sky is the limit.',
    'As real as it gets.',
    'A next gen virtual airline.',
    'Join us, fly together.',
    'Welcome aboard.',
];

function openAirportModal() {
    modal.airport = true;
}

function getQuote() {
    let index = Math.floor(Math.random() * quotes.length);
    return quotes[index];
}

let test = ref('A');

function doom() {
    test.value = (Math.random() + '')[3];
}
</script>

<template>
    <Navigation></Navigation>
</template>

<style scoped>
body {
    background: white;
}
</style>
