#!/usr/bin/env python3
"""
Main script to prepare the sample sheet and launch the nf-core/smrnaseq pipeline.
Reads configuration and sample information, creates a sample.csv file, and starts the pipeline.
"""

import pandas as pd
import subprocess
from multiprocessing import Process
import os
import configparser

def run_pipeline(pipeline_path, workdir, refpath, conf_file, contamination_path):
    """
    Launch the smrnaseq pipeline by calling the shell script.
    """
    script_path = os.path.join(pipeline_path, 'shellScript', 'smrnaPileline.sh')
    subprocess.call(['sh', script_path, workdir, refpath, conf_file, contamination_path])
    print("\n###-----------------------------------------------------------------###")
    print("Finished pipeline run ......................................!!")
    print("###-----------------------------------------------------------------###\n")

if __name__ == '__main__':
    # =========================================================================
    # Load configuration
    # =========================================================================
    pipeline_path = "/home/ubuntu/SMRNAProcesPipe"
    config = configparser.ConfigParser()
    config.read(os.path.join(pipeline_path, "data", "config.ini"))

    workdir          = config.get("PATHS", "workdir")          # main working directory
    datadir          = config.get("PATHS", "datadir")          # where FASTQ files are stored (or will be copied)
    conf_file        = config.get("PATHS", "conf_file")        # Nextflow config file
    refpath          = config.get("PATHS", "refpath")          # reference genome base directory
    bucket           = config.get("PATHS", "bucket")           # S3 bucket name (unused here, kept for reference)
    sampleinfo       = config.get("PATHS", "sampleinfo")       # TSV file with sample metadata
    regex_fq         = config.get("PATHS", "regex_fq")         # pattern to match FASTQ files (e.g. *_2.fq.gz)
    contamination_path = config.get("PATHS", "contamination_path")  # folder with contaminant FASTA files
    perform_deg      = config.get("PATHS", "perform_deg")      # whether differential expression will be run later

    # Create working directory if it does not exist
    os.makedirs(workdir, exist_ok=True)

    # =========================================================================
    # Read sample information and build the sample sheet for Nextflow
    # =========================================================================
    df = pd.read_csv(sampleinfo, sep="\t")
    fq_dicts = []

    for idx in df.index:
        lib_id = df['Library_ID'][idx]

        # Build the expected FASTQ file name (single‑end, UMI in read)
        fastq_path = os.path.join(datadir, lib_id + regex_fq.replace("*", ""))

        if perform_deg == "True":
            file_dict = {
                'sample': lib_id,
                'fastq_1': fastq_path,
                'group': df['Groups'][idx]
            }
        else:   # DEG not requested → omit group column
            file_dict = {
                'sample': lib_id,
                'fastq_1': fastq_path
            }

        fq_dicts.append(file_dict)

    # Write the sample sheet (sample.csv) required by nf-core/smrnaseq
    sample_df = pd.DataFrame(fq_dicts)
    sample_csv = os.path.join(workdir, "sample.csv")
    sample_df.to_csv(sample_csv, index=False)
    print("Sample sheet created:\n", sample_df)

    # =========================================================================
    # Launch the pipeline in a separate process
    # =========================================================================
    pipeline_process = Process(target=run_pipeline,
                               args=(pipeline_path, workdir, refpath, conf_file, contamination_path))
    pipeline_process.start()
    pipeline_process.join()