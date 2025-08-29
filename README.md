
# Erson Lab Tools: BAM Interval Coverage Checker

A simple Bash tool to quickly evaluate read coverage in BAM files across a user-defined genomic interval.  
Originally developed for **single-cell RNA-seq analysis** to check:

- Coverage of **intronic regions** (retained introns, splicing QC)
- Reads **outside annotated gene boundaries** (possible novel isoforms, antisense transcription)
- **Per-cell BAM QC** before deeper pipelines

This tool is lightweight, uses only `samtools` + `awk`, and is ideal for **fast, exploratory checks** of BAMs.

---

## Requirements
- [samtools](http://www.htslib.org/) ≥ 1.10
- bash ≥ 4

---

## When to use this tool

- **Intronic coverage**: verify if single-cell BAMs capture intronic regions  
- **Out-of-gene coverage**: detect reads mapping beyond gene boundaries  
- **Targeted QC**: test specific loci before spending compute on heavy workflows  
- **Single-cell filtering**: exclude BAMs/cells that fail to capture regions of interest

---

## Usage

```bash
bash bam_interval_threshold.sh <input_dir> <output_dir> <threshold_percentage> <region>

