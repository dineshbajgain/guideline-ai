from flask import Flask, request, jsonify
from transformers import pipeline
import requests
from dotenv import load_dotenv
app = Flask(__name__)
import os
# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline('sentiment-analysis')
# Load environment variables from .env file
load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
def fetch_github_commits(username, repo):
    url = 'https://api.github.com/repos/{username}/{repo}/commits'
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(f"{url}/commits", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def analyze_commit_frequency(commits):
    commit_dates = [commit['commit']['author']['date'] for commit in commits]
    commit_count = len(commit_dates)
    if commit_count > 20:
        return "High"
    elif commit_count > 10:
        return "Medium"
    else:
        return "Low"

def analyze_commit_sentiment(commits):
   # Initialize a list to hold the sentiment results
    sentiments = []
    
    # Process each commit message for sentiment analysis
    for commit in commits:
        commit_message = commit['commit']['message']
        if commit_message:  # Ensure the commit message is not empty
            sentiment = sentiment_pipeline(commit_message)[0]['label']
            sentiments.append(sentiment)
    
    # Calculate the number of negative sentiments
    negative_sentiments = sentiments.count('NEGATIVE')
    total_commits = len(sentiments)
    
    # Avoid division by zero by checking if total_commits is greater than zero
    if total_commits == 0:
        return "Low"
    
    # Calculate the ratio of negative sentiments to total commits
    negative_ratio = negative_sentiments / total_commits
    
    # Determine stress level based on the negative sentiment ratio
    if negative_ratio > 0.5:
        return "High"
    elif negative_ratio > 0.3:
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

@app.route('/')
def home():
    return "Welcome to the Employee Well-being API"

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    username = data.get('username')
    repo = data.get('repo')
    if not username or not repo:
        return jsonify({"error": "Missing username or repository"}), 400

    commits = fetch_github_commits(username, repo)
    stress_level = analyze_commit_frequency(commits)
    commit_frequency_stress = analyze_commit_frequency(commits)
    commit_sentiment_stress = analyze_commit_sentiment(commits)
    final_stress_level = max(commit_frequency_stress, commit_sentiment_stress, key=lambda level: ["Low", "Medium", "High"].index(level))
    recommendations = get_recommendations(final_stress_level)
    
    return jsonify({
        "stress_level": stress_level,
        "recommendations": recommendations,
        "final_stress_level": final_stress_level,
        "commit_frequency_stress": commits,
    })

if __name__ == '__main__':
    app.run(debug=True)
