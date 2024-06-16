from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.package_analysis_controller import (
    analyze_github_repo,
)
from controllers.test_controller import test_controller
from controllers.clone_repo_controller import clone_repo_controller
from controllers.get_dependency_controller import get_dependency_controller
from controllers.get_dependency_history_controller import get_dependency_history_controller
from controllers.git_commit_analytics_controller import (
    get_commit_history,
    get_highest_contributor,
    get_total_lines_updated,
)

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route("/test", methods=["POST"])
def test():
    return test_controller()

@app.route("/colne_repo", methods=["POST"])
def colne_repo():
   repo_url = request.json["repo_url"]
   clone_repo_controller(repo_url)
   return jsonify({"message": "Success"})

@app.route("/get_dependencies", methods=["POST"])
def get_dependencies():
   repo_url = request.json["repo_url"]
   return get_dependency_controller(repo_url)

@app.route("/get_dependencies/history", methods=["POST"])
def get_dependencies_hoistory():
   repo_url = request.json["repo_url"]
   package_name = request.json["package_name"]
   return get_dependency_history_controller(repo_url,package_name)

@app.route("/commit_history", methods=["POST"])
def commit_history():
    repo_url = request.json["repo_url"]
    return get_commit_history(repo_url)

@app.route("/highest_contributor", methods=["POST"])
def get_highest_contributor():
    return get_highest_contributor()

@app.route("/lines_changed", methods=["POST"])
def get_total_lines_updated():
    return get_total_lines_updated()

@app.route("/get_repo_details", methods=["POST"])
def get_repo_details():
    repo_url = request.json["repo_url"]
    custom_day = request.json["custom_day"]
    try:
        repoAnalysis = analyze_github_repo(repo_url, custom_day)
        return jsonify(repoAnalysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
