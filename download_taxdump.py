import requests
import tarfile

def download_taxdump(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise HTTPError for bad responses

    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def extract_taxdump(tar_gz_path, extract_to):
    with tarfile.open(tar_gz_path, "r:gz") as tar:
        tar.extractall(path=extract_to)

if __name__ == "__main__":
    url = "https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"
    output_path = "taxdump.tar.gz"
    extract_to = "./taxdump"

    download_taxdump(url, output_path)
    print(f"Downloaded taxdump.tar.gz to {output_path}")

    extract_taxdump(output_path, extract_to)
    print(f"Extracted taxdump.tar.gz to {extract_to}")
