<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { fetchProfile, getGravatarHash, home, useForm } from '@/api';
import IconBanner from '@/components/icon/IconBanner.vue';
import IconLogo from '@/components/icon/IconLogo.vue';
import BasicMenu from '@/components/menu/BasicMenu.vue';
import PilotMenu from '@/components/menu/PilotMenu.vue';

const profile = ref(null);
const nav = ref(null);
const menu = ref(null);
const menuButton = ref(null);

defineProps({
    pilot: {
        type: Boolean,
        default: false,
    },
});

onMounted(() => {
    fetchProfile(profile);
});

function getProfileImageSource() {
    let hash = getGravatarHash(profile.value['email']);
    return `https://www.gravatar.com/avatar/${hash}?s=512`;
}

function openAccount() {
    const account = document.querySelector(`#nav > .head .right > .account`);
    account.setAttribute('state', 'open');

    const bg = document.querySelector(`#nav > .bg`);
    bg.setAttribute('state', 'open');
}

function closeAccount() {
    const account = document.querySelector(`#nav > .head .right > .account`);
    account.setAttribute('state', 'close');

    const bg = document.querySelector(`#nav > .bg`);
    bg.setAttribute('state', 'close');
}

function toggleAccount() {
    const account = document.querySelector(`#nav > .head .right > .account`);
    if (account.getAttribute('state') === 'close') {
        openAccount();
    } else {
        closeAccount();
    }
}

function openMenu(menuName) {
    for (const menuElement of document.querySelectorAll(
        `#nav > .menus .card-sm`
    )) {
        if (menuElement.getAttribute('menu') === menuName) {
            menuElement.setAttribute('state', 'open');
        } else {
            menuElement.setAttribute('state', 'close');
        }
    }
}

function closeMenu() {
    openMenu(null);
}

function openSidebar() {
    const menus = document.querySelector(`#nav > .menus`);
    menus.setAttribute('state', 'open');
    menuButton.value.setAttribute('state', 'open');
}

function closeSidebar() {
    const menus = document.querySelector(`#nav > .menus`);
    menus.setAttribute('state', 'close');
    menuButton.value.setAttribute('state', 'close');
}

function toggleSidebar() {
    const menus = document.querySelector(`#nav > .menus`);
    if (menus.getAttribute('state') == 'close') {
        openSidebar();
    } else {
        closeSidebar();
    }
}

function closeAll() {
    closeMenu();
    closeSidebar();
    try {
        closeAccount();
    } catch (ignored) {}
}

function logout() {
    useForm()
        .submitPost('/api/logout/')
        .then((response) => {
            if (response.ok) {
                closeAll();
                home();
            }
        });
}
</script>

