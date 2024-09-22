<script setup>
import AuthLayout from "@/components/layout/AuthLayout.vue";
import TextInput from "@/components/input/TextInput.vue";
import { useForm } from "@/api/common";
import { ref } from "vue";
import router from "@/router/index";

let form = useForm(["display_name", "email", "password", "confirm_password"]);
let success = ref(false);

function onSubmit() {
    let password = form["password"];
    let confirm_password = form["confirm_password"];

    if (password !== confirm_password) {
        form.setError("confirm_password", "Password does not match.");
        return;
    }

    form.submitPost("/api/register/").then((response) => {
        if (response.ok) {
            sendEmail();
        }
    });
}

function sendEmail() {
    let formData = {
        email: form["email"],
        reason: "register",
    };

    fetch("/api/send-verify-email/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
    }).then((response) => {
        if (response.ok) {
            router.push({ name: "check-email" });
        } else {
            // todo: animate using alert.js
            alert("Internal server error!");
            console.error(response);
        }
    });
}
</script>

<template>
    <AuthLayout>
        <div v-if="success" class="inbox">
            <img src="../assets/envelope.svg" alt="Envelope" width="50px" />
            <p class="title">Check your e-mail inbox.</p>
        </div>
        <form v-else @submit.prevent="onSubmit">
            <section class="input">
                <TextInput
                    v-model="form['display_name']"
                    placeholder="Name"
                    :message="form.errors['display_name']"
                ></TextInput>
                <TextInput
                    v-model="form['email']"
                    type="email"
                    placeholder="E-mail"
                    :message="form.errors['email']"
                ></TextInput>
                <TextInput
                    v-model="form['password']"
                    type="password"
                    placeholder="Password"
                    :message="form.errors['password']"
                ></TextInput>
                <TextInput
                    v-model="form['confirm_password']"
                    type="password"
                    placeholder="Confirm Password"
                    :message="form.errors['confirm_password']"
                ></TextInput>
            </section>
            <button
                class="btn btn-primary"
                type="submit"
                :disabled="form.processing"
            >
                Sign up
            </button>
        </form>
    </AuthLayout>
</template>

<style scoped>
form {
    display: flex;
    flex-direction: column;
    row-gap: 1rem;
}

form > button {
    font-weight: 600;
}

section.input {
    display: flex;
    flex-direction: column;
}
</style>
