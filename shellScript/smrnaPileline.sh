#!/bin/bash
#===============================================================================
# Launch the nf-core/smrnaseq pipeline with UMI extraction and contamination filtering.
#===============================================================================

# Input arguments (passed from the Python script)
workdir="$1"                # working directory containing sample.csv
refpath="$2"                # base directory for igenomes references
conf_file="$3"              # custom Nextflow configuration
contamination_path="$4"      # folder with contaminant FASTA files

# Run the pipeline
nextflow run nf-core/smrnaseq \
    -profile docker,qiaseq \
    -r 2.4.0 \
    -c "$conf_file" \
    --igenomes_base "$refpath" \
    --input "${workdir}/sample.csv" \
    -work-dir "${workdir}/work" \
    --genome 'GRCh38' \
    --mirtrace_species 'hsa' \
    --three_prime_adapter auto-detect \
    --save_umi_intermeds true \
    --with_umi \
    --umitools_extract_method regex \
    --umitools_bc_pattern '.+(?P<discard_1>AACTGTAGGCACCATCAAT){s<=2}(?P<umi_1>.{12})(?P<discard_2>.*)' \
    --filter_contamination \
    --rrna "${contamination_path}/GCF_000001405.39_filtered_GRCh38.p13_rna.fna" \
    --trna "${contamination_path}/hg38-mature-tRNAs.fa" \
    --cdna "${contamination_path}/Homo_sapiens.GRCh38.cdna.all.fa.gz" \
    --ncrna "${contamination_path}/Homo_sapiens.GRCh38.ncrna.fa.gz" \
    --pirna "${contamination_path}/piRNAdb.hsa.v1_7_6.fa" \
    --save_reference \
    --outdir "${workdir}/results" \
    -resume
    
# The -resume flag allows the pipeline to restart from where it left off if interrupted.