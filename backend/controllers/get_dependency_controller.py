from pathlib import Path
from urllib.parse import urlparse
import json
from flask import jsonify
import os
from dotenv import load_dotenv
from controllers.helpers.main import create_learning_path

load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
def get_dependency_controller(repo_url, clone_dir="temp_repo"):
    url_path = urlparse(repo_url).path
    repo_name = url_path.split("/")[-1]
    clone_dir = Path(clone_dir) / repo_name
    package_json_path = Path(clone_dir) / "package.json"
    # Read the package.json file
    with open(package_json_path, "r") as file:
        data = json.load(file)
    # Get the dependencies and devDependencies
    analysis = analyze_package_json(data)
    dependencies = analysis.get("dependencies", {})
    dev_dependencies = analysis.get("devDependencies", {})
    dependency_with_progress =  create_learning_path(dependencies, dev_dependencies)
    return dependency_with_progress

def analyze_package_json(package_json):
    analysis = {
        "name": package_json.get("name"),
        "version": package_json.get("version"),
        "description": package_json.get("description"),
        "main": package_json.get("main"),
        "scripts": package_json.get("scripts"),
        "dependencies": package_json.get("dependencies"),
        "devDependencies": package_json.get("devDependencies"),
        "peerDependencies": package_json.get("peerDependencies"),
        "optionalDependencies": package_json.get("optionalDependencies"),
        "engines": package_json.get("engines"),
        "license": package_json.get("license"),
    }
    return analysis
    
