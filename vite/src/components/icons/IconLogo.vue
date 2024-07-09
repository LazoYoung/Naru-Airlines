<script setup>
import {computed} from "vue";

const props = defineProps({
    color: {
        type: String,
        default: 'white'
    }
});
const getImageSource = computed(() => {
    switch (props.color) {
        case 'white':
            return '/static/icon.svg'
        case 'blue':
            return '/static/icon_blue.svg'
        default:
            return '';
    }
})
</script>

<template>
    <img :src="getImageSource" alt="Logo"/>
</template>
