import os
from flask import Flask, request, jsonify, abort
from functools import wraps

app = Flask(__name__)

# Load environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a_default_key'

# Mock database
projects = []

# Authorization decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Simulate checking for user authorization
        if not request.headers.get('Authorization'):
            abort(403)
        return f(*args, **kwargs)
    return decorated

@app.route('/projects', methods=['POST'])
@requires_auth
def create_project():
    # Create a new project
    data = request.json
    projects.append(data)
    return jsonify(data), 201

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    # Get a single project
    project = next((p for p in projects if p['id'] == project_id), None)
    return jsonify(project) if project else (abort(404))

@app.route('/projects/<int:project_id>', methods=['PUT'])
@requires_auth
def edit_project(project_id):
    # Edit a project
    data = request.json
    project = next((p for p in projects if p['id'] == project_id), None)
    if project:
        project.update(data)
        return jsonify(project)
    return abort(404)

@app.route('/projects/<int:project_id>', methods=['DELETE'])
@requires_auth
def delete_project(project_id):
    # Delete a project
    global projects
    projects = [p for p in projects if p['id'] != project_id]
    return jsonify({'result': True})

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden'}), 403

if __name__ == "__main__":
    app.run(debug=True)