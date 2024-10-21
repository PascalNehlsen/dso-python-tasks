import os
import requests
import csv
import argparse
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from urllib.parse import urljoin

def download_pdfs_from_url(url: str, download_dir: str) -> list:
    """
    Downloads all PDFs from the given URL and saves them in the specified directory.
    Returns a list of file paths to the downloaded PDFs.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_urls = []

    # Find all PDF links in the webpage
    for link in soup.find_all('a', href=True):
        if link['href'].lower().endswith('.pdf'):
            pdf_url = urljoin(url, link['href'])
            pdf_urls.append(pdf_url)
    
    # Download all PDFs
    downloaded_files = []
    for pdf_url in pdf_urls:
        try:
            pdf_response = requests.get(pdf_url)
            pdf_name = pdf_url.split('/')[-1]
            file_path = os.path.join(download_dir, pdf_name)
            with open(file_path, 'wb') as f:
                f.write(pdf_response.content)
            downloaded_files.append(file_path)
            print(f"Downloaded: {pdf_name}")
        except Exception as e:
            print(f"Failed to download {pdf_url}: {e}")
    
    return downloaded_files

def extract_metadata(file_path: str) -> dict:
    """
    Extracts metadata from a single PDF file and returns it as a dictionary.
    Includes enhanced error handling for corrupt PDFs.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            if reader.is_encrypted:
                print(f"Skipping encrypted PDF: {file_path}")
                return {}

            meta = reader.metadata
            return {
                'Title': meta.title if meta and meta.title else 'N/A',
                'Author': meta.author if meta and meta.author else 'N/A',
                'Creator': meta.creator if meta and meta.creator else 'N/A',
                'Created': meta.creation_date if meta and meta.creation_date else 'N/A',
                'Modified': meta.modification_date if meta and meta.modification_date else 'N/A',
                'Subject': meta.subject if meta and meta.subject else 'N/A',
                'Keywords': meta.keywords if meta and meta.keywords else 'N/A',
                'Description': meta.get('/Description', 'N/A') if meta else 'N/A',
                'Producer': meta.producer if meta and meta.producer else 'N/A',
                'PDF Version': reader.pdf_version}
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return {}

def save_metadata_to_csv(
        metadata_list: list, 
        output_csv: str):
    """
    Saves a list of metadata dictionaries to a CSV file.
    """
    headers = ['Title', 'Author', 'Creator', 'Created', 'Modified', 'Subject', 'Keywords', 'Description', 'Producer', 'PDF Version']
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
        writer.writeheader()
        for metadata in metadata_list:
            writer.writerow(metadata)
    print(f"Metadata saved to {output_csv}")

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Download PDFs from a webpage and extract metadata")
    parser.add_argument('-u',
                        '--url', 
                        required=True, 
                        help="The URL of the webpage to scan for PDFs")
    parser.add_argument('-n',
                        '--name', 
                        required=True, 
                        help="The name and path of the output CSV file")
    args = parser.parse_args()

    # Create download directory
    download_dir = 'pdf_downloads'
    os.makedirs(download_dir, exist_ok=True)

    # Step 1: Download all PDFs from the specified URL
    print(f"Scanning webpage: {args.url}")
    pdf_files = download_pdfs_from_url(args.url, download_dir)

    # Step 2: Extract metadata from each downloaded PDF
    all_metadata = []
    for pdf_file in pdf_files:
        print(f"Extracting metadata from: {pdf_file}")
        metadata = extract_metadata(pdf_file)
        if metadata:
            all_metadata.append(metadata)

    # Step 3: Save the metadata to the CSV file
    save_metadata_to_csv(all_metadata, args.name)

if __name__ == "__main__":
    main()
