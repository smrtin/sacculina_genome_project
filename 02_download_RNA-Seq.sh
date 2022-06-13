#!/bin/bash

OUTDIR='resources/Cirripedia_trans'
[ -d ${OUTDIR} ] || mkdir -p  ${OUTDIR}

echo -e "\nChecking Cirripadia RNA-Seq files\n"

for ID in SRR13785538 SRR13785539 SRR13785541 SRR426836 SRR5832119 SRR13785540 ; do 

    if [ ! -f  ${OUTDIR}/${ID}_1.fastq.gz ] ; then
                
        echo -e "\tdownloading files for ${ID}\n"
        fastq-dump --outdir ${OUTDIR} --log-level 5 --gzip --split-files ${ID}  

    else 

        echo -e "\tfiles for ${ID} already exist\n"
    fi
done