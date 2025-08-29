#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

# Usage check
if [[ $# -lt 4 ]]; then
  echo "Usage: $0 <input_dir> <output_dir> <threshold_percentage> <region>"
  echo "Example: $0 /path/to/bams /path/to/output 80 17:7588574-7588776"
  exit 1
fi

bam_directory=$1   # input directory with BAMs
out_dir=$2         # output directory
threshold=$3       # e.g. 80
region=$4          # e.g. 17:7588574-7588776

mkdir -p "$out_dir"
output_csv="${out_dir}/qualifying_files.csv"

echo "sample,total_positions,covered_positions,percent_covered" > "$output_csv"

for bam in "$bam_directory"/*.bam; do
  sample=$(basename "$bam" .bam)

  echo "▶️  Processing $sample ..."

  # Ensure BAM index exists
  if [[ ! -e "$bam.bai" && ! -e "${bam%.bam}.bai" && ! -e "$bam.csi" && ! -e "${bam%.bam}.csi" ]]; then
    echo "   Index not found, creating..."
    samtools index "$bam"
  fi

  read -r tot cov pct <<< "$(
    samtools depth -a -r "$region" "$bam" \
    | awk 'BEGIN{t=0;c=0}{t++; if($3>0) c++} END{if(t>0) printf "%d %d %.2f\n", t, c, 100*c/t; else print "0 0 0.00"}'
  )"

  if (( tot == 0 )); then
    echo "   ⚠️ WARNING: $sample -> 0 positions returned (contig mismatch?)."
    continue
  fi

  if (( 100*cov >= threshold*tot )); then
    echo "   ✅ $sample qualifies ($pct% coverage, threshold=$threshold%)"
    echo "$sample,$tot,$cov,$pct" >> "$output_csv"
  else
    echo "   ❌ $sample does NOT qualify ($pct% coverage, threshold=$threshold%)"
  fi

  echo "   ✔️ Completed $sample"
done

echo "🎉 Processing complete. Saved qualifying samples to $output_csv"

