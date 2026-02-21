#!/bin/bash
#===============================================================================
# Script to download FASTQ files from an S3 bucket, concatenate multiple files
# if necessary, and place the final file directly under the data directory.
#===============================================================================

# Display usage if insufficient arguments
if [ $# -lt 5 ]; then
    echo "Usage: $0 <datadir> <lib> <bucket> <datasourcepath> <regex_fq>"
    exit 1
fi

# Input arguments
datadir="$1"          # local directory where final FASTQ will be stored (e.g. /home/ubuntu/DATA_DRIVE/SMRNA_PBATCH1/reads)
lib="$2"              # library ID (e.g. LIB7912)
bucket="$3"           # S3 bucket name
datasourcepath="$4"   # path inside the bucket (e.g. human/small_RNA/Trimmed/.../LIB7912)
regex_fq="$5"         # pattern to match FASTQ files (e.g. *_2.fq.gz)

# Remove leading asterisk from regex to form the output file suffix
suffix="${regex_fq#\*}"

# Create temporary directory for this library
tmp_dir="${datadir}/${lib}"
mkdir -p "$tmp_dir"

# Copy all matching FASTQ files from S3 to the temporary directory
# Using a specific AWS profile ("emulsion-enabl-raw") – adjust if needed.
echo "Copying from s3://${bucket}/${datasourcepath} to ${tmp_dir} ..."
aws s3 cp "s3://${bucket}/${datasourcepath}" "$tmp_dir" \
    --recursive \
    --exclude "*.txt" \
    --include "$regex_fq" \
    --profile emulsion-enabl-raw

# Collect the paths of the downloaded files
files=()
for f in "${tmp_dir}"/${regex_fq}; do
    [ -e "$f" ] && files+=("$f")
done

# Concatenate if more than one file, otherwise copy the single file
output_file="${datadir}/${lib}${suffix}"

if [ ${#files[@]} -gt 1 ]; then
    echo "Concatenating ${#files[@]} files into ${output_file} ..."
    cat "${files[@]}" > "$output_file"
elif [ ${#files[@]} -eq 1 ]; then
    echo "Copying single file to ${output_file} ..."
    cp "${files[0]}" "$output_file"
else
    echo "ERROR: No files matching pattern '${regex_fq}' found in S3 source."
    exit 1
fi

# Clean up temporary directory
rm -rf "$tmp_dir"
echo "Done."