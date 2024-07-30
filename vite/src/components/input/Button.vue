<script setup>
import { onMounted, ref, watch } from 'vue';
import InputMessage from '@/components/input/InputMessage.vue';

const props = defineProps({
    type: {
        type: String,
        default: 'lined',
    },
    color: {
        type: String,
        default: 'white',
    },
    value: {
        type: String,
        default: '',
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    form: {
        type: String,
    },
});
const model = defineModel();
const button = ref();

defineExpose({
    focus: () => button.value.focus(),
    blur: () => button.value.blur(),
});
</script>

<template>
    <button
        :form="props.form"
        :disabled="disabled"
        :class="type + ' ' + color"
        ref="button"
    >
        <slot></slot>
    </button>
</template>

<style>
button {
    height: 2.5rem;
    padding: 0 2rem;
    font-size: 1rem;
    font-weight: 600;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 0.75rem;
    cursor: pointer;
}
button:hover,
button:focus,
button:active {
    background: rgb(60, 60, 60);
}
button:focus-visible {
    outline-offset: 0.25rem;
    outline: solid 0.1rem black;
}
button:disabled {
    color: rgb(230, 230, 230);
    background: rgb(180, 180, 180);
    cursor: not-allowed;
}
button.shadowd {
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
}
button.lined {
    border-width: 1px;
    border-style: solid;
}
button.lined.white {
    background: rgb(240, 240, 240);
    border-color: rgb(210, 210, 210);
}
</style>
