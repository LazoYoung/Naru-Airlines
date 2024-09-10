<script setup>
import OpsLayout from "@/components/layout/OpsLayout.vue";
import {BFormInput} from "bootstrap-vue-next";
import AirportModal from "@/components/modal/AirportModal.vue";
import {onMounted, reactive, ref, watch} from "vue";
import AirDatepicker from "air-datepicker";
import 'air-datepicker/air-datepicker.css';
import localeEn from "air-datepicker/locale/en";

class Route {
    constructor(flt_num, origin, dest, etd, block_time, acf, reg, available = true) {
        this.flight_number = flt_num;
        this.origin = origin;
        this.dest = dest;
        this.aircraft = acf;
        this.registration = reg;
        this.available = available;

        let dep_date = this.toZuluDate(etd);
        let deltaTime = block_time * 60 * 1000;
        let arr_date = new Date(dep_date.getTime() + deltaTime)
        this.dep_zulu = this.formatTime(dep_date) + "z";
        this.arr_zulu = this.formatTime(arr_date) + "z";
        this.date = dep_date.toLocaleString(undefined, {
            timeZone: "UTC",
            month: "short",
            day: "numeric",
        });

        if (dep_date.getUTCDay() !== arr_date.getUTCDay()) {
            this.extra_day = "+1 day";
        } else {
            this.extra_day = "";
        }
    }

    formatTime(date, utc = true) {
        let hours = utc ? date.getUTCHours() : date.getHours();
        let minutes = utc ? date.getUTCMinutes() : date.getMinutes();
        let hh = hours.toString().padStart(2, '0');
        let mm = minutes.toString().padStart(2, '0');
        return `${hh}:${mm}`;
    }

    toZuluDate(string) {
        let zulu_time = new Date(string).toISOString();
        return new Date(zulu_time);
    }
}

const filters = reactive({
    departure_airport: "",
    arrival_airport: "",
    date_from: "",
    date_to: "",
    aircraft: "",
});
const openModalFrom = ref(false);
const openModalTo = ref(false);
const routes = ref([]);

onMounted(() => {
    const dp = new AirDatepicker("#date", {
        multipleDatesSeparator: ' ~ ',
        range: true,
        inline: false,
        locale: localeEn,
        dateFormat: "yyyy-MM-dd",
        onSelect: (value) => {
            console.log(value);
            let date = value.formattedDate;
            filters.date_from = date[0];

            if (date[1]) {
                filters.date_to = date[1];
            } else {
                filters.date_to = filters.date_from;
            }
        },
    });

    fetchRoutes();
});

watch(filters, (value) => fetchRoutes());

async function fetchRoutes() {
    const url = new URL("/api/schedule/", document.location.origin);

    for (let key in filters) {
        let value = filters[key];

        if (value) {
            url.searchParams.append(key, value);
        }
    }

    const response = await fetch(url);

    if (!response.ok) return;

    const json = await response.json();
    routes.value = [];

    for (const data of json) {
        const aircraft = data["aircraft"];
        const route = new Route(
            data["flight_number"],
            data["departure_airport"],
            data["arrival_airport"],
            data["departure_time"],
            data["block_time"],
            aircraft["icao_code"],
            aircraft["registration"],
            data["is_occupied"]
        );
        routes.value.push(route);
    }
}

function onSelectFrom(icao) {
    if (icao) {
        filters.departure_airport = icao;
    }
}

function onSelectTo(icao) {
    if (icao) {
        filters.arrival_airport = icao;
    }
}

function toICAO(value, event) {
    let result;

    if (value.length > 4) {
        result = value.substring(0, 4);
        event.target.value = result;
    } else {
        result = value.toUpperCase();
    }
    return result;
}

function swap() {
    const tmp = filters.departure_airport;
    filters.departure_airport = filters.arrival_airport;
    filters.arrival_airport = tmp;

    animateSwap();
}

function animateSwap() {
    const button = document.querySelector("#swap");
    const keyframes = [
        {transform: "rotate(180deg)"},
    ];
    const options = {
        duration: 200,
        iterations: 1,
    };
    button.animate(keyframes, options);
}
</script>

