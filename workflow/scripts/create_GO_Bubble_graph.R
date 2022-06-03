#!/usr/bin/env Rscript

library(GOplot)
library(ggrepel)
library(here)

source(here("workflow","scripts","local_GO_Bubble2.R"), chdir = TRUE)

args = commandArgs(trailingOnly=TRUE)

# example command: Rscript DE_noRibo/create_GO_Bubble_graph.R DE_noRibo/differential_Xpression/tmpdir_externa_vs_interna/EC.david DE_noRibo/differential_Xpression/tmpdir_externa_vs_interna/EC.genelist DE_noRibo/differential_Xpression/test_bubble_Plot

#information of interna and externa was joined
#only focusing on set of differentially expressed genes.

out_base <- args[3]

EC.david = read.table(args[1], sep='\t', header=T, quote="")
EC.genelist = read.table(args[2], sep='\t', header=T)

# plotting commands from: https://wencke.github.io/
circ <- circle_dat(EC.david, EC.genelist)


#############################
## The bubble plot (GOBubble)
#############################



####final ####

image <- GOBubble2(circ, labels = 1.3, display = 'multiple', ID = F)
ggsave(file=paste(out_base , 'svg', sep='.' ), plot=image, width=24, height=15)
ggsave(file=paste(out_base , 'pdf', sep='.' ), plot=image, width=24, height=15)

####
