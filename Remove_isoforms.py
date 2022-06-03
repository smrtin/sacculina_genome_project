#!/usr/bin/env python3

import argparse
import csv
import os
import re
import sys
import wget
import subprocess
from Bio import SeqIO
from BCBio import GFF
from io import StringIO


def read_csv(file_name):
    '''Read the CSV input file.\n
    Return dictionary.
    '''
    with open(file_name , newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(),delimiters=None)
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, delimiter=dialect.delimiter)
        data = list(reader)             # read everything else into a list of rows
    
    return data


def get_args(argv=None):
    '''Parses the command line options.\n
    Returns populated namespace.
    '''
    parser = argparse.ArgumentParser(description="collect information of species barcodes from NCBI or Bold and occurences on GBIF.")
    parser.add_argument("-i", "--infile", help="Input file name ")
    parser.add_argument("-o", "--outfile",help="output file name ")
    
    parser.add_argument("-v", "--version", action="store_true",
                        help="output version information and exit")

    if len(sys.argv) == 1:
        # display usage message when no args are passed.
        sys.exit(parser.print_usage())

    return parser.parse_args(argv)


def download_genome(taxon, genome_url):
    parts=(taxon,'genome','fas','gz')
    genome_path='.'.join(parts[:-1])
    genome_path_compressed='.'.join(parts)

    if os.path.exists(genome_path) :
        print('\tGenome file already exists.\tSkipping download')
    elif os.path.exists(genome_path_compressed):
        print('\tGenome download already complete.\tneed to decompress ')
        fout = open(genome_path, 'wb')
        command=['zcat','-f',genome_path_compressed  ]
        subprocess.run(command, stdout=fout)
        fout.close()
    else:
        print('\tGenome download starting ... ')
        wget.download(genome_url, genome_path_compressed)

        fout = open(genome_path, 'wb')
        command=['zcat','-f', genome_path_compressed  ]
        subprocess.call(command, stdout=fout)
        fout.close()


def download_gff(taxon, gff_url):

    parts=(taxon,'gff','gz')
    gff_path='.'.join(parts[:-1])
    gff_path_compressed='.'.join(parts)

    if os.path.exists(gff_path) :
        print('\tGFF file already exists.\tSkipping download')
    elif os.path.exists(gff_path_compressed):
        print('\tGFF download already complete.\tneed to decompress ')
        fout = open(gff_path, 'wb')
        command=['zcat','-f',gff_path_compressed  ]
        subprocess.run(command, stdout=fout)
        fout.close()
    else:
        print('\tGFF download starting...')
        wget.download(gff_url, gff_path_compressed)

        fout = open(gff_path, 'wb')
        command=['zcat','-f', gff_path_compressed  ]
        subprocess.call(command, stdout=fout)
        fout.close()


def extract_proteins(taxon):
    collection={}
    genome='.'.join([taxon,'genome','fas'])
    gff='.'.join([taxon,'gff'])
    
    command=['gffread', gff , '-g' ,genome ,'-y', '-','-F']
    #print('running : {cmd}'.format(cmd=command))
    p = subprocess.run(command,capture_output=True )
    Seq_Dict=SeqIO.to_dict(SeqIO.parse(StringIO(p.stdout.decode()), 'fasta'))

    print('\n\tNumber of <gffread> generated Protein sequences: {total}'.format(total=len(Seq_Dict.keys())))

    for key in Seq_Dict.keys():
        description=Seq_Dict[key].description.split(" ",1)[1]
        elements=description.split(";")
        
        for i in elements:
            name=''
            if re.match(r".+=.+", i ):
        
                name=i.split("=")[0]

                if name == 'protein_id':
                    Prot_name=i.split("=")[1]

        collection[Prot_name]=Seq_Dict[key].seq.replace('.','*')
        
    return collection


def filter_longest_per_gene(prot_dict,gene_dict):
    longest_collection=dict()

    for gene in gene_dict.keys():
        if len(gene_dict[gene]) != 0 :
            Best_length=0
            longest_name=''
            longest_seq=''
            for prot_id in gene_dict[gene]:
                sequence=prot_dict[prot_id]
                length=len(sequence)
                if length >= Best_length :
                    longest_prot=prot_id
                    longest_seq=sequence
            longest_collection[prot_id]=longest_seq
    return longest_collection


def read_gff(file):
    '''read in the gff file and store gene name and corresponding protein IDs'''

    in_handle = open(file)
    total_genes=0
    total_proteins=0
    genes_more_than_one=0
    genes=dict()

    for rec in GFF.parse(in_handle): #, target_lines=50, limit_info=dict(gff_id=['NC_060018.1']) ):
        for feat in rec.features:
            if feat.type == 'gene':
                genes[feat.id] = set()
                for sub in feat.sub_features:
                    if sub.type == 'mRNA':
                        for part in sub.sub_features:
                            if part.type == 'CDS' :
                                proteinids=part.qualifiers['protein_id']
                                genes[feat.id].update(proteinids)

                if len(genes[feat.id]) != 0 :
                    total_genes+=1
                    total_proteins+=len(genes[feat.id])
                    if len(genes[feat.id]) >= 2 :
                        genes_more_than_one +=1

    print('\tSummary of gff file:\n\tprotein-coding genes: {}\tproteins: {}\tgene with multiple proteins: {}'.format(total_genes, total_proteins, genes_more_than_one))    
    in_handle.close()

    return genes
    
def print_output(tax,prot):
    file_name='.'.join([tax,'fas'])

    with open(file_name , 'w') as outfile:
        for id in prot.keys():
            outfile.write('>{}\n{}\n'.format(id,prot[id]))
    outfile.close()
   

# MAIN
if __name__ == "__main__":

    args = get_args()
    data = read_csv(args.infile)
    #print('done..{data}'.format(data=data))
    #with Bar('Processing', max=len(data)) as bar:
    for row in data:
        print('Working on taxon: {tax}'.format(tax=row['Taxon']))
        taxon=row['Taxon']
    #        bar.next()
        download_genome(taxon,row['Genome_link'])
        download_gff(taxon ,row['GFF_link'])
        
        prot_seq=extract_proteins(row['Taxon']) 
        gff_file='.'.join([taxon , 'gff'])
        gene_dict=read_gff(gff_file)
        long_proteins=filter_longest_per_gene(prot_seq,gene_dict)

        print('\t{} longest proteins extracted'.format(len(long_proteins.keys())))
        print_output(taxon,long_proteins)
