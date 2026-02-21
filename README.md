# SMRNA Processing Pipeline

This repository contains a wrapper pipeline for analyzing small RNA‑seq data using [nf-core/smrnaseq](https://nf-co.re/smrnaseq) (version 2.4.0). It is designed for libraries with UMIs embedded in the read and includes adapter trimming, UMI extraction, contamination filtering, and miRNA quantification.

## Requirements

- Linux (Ubuntu 20.04/22.04 recommended)
- Python 3.6+ with `pandas`
- Nextflow (≥21.10)
- Docker (or Singularity)
- AWS CLI (only if downloading from S3)

## Installation

1. Clone this repository:
   ```bash
   git clone https://your-git-server/SMRNAProcesPipe.git
   cd SMRNAProcesPipe

2. Install Python dependencies:

    pip install pandas

3. Install Nextflow and Docker if not already available (see Nextflow and Docker documentation).

4. Prepare reference data:

    iGenomes GRCh38 base directory (e.g., /home/ubuntu/DATA_DRIVE_REF/references)

    Contamination FASTA files (rRNA, tRNA, cDNA, ncRNA, piRNA) in a separate folder (e.g., /home/ubuntu/DATA_DRIVE_REF/RNA_Contamination_Data)

5. Configuration

    Edit data/config.ini to set your paths and options:
    Prepare data/sample_info.tsv (tab‑separated) with at least Library_ID and (if perform_deg=True) Groups. 

## Running the Pipeline

Simply execute the Python wrapper:

    python runParallel_SMRNA.py

## Outputs

    Results are saved in workdir/results/. Key outputs include:

    multiqc/ – aggregated HTML report

    mirtrace/ – miRNA quality report

    salmon.merged.gene_counts.tsv – miRNA count matrix

    mature_counts.tsv – counts per mature miRNA

## Troubleshooting
    Out of memory: Increase resources in data/modified_base.config.

    Missing FASTQ files: Verify datadir contains files named exactly as expected.

    AWS errors: Ensure AWS CLI is configured with the correct profile.