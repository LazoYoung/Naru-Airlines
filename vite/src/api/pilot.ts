import type {Ref} from "vue";

class PilotStat {
    flightCount: number;
    flightHour: number;
    grade: number;
    rank: string;
}

async function fetchStat(ref: Ref<PilotStat | undefined>) {
    const request = await fetch("/api/pilot/stats/");

    if (!request.ok) {
        ref.value = undefined;
        return;
    }

    if (ref.value == null) {
        ref.value = new PilotStat();
    }

    const data = await request.json();
    ref.value.flightCount = data["flight_count"];
    ref.value.flightHour = data["flight_hour"];
    ref.value.grade = data["grade"];
    ref.value.rank = data["rank"];
}

export {PilotStat, fetchStat};
