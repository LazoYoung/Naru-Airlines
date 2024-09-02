<script setup>
import {ref} from "vue";

import {onMounted, watch} from "vue";

const visible = defineModel("visible", {
    type: Boolean,
    default: false
});
const bg = ref();

watch(() => visible.value, setVisible);
onMounted(() => setVisible(visible.value));

function onFocusLost(event) {
    if (event.target.id === bg.value.id) {
        close();
    }
}

function setVisible(value) {
    const div = bg.value;
    div.style.visibility = value ? "visible" : "hidden";
}

function close() {
    visible.value = false;
}
</script>

<template>
    <div class="blur-bg" ref="bg" @click="onFocusLost">
        <div class="modal">
            <div class="title-bar">
                <div class="title">
                    <slot name="title"></slot>
                </div>
                <button class="close" @click="close">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
.blur-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 10;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal {
    display: flex;
    flex-direction: column;
    border-radius: 1rem;
    background: lightgray;
    width: fit-content;
    height: fit-content;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.title-bar {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    background: #171717;
    border-top-left-radius: 1rem;
    border-top-right-radius: 1rem;
    height: 2.5rem;
}

.title {
    color: white;
    margin-left: 0.5rem;
    font-weight: 500;
    font-size: 1.2em;
}

.close {
    background: transparent;
    width: 2.5rem;
    height: 2.5rem;
}

.close > span.material-symbols-outlined {
    color: white;
    vertical-align: top;
    font-variation-settings: 'FILL' 0,
    'wght' 700,
    'GRAD' 0,
    'opsz' 24
}
</style>
