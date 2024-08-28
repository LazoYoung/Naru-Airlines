<script setup>
const stats = {
    flight_count: 55,
    flight_hours: 120,
    rating: "#3",
    rank: "First Officer",
};
</script>

<template>
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
                <span class="material-symbols-outlined">military_tech</span>
            </div>
            <div class="stat-info">
                <h2 class="stat-value-sm">{{ stats.rank }}</h2>
                <p class="stat-label">Rank</p>
            </div>
        </div>
        <div class="stat-item">
            <div class="stat-icon orange">
                <span class="material-symbols-outlined">leaderboard</span>
            </div>
            <div class="stat-info">
                <h2 class="stat-value">{{ stats.rating }}</h2>
                <p class="stat-label">Rating</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
#grid-stats {
    display: grid;
    grid-auto-columns: minmax(0, 1fr);
    grid-gap: 1rem 1rem;
}

.stat-icon {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.75rem;
}

.stat-item {
    background-color: #f3f3f3;
    border: 1px solid rgba(202, 202, 202, 0.7);
    border-radius: 0.5rem;
    padding: 1.25rem 0.75rem;
    display: flex;
    align-items: center;
    //box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.15);
}

.stat-item:nth-child(4) {
    grid-column: 2;
}

.stat-value {
    font-size: 1rem;
    font-weight: bold;
    margin: 0;
    line-height: 1.2;
}

.stat-value-sm {
    font-size: 0.8rem;
    font-weight: bold;
    margin: 0;
    line-height: 1.2;
}

.stat-label {
    font-size: 0.8rem;
    color: #666;
    margin: 0;
}

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
</style>
