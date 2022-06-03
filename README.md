# Sacculina Genome Project
A workflow for genome assembly, annotation and differential expression analysis of Sacculina carcini

## Introduction

A few arthropods evolved towards an endoparasites and show a dramatic change in body shape and anatomy, often barely resembling arthropods at all. The parasitic barnacle Sacculina carcini (Crustacea: Rhizocephala) is one prominent example in evolutionary transformation due to an endoparasitic lifestyle. The adults show no sign of their arthropod kin: segmentation, appendages and most of the internal organs usually found in arthropods are completely missing. The adult body is divided into two parts: a network of rootlets growing in the body cavity of the crab hosts and a temporary breeding sac, bearing gonads and keeping first larval stages. There is a good record of studies on morphology and life cycle, but almost nothing is known about the genome of rhizocephalan species. 

This project aims to get a better understanding about the genetic and genomic foundations of this extreme modification of morphology. Assembly and annotation of the genome and differential gene expression focussing rootlet and breeding sac. Also a comparison to the standard repertoire of other arthropod genomes and a new survey genomes dataset of the non-parasitic barnacle Balanus amphitrite was performed.

Here we document the analysis steps and provide a snakmake workflow.

Sequences can be accessed under NCBI: 
https://www.ncbi.nlm.nih.gov/bioproject/659937


## Prerequisites

Anaconda3 and singularity.

conda environment.yaml -> update to latest packages and adjust versions!

# Workflow

Different steps of the workflow are performed with snakemake. Each step can be started individually and we also provide a Jobscript for a SGE queuingsystem.


## Genome assembly

## Genome annotation 

Genome annotation is performed with FUNANNOTATE. We use the genome and RNA-Seq data for training and external data during the prediction. As external data from other Cirripedia we downloaded available TSA files from NCBI with the '02_download_TSA_cirripedia.sh'-script. In addition tho these Sequence files we also downloaded and assembled RNA-Seq data from three cirriped species.

## Comparative genomics
To download a set of genomes and their corresponding annotation we provide a tablefile, which contains download links, to the script Remove_isoforms.py. This script will automatically download the genome and gff files, extract proteinsequences and if we have multiple variants per gene, keep only the longest sequence. With this we remove isoforms that are problematic during the next orthofinder step.
Then we run orthofinder on the external protein sequences, add the gene prediction from Sacculina carcini and also reroot the generated phylogenetic tree, so it fits better to the literature.
Based on the orthofinder output we generate some graphs on duplicationsevents, gene loss and most recent common ancesteral orthogroups.

## Differential Expression analysis

Analysis of differentially expressed genes were performed on three samples, two originating from tissue samples from the interna and one from the externa. RNA-Seq reads were mapped to the genome sequence and then assembled with trinity. After the assembly additional steps were performed to add information about GO terms with the help of TRINOTATE.  Differential expression analysis was mainly done with helperscripts from trinity.
We estimated abundance by mapping reads to the transcriptome assembly, for each sample. We used RSEM to estimate expression values. 

# Citation

# References
- conda
- singularity
- snakemake
- trinity
- fastp
- flye
- BESST
- pilon
- blast
- hmmer
- funannotate
- orthofinder
- hisat2
- samtools
- seqkit

# Funding 
This project was funded by the Deutsche Forschungsgemeinschaft (DFG) - Project number 252344899

https://gepris.dfg.de/gepris/projekt/252344899



