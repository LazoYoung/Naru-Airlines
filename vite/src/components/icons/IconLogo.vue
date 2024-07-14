<script setup>
const props = defineProps({
    color: {
        type: String,
        default: 'white'
    }
});
</script>

<template>
    <img v-if="props.color === 'white'" src="../../assets/icon.svg" alt="Logo"/>
    <img v-else-if="props.color === 'blue'" src="../../assets/icon.svg" alt="Logo"/>
    <img v-else src="" alt="Logo"/>
</template>
