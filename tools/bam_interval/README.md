# Erson Lab Tools: BAM Interval Coverage Checker

A simple Bash tool to quickly evaluate read coverage in BAM files across a user-defined genomic interval.  

Originally developed for **single-cell RNA-seq analysis**, this script can be used to check:

- Coverage of **intronic regions** (e.g., retained introns, splicing QC)
- Reads **outside annotated gene boundaries** (novel isoforms, antisense transcription)
- **Per-cell BAM QC** before deeper pipelines
- General BAM QC in bulk RNA-seq or other sequencing data

This tool is lightweight, uses only `samtools` + `awk`, and is ideal for **fast, exploratory checks** of BAMs before heavier pipelines.

---

## ✨ Features
- Works with any BAM files (bulk or single-cell)
- Takes **four arguments** (input dir, output dir, threshold %, region)
- Outputs a CSV summary of coverage per sample
- Can be run on hundreds of BAMs with just one command
- Useful for **QC**, **targeted exploration**, or **filtering single cells**

---

## 🔧 Requirements
- [samtools](http://www.htslib.org/) ≥ 1.10  
- bash ≥ 4  

Install samtools:

```bash
# macOS
brew install samtools

# Ubuntu/Debian Linux
sudo apt-get install samtools
```


---

## Installation
- Clone this repository and make the script executable:

```bash
git clone https://github.com/ddioken/erson_lab.git
cd erson_lab
chmod +x bam_interval_threshold.sh
```


---

## Usage
```bash
bash bam_interval_threshold.sh <input_dir> <output_dir> <threshold_percentage> <region>
```

---

## Arguments

- `<input_dir>` — folder containing BAM files

- `<output_dir>` — folder to save results

- `<threshold_percentage>` — e.g. 80 for ≥80% coverage requirement

- `<region>` — genomic interval in chrom:start-end format (must match BAM contig naming)

---

## Example

- Check whether BAMs in /data/singlecell_bams have ≥80% coverage of an intronic BRCA1 region:

```bash
bash bam_interval_threshold.sh /data/singlecell_bams /data/output 80 17:43044295-43044497
```

This will:

- Read all BAMs in /data/singlecell_bams

- Compute coverage across 17:43,044,295–43,044,497

- Write results to /data/output/qualifying_files.csv

---

## Output

The script produces a CSV file at <output_dir>/qualifying_files.csv with columns:

| sample    | total_positions | covered_positions | percent_covered |
|-----------|-----------------|-------------------|-----------------|
| cellA.bam | 203             | 198               | 97.5            |
| cellB.bam | 203             |  75               | 36.9            |

- total_positions = length of the interval (bp)

- covered_positions = number of bases with ≥1 read

- percent_covered = coverage fraction × 100

Only samples passing the threshold are included in the final list.

---

## When to use this tool

- Intronic coverage: Verify if single-cell BAMs capture intronic regions

- Out-of-gene coverage: Detect reads mapping beyond annotated gene boundaries

- Targeted QC: Test specific loci before heavy workflows (STARsolo, CellRanger, etc.)

- Single-cell filtering: Exclude BAMs/cells that fail to capture regions of interest

---

## Notes

- Region naming must match BAM (e.g. 17: vs chr17:).

- BAMs must be indexed (.bai or .csi). The script will create indexes if missing.

- Works on macOS and Linux.

---

## Authors

Developed in **Erson Lab**  
Maintainer: [Didem Naz Dioken](https://github.com/ddioken)


