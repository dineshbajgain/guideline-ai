
from flask import request, jsonify

def test_controller():
    data = request.json
    if not data or 'repo_url' not in data:
        return jsonify({'error': 'Missing repo_url'}), 400
    return jsonify({'message': 'Success', 'repo_url': data['repo_url']})