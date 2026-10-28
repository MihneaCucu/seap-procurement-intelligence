"""Split the public 32-row CSV into related entities; validate using SQLite.

This processes the reviewed sample only. It does not resolve organization
identities, infer suppliers/items, or transform the full imported collection.
"""
from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = (
    "source_resources", "organizations", "cpv_categories", "procurement_records",
    "procurement_suppliers", "procurement_items", "bnr_exchange_rates", "currency_conversions",
)


def build() -> dict:
    manifest = json.loads((ROOT / "data/source_manifest.json").read_text(encoding="utf-8"))
    resources = {r["resource_id"]: r for r in manifest["resources"]}
    packages = {p["package_id"]: p for p in manifest["datasets"]}
    with (ROOT / "docs/data-sample.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not 20 <= len(rows) <= 50:
        raise ValueError("Expected 20-50 sample rows")
    if any(r["supplier_name"] or r["supplier_identifier"] for r in rows):
        raise ValueError("Supplier identities require review before publishing")
    if any(r[k] for r in rows for k in ("quantity", "quantity_unit", "amount_eur")):
        raise ValueError("Item/conversion evidence must be mapped before adding these values")

    tables = {name: [] for name in TABLES}
    seen_resources = set()
    seen_cpv = set()
    for index, row in enumerate(rows, 1):
        source_id = row["source_resource_id"]
        resource = resources[source_id]
        if row["source_file"] != Path(resource["path"]).name:
            raise ValueError("Source filename does not match manifest")
        if int(row["source_year"]) != int(resource["year"]) or row["source_period"] != resource["quarter"]:
            raise ValueError("Source period does not match manifest")
        expected_type = {"direct": "direct_purchase", "contracts": "published_contract",
                         "contracts_subsequent": "subsequent_contract"}[resource["kind"]]
        if row["record_type"] != expected_type:
            raise ValueError("Record type does not match source")
        if source_id not in seen_resources:
            tables["source_resources"].append({
                "source_resource_id": source_id, "package_id": resource["package_id"],
                "source_file": row["source_file"], "source_url": resource["url"],
                "license_title": packages[resource["package_id"]]["license_title"],
                "source_year": int(row["source_year"]), "source_period": row["source_period"],
            })
            seen_resources.add(source_id)
        # A provisional organization per source row avoids merging by name.
        # These sample IDs are technical references, not verified entity IDs.
        authority_id = f"sample-org-{index:04d}" if row["contracting_authority"] else None
        if authority_id:
            tables["organizations"].append({
                "organization_id": authority_id, "name": row["contracting_authority"],
                "county": row["authority_county"] or None, "identity_status": "unresolved",
            })
        cpv = row["cpv_code"] or None
        if cpv and cpv not in seen_cpv:
            tables["cpv_categories"].append({"cpv_code": cpv, "scheme_version": "unknown"})
            seen_cpv.add(cpv)
        tables["procurement_records"].append({
            "record_id": f"sample-record-{index:04d}", "source_resource_id": source_id,
            "authority_id": authority_id, "authority_name_source": row["contracting_authority"] or None,
            "record_type": row["record_type"], "procurement_reference": row["procurement_reference"] or None,
            "published_at_source": row["published_at"] or None,
            "contract_or_completion_date_source": row["contract_or_completion_date"] or None,
            "title": row["title"] or None, "cpv_code": cpv,
            "cpv_scheme_version": "unknown" if cpv else None,
            "cpv_label_source": row["cpv_label"] or None, "contract_type": row["contract_type"] or None,
            "procedure_type": row["procedure_type"] or None,
            "number_of_offers": int(row["number_of_offers"]) if row["number_of_offers"] else None,
            "amount_source": row["amount_source"] or None, "currency_source": row["currency_source"] or None,
        })
    with sqlite3.connect(":memory:") as connection:
        connection.executescript((ROOT / "schema/data-model.sql").read_text(encoding="utf-8"))
        for name in TABLES:
            for record in tables[name]:
                columns = list(record)
                sql = f"INSERT INTO {name} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})"
                connection.execute(sql, [record[c] for c in columns])
        violations = connection.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise ValueError(f"Broken references: {violations}")
        restored = connection.execute("""
            SELECT r.record_id, o.name, r.amount_source, s.source_file
            FROM procurement_records r JOIN organizations o ON o.organization_id=r.authority_id
            JOIN source_resources s ON s.source_resource_id=r.source_resource_id ORDER BY r.record_id
        """).fetchall()
        if len(restored) != len(rows):
            raise ValueError("Rows lost when joining entities")
        for original, (_, name, amount, filename) in zip(rows, restored):
            if (name, amount, filename) != (original["contracting_authority"], original["amount_source"], original["source_file"]):
                raise ValueError("Values changed when joining entities")
    return {"schema_version": "relational-v1", "scope": "reviewed_sample_only",
            "notes": ["Sample IDs are provisional technical references, not verified organization identities.",
                      "Source sheet and original row number are unavailable in this CSV projection.",
                      "Empty supplier, item, BNR-rate and conversion tables reflect missing or withheld evidence."],
            "tables": tables}


def main() -> None:
    output = build()
    path = ROOT / "docs/data-sample-normalized.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({name: len(rows) for name, rows in output["tables"].items()}))
    print(f"Written: {path}")


if __name__ == "__main__":
    main()
