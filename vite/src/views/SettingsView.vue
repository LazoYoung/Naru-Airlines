<script setup lang="ts">
import MainLayout from "@/components/layout/MainLayout.vue";
import TextInput from "@/components/input/TextInput.vue";
import TextArea from "@/components/input/TextArea.vue";
import Checkbox from "@/components/input/Checkbox.vue";
import NeoButton from "@/components/input/NeoButton.vue";
import { fetchProfile, Form, Profile, useForm } from "@/api/common";
import { onMounted, ref } from "vue";
import Gravatar from "@/components/icon/Gravatar.vue";
import router from "@/router/index";
import Alert from "@/api/alert.js";

const info = new Alert("success");
const warn = new Alert("warn");
const error = new Alert("error");
const profile = ref<Profile | undefined>();
const profileForm = useForm(["display_name", "bio"]);
const emailForm = useForm({
    email: "",
    new_email: "",
    reason: "change_email",
});
const passwordForm = useForm([
    "old_password",
    "new_password",
    "confirm_password",
]);
const notificationForm = useForm(["receive_emails"]);

defineProps({
    mustVerifyEmail: {
        type: Boolean,
    },
    status: {
        type: String,
    },
});

onMounted(() => fetchProfile(profile).then(() => onProfileFetch()));

async function saveProfile() {
    await fetchProfile(profile);

    if (profile.value == undefined) {
        error.pop("Bad response from server.");
        return;
    }

    let nameChanged =
        profileForm["display_name"] !== profile.value["display_name"];
    let bioChanged = profileForm["bio"] !== profile.value["bio"];

    if (!nameChanged && !bioChanged) {
        warn.pop("Nothing has changed.");
        return;
    }

    submitChanges(profileForm, "PUT", "/api/profile/");
}

async function savePrivacy() {
    await fetchProfile(profile);

    if (profile.value == undefined) {
        error.pop("Bad response from server.");
        return;
    }

    let passwordChanged = passwordForm["new_password"];
    let emailChanged = emailForm["new_email"] !== profile.value["email"];

    if (!passwordChanged && !emailChanged) {
        warn.pop("Nothing has changed.");
        return;
    }

    if (passwordChanged) {
        submitChanges(passwordForm, "POST", "/api/change-password/");
    }

    if (emailChanged) {
        submitChanges(
            emailForm,
            "POST",
            "/api/send-verify-email/",
            "E-mail sent!"
        );
    }
}

function saveNotification() {
    submitChanges(notificationForm, "PUT", "/api/profile/");
}

function onProfileFetch() {
    if (profile.value == undefined) {
        router
            .push({ name: "login" })
            .then(() => error.pop("Session expired."));
        return;
    }

    reloadForm();
}

function reloadForm() {
    if (profile.value == undefined) return;

    profileForm["display_name"] = profile.value["display_name"];
    profileForm["bio"] = profile.value["bio"];
    emailForm["email"] = profile.value["email"];
    emailForm["new_email"] = profile.value["email"];
    notificationForm["receive_emails"] = profile.value["receive_emails"];
    passwordForm.clear();
}

function submitChanges(
    form: Form,
    method: string,
    url: string,
    ok_message = "Changes saved!",
    fail_message = "Changes rejected."
) {
    form.submit(method, url).then((response) => {
        if (response.ok) {
            info.pop(ok_message);
        } else {
            error.pop(fail_message);
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
                            <div class="title">Profile</div>
                            <div class="subtitle">
                                Express your own identity.
                            </div>
                        </div>
                        <div id="narrow-profile-img">
                            <Gravatar
                                :email="emailForm['email']"
                                :size="300"
                                tabindex="-1"
                                large
                            ></Gravatar>
                        </div>
                        <form id="profile-form" @submit.prevent="saveProfile">
                            <TextInput
                                v-model="profileForm['display_name']"
                                :message="profileForm.errors['display_name']"
                                placeholder="Name"
                                label="Name"
                            ></TextInput>
                            <TextArea
                                optional
                                v-model="profileForm['bio']"
                                :message="profileForm.errors['bio']"
                                placeholder="Bio"
                                label="Bio"
                            ></TextArea>
                        </form>
                        <div>
                            <NeoButton
                                form="profile-form"
                                :disabled="profileForm.processing"
                            >
                                Save
                            </NeoButton>
                        </div>
                    </section>
                    <div id="wide-profile-img">
                        <Gravatar
                            :email="emailForm['email']"
                            :size="300"
                            large
                        ></Gravatar>
                    </div>
                </div>
            </section>
            <div class="wide-horizontal">
                <section class="box">
                    <div class="heading">
                        <div class="title">Privacy</div>
                        <div class="subtitle">
                            Manage your account credentials.
                        </div>
                    </div>
                    <form id="privacy-form" @submit.prevent="savePrivacy">
                        <TextInput
                            v-model="emailForm['new_email']"
                            :message="emailForm.errors['new_email']"
                            placeholder="E-mail"
                            label="E-mail"
                            type="email"
                        />
                        <TextInput
                            optional
                            v-model="passwordForm['old_password']"
                            :message="passwordForm.errors['old_password']"
                            placeholder="Current Password"
                            label="Password"
                            type="password"
                        />
                        <TextInput
                            optional
                            v-model="passwordForm['new_password']"
                            :message="passwordForm.errors['new_password']"
                            placeholder="New Password"
                            type="password"
                        />
                        <TextInput
                            optional
                            v-model="passwordForm['confirm_password']"
                            :message="passwordForm.errors['confirm_password']"
                            placeholder="Confirm Password"
                            type="password"
                        />
                    </form>
                    <div>
                        <NeoButton
                            form="privacy-form"
                            :disabled="
                                emailForm.processing || passwordForm.processing
                            "
                        >
                            Save
                        </NeoButton>
                    </div>
                </section>
                <div class="pillar-x-2"></div>
                <section class="box">
                    <div class="heading">
                        <div class="title">Notification</div>
                        <div class="subtitle">
                            Decide how you like to be notified.
                        </div>
                    </div>
                    <form
                        id="notification-form"
                        @submit.prevent="saveNotification"
                    >
                        <Checkbox
                            label="Receive e-mails"
                            v-model="notificationForm['receive_emails']"
                        />
                    </form>
                    <div class="wide-grow" />
                    <div>
                        <NeoButton
                            type="submit"
                            form="notification-form"
                            :disabled="notificationForm.processing"
                        >
                            Save
                        </NeoButton>
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
    background-color: #eeeeee;
    border: lightgray solid 2px;
    box-shadow: rgb(0, 0, 0, 70%) 0.5rem 0.5rem 0.5rem;
    padding: 2rem;
    margin-bottom: 2rem;
}

form {
    display: flex;
    flex-direction: column;
}

.heading > .title {
    color: black;
    font-size: 1.4rem;
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
