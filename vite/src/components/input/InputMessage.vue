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
    <div :class="'message ' + props.type">
        {{ message }}
    </div>
</template>

<style scoped>
.message {
    padding-top: 0.25rem;
    font-size: 0.8rem;
    font-weight: 400;
    line-height: 0.5rem;
    min-height: 1.5rem;
}
.message.info {
    color: rgb(128, 128, 128);
}
.message.error {
    color: rgb(220, 38, 38);
}
</style>
