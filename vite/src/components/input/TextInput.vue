<script setup>
import { onMounted, ref, watch } from 'vue';
import InputMessage from '@/components/input/InputMessage.vue';

const props = defineProps({
    type: {
        type: String,
        default: 'text',
    },
    placeholder: {
        type: String,
        default: '',
    },
    label: {
        type: String,
        default: '',
    },
    message: {
        type: String,
        default: null,
    },
    message_type: {
        type: String,
        default: 'error',
    },
    required: {
        type: Boolean,
        default: true,
    },
    autofocus: {
        type: Boolean,
        default: false,
    },
    readonly: {
        type: Boolean,
        default: false,
    },
    uppercase: {
        type: Boolean,
        default: false,
    },
    tabindex: {
        type: String,
        required: false,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});
const model = defineModel();
const input = ref();
const target = ref();

watch(props, (_) => reloadElements());
onMounted(() => reloadElements());
defineExpose({
    focus: () => input.value.focus(),
    blur: () => input.value.blur(),
});

function reloadElements() {
    if (input.value.hasAttribute('autofocus')) {
        input.value.focus();
    }

    if (props.uppercase) {
        input.value.style['text-transform'] = 'uppercase';
    } else {
        input.value.style['text-transform'] = 'none';
    }
}
</script>

<template>
    <!--  todo: support form-textarea, form-datetime  -->
    <div class="form">
        <label v-if="label" v-html="label"></label>
        <div class="input" ref="target">
            <input
                ref="input"
                v-model="model"
                :type="type"
                :required="required"
                :placeholder="placeholder"
                :autofocus="autofocus"
                :tabindex="tabindex"
                :readonly="readonly"
                autocomplete="off"
                spellcheck="false"
                data-gramm="false"
                :disabled="disabled"
            />
            <div class="border"></div>
        </div>
        <InputMessage
            class="message"
            :message="message"
            :type="message_type"
        ></InputMessage>
    </div>
</template>

<style>
.form > label {
    font-size: 1rem;
    font-weight: 600;
    display: block;
    padding-bottom: 0.25rem;
    line-height: 1rem;
    min-height: 1.25rem;
}
.form > .input {
    display: flex;
    width: 100%;
    height: 2.5rem;
    justify-content: center;
    align-items: center;
    border-radius: 0.75rem;
    overflow: hidden;
    position: relative;
}
.form > .input > input,
.form > .input > input:-webkit-autofill,
.form > .input > input:-webkit-autofill:hover,
.form > .input > input:-webkit-autofill:focus {
    width: 100%;
    height: 100%;
    font-size: 1rem;
    font-weight: 400;
    padding: 0 0.75rem;
    color: black;
    -webkit-text-fill-color: black !important;
}
.form > .input > .border {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 0.75rem;
    pointer-events: none;
    box-shadow: inset 0 0 0 0.1rem rgb(210, 210, 210);
}
.form > .input > input:focus ~ .border,
.form > .input > input:active ~ .border {
    box-shadow: inset 0 0 0 0.1rem rgb(0, 0, 0);
}
.form > .input > input:disabled {
    background: rgb(230, 230, 230);
    cursor: not-allowed;
}
.form > .input > input::placeholder,
.form > .input > input::-webkit-input-placeholderr {
    color: rgb(180, 180, 180);
    -webkit-text-fill-color: rgb(180, 180, 180) !important;
}
</style>
