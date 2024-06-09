import os
import json
from git import Repo
from pathlib import Path
import requests
import base64

def download_package_json(repo_url):
    owner_repo = repo_url.rstrip('/').split('/')[-2:]
    owner = owner_repo[0]
    repo = owner_repo[1]
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/package.json'
    response = requests.get(api_url)
    if response.status_code == 200:
        content = response.json()['content']
        return json.loads(base64.b64decode(content))
    else:
        raise Exception(f"Failed to fetch package.json: {response.status_code}")

def clone_repo_and_get_package_json(repo_url, clone_dir='temp_repo'):
    if os.path.exists(clone_dir):
        import shutil
        shutil.rmtree(clone_dir)
    Repo.clone_from(repo_url, clone_dir)
    package_json_path = Path(clone_dir) / 'package.json'
    if package_json_path.exists():
        with open(package_json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        raise FileNotFoundError("package.json not found in the repository")

def analyze_package_json(package_json):
    analysis = {
        'name': package_json.get('name'),
        'version': package_json.get('version'),
        'description': package_json.get('description'),
        'main': package_json.get('main'),
        'scripts': package_json.get('scripts'),
        'dependencies': package_json.get('dependencies'),
        'devDependencies': package_json.get('devDependencies'),
        'peerDependencies': package_json.get('peerDependencies'),
        'optionalDependencies': package_json.get('optionalDependencies'),
        'engines': package_json.get('engines'),
        'license': package_json.get('license')
    }
    return analysis