<template>
    <OpsLayout>
        <template #title>Flight Routes</template>
        <template #subtitle>Choose a route to schedule a new flight.</template>

        <div class="root">
            <div id="filters">
                <div id="filter-airport">
                    <BFormFloatingLabel label="Origin" label-for="from">
                        <BFormInput
                                id="from"
                                v-model="filters.departure_airport"
                                placeholder="Origin"
                                autocomplete="off"
                                :formatter="toICAO"
                        />
                        <button class="finder" tabindex="-1" @click="openModalFrom = true">
                            <span class="material-symbols-outlined">search</span>
                        </button>
                    </BFormFloatingLabel>
                    <button id="swap" tabindex="-1" @click="swap">
                        <span class="material-symbols-outlined">swap_horizontal_circle</span>
                    </button>
                    <BFormFloatingLabel label="Destination" label-for="to">
                        <BFormInput
                                id="to"
                                v-model="filters.arrival_airport"
                                placeholder="Destination"
                                autocomplete="off"
                                :formatter="toICAO"
                        />
                        <button class="finder" tabindex="-1" @click="openModalTo = true">
                            <span class="material-symbols-outlined">search</span>
                        </button>
                    </BFormFloatingLabel>
                </div>
                <div id="filter-date">
                    <BFormFloatingLabel label="Date" label-for="date">
                        <BFormInput
                                id="date"
                                placeholder="Date"
                                autocomplete="off"
                        />
                    </BFormFloatingLabel>
                </div>
                <div id="filter-aircraft">
                    <BFormFloatingLabel label="Aircraft" label-for="aircraft">
                        <BFormInput
                                id="aircraft"
                                v-model="filters.aircraft"
                                placeholder="Aircraft"
                                autocomplete="off"
                                :formatter="toICAO"
                        />
                    </BFormFloatingLabel>
                </div>
            </div>

            <div id="routes">
                <div v-for="route in routes" class="card">
                    <div class="top">
                        <div class="ident">
                            <img class="icon" src="@/assets/icon_invert.png" alt="Icon"/>
                            <span class="flt-num">{{ "NR" + route.flight_number }}</span>
                        </div>
                        <div class="badges">
                            <span class="badge rounded-pill text-bg-dark">{{ route.aircraft }}</span>
                            <span class="badge rounded-pill text-bg-dark">{{ route.registration }}</span>
                            <span v-if="route.available" class="badge rounded-pill text-bg-success">Available</span>
                            <span v-else class="badge rounded-pill text-bg-danger">Occupied</span>
                        </div>
                    </div>
                    <div class="middle">
                        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
                            <text x="20%" y="40%" class="icao">{{ route.origin }}</text>
                            <text x="80%" y="40%" class="icao">{{ route.dest }}</text>
                            <text x="20%" y="60%" class="time">{{ route.dep_zulu }}</text>
                            <text x="80%" y="60%" class="time">{{ route.arr_zulu }}</text>
                            <text x="50%" y="60%" class="date">{{ route.date }}</text>
                            <text x="50%" y="20%" class="extra">{{ route.extra_day }}</text>
                            <line x1="35%" y1="40%" x2="65%" y2="40%" stroke="dimgray" stroke-dasharray="4 2"/>
                            <svg fill="#000000" x="0" y="0" width="100%" height="100%"
                                 viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
                                <g class="plane" transform="scale(0.12) translate(0 -420)">
                                    <path d="M186.62,464H160a16,16,0,0,1-14.57-22.6l64.46-142.25L113.1,297,77.8,339.77C71.07,348.23,65.7,352,52,352H34.08a17.66,17.66,0,0,1-14.7-7.06c-2.38-3.21-4.72-8.65-2.44-16.41l19.82-71c.15-.53.33-1.06.53-1.58a.38.38,0,0,0,0-.15,14.82,14.82,0,0,1-.53-1.59L16.92,182.76c-2.15-7.61.2-12.93,2.56-16.06a16.83,16.83,0,0,1,13.6-6.7H52c10.23,0,20.16,4.59,26,12l34.57,42.05,97.32-1.44-64.44-142A16,16,0,0,1,160,48h26.91a25,25,0,0,1,19.35,9.8l125.05,152,57.77-1.52c4.23-.23,15.95-.31,18.66-.31C463,208,496,225.94,496,256c0,9.46-3.78,27-29.07,38.16-14.93,6.6-34.85,9.94-59.21,9.94-2.68,0-14.37-.08-18.66-.31l-57.76-1.54-125.36,152A25,25,0,0,1,186.62,464Z"/>
                                </g>
                            </svg>
                            <circle fill="none" stroke="dimgray" stroke-width="2px" cx="35%" cy="40%" r="2%"></circle>
                            <circle fill="dimgray" cx="35%" cy="40%" r="1%"></circle>
                            <circle fill="none" stroke="dimgray" stroke-width="2px" cx="65%" cy="40%" r="2%"></circle>
                            <circle fill="dimgray" cx="65%" cy="40%" r="1%"></circle>
                        </svg>
                    </div>
                    <div class="bottom">
                        <button type="button" class="btn btn-primary w-50 m-auto">Select Flight</button>
                    </div>
                </div>
            </div>
        </div>

        <AirportModal id="modal-from" v-model:visible="openModalFrom" @select="onSelectFrom"></AirportModal>
        <AirportModal id="modal-to" v-model:visible="openModalTo" @select="onSelectTo"></AirportModal>
    </OpsLayout>