<template>
    <nav id="nav" @mouseleave="closeMenu" ref="nav">
        <div class="bg" state="close" @click="closeAccount"></div>
        <div class="head">
            <outwrapper>
                <inwrapper>
                    <div class="left">
                        <div
                            class="button"
                            state="opecn"
                            ref="menuButton"
                            @click="toggleSidebar"
                        >
                            <div class="line top"></div>
                            <div class="line bottom"></div>
                        </div>
                    </div>
                    <div class="center">
                        <RouterLink
                            class="logo"
                            :to="{ name: 'home' }"
                            @click.stop="closeAll"
                        >
                            <img class="stat-icon" src="@/assets/logo.svg" alt="Logo" />
                        </RouterLink>
                    </div>
                    <div class="right">
                        <div class="search"></div>
                        <div v-if="profile" class="account" state="close">
                            <div class="profile" @click="toggleAccount">
                                <div class="image">
                                    <img
                                        :src="getProfileImageSource()"
                                        :alt="
                                            profile['display_name'] +
                                            `'s profile image`
                                        "
                                    />
                                </div>
                                <div class="name">
                                    {{ profile['display_name'] }}
                                </div>
                            </div>
                            <div class="dropdown">
                                <RouterLink
                                    class="button"
                                    :to="{ name: 'passport' }"
                                    @click.stop="closeAll"
                                >
                                    <div class="stat-icon">
                                        <span class="material-symbols-outlined">
                                            person_book
                                        </span>
                                    </div>
                                    <div class="text">My Passport</div>
                                </RouterLink>
                                <RouterLink
                                    class="button"
                                    :to="{ name: 'settings' }"
                                    @click.stop="closeAll"
                                >
                                    <div class="stat-icon">
                                        <span class="material-symbols-outlined">
                                            settings
                                        </span>
                                    </div>
                                    <div class="text">Settings</div>
                                </RouterLink>
                                <div class="button" @click="logout">
                                    <div class="stat-icon">
                                        <span class="material-symbols-outlined">
                                            logout
                                        </span>
                                    </div>
                                    <div class="text">Logout</div>
                                </div>
                            </div>
                        </div>
                        <div v-else class="guest">
                            <RouterLink
                                class="login"
                                :to="{ name: 'login' }"
                                @click.stop="closeAll"
                            >
                                Login
                            </RouterLink>
                            <RouterLink
                                class="signup"
                                :to="{ name: 'register' }"
                                @click.stop="closeAll"
                            >
                                Sign up
                            </RouterLink>
                        </div>
                    </div>
                </inwrapper>
            </outwrapper>
        </div>
        <div class="menus" state="close">
            <outwrapper>
                <inwrapper>
                    <div class="card-sm" menu="m1" state="close">
                        <div class="button" @mouseover="openMenu(`m1`)">
                            Booking
                        </div>
                        <div class="dropdown">
                            <div class="bg"></div>
                            <RouterLink
                                class="button"
                                :to="{ name: 'home' }"
                                @click.stop="closeAll"
                            >
                                Menu 1 name is super long
                            </RouterLink>
                            <RouterLink
                                class="button"
                                :to="{ name: 'home' }"
                                @click.stop="closeAll"
                            >
                                Menu 2
                            </RouterLink>
                            <RouterLink
                                class="button"
                                :to="{ name: 'home' }"
                                @click.stop="closeAll"
                            >
                                Menu 3
                            </RouterLink>
                        </div>
                    </div>
                    <div class="card-sm" menu="m2" state="close">
                        <div class="button" @mouseover="openMenu(`m2`)">
                            Lounge
                        </div>
                        <div class="dropdown">
                            <div class="bg"></div>
                            <RouterLink
                                class="button"
                                :to="{ name: 'home' }"
                                @click.stop="closeAll"
                            >
                                aaaaaaaaaaaaaa
                            </RouterLink>
                            <RouterLink
                                class="button"
                                :to="{ name: 'home' }"
                                @click.stop="closeAll"
                            >
                                bbbbbbbbbbb
                            </RouterLink>
                            <RouterLink
                                class="button"
                                :to="{ name: 'home' }"
                                @click.stop="closeAll"
                            >
                                ccccccccccccccccccc
                            </RouterLink>
                        </div>
                    </div>
                    <div class="card-sm" menu="m3" state="close">
                        <div class="button" @mouseover="openMenu(`m3`)">
                            Operations
                        </div>
                        <div class="dropdown">
                            <div class="bg"></div>
                            <RouterLink
                                class="button"
                                :to="{ name: 'dashboard' }"
                                @click.stop="closeAll"
                            >
                                Ops Center
                            </RouterLink>
                        </div>
                    </div>
                </inwrapper>
            </outwrapper>
        </div>
    </nav>
    <section id="nav-margin"></section>
</template>

<style>
a {
    text-decoration: none;
}

span, div {
    user-select: none;
}

#nav {
    position: static;
    width: 100%;
    z-index: 20000000;
    pointer-events: none;
    user-select: none;
}
#nav-margin {
    width: 100%;
    height: 0;
}

#nav > .bg {
    position: absolute;
    width: 100%;
    height: 100vh;
    z-index: 30000000;
    backdrop-filter: blur(10px);
    pointer-events: all;
    transition: opacity 0.1s ease-out;
}
#nav > .bg[state='close'] {
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease-out;
}

