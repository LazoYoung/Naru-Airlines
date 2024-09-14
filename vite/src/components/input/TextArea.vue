<script setup>
import {onMounted, ref, watch} from 'vue';
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
        default: 'info',
    },
    optional: {
        type: Boolean,
        default: false,
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
const textarea = ref();
const target = ref();

watch(props, (_) => reloadElements());
onMounted(() => reloadElements());
defineExpose({
    focus: () => textarea.value.focus(),
    blur: () => textarea.value.blur(),
});

function reloadElements() {
    if (textarea.value.hasAttribute('autofocus')) {
        textarea.value.focus();
    }

    if (props.uppercase) {
        textarea.value.style['text-transform'] = 'uppercase';
    } else {
        textarea.value.style['text-transform'] = 'none';
    }
}
</script>

<template>
    <!--  todo: support form-textarea, form-datetime  -->
    <div class="form">
        <label v-if="label" v-html="label"></label>
        <div class="textarea" ref="target">
            <textarea
                    ref="textarea"
                    v-model="model"
                    :type="type"
                    :required="!optional"
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

.form > .textarea {
    display: flex;
    width: 100%;
    height: 5rem;
    justify-content: center;
    align-items: center;
    border-radius: 0.75rem;
    overflow: hidden;
    position: relative;
}

.form > .textarea > textarea,
.form > .textarea > textarea:-webkit-autofill,
.form > .textarea > textarea:-webkit-autofill:hover,
.form > .textarea > textarea:-webkit-autofill:focus {
    width: 100%;
    height: 100%;
    font-size: 1rem;
    font-weight: 400;
    padding: 0.75rem 0.75rem;
    color: black;
    -webkit-text-fill-color: black !important;
}

.form > .textarea > .border {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 0.75rem;
    pointer-events: none;
    box-shadow: inset 0 0 0 0.1rem rgb(210, 210, 210);
}

.form > .textarea > textarea:focus ~ .border,
.form > .textarea > textarea:active ~ .border {
    box-shadow: inset 0 0 0 0.1rem rgb(0, 0, 0);
}

.form > .textarea > textarea:disabled {
    background: rgb(230, 230, 230);
    cursor: not-allowed;
}

.form > .textarea > textarea::placeholder,
.form > .textarea > textarea::-webkit-textarea-placeholderr {
    color: rgb(180, 180, 180);
    -webkit-text-fill-color: rgb(180, 180, 180) !important;
}
</style>
