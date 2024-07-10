<script setup>
defineProps(['message']);
</script>

<template>
    <div class="box" v-show="message">
        <p class="error">
            {{ message }}
        </p>
    </div>
</template>

<style scoped>
div.box {
    margin-bottom: 0.5rem;
}
p.error {
    font-size: 1rem;
    line-height: 1.25rem;
    color: rgb(220, 38, 38);
}
</style>
