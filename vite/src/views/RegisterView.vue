<script setup>
import AuthLayout from "@/components/layout/AuthLayout.vue";
import TextInput from "@/components/input/TextInput.vue";
import {useForm} from "@/api";
import {ref} from "vue";
import router from "@/router/index.js";

let form = useForm(['display_name', 'email', 'password', 'confirm_password']);
let success = ref(false);

function onSubmit() {
    let password = form['password'];
    let confirm_password = form['confirm_password'];

    if (password !== confirm_password) {
        form.setError("confirm_password", "Password does not match.");
        return;
    }

    form.submitPost("/api/register/")
        .then(response => {
            if (response.ok) {
                sendEmail();
            }
        });
}

function sendEmail() {
    let formData = {
        'email': form['email'],
        'reason': 'register'
    };

    fetch("/api/send-verify-email/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData),
    }).then(response => {
        if (response.ok) {
            router.push({name: 'check-email'});
        } else {
            // todo: animate using alert.js
            alert("Internal server error!");
            console.error(response);
        }
    })
}
</script>

<template>
    <AuthLayout>
        <div v-if="success" class="inbox">
            <img src="../assets/envelope.svg" alt="Envelope" width="50px"/>
            <p class="title">Check your e-mail inbox.</p>
        </div>
        <form v-else @submit.prevent="onSubmit">
            <section class="input">
                <TextInput
                        v-model="form['display_name']"
                        hint="Name"
                        label="inner"
                        :error_message="form.errors['display_name']"
                ></TextInput>
                <TextInput
                        v-model="form['email']"
                        type="email"
                        hint="E-mail"
                        :error_message="form.errors['email']"
                ></TextInput>
                <TextInput
                        v-model="form['password']"
                        type="password"
                        hint="Password"
                        :error_message="form.errors['password']"
                ></TextInput>
                <TextInput
                        v-model="form['confirm_password']"
                        type="password"
                        hint="Confirm Password"
                        :error_message="form.errors['confirm_password']"
                ></TextInput>
            </section>
            <button filled type="submit" :disabled="form.processing">Sign up</button>
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

button {
    box-shadow: black 0.3rem 0.3rem 0.3rem;
}

section.input {
    display: flex;
    flex-direction: column;
    row-gap: 1rem;
}
</style>