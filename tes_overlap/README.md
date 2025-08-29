# TES Overlap Tool (Transcript 3′ End Matcher)

This Python tool compares **transcript ends (TES)** between two transcript lists and reports overlaps within a user-defined tolerance (default ±100 bp).  
It is designed for situations where you want to know if transcript annotations or experimental results agree at the level of transcript end positions.

---

## 🔍 Why is this useful?

- **Alternative Polyadenylation (APA)** studies: detect matching or shifted transcript ends across conditions.
- **Validation:** compare reference annotations with long-read sequencing outputs (e.g., Nanopore, 3′-seq).
- **QC:** identify unexpected transcript end positions in experimental data.
- **Cross-dataset comparison:** check consistency of transcript boundaries between different sources.

---

## 📂 Input format

You can supply **CSV** or **Excel (.xlsx)** files with the following columns:

- `transcript` – transcript ID or name  
- `chrom` – chromosome (e.g., `chr1`, `chr2`)  
- `strand` – `+` or `-`  
- `start` – transcript genomic start coordinate  
- `end` – transcript genomic end coordinate  

The tool automatically computes TES:

- If `strand == '+'`, TES = `end`  
- If `strand == '-'`, TES = `start`  

---

## 🧪 Minimal Examples

We provide two minimal test files (`A.csv`, `B.csv` and `A.xlsx`, `B.xlsx`) inside this folder.

### Example A.csv

```csv
transcript,chrom,strand,start,end
A1,chr1,+,1000,2000
A2,chr1,-,5000,5500
A3,chr2,+,10000,10100
A4,chr3,+,20000,20500
```
### Example B.csv

```csv
transcript,chrom,strand,start,end
B1,chr1,+,1100,2090
B2,chr1,-,5080,5600
B3,chr2,+,10050,10120
B4,chr3,+,30000,30500
```

---

##Quick Usage

- On .csv input

```bash
cd tes_overlap
python3 tes_overlap_trxlists.py A.csv B.csv -t 100 -o tes_overlap_results.xlsx
```

- On .xlsx input
```bash
cd tes_overlap
python3 tes_overlap_trxlists.py A.xlsx B.xlsx -t 100 -o tes_overlap_results.xlsx
```

---

#Output

- Prints a summary

```Arduino
File A has 3 transcripts whose TES overlaps (±100 bp) with File B.
File B has 3 transcripts whose TES overlaps (±100 bp) with File A.
```

Produces an Excel file with 3 sheets:

- A_with_match_in_B → File A + column TES_found_in_B

- B_with_match_in_A → File B + column TES_found_in_A

- summary → counts and tolerance used

---

## Requirements

- Python ≥ 3.8

- pandas

- numpy

- xlsxwriter (for Excel output)
Install with

```bash
pip install pandas numpy xlsxwriter
```
---

## Expected results on included examples

Using the included A.csv and B.csv:

- A1 TES=2000 matches B1 TES=2090 (distance +90)

- A2 TES=5000 matches B2 TES=5080 (distance +80)

- A3 TES=10100 matches B3 TES=10120 (distance +20)

- A4 TES=20500 has no match

So the summary is:

```Arduino
File A has 3 transcripts whose TES overlaps (±100 bp) with File B.
File B has 3 transcripts whose TES overlaps (±100 bp) with File A.
```
---

## Authors

Developed in **Erson Lab**  
Maintainer: [Didem Naz Dioken](https://github.com/ddioken)


