from urllib.parse import urlparse
from pathlib import Path
def get_repo_path(repo_url):
    clone_dir = "temp_repo"
    url_path = urlparse(repo_url).path
    repo_name = url_path.split("/")[-1]
    clone_dir = Path(clone_dir) / repo_name
    return clone_dir

def create_learning_path(dependencies, dev_dependencies):
    learning_path = []

    # Generate learning resources using Gen AI
    for dependency in dependencies:
        learning_path.append({
            'dependency': dependency,
            'progress': 0  # Track progress for each dependency
        })

    for dev_dependency in dev_dependencies:
        learning_path.append({
            'dependency': dev_dependency,
            'progress': 0  # Track progress for each devDependency
        })

    return learning_path
