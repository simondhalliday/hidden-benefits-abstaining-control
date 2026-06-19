#!/usr/bin/env python3
"""Audit questionnaire demographics and free-text privacy risk.

The script produces aggregate audit files only. It does not export raw free-text
responses, majors, birthdates, or row-level demographics.
"""

from __future__ import annotations

import argparse
import re
import warnings
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

PAPER_DEMOGRAPHICS = {
    "C10": {"female_share": 0.44, "age_mean": 21.02, "age_sd": 2.34},
    "TP10": {"female_share": 0.54, "age_mean": 20.75, "age_sd": 4.20},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to the extracted Autonomy_Control archive directory.",
    )
    parser.add_argument(
        "--appendix-output",
        type=Path,
        default=Path("docs/audit/appendix_a1_demographics_audit.csv"),
    )
    parser.add_argument(
        "--privacy-output",
        type=Path,
        default=Path("docs/audit/questionnaire_privacy_audit.csv"),
    )
    return parser.parse_args()


def read_workbook(path: Path) -> pd.DataFrame:
    return pd.read_excel(path)


def clean_missing(series: pd.Series) -> pd.Series:
    out = series.astype(object).copy()
    out[out.astype(str).str.strip().isin([".", "", "nan", "NaN"])] = np.nan
    return out


def demographic_rows(frame: pd.DataFrame) -> pd.DataFrame:
    if "Subject" not in frame.columns:
        return frame.iloc[0:0].copy()
    return frame[frame["Subject"].notna()].copy()


def summarize_demographic_workbook(path: Path, treatment: str) -> dict[str, object]:
    frame = read_workbook(path)
    data = demographic_rows(frame)
    lower_cols = {str(c).lower(): c for c in frame.columns}
    age_col = lower_cols.get("age")
    gender_col = lower_cols.get("gender")
    female_dummy_col = "Unnamed: 4" if treatment == "C10" else "Unnamed: 5"

    age = pd.to_numeric(clean_missing(data[age_col]), errors="coerce")
    gender = clean_missing(data[gender_col]).astype(str).str.lower()
    female_from_text = gender.eq("female")
    female_dummy = pd.to_numeric(data.get(female_dummy_col), errors="coerce")

    paper = PAPER_DEMOGRAPHICS[treatment]
    female_share = float(female_dummy.mean(skipna=True))
    age_mean = float(age.mean(skipna=True))
    age_sd = float(age.std(skipna=True, ddof=1))
    return {
        "treatment": treatment,
        "source_file": str(path),
        "demographic_rows": int(len(data)),
        "gender_nonmissing": int(gender.replace("nan", np.nan).notna().sum()),
        "female_count_from_text": int(female_from_text.sum()),
        "female_share_from_dummy": female_share,
        "paper_female_share": paper["female_share"],
        "female_share_rounded_matches_paper": round(female_share, 2)
        == paper["female_share"],
        "age_nonmissing": int(age.notna().sum()),
        "age_mean": age_mean,
        "paper_age_mean": paper["age_mean"],
        "age_mean_rounded_matches_paper": round(age_mean, 2) == paper["age_mean"],
        "age_sd": age_sd,
        "paper_age_sd": paper["age_sd"],
        "age_sd_rounded_matches_paper": round(age_sd, 2) == paper["age_sd"],
        "note": "demographics are available for questionnaire respondents, not all zTree subjects",
    }


def questionnaire_workbooks(source: Path) -> Iterable[Path]:
    data_root = source / "data-autonomy"
    for path in sorted(data_root.rglob("*.xlsx")):
        name = path.name.lower()
        if "question" in name or name == "workbook3.xlsx":
            yield path


def privacy_audit_for_workbook(path: Path, source: Path) -> dict[str, object]:
    frame = read_workbook(path)
    lower_cols = {str(c).lower(): c for c in frame.columns}
    feeling_col = lower_cols.get("feeling")
    majors_col = lower_cols.get("majors")
    birth_col = lower_cols.get("dateofbirth")
    age_col = lower_cols.get("age")
    gender_col = lower_cols.get("gender")

    text = (
        clean_missing(frame[feeling_col]).dropna().astype(str)
        if feeling_col
        else pd.Series(dtype=str)
    )
    email_hits = int(text.str.contains(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", case=False, regex=True).sum())
    phone_hits = int(text.str.contains(r"(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", regex=True).sum())
    url_hits = int(text.str.contains(r"https?://|www\.", case=False, regex=True).sum())
    student_id_hits = int(text.str.contains(r"\b\d{8,}\b", regex=True).sum())

    majors = clean_missing(frame[majors_col]) if majors_col else pd.Series(dtype=object)
    birth = clean_missing(frame[birth_col]) if birth_col else pd.Series(dtype=object)
    age = pd.to_numeric(clean_missing(frame[age_col]), errors="coerce") if age_col else pd.Series(dtype=float)
    gender = clean_missing(frame[gender_col]) if gender_col else pd.Series(dtype=object)

    return {
        "relative_path": str(path.relative_to(source)),
        "rows": int(len(frame)),
        "free_text_nonmissing": int(text.notna().sum()),
        "free_text_max_chars": int(text.str.len().max()) if len(text) else 0,
        "email_pattern_hits": email_hits,
        "phone_pattern_hits": phone_hits,
        "url_pattern_hits": url_hits,
        "long_number_pattern_hits": student_id_hits,
        "gender_nonmissing": int(gender.notna().sum()),
        "age_nonmissing": int(age.notna().sum()),
        "birthdate_nonmissing": int(birth.notna().sum()),
        "major_nonmissing": int(majors.notna().sum()),
        "unique_majors": int(majors.dropna().astype(str).str.lower().str.strip().nunique()),
        "privacy_recommendation": "do not release raw free text or row-level demographics publicly",
    }


def main() -> None:
    args = parse_args()
    source = args.source.expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source archive directory not found: {source}")

    consolidated = source / "data-autonomy" / "Consolidated"
    appendix_rows = [
        summarize_demographic_workbook(consolidated / "Workbook3.xlsx", "C10"),
        summarize_demographic_workbook(consolidated / "questionnaires_treatment.xlsx", "TP10"),
    ]
    appendix = pd.DataFrame(appendix_rows)
    args.appendix_output.parent.mkdir(parents=True, exist_ok=True)
    appendix.to_csv(args.appendix_output, index=False)

    privacy = pd.DataFrame(
        [privacy_audit_for_workbook(path, source) for path in questionnaire_workbooks(source)]
    )
    args.privacy_output.parent.mkdir(parents=True, exist_ok=True)
    privacy.to_csv(args.privacy_output, index=False)

    print(f"Wrote {args.appendix_output}")
    print(f"Wrote {args.privacy_output}")
    print()
    print("Appendix A1 demographic checks:")
    print(appendix.to_string(index=False))
    print()
    print("Questionnaire privacy summary:")
    print(privacy.to_string(index=False))


if __name__ == "__main__":
    main()
