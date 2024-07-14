<script setup lang="ts">
import MainLayout from '@/components/layout/MainLayout.vue';
import TextInput from "@/components/input/TextInput.vue";
import Checkbox from "@/components/input/Checkbox.vue";
import {fetchProfile, Form, useForm} from "@/api.js";
import {onMounted, ref} from "vue";
import Gravatar from "@/components/icons/Gravatar.vue";
import router from "@/router/index.js";
import Alert from "@/alert.js";

const info = new Alert('success');
const warn = new Alert('warn');
const error = new Alert('error');
const profile = ref(null);
const profileForm = useForm([
    'display_name',
    'bio',
]);
const emailForm = useForm({
    'email': '',
    'new_email': '',
    'reason': 'change_email',
});
const passwordForm = useForm([
    'old_password',
    'new_password',
    'confirm_password',
]);
const notificationForm = useForm([
    'receive_emails',
]);

defineProps({
    mustVerifyEmail: {
        type: Boolean,
    },
    status: {
        type: String,
    },
});

onMounted(() => fetchProfile(profile).then(_ => onProfileFetch()));

function saveProfile() {
    let nameChanged = profileForm['display_name'] !== profile.value['display_name'];
    let bioChanged = profileForm['bio'] !== profile.value['bio'];

    if (!nameChanged && !bioChanged) {
        warn.pop("Nothing has changed.");
        return;
    }

    submit(profileForm, 'PUT', '/api/profile/');
}

function savePrivacy() {
    let passwordChanged = passwordForm['new_password'];
    let emailChanged = passwordForm['new_email'] && passwordForm['email'] !== passwordForm['new_email'];

    if (!passwordChanged && !emailChanged) {
        warn.pop("Nothing has changed.");
        return;
    }

    if (passwordChanged) {
        submit(passwordForm, 'POST', '/api/change-password/');
    }

    if (emailChanged) {
        submit(emailForm, 'POST', '/api/send-verify-email/');
    }
}

function saveNotification() {
    submit(notificationForm, 'PUT', '/api/profile/');
}

function onProfileFetch() {
    if (!profile.value) {
        router.push({name: 'login'})
            .then(_ => error.pop("Session expired."));
        return;
    }

    reloadForm();
}

function reloadForm() {
    profileForm.clear();
    profileForm['display_name'] = profile.value['display_name'];
    profileForm['bio'] = profile.value['bio'];

    emailForm.clear();
    emailForm['email'] = profile.value['email'];
    emailForm['new_email'] = profile.value['email'];

    passwordForm.clear();

    notificationForm.clear();
    notificationForm['receive_emails'] = profile.value['receive_emails'];
}

function submit(form: Form, method: string, url: string) {
    form.submit(method, url)
        .then(response => {
            if (response.ok) {
                info.pop("Changes saved.");
            } else {
                error.pop("Changes rejected.");
            }
        });
}
</script>

