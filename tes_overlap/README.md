# TES Overlap Tool (Transcript 3′ End Matcher)

This Python tool compares **transcript ends (TES)** between two transcript lists and reports overlaps within a user-defined tolerance (default ±100 bp).  
It is designed for situations where you want to know if transcript annotations or experimental results agree at the level of transcript end positions.

---

## Why is this useful?

- **Alternative Polyadenylation (APA)** studies: detect matching or shifted transcript ends across conditions.
- **Validation**: compare reference annotations with long-read sequencing outputs.
- **QC**: identify unexpected transcript end positions in experimental data.
- **Cross-dataset comparison**: check consistency of transcript boundaries between different sources.

---

## Input format

You can supply **CSV or Excel (.xlsx)** files with the following columns:

- `transcript` – transcript ID or name  
- `chrom` – chromosome (e.g., `chr1`, `chr2`)  
- `strand` – `+` or `-`  
- `start` – transcript genomic start coordinate  
- `end` – transcript genomic end coordinate  

The tool automatically computes TES:
- If `strand == +`, TES = `end`
- If `strand == -`, TES = `start`

Example A file (`A.csv`):

| transcript | chrom | strand | start | end   |
|------------|-------|--------|-------|-------|
| A1         | chr1  | +      | 1000  | 2000  |
| A2         | chr1  | -      | 5000  | 5500  |

Example B file (`B.csv`):

| transcript | chrom | strand | start | end   |
|------------|-------|--------|-------|-------|
| B1         | chr1  | +      | 1100  | 2090  |
| B2         | chr1  | -      | 5080  | 5600  |

---

## Output

- Prints a summary:

File A has 3 transcripts whose TES overlaps (±100 bp) with File B.
File B has 3 transcripts whose TES overlaps (±100 bp) with File A.

- Creates an Excel file with 3 sheets:
1. `A_with_match_in_B` → original File A + a column `TES_found_in_B`
2. `B_with_match_in_A` → original File B + a column `TES_found_in_A`
3. `summary` → counts and tolerance used

---

```bash
cd tes_overlap

# Run on CSV
python3 tes_overlap_trxlists.py A.csv B.csv -t 100 -o tes_overlap_results.xlsx

# Run on Excel
python3 tes_overlap_trxlists.py A.xlsx B.xlsx -t 100 -o tes_overlap_results.xlsx

```
---

## Requirements
   
- Python ≥  3.8
- pandas
- numpy
- xlsxwriter (for writing Excel files)

---

## Install

```bash
pip install pandas numpy xlsxwriter
```

---