#nav > .head {
    width: 100%;
    height: 4rem;
    background: rgb(240, 240, 240);
    pointer-events: all;
    z-index: 10000000;
}
#nav > .head outwrapper,
#nav > .head inwrapper {
    height: 100%;
}
#nav > .head inwrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}
#nav > .head .left,
#nav > .head .center,
#nav > .head .right {
    flex: 1;
    height: 100%;
}
#nav > .head .left {
    align-items: center;
    display: none;
}
#nav > .head .left > .button {
    position: relative;
    width: 3rem;
    height: 3rem;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: -0.5rem;
    cursor: pointer;
}
#nav > .head .left > .button > .line {
    position: absolute;
    width: 2rem;
    height: 2px;
    background: black;
}
#nav > .head .left > .button > .line.top {
    margin-bottom: 0.75rem;
}
#nav > .head .left > .button > .line.bottom {
    margin-top: 0.75rem;
}
#nav > .head .left > .button[state='open'] > .line.top {
    margin: 0;
    transform: rotate(45deg);
}
#nav > .head .left > .button[state='open'] > .line.bottom {
    margin: 0;
    transform: rotate(-45deg);
}
#nav > .head .center {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}
#nav > .head .center > .logo {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    height: 2rem;
}
#nav > .head .center > .logo > img {
    height: 100%;
}
#nav > .head .right {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    position: relative;
}
#nav > .head .right > .account {
    top: 1rem;
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    background: white;
    border-radius: 1.25rem;
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
    z-index: 50000000;
    overflow: hidden;
    max-width: 12rem;
}
#nav > .head .right > .account > .profile {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    height: 2.5rem;
    cursor: pointer;
}
#nav > .head .right > .account[state='open'] > .profile {
    width: 100%;
}
#nav > .head .right > .account > .profile > .image {
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
#nav > .head .right > .account > .profile > .image > img {
    width: 1.75rem;
    height: 1.75rem;
    background: rgb(240, 240, 240);
    border-radius: 100% 100%;
    border: solid 1px rgb(240, 240, 240);
}
#nav > .head .right > .account > .profile > .name {
    font-size: 1rem;
    font-weight: 600;
    padding-right: 1rem;
    color: black;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    display: flex;
    align-items: center;
    line-height: 1rem;
    margin-top: 1px;
}
#nav > .head .right > .guest {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    gap: 1rem;
}
#nav > .head .right > .account > .dropdown {
    width: 12rem;
    height: calc(7.5rem + 0.25rem);
    overflow: hidden;
    border-top: solid 1px rgb(210, 210, 210);
    transition: width 0.1s ease-out, height 0.1s ease-out;
    white-space: nowrap;
}
#nav > .head .right > .account[state='close'] > .dropdown {
    width: 0;
    height: 0;
    transition: width 0.2s ease-out, height 0.1s ease-out;
}
#nav > .head .right > .account > .dropdown > .button {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    cursor: pointer;
}
#nav > .head .right > .account > .dropdown > .button > .stat-icon,
#nav > .head .right > .account > .dropdown > .button > .text {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 2.5rem;
}
#nav > .head .right > .account > .dropdown > .button > .stat-icon {
    width: 2.5rem;
}
#nav > .head .right > .account > .dropdown > .button > .stat-icon > span {
    font-size: 1.25rem;
    font-weight: 600;
    padding-left: 1px;
    color: rgb(100, 100, 100);
}
#nav > .head .right > .account > .dropdown > .button > .text {
    font-size: 1rem;
    font-weight: 600;
    color: rgb(100, 100, 100);
}
#nav > .head .right > .account > .dropdown > .button:last-child {
    height: 3rem;
    padding-bottom: 0.5rem;
}
#nav > .head .right > .account > .dropdown > .button:hover {
    background: rgb(240, 240, 240);
}
#nav > .head .right > .account > .dropdown > .button:hover > .stat-icon > span {
    color: black;
}
#nav > .head .right > .account > .dropdown > .button:hover > .text {
    color: black;
}
#nav > .head .right > .guest {
    height: 100%;
    display: flex;
    align-items: flex-start;
    padding-top: 1rem;
}
#nav > .head .right > .guest > .login,
#nav > .head .right > .guest > .signup {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 2rem;
    height: 2.5rem;
    background: white;
    color: black;
    border-radius: 1000px;
    font-size: 1rem;
    font-weight: 600;
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
}
#nav > .head .right > .guest > .signup {
    background: #003468;
    color: white;
}
@media screen and (max-width: 900px) {
    #nav {
        position: fixed;
    }
    #nav-margin {
        height: 7rem;
    }
}
@media screen and (max-width: 600px) {
    #nav-margin {
        height: 4.5rem;
    }
    #nav > .head {
        height: 4.5rem;
        border-bottom: solid 1px rgb(210, 210, 210);
    }
    #nav > .head .left {
        display: flex;
    }
    #nav > .head .center {
        padding-bottom: 0.5rem;
    }
    #nav > .head .center > .logo {
        height: 1.5rem;
    }
    #nav > .head .right > .account {
        top: 1rem;
        position: absolute;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        background: white;
        border-radius: 1.25rem;
        box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
        z-index: 50000000;
        overflow: hidden;
        max-width: 12rem;
    }
    #nav > .head .right > .account > .profile > .name {
        width: 0;
        padding-right: 0;
    }
    #nav > .head .right > .account[state='open'] > .profile > .name {
        width: unset;
        padding-right: 1rem;
    }
    #nav > .head .right > .guest > .signup {
        display: none;
    }
}

