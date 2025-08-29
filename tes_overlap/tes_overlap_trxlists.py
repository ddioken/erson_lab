#!/usr/bin/env python3
import argparse
import os
import re
from typing import Dict, Tuple, List
import numpy as np
import pandas as pd

LIKELY_COLS = {
    "transcript": ["transcript", "transcript_id", "tx", "tx_id", "name", "id"],
    "chrom":      ["chrom", "chromosome", "chr"],
    "strand":     ["strand", "str"],
    "start":      ["start", "tx_start", "tss", "begin"],
    "end":        ["end", "tx_end", "stop", "finish"]
}

def guess_columns(df: pd.DataFrame) -> Dict[str, str]:
    """Try to guess column mapping (case-insensitive)."""
    lower_map = {c.lower(): c for c in df.columns}
    out: Dict[str, str] = {}
    for key, candidates in LIKELY_COLS.items():
        for cand in candidates:
            if cand in lower_map:
                out[key] = lower_map[cand]
                break
    missing = [k for k in ["transcript","chrom","strand","start","end"] if k not in out]
    if missing:
        raise ValueError(
            f"Could not auto-detect columns for: {missing}. "
            f"Found columns: {list(df.columns)}.\n"
            "Rename your columns or add --map like "
            "--map transcript=tx_id,chrom=chr,strand=str,start=tx_start,end=tx_end"
        )
    return out

def apply_manual_map(df: pd.DataFrame, mapping: List[str]) -> Dict[str, str]:
    """Apply --map entries like transcript=tx_id,chrom=chr,strand=str,start=tx_start,end=tx_end"""
    kv = {}
    for item in mapping:
        if "=" not in item:
            raise ValueError(f"Bad --map entry: {item}. Use key=column_name")
        k, v = item.split("=", 1)
        k = k.strip().lower()
        kv[k] = v.strip()
    needed = {"transcript","chrom","strand","start","end"}
    if not needed.issubset(kv):
        missing = needed - set(kv)
        raise ValueError(f"--map is missing: {missing}")
    # validate columns exist
    for k, col in kv.items():
        if col not in df.columns:
            raise ValueError(f"--map refers to column '{col}' not in DataFrame. Existing: {list(df.columns)}")
    return kv

def read_any(path: str, sheet: str | None) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(path, sheet_name=sheet or 0)
    else:
        # try CSV/TSV: detect sep
        if ext in [".tsv", ".tab"]:
            return pd.read_csv(path, sep="\t")
        return pd.read_csv(path)

def normalize_chrom(c: object) -> str | None:
    if c is None or (isinstance(c, float) and np.isnan(c)): return None
    s = str(c).strip()
    if s == "": return None
    if s.startswith("chr"): return s
    su = s.upper()
    if su in {"M","MT"}: return "chrM"
    # if numeric like "1", "2"
    return "chr"+s

def build_tx_table(df: pd.DataFrame, colmap: Dict[str,str]) -> pd.DataFrame:
    out = pd.DataFrame({
        "transcript": df[colmap["transcript"]].astype(str),
        "chrom":      df[colmap["chrom"]].apply(normalize_chrom),
        "strand":     df[colmap["strand"]].astype(str),
        "start":      pd.to_numeric(df[colmap["start"]], errors="coerce").astype("Int64"),
        "end":        pd.to_numeric(df[colmap["end"]],   errors="coerce").astype("Int64"),
    })
    out = out.dropna(subset=["chrom","strand","start","end"]).copy()
    out["start"] = out["start"].astype(int)
    out["end"]   = out["end"].astype(int)
    # TES: + => end, - => start
    out["tes"] = np.where(out["strand"] == "+", out["end"], out["start"]).astype(int)
    # keep only +/-
    out = out[out["strand"].isin(["+","-"])].reset_index(drop=True)
    return out

