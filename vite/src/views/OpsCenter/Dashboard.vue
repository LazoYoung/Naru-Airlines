<script setup>
import OpsLayout from "@/components/layout/OpsLayout.vue";
import Notam from "@/components/widget/Notam.vue";
import Stats from "@/components/widget/Stats.vue";
import Roster from "@/components/widget/Roster.vue";
</script>

<template>
    <OpsLayout>
        <template #title>Dashboard</template>

        <div id="grid">
            <div class="card card-lg">
                <h5 class="card-header">Duty Roster</h5>
                <div class="card-body">
                    <Roster></Roster>
                </div>
            </div>

            <div class="card">
                <h5 class="card-header">NOTAM</h5>
                <div class="card-body">
                    <Notam width="20rem"></Notam>
                </div>
            </div>

            <div class="card">
                <h5 class="card-header">Stats</h5>
                <div class="card-body">
                    <Stats></Stats>
                </div>
            </div>

        </div>
    </OpsLayout>
</template>

<style scoped>
#grid {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: start;
    gap: 2rem;
}

.card-body {
    max-height: 500px;
    overflow-y: auto;
}

/* Magic values */

.card-sm {
    width: 15rem;
}

.card-md {
    width: 20rem;
}

.card-lg {
    width: 30rem;
}
</style>
