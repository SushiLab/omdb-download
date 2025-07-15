import pathlib
import gzip
import collections
import subprocess
import os


class Genomes:
    genomes = None

    def __init__(self, all_genomes):
        self.genomes = all_genomes
    def __init__(self):
        self.genomes = []
    def add(self, genome):
        self.genomes.append(genome)

    def get_genomes(self):
        return set([x.genome for x in self.genomes])
    def get_genomes_by_study(self, study):
        return set([x for x in self.get_genomes() if x[1] == study])

    def get_genes(self):
        return set([x.gene_nucl for x in self.genomes] + [x.gene_aa for x in self.genomes] + [x.gene_gff for x in self.genomes])
    def get_genes_by_study(self, study):
        return set([x for x in self.get_genes() if x[1] == study])

    def get_rrna(self):
        return set([x.rrna for x in self.genomes])
    def get_rrna_by_study(self, study):
        return set([x for x in self.get_rrna() if x[1] == study])

    def get_trna(self):
        return set([x.trna for x in self.genomes])
    def get_trna_by_study(self, study):
        return set([x for x in self.get_trna() if x[1] == study])

    def get_antismash(self):
        return set([x.antismash for x in self.genomes])
    def get_antismash_by_study(self, study):
        return set([x for x in self.get_antismash() if x[1] == study])


    def get_kegg(self):
        return set([x.kegg for x in self.genomes])
    def get_kegg_by_study(self, study):
        return set([x for x in self.get_kegg() if x[1] == study])


    def get_pfam(self):
        return set([x.pfam for x in self.genomes])
    def get_pfam_by_study(self, study):
        return set([x for x in self.get_pfam() if x[1] == study])


    def get_eggnog(self):
        return set([x.eggnog for x in self.genomes])
    def get_eggnog_by_study(self, study):
        return set([x for x in self.get_eggnog() if x[1] == study])

    def get_study(self, study):
        files = set().union(*[self.get_genes_by_study(study), self.get_genomes_by_study(study), self.get_rrna_by_study(study), self.get_trna_by_study(study), self.get_antismash_by_study(study), self.get_kegg_by_study(study), self.get_pfam_by_study(study), self.get_eggnog_by_study(study)])
        return files
class Genome:

    genome = None
    gene_nucl = None
    gene_aa = None
    gene_gff = None
    rrna = None
    trna = None
    antismash = None
    kegg = None
    pfam = None
    eggnog = None


    def __init__(self, source_genome_path, study, genome_fna):
        source_genome_path = 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/genomes/genomes/' + source_genome_path.split('./', 1)[-1]
        self.genome = (source_genome_path, study, genome_fna)

        self.gene_nucl = (source_genome_path.replace('.fa.gz', '.genes.fna.gz'), study, genome_fna.replace('.fa.gz', '.genes.fna.gz'))
        self.gene_aa = (source_genome_path.replace('.fa.gz', '.genes.faa.gz'), study, genome_fna.replace('.fa.gz', '.genes.faa.gz'))
        self.gene_gff = (source_genome_path.replace('.fa.gz', '.genes.gff.gz'), study, genome_fna.replace('.fa.gz', '.genes.gff.gz'))

        self.rrna = (source_genome_path.replace('.fa.gz', '.barrnap.0.9.fna.gz'), study, genome_fna.replace('.fa.gz', '.barrnap.0.9.fna.gz'))
        self.trna = (source_genome_path.replace('.fa.gz', '.aragorn.1.2.41.tsv.gz'), study, genome_fna.replace('.fa.gz', '.aragorn.1.2.41.tsv.gz'))
        self.antismash = (source_genome_path.replace('.fa.gz', '-antismash.tar.gz'), study, genome_fna.replace('.fa.gz', '-antismash.tar.gz'))
        self.kegg = (source_genome_path.replace('.fa.gz', '.kegg.apr22.tsv.gz'), study, genome_fna.replace('.fa.gz', '.kegg.apr22.tsv.gz'))
        self.pfam = (source_genome_path.replace('.fa.gz', '.eggnog.2.1.7-5.0.2.tsv.gz'), study,genome_fna.replace('.fa.gz', '.eggnog.2.1.7-5.0.2.tsv.gz'))
        self.eggnog = (source_genome_path.replace('.fa.gz', '.pfam.37.1.tsv.gz'), study,genome_fna.replace('.fa.gz', '.pfam.37.1.tsv.gz'))