def mark_overlap(source: pd.DataFrame, target: pd.DataFrame, tol: int) -> pd.Series:
    """
    For each row in `source`, return True if there's ANY transcript in `target`
    on the same chromosome & strand whose TES is within ±tol bp.
    Efficient via grouped binary search.
    """
    # group target by chrom,strand and pre-sort by TES
    tgt_groups = {
        key: grp.sort_values("tes").reset_index(drop=True)
        for key, grp in target.groupby(["chrom","strand"], sort=False)
    }
    result = np.zeros(len(source), dtype=bool)
    for key, src_grp in source.groupby(["chrom","strand"], sort=False):
        tgt = tgt_groups.get(key)
        if tgt is None or tgt.empty:
            continue
        arr = tgt["tes"].to_numpy()
        # vectorized window existence using searchsorted
        tes_vals = src_grp["tes"].to_numpy()
        left_idx  = np.searchsorted(arr, tes_vals - tol, side="left")
        right_idx = np.searchsorted(arr, tes_vals + tol, side="right")
        hit = right_idx > left_idx
        result[src_grp.index.values] = hit
    return pd.Series(result, index=source.index)

def main():
    ap = argparse.ArgumentParser(description="Find overlapping transcript 3′ ends (TES) between two Excel/CSV files.")
    ap.add_argument("file_a", help="Excel/CSV with transcripts (A)")
    ap.add_argument("file_b", help="Excel/CSV with transcripts (B)")
    ap.add_argument("--sheet-a", default=None, help="Sheet name or index for Excel A (default first sheet)")
    ap.add_argument("--sheet-b", default=None, help="Sheet name or index for Excel B (default first sheet)")
    ap.add_argument("-t","--tolerance", type=int, default=100, help="±bp tolerance around TES (default 100)")
    ap.add_argument("--map-a", nargs="+", default=None,
        help="Manual column map for A, e.g. transcript=tx,chrom=chr,strand=str,start=tx_start,end=tx_end")
    ap.add_argument("--map-b", nargs="+", default=None,
        help="Manual column map for B (same format as --map-a)")
    ap.add_argument("-o","--output", default="tes_overlap_results.xlsx", help="Output Excel path")
    args = ap.parse_args()

    # Read
    A_raw = read_any(args.file_a, args.sheet_a)
    B_raw = read_any(args.file_b, args.sheet_b)

    # Map columns
    map_a = apply_manual_map(A_raw, args.map_a) if args.map_a else guess_columns(A_raw)
    map_b = apply_manual_map(B_raw, args.map_b) if args.map_b else guess_columns(B_raw)

    # Build normalized tables with TES
    A = build_tx_table(A_raw, map_a)
    B = build_tx_table(B_raw, map_b)

    # Mark overlaps both directions
    A_found_in_B = mark_overlap(A, B, tol=args.tolerance)
    B_found_in_A = mark_overlap(B, A, tol=args.tolerance)

    # Compose output tables (keep original columns + found flag)
    A_out = A_raw.copy()
    A_out["TES_found_in_B"] = A_found_in_B.reindex(A.index, fill_value=False).map({True:"Found", False:""})
    B_out = B_raw.copy()
    B_out["TES_found_in_A"] = B_found_in_A.reindex(B.index, fill_value=False).map({True:"Found", False:""})

    # Summary
    nA = int(A_found_in_B.sum())
    nB = int(B_found_in_A.sum())
    print(f"File A has {nA} transcripts whose TES overlaps (±{args.tolerance} bp) with File B.")
    print(f"File B has {nB} transcripts whose TES overlaps (±{args.tolerance} bp) with File A.")

    # Write Excel with two sheets
    with pd.ExcelWriter(args.output, engine="xlsxwriter") as xw:
        A_out.to_excel(xw, index=False, sheet_name="A_with_match_in_B")
        B_out.to_excel(xw, index=False, sheet_name="B_with_match_in_A")
        # add a small summary sheet
        summary = pd.DataFrame({
            "metric": ["A TES matched in B", "B TES matched in A", "tolerance_bp"],
            "value":  [nA, nB, args.tolerance]
        })
        summary.to_excel(xw, index=False, sheet_name="summary")

    print(f"Wrote results to: {args.output}")

if __name__ == "__main__":
    main()

