<script setup>
defineProps({
    title: {
        type: String,
    }
});
</script>

<template>
    <main>
        <header v-if="title">
            <div class="box">
                <h2 class="title">{{title}}</h2>
            </div>
        </header>
        <div class="content">
            <slot/>
        </div>
    </main>
</template>

<style scoped>
div.content {
    max-width: 64rem;
    margin: 1.5rem auto;
}

header {
    padding-top: 6rem;
}

header > .box {
    max-width: 64rem;
    margin: 0 auto;
    padding: 1.5rem 1rem;
}

header > .box > .title {
    font-size: 1.5rem;
    line-height: 2rem;
    font-weight: 600;
}

@media (min-width: 640px) {
    div.content {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    header > .box {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
}

@media (min-width: 1024px) {
    div.content {
        padding-left: 2rem;
        padding-right: 2rem;
    }
    header > .box {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
}
</style>