def download_file(url, dest, show_progress=False):
    dest_path = os.path.dirname(dest)
    dest_tmp_fname = '.' + os.path.basename(dest) + ".tmp"
    dest_path_tmp = os.path.join(dest_path, dest_tmp_fname)

    try:
        # Build curl command
        cmd = [
            "curl",
            "-fL",  # fail on server errors, follow redirects
            url,
            "-o", dest_path_tmp
        ]

        if show_progress:
            cmd.append("--progress-bar")
        else:
            cmd.append("--silent")

        # Run curl
        result = subprocess.run(cmd, check=True)
        # Rename only if curl succeeds
        os.rename(dest_path_tmp, dest)
        if show_progress:
            print("\nDownload complete.")

    except subprocess.CalledProcessError as e:
        if os.path.exists(dest_path_tmp):
            try:
                os.remove(dest_path_tmp)
                print(f"Partial file '{dest_path_tmp}' removed due to error.")
            except Exception as cleanup_error:
                print(f"Failed to remove partial file: {cleanup_error}")
        print(f"Download failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        if os.path.exists(dest_path_tmp):
            os.remove(dest_path_tmp)
            print(f"\nDownload interrupted. Partial file '{dest_path_tmp}' removed.")
        sys.exit(1)

# def download_file(url, dest, show_progress=False):
#     try:
#         with requests.get(url, stream=True, timeout=10) as response:
#             response.raise_for_status()  # Raise error for HTTP codes like 404, 500
#             total_size = int(response.headers.get('Content-Length', 0))
#             downloaded = 0
#             start_time = time.time()
#             dest_path = dest.rsplit('/', 1)[0]
#             dest_tmp_fname = '.' + dest.split('/')[-1] + ".tmp"
#             dest_path_tmp = dest_path + '/' + dest_tmp_fname
#
#
#             with open(dest_path_tmp, 'wb') as out_file:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     if chunk:  # skip keep-alive chunks
#                         out_file.write(chunk)
#                         downloaded += len(chunk)
#
#                     if show_progress and total_size:
#                         elapsed = time.time() - start_time
#                         speed = downloaded / elapsed if elapsed > 0 else 0
#                         percent = (downloaded / total_size) * 100
#                         bar_length = 40
#                         filled = int(bar_length * downloaded / total_size)
#                         bar = '#' * filled + '-' * (bar_length - filled)
#                         sys.stdout.write(
#                             f"\r[{bar}] {percent:6.2f}% "
#                             f"{downloaded/1024/1024:.1f}MB "
#                             f"{speed/1024/1024:.1f}MB/s"
#                         )
#                         sys.stdout.flush()
#         if total_size and downloaded != total_size:
#             raise IOError(f"Incomplete download: {downloaded} bytes vs {total_size} expected")
#             sys.exit(1)
#         os.rename(dest_path_tmp, dest)
#         if show_progress and total_size:
#             print("\nDownload complete.")
#     except (requests.RequestException, IOError, KeyboardInterrupt) as e:
#         # Clean up if download was interrupted or failed
#         if os.path.exists(dest_path_tmp):
#             try:
#                 os.remove(dest_path_tmp)
#                 print(f"Partial file '{dest_path_tmp}' removed due to error.")
#             except Exception as cleanup_error:
#                 print(f"Failed to remove partial file: {cleanup_error}")
#         print(f"Download failed: {e}")
#         sys.exit(1)






def progress_bar(current, total, width=40):
    progress = int(width * current / total)
    bar = "[" + "#" * progress + "-" * (width - progress) + f"] {current}/{total}"
    sys.stdout.write('\r' + bar)
    sys.stdout.flush()

def read_map_file():
    studies = collections.Counter()
    all_genomes = Genomes()

    with gzip.open('omdb-download.v2.tsv.gz', 'rt') as handle:
        for cnt, line in enumerate(handle, 1):
            line = line.strip()
            [_, study, other] = line.split('/', 2)
            fname = other.split('/')[-1]
            if fname.endswith('.fa.gz'):
                studies[study] += 1
                g = Genome(line, study, fname)
                all_genomes.add(g)
            else:
                print(f'unknown file {fname}')



    #

    return studies, all_genomes#, all_genes





catalogs = {}
catalogs['OMDBv2.0_NT_G_R'] = ('OMDB Nucleotide gene catalog - Redundant genes from genomes n=508,832,278', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_R/OMDBv2.0_NT_G_R.fna.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_R/OMDBv2.0_NT_G_R.cluster.tsv.gz')
catalogs['OMDBv2.0_NT_G_NR100'] = ('OMDB Nucleotide gene catalog - Non-redundant genes from genomes n=325,384,975', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_NR100/OMDBv2.0_NT_G_NR100.fna.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_NR100/OMDBv2.0_NT_G_NR100.cluster.tsv.gz')
catalogs['OMDBv2.0_NT_G_NR95'] = ('OMDB Nucleotide gene catalog - Genes from genomes clustered at 95% n=103,044,829', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_NR95/OMDBv2.0_NT_G_NR95.fna.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_NR95/OMDBv2.0_NT_G_NR95.cluster.tsv.gz')

catalogs['OMDBv2.0_AA_G_R'] = ('OMDB Amino Acids gene catalog - Redundant genes from genomes n=508,832,278','https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_R/OMDBv2.0_AA_G_R.faa.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_R/OMDBv2.0_AA_G_R.cluster.tsv.gz')
catalogs['OMDBv2.0_AA_G_NR100'] = ('OMDB Amino Acids gene catalog - Non-redundant genes from genomes n=249,518,434','https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR100/OMDBv2.0_AA_G_NR100.faa.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR100/OMDBv2.0_AA_G_NR100.cluster.tsv.gz')
catalogs['OMDBv2.0_AA_G_NR50'] = ('OMDB Amino Acids gene catalog - Genes from genomes clustered at 50% n=28,862,112','https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR50/OMDBv2.0_AA_G_NR50.faa.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR50/OMDBv2.0_AA_G_NR50.cluster.tsv.gz')
catalogs['OMDBv2.0_AA_G_NR30'] = ('OMDB Amino Acids gene catalog - Genes from genomes clustered at 30% n=18,342,415','https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR30/OMDBv2.0_AA_G_NR30.faa.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR30/OMDBv2.0_AA_G_NR30.cluster.tsv.gz')

catalogs['OMDBv2.0_SC_G_R'] = ('OMDB genomes catalog - Redundant n = 69,280,421', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_SC_G_R/OMDBv2.0_SC_G_R.fa.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_SC_G_R/OMDBv2.0_SC_G_R.cluster.tsv.gz')
catalogs['OMDBv2.0_SC_G_NR100'] = ('OMDB genomes catalog - Non-redundant n = 68,726,394', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_SC_G_NR100/OMDBv2.0_SC_G_NR100.fa.gz', 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_SC_G_NR100/OMDBv2.0_SC_G_NR100.cluster.tsv.gz')


import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="List or download utility")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # List command
    list_parser = subparsers.add_parser("list", help="List available items")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download selected items")
    download_parser.add_argument(
        "-i", nargs="+", required=True,
        help="List of entries to download - use list method to see possible options."
    )
    download_parser.add_argument(
        "-o", "--output", required=True,
        help="Download folder path"
    )

    args = parser.parse_args()

    if args.command == "list":
        print('############# Downloadable data #############')
        print('#############################################')
        print('\n')
        print('################# Catalogs ##################')
        print('\n')
        for catalog in sorted(list(catalogs.keys())):
            (description, f1, f2) = catalogs[catalog]
            print(f'{catalog} - {description}')
        print('\n')
        print(f'Example 1 - Download a catalog:\n\tpython omdb-download.py download -i {catalog} -o output_folder')
        print('\n')
        print('############# All Genomes/Genes ##############')
        print('\n')

        studies, all_genomes = read_map_file()
        total_genomes = sum([int(x[1]) for x in studies.most_common()])
        print(f'all_genomes - {total_genomes:,} genome files')
        print(f'all_genes - {total_genomes * 3:,} genes files - (nucl + aa + gff)')
        print(f'all_rrna - {total_genomes:,} barrnap files - (fna)')
        print(f'all_trna - {total_genomes:,} aragorn files - (tsv)')
        print(f'all_antismash - {total_genomes:,} antismash files - (tar)')
        print(f'all_kegg - {total_genomes:,} kegg files - (tsv)')
        print(f'all_eggnog - {total_genomes:,} eggnog files - (tsv)')
        print(f'all_pfam - {total_genomes:,} pfam files - (tsv)')

        print('\n')
        print(f'Example 2 - download all genome files:\n\tpython omdb-download.py download -i all_genomes -o output_folder')
        print('\n')

        print('\n')
        print('########### Per Study Genomes/Genes/Annotation ###########')
        print('\n')
        for study, genome_count in studies.most_common():
            print(f'{study} - {genome_count * 10:,} files - {genome_count:,} genome file(s), {genome_count * 3:,} gene files - (nucl + aa + gff) , {genome_count * 6:,} annotation files')
        print('\n')
        print(f'Example 3 - download genomes/genes/annotation from one study:\n\tpython omdb-download.py download -i HETI17-1 -o output_folder')
        print(f'Example 4 - download genomes/genes/annotation from two studies:\n\tpython omdb-download.py download -i HETI17-1 JAHN19-1 -o output_folder')

    elif args.command == "download":
        if not args.i:
            print("Error: -i/--items must include at least one item")
            sys.exit(1)
        catalogs_to_download = set()
        items_to_download = set(args.i)
        for f in items_to_download:
            if f in catalogs:
                catalogs_to_download.add(f)
        items_to_download = items_to_download - catalogs_to_download

        all_genomes: Genomes = None
        studies, all_genomes = read_map_file()


        download_all_genomes = True if 'all_genomes' in items_to_download else False
        download_all_genes = True if 'all_genes' in items_to_download else False
        download_all_rrna = True if 'all_rrna' in items_to_download else False
        download_all_trna = True if 'all_trna' in items_to_download else False
        download_all_antismash = True if 'all_antismash' in items_to_download else False
        download_all_kegg = True if 'all_kegg' in items_to_download else False
        download_all_eggnog = True if 'all_eggnog' in items_to_download else False
        download_all_pfam = True if 'all_pfam' in items_to_download else False
        items_to_download.discard('all_genomes')
        items_to_download.discard('all_genes')
        items_to_download.discard('all_rrna')
        items_to_download.discard('all_trna')
        items_to_download.discard('all_antismash')
        items_to_download.discard('all_kegg')
        items_to_download.discard('all_eggnog')
        items_to_download.discard('all_pfam')


        files_to_download = set()
        if download_all_genomes:
            files_to_download.update(all_genomes.get_genomes())
        if download_all_genes:
            files_to_download.update(all_genomes.get_genes())
        if download_all_rrna:
            files_to_download.update(all_genomes.get_rrna())
        if download_all_trna:
            files_to_download.update(all_genomes.get_rrna())
        if download_all_antismash:
            files_to_download.update(all_genomes.get_antismash())
        if download_all_kegg:
            files_to_download.update(all_genomes.get_kegg())
        if download_all_eggnog:
            files_to_download.update(all_genomes.get_eggnog())
        if download_all_pfam:
            files_to_download.update(all_genomes.get_pfam())





        for study in studies.keys():
            if study in items_to_download:
                files_to_download.update(all_genomes.get_study(study))
                items_to_download.discard(study)
        if len(items_to_download) != 0:
            print(f'Unknown items to download: {items_to_download}. Quitting.')
            sys.exit(1)


        if len(catalogs_to_download) != 0:
            pathlib.Path(args.output).mkdir(exist_ok=True, parents=True)
            print('Downloading catalogs...')
            for catalog in catalogs_to_download:
                catalog_description, catalog_sequence_file, catalog_cluster_file = catalogs[catalog]

                print(f'\tDownloading catalog {catalog}...')
                dest_sequence_file = args.output + '/' + catalog_sequence_file.split('/')[-1]
                print(f'\tDownloading sequence file to {dest_sequence_file}')
                download_file(catalog_sequence_file, dest_sequence_file, True)
                print('\tFinished downloading sequence file...')

                dest_cluster_file = args.output + '/' + catalog_cluster_file.split('/')[-1]
                print(f'\tDownloading cluster file to {dest_cluster_file}')
                download_file(catalog_cluster_file, dest_cluster_file, True)
                print('\tFinished downloading cluster file...')
            print('Finished downloading catalogs...')
        if len(files_to_download) != 0:
            pathlib.Path(args.output).mkdir(exist_ok=True, parents=True)
            print('Downloading genes/genomes/annotations...')
            for cnt, (source, study, fname) in enumerate(files_to_download, 1):
                progress_bar(cnt, len(files_to_download))
                dest_folder = f'{args.output}/{study}/'
                pathlib.Path(dest_folder).mkdir(exist_ok=True, parents=True)
                dest = f'{args.output}/{study}/{fname}'
                download_file(source, dest, False)
            print('\nFinished downloading genes/genomes/annotations ...')









if __name__ == "__main__":
    main()