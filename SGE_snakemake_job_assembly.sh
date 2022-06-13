#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j n
#$ -e SGE_logs/
#$ -o SGE_logs/
#$ -q large.q,medium.q
#$ -N saca_assembly
#$ -pe smp 56


module load anaconda3/2022.05
conda activate sacculina_genome_project

#one core will be used by snakemake to monitore the other processes
THREADS=$(expr ${NSLOTS} - 1)

snakemake \
    --snakefile workflow/Snakefile_assembly \
    --keep-going \
    --latency-wait 60 \
    --use-envmodules \
    --use-conda \
    --cores ${THREADS} \
    --verbose \
    --printshellcmds \
    --reason 


