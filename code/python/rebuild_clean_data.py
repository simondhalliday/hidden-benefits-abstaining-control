#!/usr/bin/env python3
"""Rebuild cleaned analysis data from raw zTree exports.

This script is a provenance check. It reads a local extraction of the legacy
archive, rebuilds the cleaned zTree subject-level data, derives the main Stata
analysis variables, and compares the results to the committed cleaned data.

It intentionally writes rebuilt row-level files to `tmp/`, which is ignored by
git. The committed outputs are aggregate/comparison reports only.
"""

from __future__ import annotations

import argparse
import csv
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


warnings.filterwarnings(
    "ignore",
    message="Unknown extension is not supported and will be removed",
    category=UserWarning,
    module="openpyxl",
)

DEFAULT_SOURCE = Path("/private/tmp/autonomy_control_audit/Autonomy_Control")
DEFAULT_TMP_OUTPUT = Path("tmp/rebuilt_clean_data")


AUTONOMY_ITEMS = [
    "Q1c",
    "Q2a",
    "Q3c",
    "Q4a",
    "Q5a",
    "Q6b",
    "Q7b",
    "Q8c",
    "Q9c",
    "Q10b",
    "Q11b",
    "Q12a",
]
IMPERSONAL_ITEMS = [
    "Q1a",
    "Q2b",
    "Q3b",
    "Q4c",
    "Q5b",
    "Q6a",
    "Q7c",
    "Q8b",
    "Q9a",
    "Q10a",
    "Q11c",
    "Q12c",
]
CONTROL_ITEMS = [
    "Q1b",
    "Q2c",
    "Q3a",
    "Q4b",
    "Q5c",
    "Q6c",
    "Q7a",
    "Q8a",
    "Q9c",
    "Q10c",
    "Q11a",
    "Q12b",
]


@dataclass(frozen=True)
class ExportSpec:
    path: Path
    treatment: int
    include: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to the extracted Autonomy_Control archive directory.",
    )
    parser.add_argument(
        "--cleaned-csv",
        type=Path,
        default=Path("data/processed/merged_control_treatment.csv"),
        help="Committed cleaned zTree CSV to compare against.",
    )
    parser.add_argument(
        "--cleaned-dta",
        type=Path,
        default=Path("data/processed/merged_treatment_control.dta"),
        help="Committed Stata analysis data to compare derived variables against.",
    )
    parser.add_argument(
        "--tmp-output",
        type=Path,
        default=DEFAULT_TMP_OUTPUT,
        help="Ignored directory for rebuilt row-level outputs.",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=Path("docs/audit/raw_to_clean_rebuild_audit.csv"),
        help="Aggregate rebuild audit report path.",
    )
    parser.add_argument(
        "--derived-output",
        type=Path,
        default=Path("docs/audit/derived_variable_audit.csv"),
        help="Derived-variable comparison report path.",
    )
    parser.add_argument(
        "--questionnaire-output",
        type=Path,
        default=Path("docs/audit/questionnaire_demographics_audit.csv"),
        help="Aggregate questionnaire-demographics audit report path.",
    )
    return parser.parse_args()


def classify_export(path: Path) -> ExportSpec:
    text = " ".join(path.parts[-3:]).lower()
    include = "crash" not in text and "unusable" not in text
    if "control - " in text or " - c" in text:
        treatment = 1
    elif "treatment - " in text or " - t" in text:
        treatment = 2
    else:
        treatment = 0
    return ExportSpec(path=path, treatment=treatment, include=include)


def iter_export_specs(source: Path) -> Iterable[ExportSpec]:
    data_root = source / "data-autonomy"
    for path in sorted(data_root.rglob("*.xls")):
        if "Consolidated" in path.parts:
            continue
        yield classify_export(path)


def parse_subject_rows(spec: ExportSpec) -> tuple[list[str], list[list[str]]]:
    header: list[str] | None = None
    rows: list[list[str]] = []
    with spec.path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for raw in reader:
            if len(raw) <= 16 or raw[2] != "subjects":
                continue
            if raw[3] == "Period":
                header = ["SessionId", "Exists", "Subjectsdo", "Treatment"] + raw[3:]
                if header and header[-1] == "":
                    header = header[:-1]
                continue
            if raw[3] == "":
                continue
            row = [raw[0], raw[1], raw[2], str(spec.treatment)] + raw[3:]
            if row and row[-1] == "":
                row = row[:-1]
            rows.append(row)
    if header is None:
        raise ValueError(f"No subject header found in {spec.path}")
    return header, rows


