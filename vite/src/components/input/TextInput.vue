<script setup>
import {onMounted, ref, watch} from 'vue';
import InputError from "@/components/InputError.vue";

const props = defineProps({
    type: {
        type: String,
        default: "text",
    },
    hint: {
        type: String,
        required: true,
    },
    label: {
        type: String,
        default: "inner",
    },
    fixed_label: {
        type: Boolean,
        default: false,
    },
    small: {
        type: Boolean,
        default: false,
    },
    error_message: {
        type: String,
        default: null,
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
});
const model = defineModel();
const input = ref();
const target = ref();

watch(props, _ => reloadElements());
onMounted(() => reloadElements());
defineExpose({focus: () => input.value.focus()});

function onFocusIn() {
    target.value.setAttribute('label', props.label);
}

function onFocusOut() {
    target.value.removeAttribute('label');
}

function reloadElements() {
    if (input.value.hasAttribute('autofocus')) {
        input.value.focus();
    }

    if (props.fixed_label) {
        target.value.setAttribute('label', props.label);
    } else {
        input.value.addEventListener('focusin', onFocusIn);
        input.value.addEventListener('focusout', onFocusOut);
    }

    if (props.uppercase) {
        input.value.style['text-transform'] = 'uppercase';
    } else {
        input.value.style['text-transform'] = 'none';
    }

    if (props.small) {
        target.value.setAttribute('small', '');
    } else {
        target.value.removeAttribute('small');
    }
}
</script>

<template>
    <!--  todo: support form-textarea, form-datetime  -->
    <div>
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
        <InputError :message="error_message"></InputError>
    </div>
</template>
