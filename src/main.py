import os
import shutil
import subprocess

from copystatic import copy_files_recursive
from generate_page import generate_page


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_public, "index.html"),
    )

    print("Starting server on port 8888...")
    subprocess.run(["python3", "-m", "http.server", "8888"], cwd=dir_path_public)


if __name__ == "__main__":
    main()
