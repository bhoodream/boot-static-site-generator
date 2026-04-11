import os
import shutil
import subprocess
import sys

from copystatic import copy_files_recursive
from generate_pages_recursive import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    basepath = "/"
    dest_dir = "./public"
    
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if len(sys.argv) > 2:
        dest_dir = sys.argv[2]

    print(f"Deleting {dest_dir} directory...")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    print(f"Copying static files to {dest_dir} directory...")
    copy_files_recursive(dir_path_static, dest_dir)

    print(f"Generating pages with basepath: {basepath} to {dest_dir}...")
    generate_pages_recursive(dir_path_content, template_path, dest_dir, basepath)

    print("Starting server on port 8888...")
    subprocess.run(["python3", "-m", "http.server", "8888"], cwd=dest_dir)


if __name__ == "__main__":
    main()
