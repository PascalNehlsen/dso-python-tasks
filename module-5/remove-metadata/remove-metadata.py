import subprocess
import pikepdf
from exiftool import ExifToolHelper

def clean_pdf_metadata(file: str) -> None:
    """
    Cleans metadata from a PDF file and linearizes it for fast web viewing.

    Args:
        file (str): The path to the original PDF file to be cleaned.

    Returns:
        None
    """
    # Paths for temporary files
    tmp_file = "tmp_file.pdf"    # Temporary file after cleaning metadata
    clean_file = "clean_file.pdf"  # File after linearization

    # Step 1: Use ExifToolHelper to get and display old metadata
    with ExifToolHelper() as et_helper:
        old_metadata = et_helper.get_metadata(file)
        print("Old Metadata:")
        for d in old_metadata:
            for k, v in d.items():
                print(f"{k} -> {v}")

    # Step 2: Use ExifTool to clean metadata and create tmp_file
    result = subprocess.run(["exiftool", "-all=", "-o", tmp_file, file], capture_output=True, text=True)

    # Display ExifTool output, including any warnings
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("Warning:", result.stderr)

    # Step 3: Use pikepdf to linearize the cleaned PDF and create clean_file
    with pikepdf.open(tmp_file) as pdf:
        pdf.save(clean_file, linearize=True)

    # Step 4: Use ExifToolHelper to get and display cleaned metadata
    with ExifToolHelper() as et_helper:
        cleaned_metadata = et_helper.get_metadata(clean_file)
        print("\nCleaned Metadata:")
        for d in cleaned_metadata:
            for k, v in d.items():
                print(f"{k} -> {v}")

    # Step 5: Remove the tmp_file and move clean_file to replace the original file
    subprocess.run(["rm", tmp_file], shell=True)
    subprocess.run(["mv", clean_file, file], shell=True)

    print(f"\nMetadata cleaned, file linearized, and saved as {file}")

if __name__ == "__main__":
    # Replace 'pricelist.pdf' with your actual PDF file path
    clean_pdf_metadata("pricelist.pdf")
