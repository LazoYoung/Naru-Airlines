<script setup>
import Modal from "@/components/modal/Modal.vue";
import {BFormInput} from "bootstrap-vue-next";
import {ref} from "vue";

const visible = defineModel("visible", {
    type: Boolean,
    default: false
});

const emit = defineEmits(['select']);

const props = defineProps({
    id: {
        type: String,
        required: true,
    },
    useIcao: {
        type: Boolean,
        default: true,
    },
});

const airports = ref([
    {icao: "RKSI", airport: "Incheon International", city: "Seoul"},
    {icao: "RJAA", airport: "Narita International", city: "Tokyo"},
    {icao: "KLAX", airport: "Los Angeles International", city: "California"},
    {icao: "KLAS", airport: "Harry Reid International", city: "Las Vegas"},
]);

const formTable = ref();
const canSubmit = ref(false);

function selectRow(icao) {
    const form = formTable.value;
    const radios = form.elements["icao"];
    radios.value = icao;
    canSubmit.value = true;
}

function getICAO() {
    const id = props.id;
    const radio = document.querySelector(`#${id} input[name=icao]:checked`);
    return radio ? radio.value : null;
}

function submit() {
    const icao = getICAO();

    if (icao) {
        emit('select', icao);
        visible.value = false;
    }
}
</script>

<template>
    <Modal :id="props.id" v-model:visible="visible">
        <template #title>Airport finder</template>
        <div class="content">
            <div class="search">
                <span class="material-symbols-outlined">search</span>
                <form class="form-query" @submit.prevent>
                    <BFormInput
                            type="search"
                            placeholder="Find by airport or city"
                            autocomplete="off"
                            aria-autocomplete="none"
                    ></BFormInput>
                </form>
            </div>

            <form ref="formTable">
                <table class="table">
                    <thead>
                    <tr class="table-dark">
                        <th scope="col"></th>
                        <th scope="col">ICAO</th>
                        <th scope="col">Airport</th>
                        <th scope="col">City</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-if="airports.length === 0">
                        <td colspan="4" class="text-center">No matches found.</td>
                    </tr>
                    <tr v-else v-for="data in airports" @click="selectRow(`${data.icao}`)">
                        <td><input type="radio" name="icao" :value="data.icao"/></td>
                        <td>{{ data.icao }}</td>
                        <td>{{ data.airport }}</td>
                        <td>{{ data.city }}</td>
                    </tr>
                    </tbody>
                </table>
            </form>

            <div class="footer">
                <BButton variant="primary" @click="submit" :disabled="!canSubmit">Select</BButton>
            </div>
        </div>
    </Modal>
</template>

<style scoped>
.content {
    padding: 1rem 2rem;
}

.search {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.search > span {
    background: white;
    border-radius: 1rem;
    width: 2rem;
    height: 2rem;
    line-height: 2rem;
    text-align: center;
    cursor: default;
    user-select: none;
}

.footer {
    display: flex;
    flex-direction: row;
    justify-content: center;
}

.table {
    margin: 1rem 0;
}

.table > tbody > tr, input {
    cursor: pointer;
}

th, td {
    user-select: none;
    font-weight: normal;
}
</style>
