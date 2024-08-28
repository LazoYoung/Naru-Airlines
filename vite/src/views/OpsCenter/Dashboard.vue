<script setup>
import OpsLayout from "@/components/layout/OpsLayout.vue";
import Notam from "@/components/widget/Notam.vue";
import Stats from "@/components/widget/Stats.vue";
import Roster from "@/components/widget/Roster.vue";

// todo: fetch data from server
</script>

<template>
    <OpsLayout>
        <template #title>Dashboard</template>

        <div id="grid">
            <!--            <div class="card card-lg">-->
            <!--                <h5 class="card-header">Roster</h5>-->
            <!--                <div class="card-body">-->
            <!--                    <table class="table table-hover">-->
            <!--                        <thead>-->
            <!--                        <tr>-->
            <!--                            <th scope="col">Flight #</th>-->
            <!--                            <th scope="col">From</th>-->
            <!--                            <th scope="col">To</th>-->
            <!--                            <th scope="col">Departs In</th>-->
            <!--                        </tr>-->
            <!--                        </thead>-->
            <!--                        <tbody class="table-group-divider">-->
            <!--                        <tr>-->
            <!--                            <th scope="row">NR101</th>-->
            <!--                            <td>RKSI</td>-->
            <!--                            <td>RJAA</td>-->
            <!--                            <td>50 minutes</td>-->
            <!--                        </tr>-->
            <!--                        <tr>-->
            <!--                            <th scope="row">NR102</th>-->
            <!--                            <td>RJAA</td>-->
            <!--                            <td>KLAX</td>-->
            <!--                            <td>2 days</td>-->
            <!--                        </tr>-->
            <!--                        <tr>-->
            <!--                            <th scope="row">NR103</th>-->
            <!--                            <td>KLAX</td>-->
            <!--                            <td>KLAS</td>-->
            <!--                            <td>4 days</td>-->
            <!--                        </tr>-->
            <!--                        </tbody>-->
            <!--                    </table>-->
            <!--                    <div class="d-flex justify-content-between align-items-center">-->
            <!--                        <small>These are the flights you need to fly.</small>-->
            <!--                        <a href="#" class="btn btn-sm btn-primary">Manage</a>-->
            <!--                    </div>-->
            <!--                </div>-->
            <!--            </div>-->

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
    gap: 1rem 1rem;
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
