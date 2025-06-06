# omdb-download

Download genomes, genes and catalogs of the [OMDB](https://omdb.microbiomics.io/) resource.

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

The list subroutine will show the user what data products can be downloaded.

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


all_genomes - 274282 genome files
all_genes - 822846 genes files - (nucl + aa + gff)


Example 2 - download all genome files:
	python omdb-download.py download -i all_genomes -o output_folder




########### Per Study Genomes/Genes ###########


TPAC - 139124 files - 34781 genome(s) files, 104343 gene file(s) - (nucl + aa + gff)
TOPC - 118292 files - 29573 genome(s) files, 88719 gene file(s) - (nucl + aa + gff)
BPAM22-1 - 75436 files - 18859 genome(s) files, 56577 gene file(s) - (nucl + aa + gff)
RSGB23-1 - 54560 files - 13640 genome(s) files, 40920 gene file(s) - (nucl + aa + gff)
LUOE20-1 - 46272 files - 11568 genome(s) files, 34704 gene file(s) - (nucl + aa + gff)
KOPF15-1 - 34972 files - 8743 genome(s) files, 26229 gene file(s) - (nucl + aa + gff)
SANC23-1 - 25952 files - 6488 genome(s) files, 19464 gene file(s) - (nucl + aa + gff)

...

CHEN19-1 - 4 files - 1 genome(s) files, 3 gene file(s) - (nucl + aa + gff)
YANG21-1 - 4 files - 1 genome(s) files, 3 gene file(s) - (nucl + aa + gff)


Example 3 - download genes and genomes from one study:
	python omdb-download.py download -i HETI17-1 -o output_folder
Example 4 - download genes and genomes from two studies:
	python omdb-download.py download -i HETI17-1 JAHN19-1 -o output_folder
```

### download

The download subroutine will download selected data files:

Download genomes/genes:

```bash
$ python omdb-download.py download -i HETI17-1 JAHN19-1 -o output_folder
Downloading genes/genomes...
[########################################] 64/64
Finished downloading genes/genomes ...

$ ls output_folder/*/*
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.fa.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.genes.faa.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.genes.fna.gz
output_folder/HETI17-1/HETI17-1_SAMN04447814_MAG_00000002.genes.gff.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.fa.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.genes.faa.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.genes.fna.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953129_MAG_00000001.genes.gff.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953131_MAG_00000001.fa.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953131_MAG_00000001.genes.faa.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953131_MAG_00000001.genes.fna.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953131_MAG_00000001.genes.gff.gz
output_folder/JAHN19-1/JAHN19-1_SAMN10953132_MAG_00000001.fa.gz
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




