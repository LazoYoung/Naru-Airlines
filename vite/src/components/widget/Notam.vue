<script setup>
import {BBadge} from "bootstrap-vue-next";
import {onMounted} from "vue";

const props = defineProps({
    width: {
        type: String,
        default: "15rem",
    },
});

const notams = [
    {
        title: 'Runway closure 09R/27L at EGLL',
        date: '2023-08-25',
        description: 'Runway 09R/27L at London Heathrow (EGLL) will be closed for essential maintenance work.',
        isNew: true
    },
    {
        title: 'Revision of approach procedure for KJFK',
        date: '2023-08-24',
        description: 'A new approach procedure has been implemented for runway 13L/31R at JFK Airport (KJFK).',
        isNew: false
    },
    {
        title: 'Temporary flight restrictions over KSFO',
        date: '2023-08-23',
        description: 'Temporary flight restrictions have been implemented over San Francisco International Airport (KSFO) due to an upcoming airshow.',
        isNew: false
    }
];

onMounted(() => {
    for (let header of document.querySelectorAll(".header, .desc")) {
        header.style.width = props.width;
    }
});
</script>

<template>
    <BAccordion>
        <BAccordionItem v-for="(notam, index) in notams" :key="index" :title="notam.title">
            <template #title>
                <div class="header">
                    <span class="title">{{ notam.title }}</span>
                    <BBadge v-if="notam.isNew" variant="danger" class="ml-2">New</BBadge>
                </div>
            </template>
            <div class="bg-white rounded p-3 shadow">
                <span class="small text-muted"><i class="fas fa-clock mr-1"></i>
                    {{ notam.date }}
                </span>
                <p class="desc text-small mt-2 font-weight-light">
                    {{ notam.description }}
                </p>
            </div>
        </BAccordionItem>
    </BAccordion>
</template>

<style scoped>
.header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.title {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    line-height: normal;
}
</style>
