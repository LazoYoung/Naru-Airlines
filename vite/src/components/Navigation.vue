<script setup>
import {onMounted, ref} from 'vue';
import {RouterLink} from "vue-router";
import {fetchProfile, getGravatarHash, home, useForm} from "@/api.js";
import IconBanner from "@/components/icons/IconBanner.vue";
import IconLogo from "@/components/icons/IconLogo.vue";
import BasicMenu from "@/components/menu/BasicMenu.vue";
import PilotMenu from "@/components/menu/PilotMenu.vue";

const profile = ref(null);
let lastWidth = window.innerWidth;
let lastWidthChange = null;
let nav = null;

defineProps({
    pilot: {
        type: Boolean,
        default: false
    }
});

onMounted(() => {
    fetchProfile(profile);

    nav = document.querySelector("#nav");

    window.addEventListener("resize", () => {
        if (
            window.innerWidth > lastWidth &&
            window.innerWidth > 1200 &&
            lastWidthChange !== "wide"
        ) {
            closeAll();
            lastWidthChange = "wide";
        } else if (
            window.innerWidth < lastWidth &&
            window.innerWidth <= 1200 &&
            lastWidthChange !== "narrow"
        ) {
            closeAll();
            lastWidthChange = "narrow";
        }
        lastWidth = window.innerWidth;
    });

    for (const dropdown of nav.querySelectorAll(
        ".menu-wide .element.dropdown"
    )) {
        dropdown.addEventListener("click", (event) => {
            let target = event.target;
            while (!target.classList.contains("element")) {
                if (target.classList.contains("content")) {
                    return;
                }
                target = target.parentElement;
            }
            target.getAttribute("opened") === ""
                ? closeWideDropdown(target)
                : openWideDropdown(target);
            nav.querySelectorAll(".menu-wide .element.dropdown[opened]")
                .length === 0
                ? hideBackground()
                : showBackground();
        });
    }

    for (const dropdown of nav.querySelectorAll(
        ".menu-narrow .element.dropdown"
    )) {
        dropdown.addEventListener("click", (event) => {
            let target = event.target;
            while (!target.classList.contains("element")) {
                if (target.classList.contains("content")) {
                    return;
                }
                target = target.parentElement;
            }
            target.getAttribute("opened") === ""
                ? closeNarrowDropdown(target)
                : openNarrowDropdown(target);
        });
    }

    document
        .querySelector("#nav-background")
        .addEventListener("click", closeAll);
    document
        .querySelector("#button-nav-narrow")
        .addEventListener("click", () => {
            document.querySelector("#button-nav-narrow").classList.contains("cross")
                ? closeNarrowMenu()
                : openNarrowMenu();
        });
});

function getProfileImageSource() {
    let hash = getGravatarHash(profile.value['email']);
    return `https://www.gravatar.com/avatar/${hash}?s=512`;
}

function closeAll() {
    closeWideDropdowns();
    closeNarrowDropdowns();
    foldProfile();
    closeNarrowMenu();
    hideBackground();
}

function showBackground() {
    document.querySelector("#nav-background").classList.add("show");
}

function hideBackground() {
    document.querySelector("#nav-background").classList.remove("show");
}

function openWideDropdown(element) {
    if (element) {
        closeAll();
        element.setAttribute("opened", "");
    }
}

function closeWideDropdowns() {
    for (const other of nav.querySelectorAll(
        ".menu-wide .element.dropdown"
    )) {
        closeWideDropdown(other);
    }
}

function closeWideDropdown(element) {
    element.removeAttribute("opened");
}

function expandProfile() {
    let element = document.getElementById('account');

    if (element.hasAttribute("expand"))
        return;

    closeAll();
    showBackground();
    element.setAttribute("expand", "");
    document.querySelector("#button-nav-narrow").classList.add("hidden");
}

function foldProfile() {
    let account = document.getElementById("account");
    let narrowBtn = document.getElementById("button-nav-narrow");

    if (account) {
        account.removeAttribute("expand");
    }

    if (narrowBtn) {
        narrowBtn.classList.remove("hidden");
    }
}

function openNarrowMenu() {
    closeAll();
    showBackground();
    document.querySelector("#button-nav-narrow").classList.add("cross");
    document.querySelector("#nav-bottom .menu-narrow").classList.add("show");
}

