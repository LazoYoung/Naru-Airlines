<script setup>
import { onMounted, ref, watch } from 'vue';
const props = defineProps({
    char: {
        type: String,
        required: true,
    },
    time: {
        type: Number,
        default: 100,
    },
});
let topchar = ref(props.char);
let top2char = ref(' ');
let bottomchar = ref(props.char);
let bottom2char = ref(' ');

onMounted(() => {});

watch(
    () => props.char,
    async (newVal, oldVal) => {
        await display(newVal);
    }
);

async function display(next) {
    const top = document.querySelector('.sfdc-wrapper .top .char');
    const top2 = document.querySelector('.sfdc-wrapper .top2 .char');
    const bottom = document.querySelector('.sfdc-wrapper .bottom .char');
    const bottom2 = document.querySelector('.sfdc-wrapper .bottom2 .char');

    top2char.value = next;
    bottom2char.value = next;

    top.style.transition = `transform ${props.time}ms linear`;
    bottom2.style.transition = `transform ${props.time}ms linear`;
    top.style.transform = `rotateX(-90deg)`;
    await delay(props.time);
    bottom2.style.transform = `rotateX(-180deg) scaleY(-1)`;
    await delay(props.time);

    topchar.value = next;
    bottomchar.value = next;

    top.style.transition = `transform 0s linear`;
    bottom2.style.transition = `transform 0s linear`;
    top.style.transform = `rotateX(0deg)`;
    bottom2.style.transform = `rotateX(-90deg) scaleY(-1)`;
}

async function delay(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}
</script>

<template>
    <div class="sfdc-wrapper">
        <div class="flip top2">
            <div class="char">{{ top2char }}</div>
        </div>
        <div class="flip top">
            <div class="char">{{ topchar }}</div>
        </div>
        <div class="flip bottom">
            <div class="char">{{ bottomchar }}</div>
        </div>
        <div class="flip bottom2">
            <div class="char">{{ bottom2char }}</div>
        </div>
    </div>
</template>

<style>
.sfdc-wrapper {
    position: relative;
    width: var(--sfdc-width);
    height: var(--sfdc-height);
    margin-left: calc(var(--sfdc-width) / 3 * -1);
}
.sfdc-wrapper .flip {
    position: absolute;
    width: 100%;
    height: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    perspective: var(--sfdc-perspective);
}
.sfdc-wrapper .flip.top,
.sfdc-wrapper .flip.top2 {
    top: 0;
    perspective-origin: bottom;
}
.sfdc-wrapper .flip.bottom,
.sfdc-wrapper .flip.bottom2 {
    bottom: 0;
    perspective-origin: top;
}
.sfdc-wrapper .char {
    position: absolute;
    width: 50%;
    height: 200%;
    background: var(--sfdc-flip-bg);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: var(--sfdc-flip-fs);
    font-weight: var(--sfdc-flip-fw);
    color: var(--sfdc-flip-fg);
}
.sfdc-wrapper .top2 > .char {
    top: 0;
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
}
.sfdc-wrapper .top > .char {
    top: 0;
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
}
.sfdc-wrapper .bottom > .char {
    bottom: 0;
    border-bottom-left-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
}
.sfdc-wrapper .bottom2 > .char {
    bottom: 0;
    border-bottom-left-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
    transform: rotateX(-90deg) scaleY(-1);
}
</style>
