<script setup>
import AuthLayout from "@/components/layout/AuthLayout.vue";
import {useForm} from "@/api.js";
import TextInput from "@/components/TextInput.vue";
import InputError from "@/components/InputError.vue";
import {ref} from "vue";

let form = useForm(['display_name', 'email', 'password']);
let success = ref(false);

function onSubmit() {
    form.post("/api/auth/register/")
        .then(success => {
            if (success) {
                sendEmail();
            }
        });
}

function sendEmail() {
    fetch("api/auth/send-register-email/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({'email': form['email']}),
    }).then(response => {
        if (!response.ok) {
            // todo: animate using alert.js
            alert("Internal server error!");
            console.error(response);
            return;
        }

        success.value = true;
    })
}
</script>

<template>
    <AuthLayout>
        <div v-if="success" class="inbox">
            <img src="../assets/envelope.svg" alt="Envelope" width="50px" />
            <p class="title">Check your e-mail inbox.</p>
        </div>
        <form v-else @submit.prevent="onSubmit">
            <div>
                <TextInput
                        v-model="form['display_name']"
                        hint="Name"
                        label="inner"
                        :required="true"
                ></TextInput>
                <InputError :message="form.errors['display_name']"></InputError>
            </div>
            <div>
                <TextInput
                        v-model="form['email']"
                        type="email"
                        hint="E-mail"
                        label="inner"
                        :required="true"
                ></TextInput>
                <InputError :message="form.errors['email']"></InputError>
            </div>
            <div>
                <TextInput
                        v-model="form['password']"
                        type="password"
                        hint="Password"
                        label="inner"
                        :required="true"
                ></TextInput>
                <InputError :message="form.errors['password']"></InputError>
            </div>
            <button filled type="submit" :disabled="form.processing.value">Sign up</button>
        </form>
    </AuthLayout>
</template>

<style scoped>
div.inbox {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 0;
    row-gap: 1rem;
}
p.title {
    font-size: 1.5rem;
    font-weight: bold;
}
</style>
