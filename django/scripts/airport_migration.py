import csv

from django.db import IntegrityError
from tqdm import tqdm

from flight.models import Airport


def run():
    file_path = "static/airports.csv"
    allowed_types = ["medium_airport", "large_airport"]
    lines = get_lines(file_path)
    count = 0
    skip = 0

    with open(file_path, 'r', encoding="UTF-8") as file:
        reader = csv.DictReader(file)

        for row in tqdm(reader, total=(lines - 1)):
            if not row["iata_code"] or row["type"] not in allowed_types:
                continue

            try:
                Airport.objects.create(
                    name=row["name"],
                    icao_code=row["ident"],
                    iata_code=row["iata_code"],
                    iso_country=row["iso_country"],
                    city=row["municipality"],
                    latitude=row["latitude_deg"],
                    longitude=row["longitude_deg"],
                )
                count += 1
            except IntegrityError:
                skip += 1

    if skip:
        print(f"{skip} items were skipped.")

    if count:
        print(f"{count} new airports were migrated.")
    else:
        print("No airports were migrated.")


def get_lines(file_path):
    with open(file_path, "rb") as f:
        num_lines = sum(1 for _ in f)
    return num_lines
