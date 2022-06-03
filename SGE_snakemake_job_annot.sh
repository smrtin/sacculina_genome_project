#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j n
#$ -e SGE_logs/
#$ -o SGE_logs/
#$ -q large.q,medium.q
#$ -N saca_annot
#$ -pe smp 56


module load singularity/3.6.0 
module load anaconda3/2020.02
conda activate ERTE_annotation

#one core will be used by snakemake to monitore the other processes
THREADS=$(expr ${NSLOTS} - 1)

snakemake \
    --snakefile workflow/Snakefile_annotation \
    --keep-going \
    --latency-wait 60 \
    --use-envmodules \
    --use-conda \
    --use-singularity \
    --singularity-args "--home $PWD" \
    --singularity-args "--bind $PWD/temp/:/tmp/" \
    --cores ${THREADS} \
    --verbose \
    --printshellcmds \
    --reason 

# snakemake --use-envmodules --cores ${THREADS} --verbose --printshellcmds --rerun-incomplete
# download and setup of conda environments must be performed on headnode...
# --use-conda --use-singularity --cores 1 --conda-create-envs-only


