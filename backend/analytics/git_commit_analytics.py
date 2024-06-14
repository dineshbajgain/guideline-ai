import os
import subprocess
from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)
repo_path = repo_path = os.path.join(os.path.dirname(__file__), "../temp")
INVALID_DAYS_ERROR = "Invalid 'days' parameter. It must be an integer."


@app.route("/commit-history", methods=["GET"])
def get_commit_history():

    # Get the 'days' query parameter
    days = request.args.get("days")

    git_command = ["git", "log", "--pretty=format:%h - %an, %ar : %s"]

    # Calculate the date for the --since parameter
    if days:
        try:
            days = int(days)
            since_date = (datetime.now() - datetime.timedelta(days=days)).strftime(
                "%Y-%m-%d"
            )
            git_command.extend(["--since", since_date])

        except ValueError:
            return (
                jsonify({"error": INVALID_DAYS_ERROR}),
                400,
            )
    else:
        return (
            jsonify({"error": "Missing 'days' parameter. It must be an integer."}),
            422,
        )

    try:
        result = subprocess.run(
            git_command, cwd=repo_path, text=True, capture_output=True, check=True
        )

        commits = result.stdout.split("\n")

        return jsonify(commits), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"Error occurred while fetching commit history! ": str(e)}), 500


@app.route("/highest-contributor", methods=["GET"])
def get_highest_contributor():

    # Get the 'days' query parameter
    days = request.args.get("days")

    # Calculate the date for one month ago or the --since parameter
    try:
        if days:
            days = int(days)
            duration = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        else:
            duration = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    except ValueError:
        return (
            jsonify({"error": INVALID_DAYS_ERROR}),
            400,
        )

    git_command = ["git", "shortlog", "-sn", "--since", duration]

    try:
        result = subprocess.run(
            git_command, cwd=repo_path, text=True, capture_output=True, check=True
        )

        # Parse the output to find the highest contributor
        lines = result.stdout.strip().split("\n")
        if not lines:
            return jsonify({"error": "No commits found in the last month."}), 404

        top_contributor = lines[0].strip()
        count, name = top_contributor.split("\t")

        return jsonify({"name": name, "commits": int(count)}), 200

    except subprocess.CalledProcessError as e:
        return (
            jsonify({"Error occurred while fetching highest contributor! ": str(e)}),
            500,
        )


@app.route("/lines-changed", methods=["GET"])
def get_total_lines_updated():

    # Get the 'days' query parameter
    days = request.args.get("days")

    # Calculate the date for the --since parameter
    if days:
        try:
            days = int(days)
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        except ValueError:
            return (
                jsonify({"error": INVALID_DAYS_ERROR}),
                400,
            )
    else:
        since_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    git_command = [
        "git",
        "log",
        "--since",
        since_date,
        "--pretty=tformat:",
        "--numstat",
    ]

    try:
        result = subprocess.run(
            git_command, cwd=repo_path, text=True, capture_output=True, check=True
        )

        # Parse the output to find the total lines updated
        lines = result.stdout.strip().split(",")
        if not lines:
            return (
                jsonify({"error": "No lines of code changed in the last month."}),
                404,
            )

        total_lines_updated = lines[1].strip().split(" ")[0]

        return jsonify({"total_lines_updated": int(total_lines_updated)}), 200

    except subprocess.CalledProcessError as e:
        return (
            jsonify(
                {
                    "Error occurred while fetching total lines of code changed by users! ": str(
                        e
                    )
                }
            ),
            500,
        )
