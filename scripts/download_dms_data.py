"""Download DMS datasets for MutBench ground truth generation."""
import os
import urllib.request
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'mutbench')

DMS_URL = (
    'https://raw.githubusercontent.com/jbloomlab/SARS2-mut-fitness/'
    'main/results/aa_fitness/aamut_fitness_all.csv'
)

# Known SARS-CoV-2 functional sites (amino acid positions in Spike)
KNOWN_FUNCTIONAL_SITES = {
    'RBD': list(range(319, 542)),          # Receptor Binding Domain
    'furin_cleavage': list(range(681, 686)),  # Furin cleavage site
    'fusion_peptide': list(range(816, 834)),  # Fusion peptide
    'NTD_supersite': list(range(14, 21)) + list(range(140, 159)) +
                     list(range(245, 265)),  # NTD antigenic supersite
}


def download_file(url: str, dest: str):
    if os.path.exists(dest):
        print(f"Already exists: {dest}")
        return
    print(f"Downloading {url} -> {dest}")
    urllib.request.urlretrieve(url, dest)
    print(f"Downloaded: {dest}")


def save_known_sites(dest: str):
    with open(dest, 'w') as f:
        json.dump(KNOWN_FUNCTIONAL_SITES, f, indent=2)
    print(f"Saved known functional sites: {dest}")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    download_file(DMS_URL, os.path.join(DATA_DIR, 'aamut_fitness_all.csv'))
    save_known_sites(os.path.join(DATA_DIR, 'known_functional_sites.json'))
    print("Done.")


if __name__ == '__main__':
    main()
