<script setup>
import { onMounted, ref, watch } from 'vue';

import SplitFlipDisplayChar from '@/components/SplitFlipDisplayChar.vue';

const props = defineProps({
    string: {
        type: String,
        required: true,
    },
    length: {
        type: Number,
        default: 10,
    },
});
const wrapper = ref(null);

onMounted(() => {});

watch(
    () => props.string,
    async (newVal, oldVal) => {
        await display(newVal);
    }
);

async function display(string) {
    let chars = wrapper.value.querySelectorAll('.sfdc-wrapper');
    for (let i = 0; i < chars.length; i++) {
        chars[i].
    }
}

async function delay(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}
</script>

<template>
    <div class="sfd-wrapper" ref="wrapper">
        <SplitFlipDisplayChar
            v-for="n in props.length"
            :char="props.string[n]"
            :time="100"
        ></SplitFlipDisplayChar>
    </div>
</template>

<style>
.sfd-wrapper {
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
}
.sfd-wrapper > .sfdc-wrapper {
}
</style>
