"""Download the pinned data.gov.ro resources in data/source_manifest.json."""

from __future__ import annotations

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest.json"


def download(resource: dict) -> str:
    target = ROOT / resource["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    expected = resource.get("size_bytes")
    if target.exists() and expected and target.stat().st_size == expected:
        return f"Already present: {target.relative_to(ROOT)}"

    subprocess.run(
        [
            "curl",
            "--fail",
            "--location",
            "--retry",
            "3",
            "--output",
            str(target),
            resource["url"],
        ],
        check=True,
    )
    size = target.stat().st_size
    if expected and size != expected:
        target.unlink(missing_ok=True)
        raise ValueError(f"Size mismatch for {target}: {size} != {expected}")
    return f"Downloaded: {target.relative_to(ROOT)} ({size:,} bytes)"


def main() -> None:
    resources = json.loads(MANIFEST.read_text(encoding="utf-8"))["resources"]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(download, resources):
            print(result, flush=True)


if __name__ == "__main__":
    main()
