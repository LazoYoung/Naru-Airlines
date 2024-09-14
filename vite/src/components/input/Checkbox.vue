<script setup>
import {ref, watch} from 'vue';

const button = ref();
const model = defineModel();
const props = defineProps({
    label: {
        type: String,
        required: true,
    },
    name: {
        type: String,
        required: false,
    },
});

function updateStyle() {
    let checked = model.value;
    let style = button.value.style;
    style.backgroundColor = checked ? "var(--form-input-bg)" : "var(--form-bg)";
}

watch(model, () => {
    updateStyle();
});
</script>

<template>
    <div class="root">
        <div ref="button" class="check-btn"></div>
        <label v-html="props.label"></label>
        <input
                type="checkbox"
                v-model="model"
                :name="props.name"
                @change="updateStyle()"
        >
    </div>
</template>

<style scoped>
div.root {
    display: block;
    position: relative;
    min-height: 1.5rem;
}

input {
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
    background-color: unset;
    opacity: 0;
}

label {
    display: block;
    width: auto;
    min-height: 1.5rem;
    margin-left: 2rem;
    line-height: 1.5rem;
    text-align: left;
    font-weight: 500;
    color: var(--form-input-fg);
}

.check-btn {
    --form-input-bg: dimgray;
    --form-bg: transparent;
    position: absolute;
    top: 0;
    left: 0;
    width: 1.5rem;
    height: 1.5rem;
    border: var(--form-input-bg) solid 2px;
    border-radius: 100%;
    background-color: var(--form-bg);
    transition: background-color 200ms ease-in-out;
}
</style>
