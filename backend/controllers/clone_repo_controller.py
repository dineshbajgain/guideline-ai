import os
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
def clone_repo_controller(repo_url, clone_dir="temp_repo"):
    url_path = urlparse(repo_url).path
    repo_name = url_path.split("/")[-1]
    clone_dir = Path(clone_dir) / repo_name
    if os.path.exists(clone_dir):
        import shutil
        shutil.rmtree(clone_dir)

    # Include the token in the repo_url
    repo_url_with_token = repo_url.replace("https://", f"https://{github_token}@")

    # Use subprocess to run the git command with the token in the URL
    subprocess.run(['git', 'clone', repo_url_with_token, clone_dir], check=True)

    package_json_path = Path(clone_dir) / "package.json"
    if package_json_path.exists():
        with open(package_json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        raise FileNotFoundError("package.json not found in the repository")