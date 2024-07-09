<script setup>
import {reactive} from "vue";

const props = defineProps({
    isAdmin: {
        type: Boolean,
        default: false
    },
    mapApiKey: {
        type: String,
        default: null,
    },
});
const modal = reactive({
    airport: false,
});
const quotes = [
    "Only the sky is the limit.",
    "As real as it gets.",
    "A next gen virtual airline.",
    "Join us, fly together.",
    "Welcome aboard."
];

function openAirportModal() {
    modal.airport = true;
}

function getQuote() {
    let index = Math.floor(Math.random() * quotes.length);
    return quotes[index];
}
</script>

<template>
<!--    <Head title="Home" />-->
<!--    <Navigation></Navigation>-->

    <main>
        <section id="root-header">
            <layer class="bg">
                <video autoplay loop muted>
                    <source :src="'/static/promo.mp4'" />
                </video>
            </layer>
            <layer class="cv"></layer>
            <layer class="fg">
                <outwrapper>
                    <inwrapper>
                        <h1 v-html="getQuote()"></h1>
                        <div class="buttons">
                            <button filled>Take a tour</button>
                            <button>Apply to join</button>
                        </div>
                    </inwrapper>
                </outwrapper>
            </layer>
        </section>
        <section id="root-form-designs">
            <div class="max-w-4xl mx-auto">
                <div class="pt-16">
                    <h1 class="text-4xl text-white text-center font-bold">Destinations</h1>
                    <p class="text-gray-200 text-center py-4">
                        These cities are served as our primary destinations.
                        <br>
                        We will continue to expand our flight network.
                    </p>
                    <div class="flex flex-row justify-end mb-6">
                        <button small v-if="isAdmin" @click="openAirportModal">
                            Add airport
                        </button>
                    </div>
<!--                    <DestinationMap class="h-96" :api-key="mapApiKey"></DestinationMap>-->
                </div>

                <div class="flex justify-center mt-16 px-6 sm:items-center sm:justify-between">
                    <div class="text-center text-sm text-white dark:text-gray-400 sm:text-left">
                        <div class="flex items-center gap-4">
                            <a
                                href="https://github.com/LazoYoung/naru-aviation-web"
                                target="_blank"
                                class="group inline-flex items-center hover:text-gray-700 dark:hover:text-white focus:outline focus:outline-2 focus:rounded-sm focus:outline-red-500"
                            >
                                <i class="fa-brands fa-github"></i>
                                <p class="ms-2">Crafted by Chanyoung Park</p>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

<!--    <AirportModal :show="modal.airport" @close="modal.airport = false"></AirportModal>-->

</template>

<style scoped>
/* Hides ugly scrollbars */
div {
    scrollbar-width: none;
}

div::-webkit-scrollbar {
    display: none;
}

#root-header {
    width: 100%;
    height: 100vh;
    position: relative;
}
#root-header > .bg {
    position: fixed;
}
#root-header > .bg video {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
#root-header > .cv {
    background: rgba(0, 0, 0, 0.35);
}
#root-header > .fg {
    position: fixed;
    display: flex;
    justify-content: flex-end;
    flex-direction: column;
}
#root-header > .fg h1 {
    max-width: 60rem;
    font-weight: 900;
    font-size: max(5rem, 8vw);
    color: white;
}
#root-header .buttons {
    margin-top: 3rem;
    margin-bottom: 6rem;
    display: flex;
    justify-content: flex-start;
}
#root-header .buttons > button {
    margin-right: 1.5rem;
}

#root-form-designs {
    width: 100%;
    min-height: calc(100vh - 4rem);
    position: relative;
    background-color: var(--bg);
}

#root-ticket {
    width: 100%;
    position: relative;
    background: rgb(255, 89, 0);
}
#root-ticket > .bg {
    background: rgb(255, 89, 0);
}
#root-ticket > .fg {
    position: relative;
    display: flex;
    justify-content: flex-start;
    flex-direction: column;
    padding-top: 5rem;
}
#root-ticket > .fg h1 {
    font-weight: 900;
    font-size: 9rem;
    color: white;
}
#root-ticket .boardingpass {
    position: relative;
    width: 100%;
    padding-top: 40%;
    margin-top: 5rem;
    margin-bottom: 5rem;
}
#root-ticket .content {
    width: 100%;
    height: 100%;
}
#root-ticket .content canvas {
    width: 100%;
    height: 100%;
}
#root-ticket .buttons {
    margin-top: 5rem;
    display: flex;
    justify-content: flex-end;
}
#root-ticket .buttons > button {
    margin-left: 1.5rem;
}
</style>
