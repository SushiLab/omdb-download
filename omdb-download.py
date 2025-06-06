import argparse
import sys
import urllib.request
import time
import sys
import pathlib
import gzip
import collections
import os

def download_file(url, dest, show_progress=False):
    try:
        with urllib.request.urlopen(url) as response:
            total_size = response.getheader('Content-Length')
            total_size = int(total_size) if total_size else None
            block_size = 8192
            downloaded = 0
            start_time = time.time()

            with open(dest, 'wb') as out_file:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    out_file.write(buffer)
                    downloaded += len(buffer)

                    if show_progress and total_size:
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed if elapsed > 0 else 0
                        percent = (downloaded / total_size) * 100
                        bar_length = 40
                        filled = int(bar_length * downloaded / total_size)
                        bar = '#' * filled + '-' * (bar_length - filled)
                        sys.stdout.write(
                            f"\r[{bar}] {percent:6.2f}% "
                            f"{downloaded/1024/1024:.1f}MB "
                            f"{speed/1024/1024:.1f}MB/s"
                        )
                        sys.stdout.flush()

        if show_progress and total_size:
            print("\nDownload complete.")
    except (Exception, KeyboardInterrupt) as e:
        # Clean up if download was interrupted or failed
        if os.path.exists(dest):
            try:
                os.remove(dest)
                print(f"Partial file '{dest}' removed due to error.")
            except Exception as cleanup_error:
                print(f"Failed to remove partial file: {cleanup_error}")
        print(f"Download failed: {e}")
        sys.exit(1)


def progress_bar(current, total, width=40):
    progress = int(width * current / total)
    bar = "[" + "#" * progress + "-" * (width - progress) + f"] {current}/{total}"
    sys.stdout.write('\r' + bar)
    sys.stdout.flush()

def read_map_file():
    studies = collections.Counter()
    study_2_files = collections.defaultdict(list)
    all_genomes = set()
    all_genes = set()

    with gzip.open('omdb-download.tsv.gz', 'rt') as handle:
        for cnt, line in enumerate(handle, 1):
            line = line.strip()
            [_, study, other] = line.split('/', 2)
            fname = other.split('/')[-1]
            if fname.endswith('.fa.gz'):
                studies[study] += 1
                all_genomes.add((line, study, fname))
            else:
                all_genes.add((line, study, fname))
            study_2_files[study].append((line, study, fname))

    return studies, study_2_files, all_genomes, all_genes





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
        print(f'Example 1 - Download a catalog:\n\tpython omdb-downloader.py download -i {catalog} -o output_folder')
        print('\n')
        print('############# All Genomes/Genes ##############')
        print('\n')

        studies, study_2_files, all_genomes, all_genes = read_map_file()
        total_genomes = sum([int(x[1]) for x in studies.most_common()])
        print(f'all_genomes - {total_genomes} genome files')
        print(f'all_genes - {total_genomes * 3} genes files - (nucl + aa + gff)')
        print('\n')
        print(f'Example 2 - download all genome files:\n\tpython omdb-downloader.py download -i all_genomes -o output_folder')
        print('\n')

        print('\n')
        print('########### Per Study Genomes/Genes ###########')
        print('\n')
        for study, genome_count in studies.most_common():
            print(f'{study} - {genome_count * 4} files - {genome_count} genome(s) files, {genome_count * 3} gene file(s) - (nucl + aa + gff) ')
        print('\n')
        print(f'Example 3 - download genes and genomes from one study:\n\tpython omdb-downloader.py download -i HETI17-1 -o output_folder')
        print(f'Example 4 - download genes and genomes from two studies:\n\tpython omdb-downloader.py download -i HETI17-1 JAHN19-1 -o output_folder')
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

        studies, study_2_files, all_genomes, all_genes = read_map_file()
        download_all_genomes = True if 'all_genomes' in items_to_download else False
        download_all_genes = True if 'all_genes' in items_to_download else False
        items_to_download.discard('all_genomes')
        items_to_download.discard('all_genes')
        files_to_download = set()
        if download_all_genomes:
            files_to_download.update(all_genomes)
        if download_all_genes:
            files_to_download.update(all_genes)


        for study, files in study_2_files.items():
            if study in items_to_download:
                files_to_download.update(files)
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
            print('Downloading genes/genomes...')
            for cnt, (source, study, fname) in enumerate(files_to_download, 1):
                progress_bar(cnt, len(files_to_download))
                url = 'https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/genomes/genomes/' + source.split('./', 1)[-1]
                dest_folder = f'{args.output}/{study}/'
                pathlib.Path(dest_folder).mkdir(exist_ok=True, parents=True)
                dest = f'{args.output}/{study}/{fname}'
                download_file(url, dest, False)
            print('\nFinished downloading genes/genomes ...')









if __name__ == "__main__":
    main()