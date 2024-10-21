import os
import csv
import argparse
from PyPDF2 import PdfReader
from typing import List, Dict

def clean_text(text: str) -> str:
    """
    Cleans up the input text by removing line breaks and trimming white spaces.
    If the text is None, it returns 'N/A'.
    
    Args:
        text (str): The input text to be cleaned.
    
    Returns:
        str: The cleaned text or 'N/A' if the input was None.
    """
    if not text:
        return 'N/A'
    return text.replace('\n', ' ').replace('\r', '').strip()

def extract_metadata(pdf_path: str) -> Dict[str, str]:
    """
    Extracts metadata from a given PDF file.
    
    Args:
        pdf_path (str): The path to the PDF file.
    
    Returns:
        Dict[str, str]: A dictionary containing the extracted metadata.
    """
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        meta = pdf.metadata
        
        # Extract PDF version from the document root (if available)
        pdf_version = pdf.trailer['/Root']['/Version'] if '/Version' in pdf.trailer['/Root'] else 'Unknown'

        metadata = {
            'Title': clean_text(meta.get('/Title', 'N/A')),
            'Author': clean_text(meta.get('/Author', 'N/A')),
            'Creator': clean_text(meta.get('/Creator', 'N/A')),
            'Created': clean_text(meta.get('/CreationDate', 'N/A')),
            'Modified': clean_text(meta.get('/ModDate', 'N/A')),
            'Subject': clean_text(meta.get('/Subject', 'N/A')),
            'Keywords': clean_text(meta.get('/Keywords', 'N/A')),
            'Description': clean_text(meta.get('/Description', 'N/A')),
            'Producer': clean_text(meta.get('/Producer', 'N/A')),
            'PDF Version': clean_text(pdf_version)
        }
        
        return metadata

def write_to_csv(metadata_list: List[Dict[str, str]], output_file: str) -> None:
    """
    Writes metadata to a CSV file.
    
    Args:
        metadata_list (List[Dict[str, str]]): A list of dictionaries containing metadata for each PDF.
        output_file (str): The name of the CSV file to be created.
    """
    fieldnames = [
        'Title', 
        'Author', 
        'Creator', 
        'Created', 
        'Modified', 
        'Subject', 
        'Keywords', 
        'Description', 
        'Producer', 
        'PDF Version']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for metadata in metadata_list:
            writer.writerow(metadata)

def process_single_file(file_path: str, output_file: str) -> None:
    """
    Processes a single PDF file and extracts its metadata.
    
    Args:
        file_path (str): The path to the PDF file.
        output_file (str): The name of the output CSV file.
    """
    metadata = extract_metadata(file_path)
    write_to_csv([metadata], output_file)
    print(f"Metadata from {file_path} has been written to {output_file}.")

def process_directory(directory_path: str, output_file: str) -> None:
    """
    Processes all PDF files in a directory and extracts their metadata.
    
    Args:
        directory_path (str): The path to the directory containing PDF files.
        output_file (str): The name of the output CSV file.
    """
    metadata_list = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            metadata = extract_metadata(file_path)
            metadata_list.append(metadata)
    
    write_to_csv(metadata_list, output_file)
    print(f"Metadata from files in {directory_path} has been written to {output_file}.")

def main() -> None:
    """
    Main function to parse command-line arguments and call the appropriate functions.
    It either processes a single PDF file or a directory containing multiple PDFs.
    """
    parser = argparse.ArgumentParser(description='Extract metadata from PDF files and save to a CSV file.')
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        '-f', 
        '--file', 
        type=str, 
        help='Path to a single PDF file')
    
    group.add_argument(
        '-d', 
        '--directory', 
        type=str, 
        help='Path to a directory containing multiple PDF files')
    
    parser.add_argument(
        '-n', 
        '--name', 
        type=str, 
        required=True, 
        help='Output CSV file name')

    args = parser.parse_args()

    if args.file:
        process_single_file(args.file, args.name)
    elif args.directory:
        process_directory(args.directory, args.name)

if __name__ == "__main__":
    main()
