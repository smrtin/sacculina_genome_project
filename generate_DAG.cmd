
## generate dag for parts of workflow

snakemake --dag --snakefile workflow/Snakefile_annotation | dot -Tsvg > workflow_annotation_dag.svg

