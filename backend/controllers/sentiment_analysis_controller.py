from flask import Flask, request, jsonify
from transformers import pipeline
import requests
import subprocess
from controllers.helpers.main import get_repo_path
import git

app = Flask(__name__)

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline('sentiment-analysis')

def get_commits_by_username(username, repo_path):
    try:
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits())  # Get commits from all branches
        commit_data = []

        for commit in commits:
            if commit.author.name == username:
                diff = commit.stats.total
                commit_data.append({
                    'message': commit.message,
                    'date': commit.committed_datetime,
                    'author': commit.author.name,
                    'lines_added': diff['insertions'],
                    'lines_deleted': diff['deletions'],
                    'files_changed': diff['files']
                })
        return commit_data
    except Exception as e:
        print(f"Error fetching commits: {e}")
        return []

def analyze_commit_frequency(commits):
    commit_dates = [commit['date'] for commit in commits]
    commit_count = len(commit_dates)
    if commit_count > 20:
        return "High"
    elif commit_count > 10:
        return "Medium"
    else:
        return "Low"


def analyze_commit_sentiment(commits):
    sentiments = []
    total_lines_added = 0
    total_lines_deleted = 0
    total_files_changed = 0
    
    for commit in commits:
        commit_message = commit['message']
        if commit_message:  # Ensure the commit message is not empty
            sentiment = sentiment_pipeline(commit_message)[0]['label']
            sentiments.append(sentiment)
        
        # Aggregate line change metrics
        total_lines_added += commit['lines_added']
        total_lines_deleted += commit['lines_deleted']
        total_files_changed += commit['files_changed']
    
    negative_sentiments = sentiments.count('NEGATIVE')
    total_commits = len(sentiments)
    
    if total_commits == 0:
        return "Low"
    
    negative_ratio = negative_sentiments / total_commits
    line_change_stress = (total_lines_added + total_lines_deleted + total_files_changed) / total_commits

    # Consider both negative sentiment ratio and line change stress
    if negative_ratio > 0.5 and 100 > line_change_stress:
        return "High"
    elif negative_ratio > 0.3 and 50 > line_change_stress :
        return "Medium"
    else:
        return "Low"

def get_recommendations(stress_level):
    recommendations = {
        "High": ["Take a break", "Meditate for 10 minutes", "Talk to a counselor"],
        "Medium": ["Take a short walk", "Practice deep breathing", "Review your task list"],
        "Low": ["Keep up the good work!", "Maintain your current routine"]
    }
    return recommendations.get(stress_level, [])

def sentiment_analysis_controller(repo_url, user_name):
    repo_path = get_repo_path(repo_url)
    commits = get_commits_by_username(user_name, repo_path)
    if not commits:
        return jsonify({"error": "No commits found or failed to fetch commits"}), 404

    commit_frequency_stress = analyze_commit_frequency(commits)
    commit_sentiment_stress = analyze_commit_sentiment(commits)
    final_stress_level = max(commit_frequency_stress, commit_sentiment_stress, key=lambda level: ["Low", "Medium", "High"].index(level))
    recommendations = get_recommendations(final_stress_level)
    
    return jsonify({
        "stress_level": final_stress_level,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
