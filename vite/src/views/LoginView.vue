<script setup>
import AuthLayout from "@/components/layout/AuthLayout.vue";
import TextInput from "@/components/TextInput.vue";
import {home, useForm} from "@/api.js";
import InputError from "@/components/InputError.vue";

const form = useForm(['email', 'password']);

function onSubmit() {
    form.post("/api/auth/login/")
        .then(success => {
            if (success) {
                home();
            }
        });
}
</script>

<template>
    <AuthLayout>
        <form @submit.prevent="onSubmit">
            <div>
                <TextInput
                        type="email"
                        v-model="form['email']"
                        hint="E-mail"
                        label="inner"
                        :required="true"
                ></TextInput>
                <InputError :message="form.errors['email']"></InputError>
            </div>
            <div>
                <TextInput
                        type="password"
                        v-model="form['password']"
                        hint="Password"
                        label="inner"
                        :required="true"
                ></TextInput>
                <InputError :message="form.errors['password']"></InputError>
            </div>
            <button filled type="submit" :disabled="form.processing.value">Login</button>
        </form>
    </AuthLayout>
</template>

<style scoped>

</style>
