<script setup>
import OpsLayout from "@/components/layout/OpsLayout.vue";
import {useRoute} from "vue-router";
import {onMounted, ref, watch} from "vue";
import Dispatcher from "@/components/widget/Dispatcher.vue";

const route = useRoute();
const flight = ref({
    number: 'N/A',
    type: 'Routine',
    aircraft: 'A320',
    registration: 'HL7800',
    origin: 'KJFK',
    destination: 'KDTW',
    date: 'Wed, Aug 28',
    eobt: '14:30 UTC',
    eibt: '16:40 UTC',
    status: 'Departed',
});
const flightUpdates = ref([
    {status: 'Flight scheduled', time: 'Aug 28, 03:15 UTC'},
    {status: 'Boarding start', time: 'Aug 28, 03:15 UTC'},
    {status: 'Departed', time: 'Aug 28, 03:15 UTC'},
    {status: 'In flight', time: 'Aug 28, 03:15 UTC'},
    {status: 'Arrived', time: 'Aug 28, 03:15 UTC'},
]);

watch(
    () => route.params['flightNumber'],
    (newValue) => {
        flight.value.number = newValue;
    }
);

onMounted(() => {
    flight.value.number = route.params['flightNumber'];
});
</script>

<template>
    <OpsLayout>
        <template #title>Flight Info</template>
        <template #subtitle>Naru Airlines Flight {{ flight.number }}</template>
        <div class="root">
            <div class="card briefing">
                <h5 class="card-header">Flight Briefing</h5>
                <div class="card-body">
                    <div id="briefing-content">
                        <div id="briefing-header">
                            <svg width="100%" height="70" class="illust">
                                <defs>
                                    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5"
                                            orient="auto">
                                        <polygon points="0 0, 10 3.5, 0 7"/>
                                    </marker>
                                </defs>
                                <text class="icao" x="40" y="20">
                                    {{ flight.origin }}
                                </text>
                                <text class="icao" x="360" y="20">
                                    {{ flight.destination }}
                                </text>
                                <line x1="100" y1="20" x2="280" y2="20" stroke-width="2" marker-end="url(#arrowhead)"/>
                                <text class="time" x="40" y="50">{{ flight.eobt }}</text>
                                <text class="time" x="360" y="50">{{ flight.eibt }}</text>
                                <text class="time" x="195" y="50">{{ flight.date }}</text>
                            </svg>
                        </div>
                        <div id="ident">
                            <div class="subject">Identifier</div>
                            <table class="table">
                                <tr>
                                    <td>Flight number</td>
                                    <td>{{ flight.number }}</td>
                                </tr>
                                <tr>
                                    <td>Flight type</td>
                                    <td>{{ flight.type }}</td>
                                </tr>
                                <tr>
                                    <td>Aircraft</td>
                                    <td>{{ flight.aircraft }}</td>
                                </tr>
                                <tr>
                                    <td>Registration</td>
                                    <td>{{ flight.registration }}</td>
                                </tr>
                            </table>
                        </div>
                        <div id="departure">
                            <div class="subject">Departure</div>
                            <table class="table">
                                <tr>
                                    <td>Date</td>
                                    <td>{{ flight.date }}</td>
                                </tr>
                                <tr>
                                    <td>Time</td>
                                    <td>{{ flight.eobt }}</td>
                                </tr>
                                <tr>
                                    <td>Status</td>
                                    <td>{{ flight.status }}</td>
                                </tr>
                            </table>
                        </div>
<!--                        <div id="tech-log">-->
<!--                            <div class="subject">Technical Log</div>-->
<!--                            <table class="table">-->
<!--                                <tr>-->
<!--                                    <td>{{ flight.technicalLog }}</td>-->
<!--                                </tr>-->
<!--                            </table>-->
<!--                        </div>-->
                        <div class="btn btn-danger">Cancel Flight</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h5 class="card-header">Dispatcher</h5>
                <div class="card-body">
                    <Dispatcher></Dispatcher>
                </div>
            </div>

            <div class="card card-sm">
                <h5 class="card-header">Update</h5>
                <div class="card-body">
                    <div class="timeline">
                        <div class="timeline-item" v-for="(item, index) in flightUpdates" :key="index">
                            <div class="timeline-content">
                                <div class="timeline-status">{{ item.status }}</div>
                                <div class="timeline-time">{{ item.time }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </OpsLayout>
</template>

<style scoped>
.root {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: start;
    gap: 2rem;
}

.card-sm {
    width: 15rem;
}

.briefing {
    width: fit-content;
}

.btn {
    display: block;
    width: 100%;
    margin-bottom: 10px;
}

.timeline {
    position: relative;
    padding-left: 20px;
    margin: 1rem;
}

.timeline-item {
    position: relative;
    margin-bottom: 15px;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -25px;
    top: 5px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #007bff;
}

.timeline-item::after {
    content: '';
    position: absolute;
    left: -21px;
    top: 15px;
    width: 2px;
    height: calc(100% + 10px);
    background-color: #007bff;
}

.timeline-item:last-child::after {
    display: none;
}

.timeline-content {
    display: flex;
    flex-direction: column;
}

.timeline-status {
    font-weight: 600;
}

.timeline-time {
    color: darkslategray;
    font-size: small;
    line-height: normal;
}

#briefing-content {
    display: flex;
    flex-direction: column;
    row-gap: 1rem;
    width: 400px;
    margin: 1rem 1rem;
}

.subject {
    display: block;
    font-size: 1em;
    font-weight: 600;
    margin-bottom: 0.75rem;
}


/* Table */

table {
    width: 100%;
    border-collapse: collapse;
    border-top: 1px solid #ddd;
}

td {
    width: 50%;
    padding: 8px;
    //border-bottom: 1px solid #ddd;
}


/* SVG */

line, marker {
    stroke: black;
}

.icao {
    font-size: 18px;
    font-weight: 800;
    text-anchor: middle;
    alignment-baseline: middle;
}

.time {
    fill: dimgray;
    font-size: 14px;
    text-anchor: middle;
}
</style>
