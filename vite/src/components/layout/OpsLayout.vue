<script setup>
// noinspection JSUnusedGlobalSymbols
import {onMounted, onUnmounted, ref} from "vue";

const vButton = {
    mounted: (el) => {
        el.addEventListener('mouseenter', onButtonSelect);
        el.addEventListener('focusin', onButtonSelect);
        el.addEventListener('mouseleave', onButtonRelease);
        el.addEventListener('focusout', onButtonRelease);
    },
    unmounted: (el) => {
        el.removeEventListener('mouseenter', onButtonSelect);
        el.removeEventListener('focusin', onButtonSelect);
        el.removeEventListener('mouseleave', onButtonRelease);
        el.removeEventListener('focusout', onButtonRelease);
    },
};

const timeRef = ref();
let tickId = null;

onMounted(() => {
    tickId = setInterval(onTick, 1000);
});

onUnmounted(() => {
    if (tickId) {
        clearInterval(tickId);
    }
});

function onTick() {
    let date = new Date();
    let h = String(date.getUTCHours()).padStart(2, '0');
    let m = String(date.getUTCMinutes()).padStart(2, '0');
    let s = String(date.getUTCSeconds()).padStart(2, '0');
    timeRef.value.innerHTML = `${h}:${m}:${s}`;
}

function onButtonSelect(event) {
    event.target.setAttribute('selected', 'true');
}

function onButtonRelease(event) {
    event.target.removeAttribute('selected');
}
</script>

<template>
    <div id="root">
        <div id="lhs">
            <RouterLink :to="{'name': 'home'}">
                <div id="logo">
                    <img src="@/assets/logo.svg" alt="Logo">
                    <div id="subtitle">Operations Center</div>
                </div>
            </RouterLink>
            <div id="links">
                <RouterLink :to="{name: 'dashboard'}">
                    <div class="nav-btn" v-button>
                        <div class="icon-box">
                            <span class="material-symbols-outlined">dashboard</span>
                            <span class="nav-label">Dashboard</span>
                        </div>
                        <span class="material-symbols-outlined">keyboard_arrow_right</span>
                    </div>
                </RouterLink>
                <RouterLink :to="{name: 'dispatcher'}">
                    <div class="nav-btn" v-button>
                        <div class="icon-box">
                            <span class="material-symbols-outlined">description</span>
                            <span class="nav-label">Dispatcher</span>
                        </div>
                        <span class="material-symbols-outlined">keyboard_arrow_right</span>
                    </div>
                </RouterLink>
                <RouterLink :to="{name: 'pilot-settings'}">
                    <div class="nav-btn" v-button>
                        <div class="icon-box">
                            <span class="material-symbols-outlined">settings</span>
                            <span class="nav-label">Settings</span>
                        </div>
                        <span class="material-symbols-outlined">keyboard_arrow_right</span>
                    </div>
                </RouterLink>
            </div>
            <div class="flex-grow"></div>
            <div id="utc">
                <div class="label">UTC TIME</div>
                <div class="time" ref="timeRef"></div>
            </div>
        </div>
        <div id="rhs">
            <div id="header">
                <!--       todo - add breadcrumb         -->
            </div>
            <div id="content">
                <h3 id="title">
                    <slot name="title"></slot>
                </h3>
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style scoped>
a {
    text-decoration: none;
}

.flex-grow {
    visibility: hidden;
    flex-grow: 1;
}

#root {
    display: flex;
    flex-direction: row;
    justify-items: stretch;
}

#lhs {
    display: flex;
    flex-direction: column;
    background-color: #171717;
    //background-color: #64b8d7;
    //background-color: skyblue;
    //background-color: #04061f;
    min-width: 18rem;
    height: 100vh;
}

#rhs {
    flex-grow: 1;
    background-color: gainsboro;
}

#header {
    height: 0;
    background-color: dimgray;
}

#content {
    margin: 4rem;
}

#title {
    margin-bottom: 2rem;
}

#logo {
    display: flex;
    flex-direction: column;
    row-gap: 0.5rem;
    padding: 1.5rem 2rem;
}

#links {
    display: flex;
    flex-direction: column;
    row-gap: 0.2rem;
    margin-top: 1.5rem;
}

#subtitle {
    color: #00458b;
    font-style: italic;
    font-weight: 600;
    font-size: 1rem;
    margin: 0 auto;
}

#utc {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 2rem 0;
    row-gap: 0.5rem;
}

#utc > .label {
    color: white;
    font-size: 1rem;
}

#utc > .time {
    color: white;
    font-size: 1.2rem;
    font-weight: 500;
}

.nav-btn {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 3rem;
    padding: 1rem;
    margin: 0 0.5rem;
    border-radius: 0.5rem;
    justify-content: space-between;
    color: white;
}

.nav-btn[selected] {
    //background-color: #00458b;
    background-color: dimgray;
}

.nav-btn span {
    color: white;
    //color: #00458b;
    //color: black;
    font-size: 1.1rem;
    font-weight: 500;
}

.nav-btn .material-symbols-outlined {
    font-size: 1.5rem;
    font-weight: 400;
}

.icon-box {
    display: flex;
    align-items: center;
    column-gap: 0.8rem;
}

@media screen and (max-width: 600px) {
    #content {
        margin: 2rem;
    }
}
</style>