#nav > .menus {
    background: rgb(240, 240, 240);
    pointer-events: all;
    height: 3rem;
    padding-top: 0.35rem;
    border-bottom: solid 1px rgb(210, 210, 210);
}
#nav > .menus inwrapper {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 6rem;
}
#nav > .menus .card-sm > .button {
    display: inline-block;
    height: 2.65rem;
    font-size: 1.5rem;
    font-weight: 500;
    color: rgb(128, 128, 128);
    cursor: pointer;
}
#nav > .menus .card-sm > .button:hover,
#nav > .menus .card-sm[state='open'] > .button {
    color: black;
    border-bottom: solid 2px black;
}
#nav > .menus .card-sm > .dropdown {
    position: fixed;
    width: 100%;
    padding-top: 1rem;
    padding-bottom: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 1rem;
    z-index: 10000000;
}
#nav > .menus .card-sm[state='close'] > .dropdown {
    display: none;
}
#nav > .menus .card-sm > .dropdown > .button {
    font-size: 1.25rem;
    z-index: 10000000;
}
#nav > .menus .card-sm > .dropdown > .bg {
    position: absolute;
    top: 0;
    left: -100%;
    width: 300%;
    height: 100%;
    background: rgb(240, 240, 240);
    border-bottom: solid 1px rgb(210, 210, 210);
}
@media screen and (max-width: 600px) {
    #nav > .menus {
        position: fixed;
        width: 100%;
        left: 0;
        height: auto;
        padding-top: 0;
        border-bottom: none;
    }
    #nav > .menus[state='close'] {
        display: none;
    }
    #nav > .menus outwrapper {
        padding: 0;
    }
    #nav > .menus inwrapper {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 0rem;
    }
    #nav > .menus .card-sm {
        width: 100%;
        border-bottom: solid 1px rgb(210, 210, 210);
    }
    #nav > .menus .card-sm[state='close'] {
        display: block;
    }
    #nav > .menus .card-sm > .button,
    #nav > .menus .card-sm > .button:hover,
    #nav > .menus .card-sm[state='open'] > .button {
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
        padding: 0 1rem;
        width: 100%;
        height: 2.5rem;
        font-size: 1.5rem;
        font-weight: 500;
        color: black;
        border-bottom: none;
        cursor: default;
    }
    #nav > .menus .card-sm[state='close'] > .dropdown,
    #nav > .menus .card-sm > .dropdown {
        position: static;
        display: block;
        padding: 1rem 1rem;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    #nav > .menus .card-sm > .dropdown > .bg {
        display: none;
    }
}
</style>
