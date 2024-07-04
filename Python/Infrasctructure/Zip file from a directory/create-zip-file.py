import os
import zipfile

zip_dir_name = "./Python/Infrasctructure/Zip file from a directory/ZipTarget"
# zip_dir_name = "f:/test/"
output_filename = "./Python/Infrasctructure/Zip file from a directory/compressed_file.zip"
# output_filename = "f:/compressed_file.zip"

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(zip_dir_name, zipf)