<script setup>
import AuthLayout from "@/components/layout/AuthLayout.vue";
import TextInput from "@/components/input/TextInput.vue";
import {useForm} from "@/api";
import router from "@/router/index.js";

const form = useForm({
    'email': '',
    'new_password': '',
    'confirm_password': '',
    'reason': 'reset_password',
});

function onSubmit() {
    form.submitPost("/api/send-verify-email/")
        .then(response => {
            if (response.ok) {
                router.push({name: 'check-email'});
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
                        v-model="form['new_password']"
                        hint="New password"
                        :error_message="form.errors['new_password']"
                ></TextInput>
                <TextInput
                        type="password"
                        v-model="form['confirm_password']"
                        hint="Confirm password"
                        :error_message="form.errors['confirm_password']"
                ></TextInput>
            </section>
            <button type="submit" :disabled="form.processing" filled>Reset password</button>
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
</style>
