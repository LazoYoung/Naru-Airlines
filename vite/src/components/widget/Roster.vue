<script setup>

</script>

<template>
    <div class="list-group">
        <RouterLink :to="{name: 'flight', params: {flightNumber: '101'}}" href="#" class="list-group-item list-group-item-action clickable">
            <div class="d-flex w-100 mb-1 justify-content-between align-items-start">
                <h5>NR101</h5>
                <span class="badge text-bg-warning">Departs in 50 min</span>
            </div>
            <div class="small mb-2">RKSI &rightarrow; RJAA</div>
            <div class="small">09:00 ~ 11:30</div>
        </RouterLink>
        <RouterLink :to="{name: 'flight', params: {flightNumber: '102'}}" class="list-group-item list-group-item-action clickable">
            <div class="d-flex w-100 mb-1 justify-content-between align-items-start">
                <h5>NR102</h5>
                <span class="badge text-bg-secondary">Departs in 2 days</span>
            </div>
            <div class="small mb-2">RJAA &rightarrow; KLAX</div>
            <div class="small">05:00 ~ 10:00</div>
        </RouterLink>
        <RouterLink :to="{name: 'flight', params: {flightNumber: '103'}}" class="list-group-item list-group-item-action clickable">
            <div class="d-flex w-100 mb-1 justify-content-between align-items-start">
                <h5>NR103</h5>
                <span class="badge text-bg-secondary">Departs in 4 days</span>
            </div>
            <div class="small mb-2">KLAX &rightarrow; KLAS</div>
            <div class="small">21:00 ~ 22:00</div>
        </RouterLink>
    </div>
</template>

<style scoped>
.clickable:hover,
.clickable:focus {
    background-color: rgb(245, 245, 245);
}
</style>