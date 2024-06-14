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

def analyze_github_repo(repo_url):
    # Extract owner and repo name from URL
    owner, repo = repo_url.split('/')[-2:]

    # Construct the URL for the GitHub API
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
            'Authorization': f'token '
        }
    # Make the GET request
    response = requests.get(url)

    # Extract the required information
    data = response.json()
    repo_name = data.get('name')
    language = data.get('language')
    default_branch = data.get('default_branch')
    total_commits = data.get('size')
    total_prs = data.get('open_issues_count')  # This includes issues as well
    total_branches = len(requests.get(f"{url}/branches",headers=headers).json())
    total_contributors = len(requests.get(f"{url}/contributors",headers=headers).json())
    
    # Get the list of contributors
    contributors_response = requests.get(f"{url}/contributors",headers=headers)
    if contributors_response.status_code == 200:
        contributors = []
        for user in contributors_response.json():
            contributors.append({
                "name": user['login'],
                "contribution":user['contributions'],
            })

    else:
        contributors = []


    last_update = data.get('updated_at')

    # Get the list of vulnerabilities
    vulnerabilities = requests.get(f"{url}/security/advisories").json()

    # Get the security issues
    security_issues = requests.get(f"{url}/issues?labels=security").json()

    # Save to file
    # with open('output.md', 'w') as f:
    #     f.write(f"# {repo} Analysis\n")
    #     f.write(f"- Language: {language}\n")
    #     f.write(f"- Default Branch: {default_branch}\n")
    #     f.write(f"- Total Commits: {total_commits}\n")
    #     f.write(f"- Total PRs: {total_prs}\n")
    #     f.write(f"- Total Branches: {total_branches}\n")
    #     f.write(f"- Total Contributors: {total_contributors}\n")
    #     f.write(f"- Last Update: {last_update}\n")
    #     f.write(f"- Vulnerabilities: {vulnerabilities}\n")
    #     f.write(f"- Security Issues: {security_issues}\n")

    # Return the information
    return {
        'repo_name': repo_name,
        'language': language,
        'default_branch': default_branch,
        'total_commits': total_commits,
        'total_prs': total_prs,
        'total_branches': total_branches,
        'total_contributors': total_contributors,
        'last_update': last_update,
        'vulnerabilities': vulnerabilities,
        'security_issues': security_issues,
        'contributors': contributors
    } 