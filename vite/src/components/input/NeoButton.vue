<script setup>
import {onMounted, ref, watch} from 'vue';
import InputMessage from '@/components/input/InputMessage.vue';

const props = defineProps({
    type: {
        type: String,
        default: 'submit',
    },
    size: {
        type: String,
        default: 'medium',
    },
    variant: {
        type: String,
        default: 'filled',
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
            ref="button"
            :type="props.type"
            :form="props.form"
            :size="props.size"
            :variant="props.variant"
            :color="props.color"
            :disabled="disabled"
    >
        <slot></slot>
    </button>
</template>

<style>
button {
    --white-fg: rgb(240, 240, 240);
    --white-bg: rgb(210, 210, 210);
    --white-bg-tint: rgb(180, 180, 180);
}

button {
    width: 8rem;
    height: 3rem;
    padding: 0 3rem;
    font-size: 1rem;
    font-weight: 600;
    border-width: 2px;
    border-style: solid;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 0.75rem;
    cursor: pointer;
}

button[size='large'] {
    width: 10rem;
    height: 5rem;
    padding: 0 3rem;
    font-size: 1.25rem;
}

button[size='small'] {
    width: 6rem;
    height: 2.5rem;
    padding: 0 2rem;
    font-size: 1rem;
}

button[size='tiny'] {
    width: 4rem;
    height: 1.5rem;
    padding: 0 1rem;
    font-size: 0.75rem;
}

button:focus-visible {
    outline-offset: 0.25rem;
    outline: solid 0.1rem black;
}

button[variant='shadowed'] {
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
}

button[color='white'] {
    border-color: var(--white-bg);
}

button[variant='filled'][color='white'] {
    background: var(--white-bg);
    border-color: var(--white-bg-tint);
}

button:hover,
button:focus,
button:active {
    background: var(--white-bg);
}

button:hover[variant='filled'],
button:focus[variant='filled'],
button:active[variant='filled'] {
    background: var(--white-bg-tint);
}

button:disabled {
    color: rgb(230, 230, 230);
    background: rgb(180, 180, 180) !important;
    cursor: not-allowed;
}
</style>
