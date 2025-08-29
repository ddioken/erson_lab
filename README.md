
# Erson Lab: BAM Interval Coverage Checker

This script checks BAM files to see if a given genomic interval
has sufficient coverage.

## Requirements
- [samtools](http://www.htslib.org/) ≥ 1.10
- bash ≥ 4

## Usage

```bash
bash bam_interval_threshold.sh <input_dir> <output_dir> <threshold_percentage> <region>
