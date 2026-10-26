"""Privacy retention utility. Dry-run by default.

Example: python -m scripts.purge_incidents --days 30
         python -m scripts.purge_incidents --days 30 --confirm
Must be run against the correct DATABASE_URL. Deletion is irreversible.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta, timezone
from sqlalchemy import delete, func, select
from backend.app.db import Incident, SessionLocal

def purge(days: int, confirm: bool = False) -> int:
    if not 1 <= days <= 3650:
        raise ValueError("days must be between 1 and 3650")
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    with SessionLocal() as session:
        count = session.scalar(select(func.count()).select_from(Incident).where(Incident.created_at < cutoff)) or 0
        if confirm and count:
            session.execute(delete(Incident).where(Incident.created_at < cutoff))
            session.commit()
        return count

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    count = purge(args.days, args.confirm)
    print(f"{'Deleted' if args.confirm else 'Would delete'} {count} incidents older than {args.days} days.")

if __name__ == "__main__":
    main()
