<script setup>
import OpsLayout from "@/components/layout/OpsLayout.vue";
import {BFormInput} from "bootstrap-vue-next";
import AirportModal from "@/components/modal/AirportModal.vue";
import {onMounted, ref} from "vue";
import AirDatepicker from "air-datepicker";
import 'air-datepicker/air-datepicker.css';
import localeEn from "air-datepicker/locale/en";

const icao_from = ref("");
const icao_to = ref("");
const openModalFrom = ref(false);
const openModalTo = ref(false);

onMounted(() => {
    const dp = new AirDatepicker("#date", {
        multipleDatesSeparator: ' - ',
        range: true,
        inline: false,
        locale: localeEn,
    });
});

function onSelectFrom(icao) {
    if (icao) {
        icao_from.value = icao;
    }
}

function onSelectTo(icao) {
    if (icao) {
        icao_to.value = icao;
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
    const tmp = icao_from.value;
    icao_from.value = icao_to.value;
    icao_to.value = tmp;

    animateSwap();

    // todo: submit form
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

        <div id="root">
            <BForm @submit.prevent>
                <search id="filter">
                    <div id="filter-airport">
                        <BFormFloatingLabel label="Origin" label-for="from">
                            <BFormInput
                                    id="from"
                                    v-model="icao_from"
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
                                    v-model="icao_to"
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
                                    placeholder="Aircraft"
                                    autocomplete="off"
                                    :formatter="toICAO"
                            />
                        </BFormFloatingLabel>
                    </div>
                </search>
            </BForm>
        </div>

        <AirportModal id="modal-from" v-model:visible="openModalFrom" @select="onSelectFrom"></AirportModal>
        <AirportModal id="modal-to" v-model:visible="openModalTo" @select="onSelectTo"></AirportModal>
    </OpsLayout>
</template>

<style scoped>
#filter {
    width: fit-content;
    padding: 1.5rem;
    border-radius: 1rem;
    background-color: gray;
    justify-content: space-between;
}

#filter, #filter > div {
    display: flex;
    flex-direction: row;
    align-items: center;
}

#filter > div:not(:last-child):after {
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
</style>
