<script setup>
import Button from '@/components/input/Button.vue';
</script>

<template>
    <section id="booking-new"></section>

    <section id="booking-index">
        <outwrapper>
            <inwrapper>
                <div class="title">
                    <h2>My Bookings</h2>
                </div>
                <div class="index">
                    <div class="booking">
                        <div class="title"></div>
                        <div class="content">
                            <div class="info">
                                <div class="line line1">
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 3)"
                                    >
                                        <div class="key">Booking No.</div>
                                        <div class="value">CXV123</div>
                                    </div>
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 3)"
                                    >
                                        <div class="key">Flight No.</div>
                                        <div class="value">NR 224</div>
                                    </div>
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 6)"
                                    >
                                        <div class="key">Aircraft</div>
                                        <div class="value">Boeing 737-800</div>
                                    </div>
                                </div>
                                <div class="line line2">
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 2.5)"
                                    >
                                        <div class="key">Date</div>
                                        <div class="value">2024-01-01</div>
                                    </div>
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 1.5)"
                                    >
                                        <div class="key">Time</div>
                                        <div class="value">17:30</div>
                                    </div>
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 4)"
                                    >
                                        <div class="key">From</div>
                                        <div class="value">Seoul / ICN</div>
                                    </div>
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 4)"
                                    >
                                        <div class="key">To</div>
                                        <div class="value">New York / JFK</div>
                                    </div>
                                </div>
                                <div class="line line3">
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 8)"
                                    >
                                        <div class="key">Passenger</div>
                                        <div class="value">JO/SUNGWANMR</div>
                                    </div>
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 2)"
                                    >
                                        <div class="key">Class</div>
                                        <div class="value">Economy</div>
                                    </div>
                                    <div
                                        class="set"
                                        style="width: calc(100% / 12 * 2)"
                                    >
                                        <div class="key">Seat</div>
                                        <div class="value">A46</div>
                                    </div>
                                </div>
                            </div>
                            <div class="control">
                                <Button>Print</Button>
                                <Button>Print</Button>
                                <Button color="red">Cancel</Button>
                            </div>
                        </div>
                    </div>
                </div>
            </inwrapper>
        </outwrapper>
    </section>
</template>

<style>
#booking-index .booking {
    width: 100%;
    border: solid 1px rgb(210, 210, 210);
    border-radius: 1.5rem;
    background: rgb(240, 240, 240);
}
#booking-index .booking > .content {
    display: flex;
}
#booking-index .booking > .content > .info {
    width: 80%;
}
#booking-index .booking > .content > .control {
    border-left: solid 1px rgb(210, 210, 210);
    width: 20%;
    padding: 0.75rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
#booking-index .booking > .content > .control > * {
    width: 100%;
}
#booking-index .booking .line {
    display: flex;
}
#booking-index .booking .line > .set {
    display: flex;
    flex-direction: column;
    border-right: solid 1px rgb(210, 210, 210);
}
#booking-index .booking .line > .set > .key {
    font-size: 0.8rem;
    font-weight: 600;
    color: #003468;
    padding-top: 0.75rem;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
}
#booking-index .booking .line > .set > .value {
    font-size: 1.25rem;
    font-weight: 400;
    padding-bottom: 0.75rem;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
}
#booking-index .booking .line > .set:first-child > * {
    padding-left: 1rem;
}
#booking-index .booking .line > .set:last-child {
    border-right: none;
}
#booking-index .booking .line1 {
    border-bottom: solid 1px rgb(210, 210, 210);
}
#booking-index .booking .line2 {
    border-bottom: solid 1px rgb(210, 210, 210);
}
</style>