</template>

<style scoped>
svg > text {
    text-anchor: middle;
    alignment-baseline: middle;
}

svg > .icao {
    font-size: 1.5em;
    font-weight: 600;
}

svg > .time {
    fill: #424242;
    font-size: 1em;
    font-weight: 600;
}

svg > .date {
    fill: #424242;
    font-size: 1em;
    font-weight: 600;
}

svg > .extra {
    fill: dimgray;
    font-size: 0.8em;
    font-weight: 500;
}

svg > .plane {
    transform-origin: center;
}

.root {
    display: flex;
    flex-direction: column;
    row-gap: 2rem;
}

#filters {
    width: fit-content;
    padding: 1.5rem;
    border-radius: 1rem;
    background-color: #afafaf;
    justify-content: space-between;
}

#filters, #filters > div {
    display: flex;
    flex-direction: row;
    align-items: center;
}

#filters > div:not(:last-child):after {
    content: "";
    border: 1px solid white;
    height: 3rem;
    margin: 0 1.5rem;
}

#from, #to, #aircraft {
    width: 9rem;
}

#date {
    width: 14rem;
}

.finder {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    padding: 1rem 0.75rem;
    z-index: 3;
    background: transparent;
    cursor: pointer;
}

#swap {
    height: fit-content;
    padding: 0.5rem 0.5rem;
    background-color: rgba(0, 0, 0, 0);
}

#swap .material-symbols-outlined {
    color: white;
    vertical-align: top;
    font-variation-settings: 'FILL' 1,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24
}

#routes {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 1rem;
    align-items: start;
    width: fit-content;
}

@media screen and (max-width: 1200px) {
    #routes {
        grid-template-columns: 1fr;
    }
}

#routes > .card {
    background-color: white;
    max-width: 26rem;
    padding: 1rem;
    border-radius: 1rem;
}

.card > .top {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.card > .top > .ident {
    display: flex;
    flex-direction: row;
    column-gap: 0.5rem;
}

.card > .top > .ident > .icon {
    width: 1.75rem;
    height: 1.75rem;
    border-radius: 2rem;
}

.card > .top > .ident > .flt-num {
    font-size: 1.3em;
    font-weight: 600;
}

.card > .middle {
    width: 24rem;
    height: 8rem;
}

.card > .bottom {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: end;
}

.dash-top {
    border-top: 2px groove lightgray;
    padding-top: 1rem;
}

.dash-bottom {
    border-bottom: 2px groove lightgray;
    padding-bottom: 1rem;
}

.card .badges {
    display: flex;
    flex-direction: row;
    column-gap: 0.5rem;
}
</style>
