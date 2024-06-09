from package_analysis import clone_repo_and_get_package_json, analyze_package_json
from learning_path import create_learning_path, update_progress
from documentation import generate_documentation
import json

def main():
    repo_url = input("Enter the GitHub repository URL: ")

    try:
        package_json = clone_repo_and_get_package_json(repo_url)
        analysis = analyze_package_json(package_json)
        
        dependencies = analysis.get('dependencies', {})
        dev_dependencies = analysis.get('devDependencies', {})
        scripts = analysis.get('scripts', {})

        # Print dependencies, devDependencies, and scripts
        print("Dependencies:", json.dumps(dependencies, indent=4))
        print("DevDependencies:", json.dumps(dev_dependencies, indent=4))
        print("Scripts:", json.dumps(scripts, indent=4))

        # Generate documentation
        generate_documentation(repo_url, dependencies, dev_dependencies, scripts)

        # Create learning path
        learning_path = create_learning_path(dependencies, dev_dependencies)
        print(json.dumps(learning_path, indent=4))

        with open('requirements.txt', 'w') as f:
            f.write("requests==2.28.2\n")
            f.write("gitpython==3.1.31\n")
            f.write("nodeenv==1.6.0\n")
            f.write("openai==0.12.0\n")

        update_progress(learning_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
