<script setup lang="ts">
import MainLayout from "@/components/layout/MainLayout.vue";
</script>

<template>
    <MainLayout>
        <div class="inbox">
            <img src="../assets/envelope.svg" alt="Envelope" width="50px"/>
            <p class="title">Check your e-mail inbox.</p>
        </div>
    </MainLayout>
</template>

<style scoped>
div.inbox {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10rem 0;
    row-gap: 1rem;
    max-width: 100vw;
    border-radius: 0;
    background-color: gray;
}

p.title {
    font-size: 1.5rem;
    font-weight: bold;
}

@media (min-width: 640px) {
    div.inbox {
        max-width: 100%;
        border-radius: 1rem;
    }
}
</style>
