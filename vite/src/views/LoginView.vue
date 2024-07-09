<script setup>
import {onMounted, ref} from "vue";

const email = ref();
const password = ref();
const button = ref();

async function onClick(event) {
    event.preventDefault();

    let response = await fetch("http://localhost:8000/auth/login/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            'email': email.value,
            'password': password.value,
        })
    });

    if (response.ok) {
        alert("Login success");
    } else {
        alert("Login failed");
    }
}

onMounted(_ => {
    button.value.addEventListener('click', onClick);
});
</script>

<template>
    <form>
        <input type="email" v-model="email" placeholder="E-mail" />
        <input type="password" v-model="password" placeholder="Password" />
        <button ref="button">Login</button>
    </form>
</template>

<style scoped>

</style>