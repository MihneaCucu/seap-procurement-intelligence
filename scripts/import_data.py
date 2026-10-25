"""Convert the official SEAP source exports listed in data/source_manifest.json to Parquet."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest.json"
OUT = ROOT / "data" / "processed"


def load_source(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as stream:
            first_line = stream.readline()
        if first_line.startswith("|NUMAR_ACHIZITIE_DIRECTA|"):
            frame = load_2024_direct_csv(path)
        else:
            frame = pd.read_csv(
                path,
                dtype="string",
                encoding="utf-8-sig",
                sep=",",
                keep_default_na=False,
                low_memory=False,
            )
            frame.columns = [str(column).strip() for column in frame.columns]
        frame["source_sheet"] = "CSV"
    elif suffix in {".xls", ".xlsx"}:
        sheets = pd.read_excel(
            path,
            sheet_name=None,
            dtype="string",
            engine="xlrd" if suffix == ".xls" else "openpyxl",
        )
        sheet_frames = []
        for sheet_name, sheet_frame in sheets.items():
            sheet_frame = sheet_frame.loc[:, ~sheet_frame.columns.astype(str).str.match(r"^Unnamed")]
            sheet_frame.columns = [str(column).strip() for column in sheet_frame.columns]
            for column in sheet_frame.columns:
                sheet_frame[column] = sheet_frame[column].str.strip()
            sheet_frame["source_sheet"] = sheet_name
            sheet_frames.append(sheet_frame)
        frame = pd.concat(sheet_frames, ignore_index=True, sort=False)
    else:
        raise ValueError(f"Unsupported source format: {path.suffix}")

    # Empty strings become nulls; values otherwise remain untyped at this stage.
    frame = frame.replace(r"^\s*$", pd.NA, regex=True)
    return frame


def load_2024_direct_csv(path: Path) -> pd.DataFrame:
    """Parse the 2024 direct-purchase CSV whose numeric columns are unquoted."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        headers = re.findall(r"\|([^|]*)\|", stream.readline())
        rows = []
        batches = []
        line_number = 1
        for line in stream:
            line_number += 1
            if not line.strip():
                continue
            first_line_number = line_number
            while True:
                matches = list(re.finditer(r"\|([^|]*)\|", line))
                cpv_match = (
                    re.search(r"\|,\|(\d{8}-\d)\|,\|", line[matches[4].end() :])
                    if len(matches) >= 5
                    else None
                )
                if cpv_match:
                    break
                continuation = stream.readline()
                if not continuation or line_number - first_line_number >= 10:
                    raise ValueError(f"Could not complete row beginning at {path}:{first_line_number}")
                line += continuation
                line_number += 1
            if len(matches) < 11:
                raise ValueError(f"Unexpected wrapped field count at {path}:{first_line_number}")
            cpv_start = matches[4].end() + cpv_match.start()
            cpv_end = matches[4].end() + cpv_match.end()
            description = re.sub(r"\s+", " ", line[matches[4].end() : cpv_start].strip().lstrip(",|").strip())
            tail = line[cpv_end:]
            cpv_name, separator, after_cpv_name = tail.partition("|")
            tail_matches = list(re.finditer(r"\|([^|]*)\|", after_cpv_name))
            if not separator or len(tail_matches) < 3:
                raise ValueError(f"Unexpected fields after CPV code at {path}:{first_line_number}")
            amounts_start = tail_matches[0].end()
            amounts_end = tail_matches[1].start()
            amounts = after_cpv_name[amounts_start:amounts_end].strip().strip(",").split(",")
            if len(amounts) != 2:
                raise ValueError(f"Unexpected amount fields at {path}:{first_line_number}")
            rows.append(
                [match.group(1).strip() for match in matches[:5]]
                + [description, cpv_match.group(1)]
                + [cpv_name.strip(), tail_matches[0].group(1).strip()]
                + [value.strip() for value in amounts]
                + [match.group(1).strip() for match in tail_matches[1:3]]
            )
            if len(rows) == 100_000:
                batches.append(pd.DataFrame.from_records(rows, columns=headers, coerce_float=False))
                rows = []
        if rows:
            batches.append(pd.DataFrame.from_records(rows, columns=headers, coerce_float=False))
    return pd.concat(batches, ignore_index=True).astype("string") if batches else pd.DataFrame(columns=headers)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    audit = []
    outputs: dict[str, int] = {}

    for resource in manifest["resources"]:
        source_path = ROOT / resource["path"]
        expected_size = resource.get("size_bytes")
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        if expected_size and source_path.stat().st_size != expected_size:
            raise ValueError(
                f"Incomplete source {source_path}: {source_path.stat().st_size} "
                f"bytes; expected {expected_size}"
            )

        frame = load_source(source_path)
        frame.insert(0, "source_year", int(resource["year"]))
        frame.insert(1, "source_quarter", resource["quarter"])
        frame.insert(2, "record_type", resource["kind"])
        frame.insert(3, "source_resource_id", resource["resource_id"])
        frame.insert(4, "source_file", source_path.name)
        metadata_columns = {
            "source_year",
            "source_quarter",
            "record_type",
            "source_resource_id",
            "source_file",
            "source_sheet",
        }
        source_columns = [column for column in frame.columns if column not in metadata_columns]

        target = OUT / resource["kind"] / f"year={resource['year']}" / f"quarter={resource['quarter']}.parquet"
        target.parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(target, index=False, compression="zstd")

        outputs[resource["kind"]] = outputs.get(resource["kind"], 0) + len(frame)
        audit.append(
            {
                "year": resource["year"],
                "quarter": resource["quarter"],
                "record_type": resource["kind"],
                "source_file": source_path.name,
                "source_resource_id": resource["resource_id"],
                "rows": len(frame),
                "columns": len(source_columns),
                "field_names": source_columns,
                "null_cells": int(frame.isna().sum().sum()),
                "source_bytes": source_path.stat().st_size,
                "parquet_file": str(target.relative_to(ROOT)),
                "parquet_bytes": target.stat().st_size,
            }
        )
        print(f"{resource['year']} {resource['quarter']} {resource['kind']}: {len(frame):,} rows -> {target}", flush=True)

    report = {
        "source": manifest["source"],
        "license": manifest["license"],
        "record_totals": outputs,
        "tables": audit,
        "schema_notes": [
            "Original source field names are retained; schemas vary across years and quarters.",
            "Values remain strings and blanks become nulls; semantic typing and deduplication are pending data profiling.",
            "Direct purchases and published contracts are stored separately.",
        ],
    }
    report_path = OUT / "import_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nTotals: {outputs}")
    print(f"Import report: {report_path}")


if __name__ == "__main__":
    main()
