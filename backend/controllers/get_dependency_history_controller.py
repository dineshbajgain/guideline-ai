from pathlib import Path
from urllib.parse import urlparse
import json
from flask import jsonify
import os
from dotenv import load_dotenv
import requests
import subprocess
from controllers.helpers.main import get_repo_path

def get_dependency_history_controller(repo_url, package_name):
    repo_path = get_repo_path(repo_url)
    with open(repo_path / "package-lock.json", "r") as file:
        lock_data = json.load(file)

    # Get the details of the given package from package-lock.json
    package_info = lock_data.get("dependencies", {}).get(package_name)
    if not package_info:
        return {"error": "Package not found"}, 404

    # Use git log to find out who added this package and when
    git_command = ["git", "log", "-S", f'"{package_name}":', "--pretty=format:'{\"commit_id\":\"%H\",\"username\":\"%an\",\"date_time\":\"%ai\",\"commit_message\":\"%s\"}'", "package.json"]
    result = subprocess.run(git_command, cwd=repo_path, text=True, capture_output=True, check=True)
    commits = result.stdout.split("\n")
    commits_json = [json.loads(commit.strip("'")) for commit in commits if commit]
    package_info["added_by"] = commits_json[0] if commits_json else None

    # Use the npm API to get the package data
    response = requests.get(f"https://registry.npmjs.org/{package_name}")
    pkg_data = response.json()
    package_info["npm_url"] = f"https://www.npmjs.com/package/{package_name}"
    package_info["github_url"] = pkg_data.get("repository", {}).get("url")
    package_info["readme"] = pkg_data.get("readme")

    return package_info