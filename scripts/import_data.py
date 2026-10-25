"""Convert the official SEAP source exports listed in data/source_manifest.json to Parquet."""

from __future__ import annotations

import json
import re
import tempfile
import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest.json"
OUT = ROOT / "data" / "processed"


def load_source(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("rb") as stream:
            header_bytes = stream.readline()
            sample_bytes = header_bytes + stream.read(1_000_000)
        try:
            sample_bytes.decode("utf-8-sig")
            encoding = "utf-8-sig"
        except UnicodeDecodeError:
            # Older Romanian catalog exports may use a Windows code page.
            sample_bytes.decode("cp1250", errors="replace")
            encoding = "cp1250"
        first_line = header_bytes.decode(encoding, errors="replace").lstrip("\ufeff")

        if first_line.startswith("|NUMAR_ACHIZITIE_DIRECTA|"):
            frame = load_2024_direct_csv(path)
        elif "|,|" in first_line:
            # These catalog CSVs wrap every field in pipes but leave numeric
            # amounts unwrapped, with comma separators between the amounts.
            with tempfile.TemporaryFile(mode="w+t", encoding="utf-8", newline="") as normalized:
                with path.open(encoding=encoding, errors="replace", newline="") as source:
                    expected_fields = first_line.count("|,|") + 1
                    pending = ""
                    for physical_line in source:
                        pending += physical_line
                        line = re.sub(
                            r"\|,(-?\d*(?:\.\d+)?),(-?\d*(?:\.\d+)?),\|",
                            "\x1f\\1\x1f\\2\x1f",
                            pending,
                        ).replace("|,|", "\x1f")
                        if len(line.rstrip("\r\n").split("\x1f")) < expected_fields:
                            continue
                        normalized.write(re.sub(r"[\r\n]+", " ", line).rstrip() + "\n")
                        pending = ""
                    if pending:
                        normalized.write(re.sub(r"[\r\n]+", " ", pending.replace("|,|", "\x1f")).rstrip() + "\n")
                normalized.seek(0)
                frame = pd.read_csv(
                    normalized,
                    dtype="string",
                    sep="\x1f",
                    quoting=csv.QUOTE_NONE,
                    keep_default_na=False,
                    low_memory=False,
                )
            frame.columns = [str(column).strip().strip("|") for column in frame.columns]
            for column in frame.columns:
                frame[column] = frame[column].str.strip().str.strip("|")
        elif "^" in first_line:
            expected_fields = first_line.count("^") + 1
            with tempfile.TemporaryFile(mode="w+t", encoding="utf-8", newline="") as normalized:
                with path.open(encoding=encoding, errors="replace", newline="") as source:
                    pending = ""
                    for physical_line in source:
                        pending += physical_line
                        if pending.count("^") < expected_fields - 1:
                            continue
                        fields = pending.rstrip("\r\n").split("^")
                        if len(fields) > expected_fields:
                            fields = fields[: expected_fields - 2] + [
                                " ".join(fields[expected_fields - 2 : -1]),
                                fields[-1],
                            ]
                        normalized.write("^".join(fields).replace("\r", " ").replace("\n", " ") + "\n")
                        pending = ""
                    if pending:
                        normalized.write(pending.rstrip("\r\n").replace("\r", " ").replace("\n", " ") + "\n")
                normalized.seek(0)
                frame = pd.read_csv(
                    normalized,
                    dtype="string",
                    sep="^",
                    quoting=csv.QUOTE_NONE,
                    keep_default_na=False,
                    low_memory=False,
                )
            frame.columns = [str(column).strip() for column in frame.columns]
            for column in frame.columns:
                frame[column] = frame[column].str.strip()
        else:
            delimiter = ","
            if "|,|" not in first_line:
                counts = {candidate: first_line.count(candidate) for candidate in ("|", "^", ";", "\t", ",")}
                delimiter = max(counts, key=counts.get)
            frame = pd.read_csv(
                path,
                dtype="string",
                encoding=encoding,
                encoding_errors="replace",
                sep=delimiter,
                keep_default_na=False,
                low_memory=False,
            )
            frame.columns = [str(column).strip().strip("|") for column in frame.columns]
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
            sheet_frame = sheet_frame.loc[:, ~sheet_frame.columns.astype(str).str.match(r"^Unnamed")].copy()
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
            if line.startswith("|DENUMIRE_AC|,|CUI_AC|,|COD_NUTS|,|DENUMIRE_NUTS|"):
                # A 2022 Q2 direct-purchase export has a second, appended
                # contracts table; contracts are imported from their own
                # catalog resources instead of mixing record types here.
                break
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
        target = OUT / resource["kind"] / f"year={resource['year']}" / f"quarter={resource['quarter']}.parquet"
        expected_size = resource.get("size_bytes")
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        if expected_size and source_path.stat().st_size != expected_size:
            raise ValueError(
                f"Incomplete source {source_path}: {source_path.stat().st_size} "
                f"bytes; expected {expected_size}"
            )

        if target.is_file():
            existing = pd.read_parquet(target)
            if "source_resource_id" in existing and existing["source_resource_id"].eq(resource["resource_id"]).all():
                source_columns = [
                    column
                    for column in existing.columns
                    if column not in {"source_year", "source_quarter", "record_type", "source_resource_id", "source_file", "source_sheet"}
                ]
                outputs[resource["kind"]] = outputs.get(resource["kind"], 0) + len(existing)
                audit.append(
                    {
                        "year": resource["year"],
                        "quarter": resource["quarter"],
                        "record_type": resource["kind"],
                        "source_file": source_path.name,
                        "source_resource_id": resource["resource_id"],
                        "rows": len(existing),
                        "columns": len(source_columns),
                        "field_names": source_columns,
                        "null_cells": int(existing.isna().sum().sum()),
                        "source_bytes": source_path.stat().st_size,
                        "parquet_file": str(target.relative_to(ROOT)),
                        "parquet_bytes": target.stat().st_size,
                    }
                )
                print(f"{resource['year']} {resource['quarter']} {resource['kind']}: {len(existing):,} rows (reused)", flush=True)
                continue

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
