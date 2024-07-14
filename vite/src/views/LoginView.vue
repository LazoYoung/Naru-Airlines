<script setup>
import AuthLayout from "@/components/layout/AuthLayout.vue";
import TextInput from "@/components/input/TextInput.vue";
import {home, useForm} from "@/api.js";
import Checkbox from "@/components/input/Checkbox.vue";

const form = useForm(['email', 'password']);

function onSubmit() {
    form.submitPost("/api/login/")
        .then(response => {
            if (response.ok) {
                home();
            } else {
                form['password'] = '';
            }
        });
}
</script>

<template>
    <AuthLayout>
        <form @submit.prevent="onSubmit">
            <section class="input">
                <TextInput
                        type="email"
                        v-model="form['email']"
                        hint="E-mail"
                        :error_message="form.errors['email']"
                ></TextInput>
                <TextInput
                        type="password"
                        v-model="form['password']"
                        hint="Password"
                        :error_message="form.errors['password']"
                ></TextInput>
            </section>
            <section class="controls">
                <Checkbox label="Remember me" v-model="form['remember']"></Checkbox>
                <RouterLink class="reset-link" :to="{name: 'reset-password'}">Forgot password?</RouterLink>
            </section>
            <button type="submit" :disabled="form.processing" filled>Login</button>
        </form>
    </AuthLayout>
</template>

<style scoped>
form {
    display: flex;
    flex-direction: column;
    row-gap: 1.5rem;
    padding: 1rem;
}

section.input {
    display: flex;
    flex-direction: column;
    row-gap: 1rem;
}

button {
    box-shadow: black 0.3rem 0.3rem 0.3rem;
}

section.controls {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.reset-link {
    color: aliceblue;
    line-height: 1.5rem;
    font-weight: 300;
    font-size: 1rem;
    text-decoration: underline;
}
</style>
