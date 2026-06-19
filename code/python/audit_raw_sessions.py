#!/usr/bin/env python3
"""Audit raw zTree session exports against the cleaned analysis data.

This script does not copy raw data into the repository. It reads a local
extraction of the legacy archive and reports which zTree subject exports appear
to feed the cleaned analysis data.

Usage:

    python code/python/audit_raw_sessions.py --source /path/to/Autonomy_Control

If --source is omitted, the script tries the scratch extraction path used during
the initial repository audit.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


DEFAULT_SOURCE = Path("/private/tmp/autonomy_control_audit/Autonomy_Control")


@dataclass(frozen=True)
class SessionExport:
    relative_path: str
    session_id: str
    treatment_hint: str
    usable_hint: str
    subject_rows: int
    unique_subjects: int
    unique_groups: int
    role_1_count: int
    role_2_count: int
    role_3_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to the extracted Autonomy_Control archive directory.",
    )
    parser.add_argument(
        "--cleaned",
        type=Path,
        default=Path("data/processed/merged_control_treatment.csv"),
        help="Path to the cleaned CSV in this repository.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/audit/raw_session_audit.csv"),
        help="CSV report path to write.",
    )
    return parser.parse_args()


def iter_ztree_exports(source: Path) -> Iterable[Path]:
    data_root = source / "data-autonomy"
    for path in sorted(data_root.rglob("*.xls")):
        if "Consolidated" in path.parts:
            continue
        yield path


def treatment_hint(path: Path) -> str:
    text = " ".join(path.parts[-3:]).lower()
    if "crash" in text or "unusable" in text:
        return "crash/unusable"
    if "control - " in text or " - c" in text:
        return "C10"
    if "treatment - " in text or " - t" in text:
        return "TP10"
    return "unknown"


def usable_hint(path: Path) -> str:
    text = str(path).lower()
    if "crash" in text or "unusable" in text:
        return "exclude"
    return "candidate"


def subject_rows_from_ztree_export(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            if len(row) <= 16:
                continue
            if row[2] != "subjects":
                continue
            if row[3] in ("Period", ""):
                continue
            rows.append(row)
    return rows


def summarize_export(path: Path, source: Path) -> SessionExport:
    rows = subject_rows_from_ztree_export(path)
    session_id = path.stem
    subjects = {row[4] for row in rows}
    groups = {row[5] for row in rows}
    roles = [row[16] for row in rows]
    return SessionExport(
        relative_path=str(path.relative_to(source)),
        session_id=session_id,
        treatment_hint=treatment_hint(path),
        usable_hint=usable_hint(path),
        subject_rows=len(rows),
        unique_subjects=len(subjects),
        unique_groups=len(groups),
        role_1_count=roles.count("1"),
        role_2_count=roles.count("2"),
        role_3_count=roles.count("3"),
    )


def main() -> None:
    args = parse_args()
    source = args.source.expanduser().resolve()
    cleaned = args.cleaned.expanduser().resolve()
    output = args.output.expanduser()

    if not source.exists():
        raise SystemExit(f"Source archive directory not found: {source}")
    if not cleaned.exists():
        raise SystemExit(f"Cleaned data file not found: {cleaned}")

    exports = [summarize_export(path, source) for path in iter_ztree_exports(source)]
    cleaned_df = pd.read_csv(cleaned)
    cleaned_counts = (
        cleaned_df.groupby(["Treatment", "SessionId"])
        .size()
        .rename("cleaned_rows")
        .reset_index()
    )
    cleaned_by_session = {}
    for row in cleaned_counts.itertuples(index=False):
        cleaned_by_session[str(row.SessionId)] = {
            "cleaned_treatment": int(row.Treatment),
            "cleaned_rows": int(row.cleaned_rows),
        }

    rows = []
    for export in exports:
        cleaned_match = cleaned_by_session.get(export.session_id, {})
        cleaned_rows = int(cleaned_match.get("cleaned_rows", 0))
        cleaned_treatment = cleaned_match.get("cleaned_treatment", "")
        rows.append(
            {
                **export.__dict__,
                "cleaned_treatment": cleaned_treatment,
                "cleaned_rows": cleaned_rows,
                "appears_in_cleaned_data": cleaned_rows > 0,
                "raw_rows_match_cleaned_rows": export.subject_rows == cleaned_rows,
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)

    print(f"Wrote {output}")
    print()
    print("Raw zTree candidate exports:")
    print(pd.DataFrame(rows).to_string(index=False))
    print()
    print("Cleaned data session counts:")
    print(cleaned_counts.to_string(index=False))


if __name__ == "__main__":
    main()
