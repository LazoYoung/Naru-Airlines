<script setup>
import OpsLayout from "@/components/layout/OpsLayout.vue";
import {BFormInput} from "bootstrap-vue-next";

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
    const from = document.querySelector("#from");
    const to = document.querySelector("#to");
    const tmp = from.value;
    from.value = to.value;
    to.value = tmp;

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
            <search id="filter">
                <BForm @submit.prevent>
                    <div id="filter-layout">
                        <BFormFloatingLabel label="From" label-for="from">
                            <BFormInput
                                    id="from"
                                    placeholder="From"
                                    autocomplete="off"
                                    :formatter="toICAO"
                            />
                        </BFormFloatingLabel>
                        <button id="swap" tabindex="-1" @click="swap">
                            <span class="material-symbols-outlined">swap_horizontal_circle</span>
                        </button>
                        <BFormFloatingLabel label="To" label-for="to">
                            <BFormInput
                                    id="to"
                                    placeholder="To"
                                    autocomplete="off"
                                    :formatter="toICAO"
                            />
                        </BFormFloatingLabel>
                    </div>
                </BForm>
            </search>
        </div>
    </OpsLayout>
</template>

<style scoped>
/* Override main.css */
.form-floating>label {
    all: unset;

    //line-height: unset !important;
}
/* ----------------- */

#filter {
    width: fit-content;
    padding: 1.5rem;
    border-radius: 1rem;
    background-color: gray;
}

#filter-layout {
    display: flex;
    flex-direction: row;
    align-items: center;
}

#swap {
    height: fit-content;
    padding: 0.5rem 0.5rem;
    background-color: rgba(0, 0, 0, 0);
}

#swap .material-symbols-outlined {
    color: white;
    font-variation-settings: 'FILL' 1,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24
}
</style>
