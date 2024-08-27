<script setup>
import OpsLayout from "@/components/layout/OpsLayout.vue";
import {BBadge} from "bootstrap-vue-next";

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

const stats = {
    flight_count: 55,
    flight_hours: 120,
    rating: "#1",
    rank: "First Officer",
};

// todo: fetch data from server
</script>

<template>
    <OpsLayout>
        <h3 id="title">Dashboard</h3>
        <div id="grid-widget">
            <!--            <div class="card card-lg">-->
            <!--                <h5 class="card-header">Roster</h5>-->
            <!--                <div class="card-body">-->
            <!--                    <table class="table table-hover">-->
            <!--                        <thead>-->
            <!--                        <tr>-->
            <!--                            <th scope="col">Flight #</th>-->
            <!--                            <th scope="col">From</th>-->
            <!--                            <th scope="col">To</th>-->
            <!--                            <th scope="col">Departs In</th>-->
            <!--                        </tr>-->
            <!--                        </thead>-->
            <!--                        <tbody class="table-group-divider">-->
            <!--                        <tr>-->
            <!--                            <th scope="row">NR101</th>-->
            <!--                            <td>RKSI</td>-->
            <!--                            <td>RJAA</td>-->
            <!--                            <td>50 minutes</td>-->
            <!--                        </tr>-->
            <!--                        <tr>-->
            <!--                            <th scope="row">NR102</th>-->
            <!--                            <td>RJAA</td>-->
            <!--                            <td>KLAX</td>-->
            <!--                            <td>2 days</td>-->
            <!--                        </tr>-->
            <!--                        <tr>-->
            <!--                            <th scope="row">NR103</th>-->
            <!--                            <td>KLAX</td>-->
            <!--                            <td>KLAS</td>-->
            <!--                            <td>4 days</td>-->
            <!--                        </tr>-->
            <!--                        </tbody>-->
            <!--                    </table>-->
            <!--                    <div class="d-flex justify-content-between align-items-center">-->
            <!--                        <small>These are the flights you need to fly.</small>-->
            <!--                        <a href="#" class="btn btn-sm btn-primary">Manage</a>-->
            <!--                    </div>-->
            <!--                </div>-->
            <!--            </div>-->

            <div class="card card-lg">
                <h5 class="card-header">Duty Roster</h5>
                <div class="card-body">
                    <div class="list-group">
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 mb-1 justify-content-between align-items-start">
                                <h5>NR101</h5>
                                <span class="badge text-bg-warning">Departs in 50 min</span>
                            </div>
                            <div class="small mb-2">RKSI &rightarrow; RJAA</div>
                            <div class="small">09:00 ~ 11:30</div>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 mb-1 justify-content-between align-items-start">
                                <h5>NR102</h5>
                                <span class="badge text-bg-light">Departs in 2 days</span>
                            </div>
                            <div class="small mb-2">RJAA &rightarrow; KLAX</div>
                            <div class="small">05:00 ~ 10:00</div>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 mb-1 justify-content-between align-items-start">
                                <h5>NR103</h5>
                                <span class="badge text-bg-light">Departs in 4 days</span>
                            </div>
                            <div class="small mb-2">KLAX &rightarrow; KLAS</div>
                            <div class="small">21:00 ~ 22:00</div>
                        </a>
                    </div>
                </div>
            </div>

            <div class="card">
                <h5 class="card-header">NOTAM</h5>
                <div class="card-body">
                    <BAccordion>
                        <BAccordionItem v-for="(notam, index) in notams" :key="index" :title="notam.title">
                            <template #title>
                                <div class="d-flex justify-content-between align-items-center w-100">
                                    <span>{{ notam.title }}</span>
                                    <BBadge v-if="notam.isNew" variant="danger" class="ml-2">New</BBadge>
                                </div>
                            </template>
                            <div class="bg-white rounded p-3 shadow">
                                <span class="small text-muted"><i class="fas fa-clock mr-1"></i>
                                    {{ notam.date }}
                                </span>
                                <p class="text-small mt-2 font-weight-light">{{ notam.description }}</p>
                            </div>
                        </BAccordionItem>
                    </BAccordion>
                </div>
            </div>

            <div class="card">
                <h5 class="card-header">Stats</h5>
                <div class="card-body">
                    <div id="grid-stats">
                        <div class="stat-item">
                            <div class="stat-icon blue">
                                <span class="material-symbols-outlined">airlines</span>
                            </div>
                            <div class="stat-info">
                                <h2 class="stat-value">{{ stats.flight_count }}</h2>
                                <p class="stat-label">Flights</p>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon yellow">
                                <span class="material-symbols-outlined">timer</span>
                            </div>
                            <div class="stat-info">
                                <h2 class="stat-value">{{ stats.flight_hours }}</h2>
                                <p class="stat-label">Flight hours</p>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon green">
                                <span class="material-symbols-outlined">leaderboard</span>
                            </div>
                            <div class="stat-info">
                                <h2 class="stat-value">{{ stats.rating }}</h2>
                                <p class="stat-label">Rating</p>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon orange">
                                <span class="material-symbols-outlined">military_tech</span>
                            </div>
                            <div class="stat-info">
                                <h2 class="stat-value-sm">{{ stats.rank }}</h2>
                                <p class="stat-label">Rank</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </OpsLayout>
</template>

<style scoped>
#grid-widget {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: start;
    gap: 1rem 1rem;
}

#title {
    margin-bottom: 2rem;
}

/* NOTAM */

.card-body {
    max-height: 500px;
    overflow-y: auto;
}


/* Stats */

#grid-stats {
    display: grid;
    grid-auto-columns: minmax(0, 1fr);
    grid-gap: 1rem 1rem;
}

.stat-item {
    background-color: #fafafa;
    border: 1px solid rgba(0, 0, 0, 0.3);
    border-radius: 15px;
    padding: 20px;
    display: flex;
    align-items: center;
    //box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.15);
}

.stat-item:nth-child(4) {
    grid-column: 2;
}

.stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
}

.stat-value {
    font-size: 18px;
    font-weight: bold;
    margin: 0;
    line-height: 1.2;
}

.stat-value-sm {
    font-size: 14px;
    font-weight: bold;
    margin: 0;
    line-height: 1.2;
}

.stat-label {
    font-size: 14px;
    color: #666;
    margin: 0;
}


/* Magic values */

.orange {
    background-color: #FFE5D3;
}

.green {
    background-color: #E8F5E9;
}

.blue {
    background-color: #E3F2FD;
}

.yellow {
    background-color: #FFF8E1;
}

.card-sm {
    width: 15rem;
}

.card-md {
    width: 20rem;
}

.card-lg {
    width: 30rem;
}
</style>
