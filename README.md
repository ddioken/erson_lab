# Erson Lab Tools

A small collection of lightweight, practical tools for RNA-seq & transcriptomics.  
Each tool lives in its own folder with a focused README, examples, and usage.

---

## 📦 Toolbox


### 1) BAM Interval Coverage Checker — fast BAM CC

**Folder:** [`tools/tes_overlap`](tools/bam_interval)

- Quick coverage check for a genomic interval across many BAMs
- Useful for intronic coverage, reads outside gene boundaries

**Quick start**
```bash
bash tools/bam_interval/bam_interval_threshold.sh \
  /path/to/bams \
  results/ \
  5 \
  chr1:100000-101000
```


### 2) TES Overlap Tool — compare transcript 3′ ends
**Folder:** [`tools/tes_overlap`](tools/tes_overlap)

- Compares **transcript ends (TES)** between two transcript lists (CSV/XLSX)
- Calls overlaps within **±N bp** (default 100), **same chromosome & strand**
- Outputs an Excel workbook annotating which transcripts match across files

**Quick start**
```bash
python3 tools/tes_overlap/tes_overlap_trxlists.py \
  tools/tes_overlap/A.csv \
  tools/tes_overlap/B.csv \
  -t 100 \
  -o tes_overlap_results.xlsx
```

---

## Requirements

Tool-specific requirements are listed inside each folder.
Common Python deps (for TES tool): pandas, numpy, xlsxwriter.

Install
```bash
pip install pandas numpy xlsxwriter
```
---

## Authors

Developed in **Erson Lab**  
Maintainer: [Didem Naz Dioken](https://github.com/ddioken)