def rebuild_ztree_data(source: Path) -> pd.DataFrame:
    all_rows: list[list[str]] = []
    expected_header: list[str] | None = None
    for spec in iter_export_specs(source):
        if not spec.include:
            continue
        if spec.treatment not in (1, 2):
            raise ValueError(f"Could not infer treatment for {spec.path}")
        header, rows = parse_subject_rows(spec)
        if expected_header is None:
            expected_header = header
        elif header != expected_header:
            raise ValueError(f"Header mismatch in {spec.path}")
        all_rows.extend(rows)
    if expected_header is None:
        raise ValueError("No usable zTree exports found")
    rebuilt = pd.DataFrame(all_rows, columns=expected_header)
    return sort_cleaned(rebuilt)


def sort_cleaned(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["_treatment_sort"] = pd.to_numeric(out["Treatment"], errors="coerce")
    out["_subject_sort"] = pd.to_numeric(out["Subject"], errors="coerce")
    out = out.sort_values(["_treatment_sort", "SessionId", "_subject_sort"]).drop(
        columns=["_treatment_sort", "_subject_sort"]
    )
    return out.reset_index(drop=True)


def normalize_for_compare(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        numeric = pd.to_numeric(out[col], errors="coerce")
        nonmissing = out[col].notna() & (out[col].astype(str) != "")
        numeric_share = numeric[nonmissing].notna().mean() if nonmissing.any() else 0
        if numeric_share == 1:
            out[col] = numeric.astype(float)
        else:
            out[col] = out[col].astype(str)
    return out


def compare_cleaned(rebuilt: pd.DataFrame, cleaned: pd.DataFrame) -> pd.DataFrame:
    cleaned_sorted = sort_cleaned(cleaned)
    rows = [
        {
            "check": "row_count",
            "status": "pass" if len(rebuilt) == len(cleaned_sorted) else "fail",
            "detail": f"rebuilt={len(rebuilt)} cleaned={len(cleaned_sorted)}",
        },
        {
            "check": "column_count",
            "status": "pass" if rebuilt.shape[1] == cleaned_sorted.shape[1] else "fail",
            "detail": f"rebuilt={rebuilt.shape[1]} cleaned={cleaned_sorted.shape[1]}",
        },
        {
            "check": "column_names",
            "status": "pass" if list(rebuilt.columns) == list(cleaned_sorted.columns) else "fail",
            "detail": "ordered column names match",
        },
    ]
    rebuilt_norm = normalize_for_compare(rebuilt)
    cleaned_norm = normalize_for_compare(cleaned_sorted)
    numeric_diffs: list[float] = []
    exact_diffs = 0
    for col in rebuilt_norm.columns:
        if np.issubdtype(rebuilt_norm[col].dtype, np.number):
            diff = (rebuilt_norm[col] - cleaned_norm[col]).abs()
            numeric_diffs.extend(diff.dropna().tolist())
        else:
            exact_diffs += int((rebuilt_norm[col] != cleaned_norm[col]).sum())
    max_numeric_diff = max(numeric_diffs) if numeric_diffs else 0.0
    rows.append(
        {
            "check": "cell_values_numeric_tolerance",
            "status": "pass" if exact_diffs == 0 and max_numeric_diff < 1e-5 else "fail",
            "detail": f"exact_string_diffs={exact_diffs}; max_numeric_diff={max_numeric_diff:.10g}",
        }
    )
    return pd.DataFrame(rows)


def as_numeric(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def derive_analysis_variables(rebuilt: pd.DataFrame) -> pd.DataFrame:
    df = rebuilt.copy()
    numeric_cols = [
        c
        for c in df.columns
        if c not in {"SessionId", "Subjectsdo"}
    ]
    df = as_numeric(df, numeric_cols)

    derived = df.copy()
    derived["pid"] = derived["SessionId"].astype(str) + derived["Subject"].astype(int).astype(str)
    derived["finalearnings"] = derived["TotalPayoff"] / 5
    derived["autonomy"] = derived[AUTONOMY_ITEMS].sum(axis=1)
    derived["impersonal"] = derived[IMPERSONAL_ITEMS].sum(axis=1)
    derived["controlpref"] = derived[CONTROL_ITEMS].sum(axis=1)
    derived["transdif"] = derived["TransferUnbounded"] - derived["TransferBounded"]
    derived["treatmentstring"] = np.where(
        derived["Treatment"] == 1, "Experiment 1", "Experiment 2"
    )
    derived["transferubx"] = derived["TransferUnbounded"].where(
        derived["TransferUnbounded"] >= 10, 10
    )
    derived["transdifxb"] = derived["transferubx"] - derived["TransferBounded"]
    derived["controlneg"] = (
        (derived["TransferBounded"] < derived["TransferUnbounded"])
        & (derived["PlayedRoleA"] == 1)
    ).astype(float)
    derived["stauto"] = (derived["autonomy"] - derived["autonomy"].mean()) / derived[
        "autonomy"
    ].std(ddof=1)
    derived["stimp"] = (derived["impersonal"] - derived["impersonal"].mean()) / derived[
        "impersonal"
    ].std(ddof=1)
    derived["stcont"] = (derived["controlpref"] - derived["controlpref"].mean()) / derived[
        "controlpref"
    ].std(ddof=1)
    derived["treatdum"] = (derived["Treatment"] == 2).astype(float)
    derived["tpstimp"] = derived["treatdum"] * derived["stimp"]
    derived["tpstauto"] = derived["treatdum"] * derived["stauto"]
    derived["tpstcont"] = derived["treatdum"] * derived["stcont"]
    derived["controlpos"] = (
        (derived["TransferBounded"] > derived["TransferUnbounded"])
        & (derived["PlayedRoleA"] == 1)
    ).astype(float)
    derived["controlneutral"] = (
        (derived["TransferBounded"] == derived["TransferUnbounded"])
        & (derived["PlayedRoleA"] == 1)
    ).astype(float)
    derived["controlcat"] = "."
    derived.loc[derived["controlpos"] == 1, "controlcat"] = "Positive"
    derived.loc[derived["controlneutral"] == 1, "controlcat"] = "Neutral"
    derived.loc[derived["controlneg"] == 1, "controlcat"] = "Negative"
    derived["controlcats"] = np.nan
    derived.loc[derived["controlpos"] == 1, "controlcats"] = 1
    derived.loc[derived["controlneutral"] == 1, "controlcats"] = 2
    derived.loc[derived["controlneg"] == 1, "controlcats"] = 3
    derived["categories"] = derived["controlcat"]
    return derived


def compare_derived(rebuilt_derived: pd.DataFrame, cleaned_dta: pd.DataFrame) -> pd.DataFrame:
    lower_map = {c.lower(): c for c in rebuilt_derived.columns}
    cleaned = cleaned_dta.sort_values(["treatment", "sessionid", "subject"]).reset_index(drop=True)
    rebuilt = rebuilt_derived.sort_values(["Treatment", "SessionId", "Subject"]).reset_index(drop=True)
    checks = [
        "pid",
        "finalearnings",
        "autonomy",
        "impersonal",
        "controlpref",
        "transdif",
        "treatmentstring",
        "transferubx",
        "transdifxb",
        "controlneg",
        "stauto",
        "stimp",
        "stcont",
        "treatdum",
        "tpstimp",
        "tpstauto",
        "tpstcont",
        "controlpos",
        "controlneutral",
        "controlcat",
        "controlcats",
        "categories",
    ]
    rows = []
    for col in checks:
        source_col = lower_map.get(col, col)
        rebuilt_values = rebuilt[source_col]
        cleaned_values = cleaned[col]
        rebuilt_numeric = pd.to_numeric(rebuilt_values, errors="coerce")
        cleaned_numeric = pd.to_numeric(cleaned_values, errors="coerce")
        if rebuilt_numeric.notna().any() or cleaned_numeric.notna().any():
            diff = (rebuilt_numeric - cleaned_numeric).abs()
            max_abs_diff = diff.max(skipna=True)
            mismatch_count = int((diff.fillna(0) > 1e-5).sum())
            status = "pass" if mismatch_count == 0 else "fail"
            detail = f"max_abs_diff={max_abs_diff:.10g}; mismatch_count={mismatch_count}"
        else:
            mismatch_count = int((rebuilt_values.astype(str) != cleaned_values.astype(str)).sum())
            status = "pass" if mismatch_count == 0 else "fail"
            detail = f"string_mismatch_count={mismatch_count}"
        rows.append({"variable": col, "status": status, "detail": detail})
    return pd.DataFrame(rows)


def questionnaire_workbooks(source: Path) -> Iterable[Path]:
    data_root = source / "data-autonomy"
    for path in sorted(data_root.rglob("*.xlsx")):
        name = path.name.lower()
        if "question" in name or name in {"workbook3.xlsx"}:
            yield path


def clean_placeholder_values(series: pd.Series) -> pd.Series:
    out = series.astype(object).copy()
    out[out.astype(str) == "."] = np.nan
    return out


def questionnaire_audit(source: Path) -> pd.DataFrame:
    rows = []
    for path in questionnaire_workbooks(source):
        try:
            frame = pd.read_excel(path)
        except Exception as exc:  # pragma: no cover - audit script logging
            rows.append(
                {
                    "relative_path": str(path.relative_to(source)),
                    "rows": 0,
                    "gender_nonmissing": 0,
                    "age_nonmissing": 0,
                    "female_share": np.nan,
                    "mean_age": np.nan,
                    "note": f"read_error: {exc}",
                }
            )
            continue

        lower_cols = {str(c).lower(): c for c in frame.columns}
        gender_col = lower_cols.get("gender")
        age_col = lower_cols.get("age")
        session_col = lower_cols.get("session")
        gender = (
            clean_placeholder_values(frame[gender_col])
            if gender_col
            else pd.Series(dtype=object)
        )
        age = (
            pd.to_numeric(clean_placeholder_values(frame[age_col]), errors="coerce")
            if age_col
            else pd.Series(dtype=float)
        )
        gender_lower = gender.astype(str).str.lower()
        female = gender_lower.eq("female")
        rows.append(
            {
                "relative_path": str(path.relative_to(source)),
                "session_values": ";".join(sorted(frame[session_col].dropna().astype(str).unique())) if session_col else "",
                "rows": len(frame),
                "gender_nonmissing": int(gender.notna().sum()) if gender_col else 0,
                "age_nonmissing": int(age.notna().sum()) if age_col else 0,
                "female_share": female[gender.notna()].mean() if gender_col and gender.notna().any() else np.nan,
                "mean_age": age.mean(skipna=True) if age_col else np.nan,
                "note": "aggregate only; raw free-text not exported",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    source = args.source.expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source archive directory not found: {source}")

    rebuilt = rebuild_ztree_data(source)
    cleaned_csv = pd.read_csv(args.cleaned_csv)
    cleaned_dta = pd.read_stata(args.cleaned_dta)

    args.tmp_output.mkdir(parents=True, exist_ok=True)
    rebuilt.to_csv(args.tmp_output / "rebuilt_merged_control_treatment.csv", index=False)

    audit = compare_cleaned(rebuilt, cleaned_csv)
    args.audit_output.parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(args.audit_output, index=False)

    derived = derive_analysis_variables(rebuilt)
    derived.to_csv(args.tmp_output / "rebuilt_merged_treatment_control_derived.csv", index=False)
    derived_audit = compare_derived(derived, cleaned_dta)
    args.derived_output.parent.mkdir(parents=True, exist_ok=True)
    derived_audit.to_csv(args.derived_output, index=False)

    q_audit = questionnaire_audit(source)
    args.questionnaire_output.parent.mkdir(parents=True, exist_ok=True)
    q_audit.to_csv(args.questionnaire_output, index=False)

    print(f"Wrote rebuilt row-level files to {args.tmp_output}")
    print(f"Wrote {args.audit_output}")
    print(f"Wrote {args.derived_output}")
    print(f"Wrote {args.questionnaire_output}")
    print()
    print("Raw-to-clean checks:")
    print(audit.to_string(index=False))
    print()
    print("Derived-variable checks:")
    print(derived_audit.to_string(index=False))


if __name__ == "__main__":
    main()