function closeNarrowMenu() {
    document.querySelector("#button-nav-narrow").classList.remove("cross");
    document.querySelector("#nav-bottom .menu-narrow").classList.remove("show");
    hideBackground();
}

function openNarrowDropdown(element) {
    if (element) {
        closeNarrowDropdowns();
        element.setAttribute("opened", "");
    }
}

function closeNarrowDropdowns() {
    for (const other of nav.querySelectorAll(
        ".menu-narrow .element.dropdown"
    )) {
        closeNarrowDropdown(other);
    }
}

function closeNarrowDropdown(element) {
    element.removeAttribute("opened");
}

function logout() {
    useForm().submitPost("/api/logout/")
        .then(response => {
            if (response.ok) {
                closeAll();
                home();
            }
        });
}
</script>

<template>
    <nav id="nav">
        <div id="nav-background"></div>
        <div id="nav-top">
            <div class="left">
                <RouterLink :to="{name: 'home'}" class="logo">
                    <div class="icon">
                        <IconLogo :color="pilot ? 'blue' : 'white'"></IconLogo>
                    </div>
                    <div class="text">
                        <IconBanner/>
                    </div>
                </RouterLink>
            </div>
            <div class="center">
                <div class="menu menu-wide">
                    <PilotMenu v-if="pilot"></PilotMenu>
                    <BasicMenu v-else></BasicMenu>
                </div>
            </div>
            <div class="right">
                <div v-if="profile" id="account" @click="expandProfile">
                    <div class="profile-badge">
                        <img class="image" :src="getProfileImageSource()" alt="image">
                        <div class="name">{{ profile['display_name'] }}</div>
                    </div>
                    <RouterLink :to="{name: 'settings'}" @click.stop="closeAll" class="element">
                        <div class="pillar"></div>
                        <img class="icon" src="../assets/gear.svg" alt="settings">
                        <span>Settings</span>
                        <div class="pillar"></div>
                    </RouterLink>
                    <a @click.stop="logout" class="element">
                        <div class="pillar"></div>
                        <img class="icon" src="../assets/exit.svg" alt="exit">
                        <span>Log out</span>
                        <div class="pillar"></div>
                    </a>
                </div>
                <div v-else id="guest">
                    <RouterLink :to="{name: 'login'}">
                        <button small>Login</button>
                    </RouterLink>
                    <RouterLink :to="{name: 'register'}">
                        <button small>Sign up</button>
                    </RouterLink>
                </div>
                <div class="narrowmenu">
                    <div id="button-nav-narrow">
                        <div class="line top"></div>
                        <div class="line bottom"></div>
                    </div>
                </div>
            </div>
        </div>
        <div id="nav-bottom">
            <div class="narrow-nav menu menu-narrow">
                <PilotMenu v-if="pilot"></PilotMenu>
                <BasicMenu v-else></BasicMenu>
            </div>
        </div>
    </nav>
</template>

<style>
#nav {
    --nav-bg: black;
    --nav-fg: white;
    --nav-button-bg: rgb(45, 45, 45);
    --nav-button-bg-hover: rgb(80, 80, 80);

    position: fixed;
    width: 100%;
    height: 100vh;
    overflow: hidden;

    z-index: 20000000;
    pointer-events: none;
}

#nav-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgb(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    opacity: 0;
    transition: opacity 0.1s ease-out;
    pointer-events: none;
}

#nav-background.show {
    opacity: 1;
    transition: opacity 0.2s ease-out;
    pointer-events: all;
}

#nav .menu .element > label {
    display: flex;
    justify-content: flex-start;
    align-items: center;
}

#nav .menu .element > label > .name {
    font-size: 1.25rem;
    font-weight: 500;
    line-height: 1.25rem;
    word-break: keep-all;
    cursor: pointer;
}

#nav .menu .element > label:hover > .name {
    text-decoration: underline;
}

#nav .menu .element > label > .arrow {
    display: inline-block;
    font-size: 0.8rem;
    line-height: 1.25rem;
    font-weight: 500;
    margin-left: 0.35rem;
}

