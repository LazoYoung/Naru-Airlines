<script setup lang="ts">
import TextInput from "@/components/input/TextInput.vue";
import { Form, home, useForm } from "@/api/common";
import AuthLayout from "@/components/layout/AuthLayout.vue";

const form: Form = useForm(["email", "password"]);

function onSubmit() {
    form.submitPost("/api/login/").then((response) => {
        if (response.ok) {
            home();
        } else {
            form["password"] = "";
        }
    });
}
</script>

<template>
    <AuthLayout>
        <form class="form-group" @submit.prevent="onSubmit">
            <TextInput
                type="email"
                placeholder="Email"
                v-model="form['email']"
                :message="form.errors['email']"
            />
            <TextInput
                type="password"
                placeholder="Password"
                v-model="form['password']"
                :message="form.errors['password']"
            />
            <div class="actions">
                <RouterLink class="reset-link" :to="{ name: 'reset-password' }">
                    Forgot password?
                </RouterLink>
            </div>
            <button
                class="btn btn-primary"
                type="submit"
                :disabled="form.processing"
            >
                Login
            </button>
        </form>
    </AuthLayout>
</template>

<style scoped>
.form-group .actions {
    display: flex;
    flex-direction: row-reverse;
    font-size: 0.8em;
}

.form-group button {
    margin-top: 1rem;
    font-weight: 600;
}

.form-group {
    display: flex;
    flex-direction: column;
}
</style>
