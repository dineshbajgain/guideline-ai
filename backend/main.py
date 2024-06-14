from flask import Flask, request, jsonify
from flask_cors import CORS
from package_analysis import (
    clone_repo_and_get_package_json,
    analyze_package_json,
    analyze_github_repo,
)
from learning_path import create_learning_path, update_progress
from documentation import generate_documentation
from gen_ai import generate_learning_resources
from analytics import git_commit_analytics

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route("/test", methods=["POST"])
def test():
    data = request.json
    if not data or "repo_url" not in data:
        return jsonify({"error": "Missing repo_url"}), 400
    return jsonify({"message": "Success", "repo_url": data["repo_url"]})


@app.route("/getRepoAnalysis", methods=["POST"])
def getRepoAnalysis():
    repo_url = request.json["repo_url"]
    custom_day = request.json["custom_day"]
    try:
        repoAnalysis = analyze_github_repo(repo_url, custom_day)
        return jsonify(repoAnalysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/getDependencies", methods=["POST"])
def getDependencies():
    repo_url = request.json["repo_url"]

    try:
        package_json = clone_repo_and_get_package_json(repo_url)
        analysis = analyze_package_json(package_json)
        dependencies = analysis.get("dependencies", {})
        dev_dependencies = analysis.get("devDependencies", {})
        scripts = analysis.get("scripts", {})
        # Extract the required information language, default_branch, total_commits, total_prs, total_branches, total_contributors,
        # last_update, vulnerabilities, security_issues
        return jsonify(
            {
                "dependencies": dependencies,
                "devDependencies": dev_dependencies,
                "scripts": scripts,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze", methods=["POST"])
def analyze():
    repo_url = request.json["repo_url"]

    try:
        package_json = clone_repo_and_get_package_json(repo_url)
        analysis = analyze_package_json(package_json)
        repoAnalysis = analyze_github_repo(repo_url)

        dependencies = analysis.get("dependencies", {})
        dev_dependencies = analysis.get("devDependencies", {})
        scripts = analysis.get("scripts", {})

        # Generate documentation
        generate_documentation(repo_url, dependencies, dev_dependencies, scripts)

        # Create learning path
        learning_path = create_learning_path(dependencies, dev_dependencies)

        return jsonify(
            {
                "dependencies": dependencies,
                "devDependencies": dev_dependencies,
                "scripts": scripts,
                "learning_path": learning_path,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_progress", methods=["PUT"])
def update():
    learning_path = request.json["learning_path"]
    updated_learning_path = update_progress(learning_path)
    return jsonify(updated_learning_path)


@app.route("/createLearningPath", methods=["POST"])
def createLearningPath():
    # Get the dependencies and devDependencies from the github repo and create a learning path
    repo_url = request.json["repo_url"]
    try:
        package_json = clone_repo_and_get_package_json(repo_url)
        analysis = analyze_package_json(package_json)
        dependencies = analysis.get("dependencies", {})
        dev_dependencies = analysis.get("devDependencies", {})
        learning_path = create_learning_path(dependencies, dev_dependencies)
        return jsonify(learning_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generateText", methods=["POST"])
def generateText():
    dependency = request.json["dependency"]
    resources = generate_learning_resources(dependency)
    return jsonify({"resources": resources})


@app.route("/commit-history", methods=["POST"])
def get_commit_history():
    return git_commit_analytics.get_commit_history()


@app.route("/highest-contributor", methods=["POST"])
def get_highest_contributor():
    return git_commit_analytics.get_highest_contributor()


@app.route("/lines-changed", methods=["POST"])
def get_total_lines_updated():
    return git_commit_analytics.get_total_lines_updated()


if __name__ == "__main__":
    app.run(debug=True)
