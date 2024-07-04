# Take an input directlry and writes it to an output zip file

import os
import zipfile
# https://docs.python.org/3/library/zipfile.html

# This example can be used or the path specifically ( as provided )
# zip_dir_name = "./Python/Infrasctructure/Zip file from a directory/ZipTarget"
# output_filename = "./Python/Infrasctructure/Zip file from a directory/compressed_file.zip"

# Or you can create your own test directory
# Have the zip file written to your selected path
# For example the samples below 
zip_dir_name = "f:/test/"
output_filename = "f:/compressed_file.zip"

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(zip_dir_name, zipf)