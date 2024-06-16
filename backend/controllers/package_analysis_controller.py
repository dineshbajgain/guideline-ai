import os
import json
from git import Repo
from pathlib import Path
import requests
import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv
import subprocess
from controllers.helpers.main import get_repo_path

load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')

def download_package_json(repo_url):
    owner_repo = repo_url.rstrip("/").split("/")[-2:]
    owner = owner_repo[0]
    repo = owner_repo[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/package.json"
    response = requests.get(api_url)
    if response.status_code == 200:
        content = response.json()["content"]
        return json.loads(base64.b64decode(content))
    else:
        raise FileNotFoundError(f"Failed to fetch package.json: {response.status_code}")


def clone_repo_and_get_package_json(repo_url, clone_dir="temp_repo"):
    if os.path.exists(clone_dir):
        import shutil

        shutil.rmtree(clone_dir)
    Repo.clone_from(repo_url, clone_dir)
    package_json_path = Path(clone_dir) / "package.json"
    if package_json_path.exists():
        with open(package_json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        raise FileNotFoundError("package.json not found in the repository")


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


def analyze_github_repo(repo_url, custom_day):
    # Get the repository name and default branch
    repo_path = get_repo_path(repo_url)
    repo_name = os.path.basename(repo_path)
    default_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path).decode().strip()

    # Get the total commits
    total_commits = int(subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=repo_path).decode().strip())

    # Get the total branches
    total_branches = len(subprocess.check_output(["git", "branch", "-r"], cwd=repo_path).decode().strip().split("\n"))

    # Get the total contributors
    total_contributors = len(subprocess.check_output(["git", "shortlog", "-sn", "HEAD"], cwd=repo_path).decode().strip().split("\n"))

    # Get the last update
    last_update = subprocess.check_output(["git", "log", "-1", "--format=%cd"], cwd=repo_path).decode().strip()

    # Get the contributors and their contributions
    contributors_output = subprocess.check_output(["git", "shortlog", "-sn", "HEAD"], cwd=repo_path).decode().strip().split("\n")
    contributors = [{"name": line.split("\t")[1], "contribution": int(line.split("\t")[0])} for line in contributors_output]

    # Identify the top contributor
    top_contributor = contributors[0]["name"] if contributors else None
    top_contributor_changes = contributors[0]["contribution"] if contributors else 0

    # Get the code owners
    code_owners = []
    try:
        with open(os.path.join(repo_path, ".github", "CODEOWNERS"), "r") as file:
            for line in file:
                if line.startswith("*"):
                    code_owners.extend([owner.strip() for owner in line[1:].split("@")[1:]])
    except FileNotFoundError:
        pass

    # Identify the top 3 contributors
    top_contributors = [contributor["name"] for contributor in contributors[:3]]

    # Combine code owners and top contributors to form the reviewers
    reviewers = list(set(code_owners + top_contributors))

    # Return the information
    return {
        "repo_name": repo_name,
        "default_branch": default_branch,
        "total_commits": total_commits,
        "total_branches": total_branches,
        "total_contributors": total_contributors,
        "last_update": last_update,
        "contributors": contributors,
        "top_contributor": top_contributor,
        "top_contributor_changes": top_contributor_changes,
        "reviewers": reviewers
    }
