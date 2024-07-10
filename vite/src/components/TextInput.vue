<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps({
    hint: {
        type: String,
        required: false,
    },
    label: {
        type: String,
        required: false,
    },
    type: {
        type: String,
        default: "text",
    },
    required: {
        type: Boolean,
        default: false,
    },
    autofocus: {
        type: Boolean,
        default: false,
    },
    uppercase: {
        type: Boolean,
        default: false,
    },
    readonly: {
        type: Boolean,
        default: false,
    },
    tabindex: {
        type: String,
        required: false,
    },
});
const model = defineModel();
const input = ref();
const target = ref();

onMounted(() => {
    if (input.value.hasAttribute('autofocus')) {
        input.value.focus();
    }
    input.value.addEventListener('focusin', onFocusIn);
    input.value.addEventListener('focusout', onFocusOut);

    if (props.uppercase) {
        input.value.style['text-transform'] = 'uppercase';
    }
});

defineExpose({ focus: () => input.value.focus() });

function onFocusIn() {
    target.value.setAttribute('label', props.label);
}

function onFocusOut() {
    target.value.removeAttribute('label');
}
</script>

<template>
    <form-input-text ref="target">
        <input
            ref="input"
            v-model="model"
            :type="type"
            :required="required"
            :placeholder="hint"
            :autofocus="autofocus"
            :tabindex="tabindex"
            :readonly="readonly"
            autocomplete="off"
            spellcheck="false"
            data-gramm="false"
        />
        <label class="btn-label" v-html="hint"></label>
        <form-input-border></form-input-border>
    </form-input-text>
</template>
