<script setup>
import {onMounted, ref} from "vue";

class Flight {
    constructor(number, origin, dest, etd, eta) {
        const _MS_PER_MIN = 1000 * 60
        const now = new Date(Date.now());
        const dep_date = this.toZuluDate(etd);
        const arr_date = this.toZuluDate(eta);
        const minutes = Math.floor((dep_date - now) / _MS_PER_MIN);

        if (minutes < 0) {
            this.badge_color = "text-bg-danger";
            this.timer = "Departed";
        } else {
            this.timer = "Departs in " + this.formatDuration(minutes);

            if (minutes < 60) {
                this.badge_color = "text-bg-warning";
            } else {
                this.badge_color = "text-bg-secondary";
            }
        }

        this.dep_zulu = this.formatTime(dep_date) + "z";
        this.arr_zulu = this.formatTime(arr_date) + "z";
        this.number = number;
        this.origin = origin;
        this.dest = dest;
    }

    formatDuration(minutes) {
        let weeks = 0;
        let days = 0;
        let hours = 0;

        if (minutes >= 60) {
            hours = Math.floor(minutes / 60);
            minutes %= 60;
        }

        if (hours >= 24) {
            days = Math.floor(hours / 24);
            hours %= 24;
        }

        if (days >= 7) {
            weeks = Math.floor(days / 7);
            days %= 7;
        }

        if (weeks) {
            return this.formatPlural(weeks, "week", "weeks");
        }

        if (days) {
            return this.formatPlural(days, "day", "days");
        }

        if (hours) {
            return this.formatPlural(hours, "hour", "hours");
        }

        return this.formatPlural(minutes, "minute", "minutes");
    }

    formatPlural(value, singular, plural) {
        return (value > 1) ? `${value} ${plural}` : `${value} ${singular}`;
    }

    formatTime(date, utc = true) {
        let hours = utc ? date.getUTCHours() : date.getHours();
        let minutes = utc ? date.getUTCMinutes() : date.getMinutes();
        let hh = hours.toString().padStart(2, '0');
        let mm = minutes.toString().padStart(2, '0');
        return `${hh}:${mm}`;
    }

    toZuluDate(string) {
        let zulu_time = new Date(string).toISOString();
        return new Date(zulu_time);
    }
}

const flights = ref();

onMounted(() => {
    flights.value = [
        new Flight(101, "RKSI", "RJAA", "2024-09-06T18:00:00.000000+09:00", "2024-09-06T20:30:00.000000+09:00", true),
        new Flight(102, "RJAA", "KLAX", "2024-09-07T14:00:00.000000+09:00", "2024-09-07T19:00:00.000000+09:00"),
        new Flight(103, "KLAX", "KLAS", "2024-09-08T06:00:00.000000+09:00", "2024-09-08T07:00:00.000000+09:00"),
    ];
});
</script>

<template>
    <div class="list-group">
        <RouterLink
                v-for="flight in flights"
                :to="{name: 'flight', params: {flightNumber: flight.number}}"
                href="#"
                class="list-group-item list-group-item-action clickable"
        >
            <div class="d-flex w-100 mb-1 justify-content-between align-items-start">
                <h5>{{ "NR" + flight.number }}</h5>
                <span :class="`badge ` + flight.badge_color">{{ flight.timer }}</span>
            </div>
            <div class="small mb-2">{{ flight.origin + " &rightarrow; " + flight.dest }}</div>
            <div class="small">{{ flight.dep_zulu + " ~ " + flight.arr_zulu }}</div>
        </RouterLink>
    </div>
</template>

<style scoped>
.clickable:hover,
.clickable:focus {
    background-color: rgb(245, 245, 245);
}
</style>
