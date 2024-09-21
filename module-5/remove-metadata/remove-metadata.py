from exiftool import ExifToolHelper
import pikepdf

file = "pricelist.pdf"

with ExifToolHelper() as et:
    for d in et.get_metadata({file}):
        for k, v in d.items():
            print(f"{k} = {v}")
