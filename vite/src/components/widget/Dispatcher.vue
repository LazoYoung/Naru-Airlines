<script setup>
import {BNav} from "bootstrap-vue-next";
import {ref} from "vue";

const loadsheet = ref({
    passengerCount: 125,
    cargoPayload: 1800,
    blockFuel: 5100,
});

const tab = ref({
    loadsheet: true,
    ofp: false,
});

function changeTab(key) {
    for (let k in tab.value) {
        tab.value[k] = false;
    }
    tab.value[key] = true;
}
</script>

<template>
    <div id="root">
        <div id="nav-container">
            <BNav underline>
                <BNavItem :active="tab.loadsheet" @click="changeTab('loadsheet')">Loadsheet</BNavItem>
                <BNavItem :active="tab.ofp" @click="changeTab('ofp')">Flightplan</BNavItem>
            </BNav>
        </div>
        <div v-if="tab.loadsheet" id="loadsheet">
            <table class="table">
                <tr>
                    <td class="w-50">Passengers</td>
                    <td>{{ loadsheet.passengerCount }}</td>
                </tr>
                <tr>
                    <td class="w-50">Cargo</td>
                    <td>{{ loadsheet.cargoPayload }} kg</td>
                </tr>
                <tr>
                    <td class="w-50">Block Fuel</td>
                    <td>{{ loadsheet.blockFuel }} kg</td>
                </tr>
            </table>
        </div>
        <div v-else-if="tab.ofp" id="ofp">
            <div class="small">Flightplan is not prepared yet.</div>
        </div>
    </div>
</template>

<style scoped>
#root {
    margin: 0 1rem 1rem;
    width: 20rem;
}

#nav-container {
    margin-bottom: 1rem;
}

#loadsheet {
    display: flex;
    flex-direction: column;
    row-gap: 0.5rem;
}


/* Table */

table {
    width: 100%;
    border-collapse: collapse;
}

td {
    width: 50%;
    padding: 8px;
}
</style>