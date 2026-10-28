"""Build a deterministic offline ZIP of the static research portfolio.

Only site/ content is packaged: no DB, secrets, API tokens, models, training data,
Python environment or application credentials. The SHA-256 checksum is NOT a
digital signature.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from scripts.verify_site import validate_site, SITE

NAME = "civicshield-static-portfolio-v0.2.0.zip"
STAMP = (1980, 1, 1, 0, 0, 0)

def package_site(output: Path, site: Path = SITE) -> dict:
    # Validate the canonical site before packaging.
    if site.resolve() == SITE.resolve():
        validate_site()
    output.mkdir(parents=True, exist_ok=True)
    zip_path = output / NAME
    sources = sorted(p for p in site.rglob("*") if p.is_file())
    if not sources or not (site / "index.html").is_file():
        raise ValueError("Expected static site with index.html")
    manifest = {
        "type": "civicshield-static-portfolio",
        "version": "0.2.0",
        "not_an_emergency_service": True,
        "offline_visualization": True,
        "contains_real_incident_data": False,
        "files": [],
    }
    total_bytes = 0
    entries = []
    for source in sources:
        if source.is_symlink():
            raise ValueError("Symbolic links cannot be packaged")
        relative = source.relative_to(site).as_posix()
        if relative.startswith(".") or any(part.startswith(".") for part in source.relative_to(site).parts):
            raise ValueError("Hidden files cannot be packaged")
        data = source.read_bytes()
        total_bytes += len(data)
        if total_bytes > 30_000_000:
            raise ValueError("Static portfolio archive is unexpectedly large")
        manifest["files"].append({
            "path": relative, "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
        entries.append((relative, data))
    payload = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    entries.append(("MANIFEST.json", payload))
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, data in entries:
            info = zipfile.ZipInfo(relative, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    checksum = output / (NAME + ".sha256")
    checksum.write_text(f"{digest}  {NAME}\n", encoding="utf-8")
    return {
        "status": "static_portfolio_packaged",
        "zip": str(zip_path),
        "checksum": str(checksum),
        "files": len(sources),
        "external_deployment_verified": False,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist/portfolio"))
    args = parser.parse_args()
    print(json.dumps(package_site(args.output), indent=2))

if __name__ == "__main__":
    main()