<template>
    <MainLayout title="Settings">
        <div class="vertical">
            <section class="box">
                <div class="horizontal">
                    <section class="grow">
                        <div class="heading">
                            <p class="title">Profile</p>
                            <p class="subtitle">Express your own identity.</p>
                        </div>
                        <div id="narrow-profile-img">
                            <Gravatar :email="emailForm['email']" :size="300" large></Gravatar>
                        </div>
                        <form id="profile-form" @submit.prevent="saveProfile">
                            <TextInput
                                    v-model="profileForm['display_name']"
                                    :error_message="profileForm.errors['display_name']"
                                    hint="Name"
                                    label="top"
                                    fixed_label
                            ></TextInput>
                            <TextInput
                                    v-model="profileForm['bio']"
                                    :error_message="profileForm.errors['bio']"
                                    :required="false"
                                    hint="Bio"
                                    label="top"
                                    fixed_label
                            ></TextInput>
                        </form>
                        <div>
                            <button
                                    type="submit"
                                    form="profile-form"
                                    :disabled="profileForm.processing"
                                    small filled
                            >
                                Save
                            </button>
                        </div>
                    </section>
                    <div id="wide-profile-img">
                        <Gravatar :email="emailForm['email']" :size="300" large></Gravatar>
                    </div>
                </div>
            </section>
            <div class="wide-horizontal">
                <section class="box">
                    <div class="heading">
                        <p class="title">Privacy</p>
                        <p class="subtitle">Manage your account credentials.</p>
                    </div>
                    <form id="privacy-form" @submit.prevent="savePrivacy">
                        <TextInput
                                v-model="emailForm['new_email']"
                                :error_message="emailForm.errors['new_email']"
                                hint="E-mail"
                                label="top"
                                type="email"
                                fixed_label
                        />
                        <TextInput
                                v-model="passwordForm['old_password']"
                                :error_message="passwordForm.errors['old_password']"
                                :required="false"
                                hint="Current Password"
                                label="top"
                                type="password"
                                small fixed_label
                        />
                        <TextInput
                                v-model="passwordForm['new_password']"
                                :error_message="passwordForm.errors['new_password']"
                                :required="false"
                                hint="New Password"
                                label="top"
                                type="password"
                                small fixed_label
                        />
                        <TextInput
                                v-model="passwordForm['confirm_password']"
                                :error_message="passwordForm.errors['confirm_password']"
                                :required="false"
                                hint="Confirm Password"
                                label="top"
                                type="password"
                                small fixed_label
                        />
                    </form>
                    <div>
                        <button
                                type="submit"
                                form="privacy-form"
                                :disabled="emailForm.processing || passwordForm.processing"
                                small filled
                        >
                            Save
                        </button>
                    </div>
                </section>
                <div class="pillar-x-2"></div>
                <section class="box">
                    <div class="heading">
                        <p class="title">Notification</p>
                        <p class="subtitle">Decide how you like to be notified.</p>
                    </div>
                    <form id="notification-form" @submit.prevent="saveNotification">
                        <Checkbox label="Receive e-mails" v-model="notificationForm['receive_emails']"/>
                    </form>
                    <div class="wide-grow"/>
                    <div>
                        <button
                                type="submit"
                                form="notification-form"
                                :disabled="notificationForm.processing"
                                small filled
                        >
                            Save
                        </button>
                    </div>
                </section>
            </div>
        </div>
    </MainLayout>
</template>

<style scoped>
div.vertical {
    display: flex;
    flex-direction: column;
}

div.horizontal {
    display: flex;
    flex-direction: row;
    justify-content: stretch;
}

div.wide-horizontal {
    display: flex;
    flex-direction: column;
    justify-content: stretch;
}

div.wide-horizontal > section {
    flex-grow: 1;
}

div.pillar-x-2 {
    visibility: hidden;
    width: 2rem;
}

.grow {
    flex-grow: 1;
}

.wide-grow {
    flex-grow: 0;
}

#profile-form {
    flex-grow: 1;
}

#wide-profile-img {
    display: none;
    margin-left: 6rem;
    width: 300px;
    height: 300px;
}

#narrow-profile-img {
    display: block;
    width: 300px;
    height: 300px;
}

section {
    display: flex;
    flex-direction: column;
    row-gap: 2rem;
}

section.box {
    background-color: dimgray;
    box-shadow: rgb(0, 0, 0, 70%) 0.5rem 0.5rem 0.5rem;
    padding: 2rem;
    margin-bottom: 2rem;
}

form {
    display: flex;
    flex-direction: column;
    row-gap: 1rem;
}

button {
    box-shadow: rgb(0, 0, 0, 50%) 0.2rem 0.2rem 0.2rem;
}

.heading > .title {
    color: aliceblue;
    font-size: 1.4rem;
    padding-bottom: 0.5rem;
}

.heading > .subtitle {
    color: darkgray;
    font-size: 1rem;
}

input[type="checkbox"] {
    width: 1rem;
    height: 1rem;
}

@media (min-width: 800px) {
    #wide-profile-img {
        display: block;
    }

    #narrow-profile-img {
        display: none;
    }
}

@media (min-width: 1200px) {
    section {
        border-radius: 0.5rem;
    }

    .wide-grow {
        flex-grow: 1;
    }

    div.wide-horizontal {
        display: flex !important;
        flex-direction: row !important;
        justify-content: stretch !important;
    }
}
</style>
