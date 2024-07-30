<script setup>
const props = defineProps({
    message: {
        type: String,
        default: undefined,
    },
    type: {
        type: String,
        default: 'error',
    },
});
</script>

<template>
    <p :class="'message ' + props.type">
        {{ message }}
    </p>
</template>

<style scoped>
.message {
    padding-top: 0.25rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1rem;
    min-height: 1.25rem;
}
.message.info {
    color: rgb(128, 128, 128);
}
.message.error {
    color: rgb(220, 38, 38);
}
</style>
