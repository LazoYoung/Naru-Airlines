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
            <form class="form-query" @submit.prevent>
                <BFormInput
                        type="search"
                        placeholder="Find by airport or city"
                        autocomplete="off"
                        aria-autocomplete="none"
                ></BFormInput>
            </form>

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
                    <tr @click="selectRow('RKSI')">
                        <td><input type="radio" name="icao" value="RKSI"/></td>
                        <td>RKSI</td>
                        <td>Incheon International</td>
                        <td>Seoul</td>
                    </tr>
                    <tr @click="selectRow('RJAA')">
                        <td><input type="radio" name="icao" value="RJAA"/></td>
                        <td>RJAA</td>
                        <td>Narita International</td>
                        <td>Tokyo</td>
                    </tr>
                    <tr @click="selectRow('KLAX')">
                        <td><input type="radio" name="icao" value="KLAX"/></td>
                        <td>KLAX</td>
                        <td>Los Angeles International</td>
                        <td>California</td>
                    </tr>
                    <tr @click="selectRow('KLAS')">
                        <td><input type="radio" name="icao" value="KLAS"/></td>
                        <td>KLAS</td>
                        <td>Harry Reid International</td>
                        <td>Las Vegas</td>
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
