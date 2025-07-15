# omdb-download

Download genomes, genes, annotations and catalogs of the [OMDB](https://omdb.microbiomics.io/) resource.

## Installation:

The tool is written in Python (tested with >=3.9), works without any further python dependencies and was tested on MacOS and Linux.

```bash
$ git clone git@github.com:SushiLab/omdb-download.git
$ cd omdb-download
$ python omdb-download.py  --help
usage: omdb-download.py [-h] {list,download} ...

List or download utility

positional arguments:
  {list,download}
    list           List available items
    download       Download selected items

options:
  -h, --help       show this help message and exit

```


## Usage:

### list

The list command will print what data products can be downloaded.

```bash
$python omdb-download.py list
############# Downloadable data #############
#############################################


################# Catalogs ##################


OMDBv2.0_AA_G_NR100 - OMDB Amino Acids gene catalog - Non-redundant genes from genomes n=249,518,434
OMDBv2.0_AA_G_NR30 - OMDB Amino Acids gene catalog - Genes from genomes clustered at 30% n=18,342,415
OMDBv2.0_AA_G_NR50 - OMDB Amino Acids gene catalog - Genes from genomes clustered at 50% n=28,862,112
OMDBv2.0_AA_G_R - OMDB Amino Acids gene catalog - Redundant genes from genomes n=508,832,278
OMDBv2.0_NT_G_NR100 - OMDB Nucleotide gene catalog - Non-redundant genes from genomes n=325,384,975
OMDBv2.0_NT_G_NR95 - OMDB Nucleotide gene catalog - Genes from genomes clustered at 95% n=103,044,829
OMDBv2.0_NT_G_R - OMDB Nucleotide gene catalog - Redundant genes from genomes n=508,832,278
OMDBv2.0_SC_G_NR100 - OMDB genomes catalog - Non-redundant n = 68,726,394
OMDBv2.0_SC_G_R - OMDB genomes catalog - Redundant n = 69,280,421


Example 1 - Download a catalog:
	python omdb-download.py download -i OMDBv2.0_SC_G_R -o output_folder


############# All Genomes/Genes ##############


all_genomes - 274,282 genome files
all_genes - 822,846 genes files - (nucl + aa + gff)
all_rrna - 274,282 barrnap files - (fna)
all_trna - 274,282 aragorn files - (tsv)
all_antismash - 274,282 antismash files - (tar)
all_kegg - 274,282 kegg files - (tsv)
all_eggnog - 274,282 eggnog files - (tsv)
all_pfam - 274,282 pfam files - (tsv)


Example 2 - download all genome files:
	python omdb-download.py download -i all_genomes -o output_folder




########### Per Study Genomes/Genes/Annotation ###########


TPAC - 347,810 files - 34,781 genome file(s), 104,343 gene files - (nucl + aa + gff) , 208,686 annotation files
TOPC - 295,730 files - 29,573 genome file(s), 88,719 gene files - (nucl + aa + gff) , 177,438 annotation files
BPAM22-1 - 188,590 files - 18,859 genome file(s), 56,577 gene files - (nucl + aa + gff) , 113,154 annotation files
RSGB23-1 - 136,400 files - 13,640 genome file(s), 40,920 gene files - (nucl + aa + gff) , 81,840 annotation files
LUOE20-1 - 115,680 files - 11,568 genome file(s), 34,704 gene files - (nucl + aa + gff) , 69,408 annotation files
KOPF15-1 - 87,430 files - 8,743 genome file(s), 26,229 gene files - (nucl + aa + gff) , 52,458 annotation files
SANC23-1 - 64,880 files - 6,488 genome file(s), 19,464 gene files - (nucl + aa + gff) , 38,928 annotation files

...

HETI17-1 - 10 files - 1 genome file(s), 3 gene files - (nucl + aa + gff) , 6 annotation files
NGUG20-1 - 10 files - 1 genome file(s), 3 gene files - (nucl + aa + gff) , 6 annotation files
CHEN19-1 - 10 files - 1 genome file(s), 3 gene files - (nucl + aa + gff) , 6 annotation files
YANG21-1 - 10 files - 1 genome file(s), 3 gene files - (nucl + aa + gff) , 6 annotation files


Example 3 - download genes and genomes from one study:
	python omdb-download.py download -i HETI17-1 -o output_folder
Example 4 - download genes and genomes from two studies:
	python omdb-download.py download -i HETI17-1 JAHN19-1 -o output_folder
```

### download

The download command will download selected data files:

Download genomes/genes/annotations:

```bash
$ python omdb-download.py download -i HETI17-1 JAHN19-1 -o output_folder
Downloading genes/genomes/annotations...
[########################################] 160/160
Finished downloading genes/genomes/annotations ...

$ ls output_folder/*/* | sort
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002-antismash.tar.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.aragorn.1.2.41.tsv.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.barrnap.0.9.fna.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.eggnog.2.1.7-5.0.2.tsv.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.fa.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.genes.faa.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.genes.fna.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.genes.gff.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.kegg.apr22.tsv.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.pfam.37.1.tsv.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001-antismash.tar.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.aragorn.1.2.41.tsv.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.barrnap.0.9.fna.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.eggnog.2.1.7-5.0.2.tsv.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.fa.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.genes.faa.gz
...
```

Download a catalog:

```bash
$ python omdb-download.py download -i OMDBv2.0_AA_G_NR50 -o output_folder
Downloading catalogs...
	Downloading catalog OMDBv2.0_AA_G_NR50...
	Downloading sequence file to output_folder/OMDBv2.0_AA_G_NR50.faa.gz
######################################################################################################################################################### 100.0%

Download complete.
	Finished downloading sequence file...
	Downloading cluster file to output_folder/OMDBv2.0_AA_G_NR50.cluster.tsv.gz
######################################################################################################################################################### 100.0%

Download complete.
	Finished downloading cluster file...
Finished downloading catalogs..
```




