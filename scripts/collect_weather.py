"""Opt-in, one-shot nonofficial weather collection to local ignored JSONL file.

Schedule with your OS scheduler only after verifying Open-Meteo license and quotas.
Do not collect identifiable personal locations.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
from civicshield.ingestion.open_meteo import fetch_weather

def save_jsonl(record: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        descriptor = os.open(path, os.O_CREAT | os.O_WRONLY, 0o600)
        os.close(descriptor)
    with path.open("a", encoding="utf-8") as output:
        output.write(json.dumps(record, ensure_ascii=False) + "\n")

async def collect(latitude: float, longitude: float, output: Path):
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError("invalid latitude/longitude")
    record = await fetch_weather(latitude, longitude)
    save_jsonl(record, output)
    return record

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--latitude", type=float, required=True)
    p.add_argument("--longitude", type=float, required=True)
    p.add_argument("--output", type=Path, default=Path("data/raw/open_meteo_history.jsonl"))
    args = p.parse_args()
    record = asyncio.run(collect(args.latitude, args.longitude, args.output))
    print(f"Collected {record['source_type']} record at {record['source_timestamp_utc']}. Never an official alert.")

if __name__ == "__main__":
    main()
