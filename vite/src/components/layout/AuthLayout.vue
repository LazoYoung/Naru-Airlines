<script setup>
</script>

<template>
    <main>
        <div id="auth_body">
            <div id="logo">
                <RouterLink :to="{name: 'home'}">
                    <img src="@/assets/icon.png" alt="Naru Airlines Logo">
                </RouterLink>
            </div>

            <slot/>
        </div>
    </main>
</template>

<style scoped>
main {
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

#auth_body {
    width: 60%;
    padding: 1rem 1.5rem 1rem 1.5rem;
    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);
    background-color: white;
}

#logo {
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-bottom: 1rem;
}

#logo img {
    width: 4rem;
}

@media (min-width: 640px) {
    main {
        justify-content: center;
        padding-top: 0;
        background-color: #eeeeee;
    }

    #auth_body {
        max-width: 18rem;
        border-radius: 0.5rem;
    }
}
</style>
