<script setup>
import MainLayout from '@/components/layout/MainLayout.vue';
// import DeleteUserForm from './Partials/DeleteUserForm.vue';
// import UpdatePasswordForm from './Partials/UpdatePasswordForm.vue';
// import UpdateProfileInformationForm from './Partials/UpdateProfileInformationForm.vue';
// import APIKeyForm from "@/Pages/Profile/Partials/APIKeyForm.vue";
// import SimbriefForm from "@/Pages/Profile/Partials/SimbriefForm.vue";

defineProps({
    mustVerifyEmail: {
        type: Boolean,
    },
    status: {
        type: String,
    },
});
</script>

<template>
    <MainLayout title="Profile">
        <p>Test</p>
<!--        <div class="max-w-5xl mx-auto sm:px-6 lg:px-8 space-y-6">-->
<!--            <div class="p-8 bg-gray-400 shadow sm:rounded-lg">-->
<!--                <UpdateProfileInformationForm-->
<!--                    :must-verify-email="mustVerifyEmail"-->
<!--                    :status="status"-->
<!--                />-->
<!--            </div>-->

<!--            <div class="p-8 bg-gray-400 shadow sm:rounded-lg">-->
<!--                <APIKeyForm class="max-w-lg" />-->
<!--            </div>-->

<!--            <div class="p-8 bg-gray-400 shadow sm:rounded-lg">-->
<!--                <SimbriefForm class="max-w-lg" />-->
<!--            </div>-->

<!--            <div class="p-8 bg-gray-400 shadow sm:rounded-lg">-->
<!--                <UpdatePasswordForm class="max-w-lg" />-->
<!--            </div>-->

<!--            <div class="p-8 bg-gray-400 shadow sm:rounded-lg">-->
<!--                <DeleteUserForm class="max-w-lg" />-->
<!--            </div>-->
<!--        </div>-->
    </MainLayout>
</template>
