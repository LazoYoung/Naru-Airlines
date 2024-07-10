<script setup>
import Logo from "@/components/icons/IconLogo.vue";
</script>

<template>
    <main>
        <div>
            <RouterLink :to="{name: 'home'}">
                <Logo id="auth_logo" />
            </RouterLink>
        </div>

        <div id="auth_body">
            <slot />
        </div>
    </main>
</template>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding-top: 3rem;
    background-color: rgb(0, 0, 0);
}
#auth_body {
    width: 100%;
    margin-top: 1.5rem;
    padding: 1rem 1.5rem 1rem 1.5rem;
    background-color: var(--form-bg);
    overflow: hidden;
}
#auth_logo {
    width: 6rem;
    height: 6rem;
    fill: currentColor;
}
@media (min-width: 640px) {
    main {
        justify-content: center;
        padding-top: 0;
    }
    #auth_body {
        max-width: 28rem;
        border-radius: 0.5rem;
    }
}
</style>