#nav .menu .element > label > .arrow-link {
    display: inline-block;
    font-size: 1.25rem;
    line-height: 1.25rem;
    font-weight: 500;
    margin: 0.35rem;
}

#nav-top {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    width: 100%;
    height: 5rem;
    background-color: var(--nav-bg);
    align-items: center;
    justify-content: space-between;
    pointer-events: all;
    z-index: 20000000;
}

#nav-top > * {
    flex-wrap: nowrap;
}

#nav-top > .left {
    width: 18rem;
    padding-left: 2rem;
    display: flex;
    align-items: center;
}

#nav-top > .left > .logo {
    height: 2.6rem;
}

#nav-top .logo {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
}

#nav-top .logo .icon {
    height: 100%;
}

#nav-top .logo .text {
    height: 70%;
    margin-left: 0.35rem;
}

#nav-top .logo .icon > img,
#nav-top .logo .text > img {
    height: 100%;
    fill: white;
}

#nav-top .logo .icon > svg,
#nav-top .logo .text > svg {
    height: 100%;
    fill: white;
}

#nav-top > .center {
    width: calc(100% - 40rem);
    max-width: 75vw;
}

#nav-top .menu-wide {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-wrap: wrap;
}

#nav-top .menu-wide .element {
    display: flex;
    position: relative;
    margin-left: 2.5rem;
    width: fit-content;
    justify-content: flex-start;
    align-items: center;
}

#nav-top .menu-wide .element:first-child {
    margin-left: 0;
}

#nav-top .menu-wide .element.dropdown[opened] > label > .arrow {
    transform: rotate(180deg);
}

#nav-top .menu-wide .element.dropdown > .content {
    display: none;
}

#nav-top .menu-wide .element.dropdown[opened] > .content {
    display: block;
    position: absolute;
    background: var(--nav-bg);
    padding: 0 0.75rem 0 0.75rem;
    top: 2rem;
    left: -0.75rem;
}

#nav-top .menu-wide .element.dropdown > .content > a {
    display: flex;
    width: max-content;
    font-size: 1.25rem;
    font-weight: 500;
    line-height: 1.25rem;
    margin: 0.75rem 0 0.75rem 0;
    word-break: keep-all;
    cursor: pointer;
    justify-content: flex-start;
    align-items: center;
}

#nav-top .menu-wide .element.dropdown > .content > a span {
    margin-left: 0.35rem;
}

#nav-top .menu-wide .element.dropdown > .content > a:hover label {
    text-decoration: underline;
    cursor: pointer;
}

#nav-top > .right {
    width: 18rem;
    padding-right: 2rem;
    display: flex;
    justify-content: flex-end;
}

#button-nav-narrow {
    width: 2.5rem;
    height: 2.5rem;
    position: relative;
    cursor: pointer;
    margin-left: 1rem;
    display: none;
}

#button-nav-narrow > .line {
    position: absolute;
    width: 100%;
    height: 0;
    border-bottom: solid 2px var(--nav-fg);
    transition: top 0.1s ease-out, bottom 0.1s ease-out, transform 0.1s ease-out;
}

#button-nav-narrow > .top {
    top: 0.75rem;
}

#button-nav-narrow > .bottom {
    bottom: 0.75rem;
}

#button-nav-narrow.cross > .top {
    top: calc(1.25rem - 1px);
    transform: rotate(45deg);
}

#button-nav-narrow.cross > .bottom {
    bottom: calc(1.25rem - 1px);
    transform: rotate(-45deg);
}

#guest {
    display: flex;
    align-items: center;
    column-gap: 1rem;
}

#account {
    border-radius: 5rem;
    max-height: 2.4rem;
    padding: 0.35rem 0.65rem 0.35rem 0.35rem;
    background: var(--nav-button-bg);
    cursor: pointer;
    transition: max-height 0.5s ease-in-out;
}

#account[expand] {
    position: fixed;
    top: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    row-gap: 1.25rem;
    border-radius: 1rem;
    height: fit-content;
    max-height: 30rem;
    cursor: default;
    padding: 1rem;
    background: var(--nav-button-bg);
}

#account > .profile-badge {
    display: flex;
    flex-direction: row;
    align-items: center;
}

