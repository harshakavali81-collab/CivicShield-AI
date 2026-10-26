"""Consistent snapshot for local SQLite demo only. Backups contain private information."""
import argparse
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy.engine import make_url
from backend.app.config import database_url

def backup(destination: str | Path) -> Path:
    parsed = make_url(database_url())
    if parsed.drivername != "sqlite":
        raise RuntimeError("SQLite only; use pg_dump with PostgreSQL")
    src = parsed.database
    if not src or src == ":memory:":
        raise RuntimeError("Cannot snapshot in-memory SQLite")
    target = Path(destination).resolve()
    if not Path(src).exists():
        raise FileNotFoundError(f"Database not found: {src}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite backup: {target}")
    with sqlite3.connect(src) as source, sqlite3.connect(str(target)) as dest:
        source.backup(dest)
    os.chmod(target, 0o600)
    return target

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", default="")
    args = p.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(backup(args.output or f"backups/civicshield-{stamp}.db"))

if __name__ == "__main__":
    main()
