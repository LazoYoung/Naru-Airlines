import csv

from tqdm import tqdm

from flight.models import Airport


# noinspection PyTypeChecker
def run():
    file_path = "scripts/airports.csv"
    allowed_types = ["medium_airport", "large_airport"]
    lines = get_lines(file_path)

    with open(file_path, 'r', encoding="UTF-8") as file:
        reader = csv.DictReader(file)
        airports = []

        for row in tqdm(reader, total=(lines - 1)):
            if not row["iata_code"] or row["type"] not in allowed_types:
                continue

            instance = Airport(
                name=row["name"],
                icao_code=row["ident"],
                iata_code=row["iata_code"],
                iso_country=row["iso_country"],
                city=row["municipality"],
                latitude=row["latitude_deg"],
                longitude=row["longitude_deg"],
            )
            airports.append(instance)

        bulk = Airport.objects.bulk_create(airports)
        print(f"Inserted {len(bulk)} airports into DB.")


def get_lines(file_path):
    with open(file_path, "rb") as f:
        num_lines = sum(1 for _ in f)
    return num_lines
