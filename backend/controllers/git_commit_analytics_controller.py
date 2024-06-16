import os
import subprocess
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from controllers.helpers.main import get_repo_path
app = Flask(__name__)
import json

repo_path = ''
INVALID_DAYS_ERROR = "Invalid 'days' parameter. It must be an integer."
REPO_NOT_EXIST_ERROR = "Repository not cloned or does not exist!"


def __does_repo_exist(repo_url):
    global repo_path
    repo_path= get_repo_path(repo_url)
    print(repo_path)
    return os.path.exists(repo_path)


def get_commit_history(repo_url):

    if not __does_repo_exist(repo_url):
        return jsonify({"error": REPO_NOT_EXIST_ERROR}), 404

    # Get the 'days' query parameter
    days = request.json["days"]

    git_command = ["git", "log", "--pretty=format:'{\"commit_id\":\"%H\",\"username\":\"%an\",\"date_time\":\"%ai\",\"commit_message\":\"%s\"}'"]

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
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    git_command.extend(["--since", since_date])

    try:
        result = subprocess.run(
            git_command, cwd=repo_path, text=True, capture_output=True, check=True
        )

        commits = result.stdout.split("\n")
        # Remove the outer single quotes and parse each string as JSON
        # Remove the outer single quotes and parse each string as JSON
        commits_json = []
        for commit in commits:
            if commit:
                commit_json = json.loads(commit.strip("'"))
                commit_date = datetime.strptime(commit_json["date_time"], "%Y-%m-%d %H:%M:%S %z")
                diff_days = (datetime.now(commit_date.tzinfo) - commit_date).days
                commit_json["diff_days"] = diff_days
                commits_json.append(commit_json)
                
        return jsonify(commits_json), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"Error occurred while fetching commit history! ": str(e)}), 500


def get_highest_contributor():

    if not __does_repo_exist():
        return jsonify({"error": REPO_NOT_EXIST_ERROR}), 404

    # Get the 'days' query parameter
    days = request.json["days"]

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


def get_total_lines_updated():

    if not __does_repo_exist():
        return jsonify({"error": REPO_NOT_EXIST_ERROR}), 404

    # Get the 'days' query parameter
    days = request.json["days"]

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
        "--pretty=format:%an",
        "--numstat",
    ]

    try:
        result = subprocess.run(
            git_command, cwd=repo_path, text=True, capture_output=True, check=True
        )

        lines = result.stdout.strip().split("\n")
        user_changes = __parse_lines(lines)

        sorted_changes = sorted(
            user_changes.items(),
            key=lambda x: (x[1]["added"] + x[1]["removed"]),
            reverse=True,
        )

        return jsonify(sorted_changes), 200

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


def __parse_lines(lines):
    user_changes = {}
    current_user = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not line[0].isdigit():  # Assume user names don't start with a digit
            current_user = line
            if current_user not in user_changes:
                user_changes[current_user] = {"added": 0, "removed": 0}
        else:
            try:
                add, rm, _ = line.split()
                user_changes[current_user]["added"] += int(add)
                user_changes[current_user]["removed"] += int(rm)
            except ValueError:
                continue

    return user_changes
