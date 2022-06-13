#!/bin/bash


# download TSA from NCBI 
# belonging to Cirripedia Taxonomy ID 6675

#module load anaconda3/2022.05
#conda activate sacculina_genome_project

[ -d resources/external_TSA/ ] || mkdir -p resources/external_TSA/
cd resources/external_TSA/

OUT_LIST="../../external_sequences.list"
echo -e "species\tfile" > ${OUT_LIST}

esearch -db nuccore -query '((txid6675[Organism:exp]) AND ("tsa master"[Properties] ))' | efetch -format gb | grep -P '^TSA\W+|^SOURCE\W+' - | sed -r 's/\W+/\t/g' | cut -f2,3 | paste - - | sed -r 's/\t/_/' | cut -f1,2 | while read NAME ID ; do 
 
	echo -e "\ntaxon: ${NAME} ID: ${ID}" 
	NUM=$(grep -c ${NAME} ${OUT_LIST} )
	if [ ${NUM} -gt 0 ]; then 

	echo -e "${NAME}-tsa${NUM}\tresources/external_TSA/${NAME}_ncbi_${ID}.fasta" >> ${OUT_LIST}
	
	else
	echo -e "${NAME}-tsa\tresources/external_TSA/${NAME}_ncbi_${ID}.fasta" >> ${OUT_LIST}
	fi
	# download the transcriptome from NCBI
	fastq-dump -F --fasta default --stdout ${ID} > ${NAME}_ncbi_${ID}.fasta 
	echo -e "\t---> complete.\n" 
done