#account .image {
    width: 1.8rem;
    height: 1.8rem;
    border-radius: 100%;
    border: solid 1px var(--nav-fg);
}

#account[expand] .image {
    width: 3.2rem;
    height: 3.2rem;
    border-radius: 100%;
    border: solid 1px var(--nav-fg);
}

#account > .element {
    display: none;
}

#account[expand] > .element {
    display: flex;
    flex-direction: row;
    font-weight: bold;
    cursor: pointer;
}

#account[expand] > .element > .pillar {
    visibility: hidden;
    flex-grow: 1;
}

#account[expand] > .element > span {
    font-size: 1rem;
    font-weight: 500;
    align-content: center;
    width: 4rem;
}

#account[expand] .icon {
    width: 1.75rem;
    margin-inline-end: 0.5rem;
}

#account .name {
    font-size: 1.0rem;
    font-weight: 500;
    margin-left: 0.5rem;
    cursor: pointer;
}

#account[expand] .name {
    font-weight: normal;
    margin-left: 1rem;
    cursor: default;
}

#account:hover {
    background: var(--nav-button-bg-hover);
}

#account:hover .name {
    text-decoration: underline;
}

#account[expand]:hover .name {
    text-decoration: none;
}

#account[expand] .element:hover {
    text-decoration: underline;
}

#nav-bottom {
    position: absolute;
    top: 5rem;
    left: 0;
    width: 100%;
    height: calc(100% - 5rem);
    z-index: 19000000;
}

#nav-bottom .menu-narrow {
    position: absolute;
    top: -100%;
    left: 0;
    width: 100%;
    background: var(--nav-bg);
    pointer-events: all;
    overflow-x: hidden;
    opacity: 0;
    transition: top 0.2s ease-out, opacity 0.1s ease-out;
}

#nav-bottom .menu-narrow.show {
    top: 0;
    max-height: 100%;
    overflow-x: auto;
    opacity: 1;
    transition: top 0.2s ease-out, opacity 0.2s ease-out;
}

#nav-bottom .menu-narrow .element {
    display: block;
    width: calc(100% - 4rem);
    padding: 1rem 2rem;
    border-bottom: solid 1px var(--nav-fg);
}

#nav-bottom .menu-narrow .element:first-child {
    border-top: solid 1px var(--nav-fg);
}

#nav-bottom .menu-narrow .element.dropdown > .content {
    display: none;
}

#nav-bottom .menu-narrow .element.dropdown[opened] > .content {
    display: block;
    padding: 1rem 1rem 0 1rem;
    top: 2rem;
    left: -0.75rem;
}

#nav-bottom .menu-narrow .element.dropdown[opened] > label > .arrow {
    transform: rotate(180deg);
}

#nav-bottom .menu-narrow .element.dropdown > .content > a {
    display: flex;
    font-size: 1.25rem;
    font-weight: 500;
    line-height: 1.25rem;
    margin-top: 0.75rem;
    cursor: pointer;
    justify-content: flex-start;
    align-items: center;
}

#nav-bottom .menu-narrow .element.dropdown > .content > a:first-child {
    margin-top: 0;
}

#nav-bottom .menu-narrow .element.dropdown > .content > a span {
    margin-left: 0.35rem;
}

#nav-bottom .menu-narrow .element.dropdown > .content > a:hover label {
    text-decoration: underline;
    cursor: pointer;
}

@media (max-width: 1200px) {
    #nav-top > .center {
        display: none;
    }

    #button-nav-narrow {
        display: block;
    }

    #button-nav-narrow.hidden {
        display: none;
    }
}

@media (max-width: 900px) {
    #nav-top > .left {
        padding-left: 1rem;
    }

    #nav-top > .right {
        padding-right: 1rem;
    }

    #nav-bottom .menu-narrow .element {
        width: calc(100% - 2rem);
        padding: 1rem 1rem;
    }
}

@media (max-width: 600px) {
    #nav-top {
        height: 4rem;
    }

    #nav-top > .left > .logo > .text {
        display: none;
    }

    #nav-bottom {
        top: 4rem;
        height: calc(100% - 4rem);
    }

    #nav-bottom .menu-narrow.show {
        height: 100%;
    }
}

@media print {
    #nav-top {
        display: none;
    }
}
</style>
