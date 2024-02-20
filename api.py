from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

DIYML = Flask(__name__)

# Assuming a directory for saving uploaded files
UPLOAD_FOLDER = 'uploads'
DIYML.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create project
@DIYML.route('/create_project', methods=['POST'])
def create_project():
    return jsonify({"message": "Project created successfully", "project_id": 1})
# Upload data
@DIYML.route('/upload_data/<project_id>', methods=['POST'])
def upload_data(project_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(DIYML.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Data uploaded successfully", "filename": filename})
# Upload label
@DIYML.route('/upload_labels/<project_id>', methods=['POST'])
def upload_labels(project_id):
    labels = request.json
    return jsonify({"message": "Labels uploaded successfully", "labels": labels})
# Analyze daata
@DIYML.route('/analyze_data/<project_id>', methods=['GET'])
def analyze_data(project_id):
    return jsonify({"message": "Data analysis complete", "analysis": "Some stats"})
# Add training points
@DIYML.route('/add_data/<project_id>', methods=['POST'])
def add_data(project_id):
    return jsonify({"message": "Data added successfully"})
# Remove training points
@DIYML.route('/remove_data/<project_id>', methods=['POST'])
def remove_data(project_id):
    data_ids = request.json.get('data_ids')
    return jsonify({"message": "Data removed successfully", "removed_ids": data_ids})
# Configure training parameters
@DIYML.route('/configure_parameters/<project_id>', methods=['POST'])
def configure_training(project_id):
    training_params = request.json
    return jsonify({"message": "Training parameters", "params": training_params})
# Get training states
@DIYML.route('/training_stats/<project_id>/<training_id>', methods=['GET'])
def get_training_stats(project_id, training_id):
    training_stats = {
        "accuracy": acuracy,
        "loss": loss,
        "epochs": epochs
    }
    return jsonify({"message": "Training stats fetched successfully", "training_stats": training_stats})
# Test and get result
@DIYML.route('/test_model/<project_id>/<model_id>', methods=['POST'])
def test_model(project_id, model_id):
    test_results = {
        "total_tests": number_test,
        "accuracy": accuracy
    }
    return jsonify({"message": "Model tested successfully", "test_results": test_results})
# deploy model
@DIYML.route('/deploy_model/<project_id>', methods=['POST'])
def deploy_model(project_id):
    return jsonify({"message": "Model deployed", "deployment_id": "unique_api_endpoint"})
# run and track iterations
@DIYML.route('/projects/<project_id>/iterations', methods=['POST'])
def start_training_iteration(project_id):
    user_id = request.json.get('user_id') 
    iteration_details = request.json.get('details', {})
    iteration_id = queue_training_job(project_id, iteration_details)

    return jsonify({"message": "Training iteration started", "iteration_id": iteration_id})
@DIYML.route('/projects/<project_id>/iterations/<iteration_id>', methods=['GET'])
def track_training_iteration(project_id, iteration_id):
    user_id = request.args.get('user_id') 
    iteration_status = get_training_status(iteration_id)

    return jsonify({"iteration_id": iteration_id, "status": iteration_status})


# intference API to run and get result
@DIYML.route('/inference/<deployment_id>', methods=['POST'])
def run_inference(deployment_id):
    image = request.files['image']
    user_id = get_user_id_from_request(request)
    if not validate_deployment_access(user_id, deployment_id):
        return jsonify({"error": "Unauthorized access to deployment"}), 403
    results = process_image_and_run_inference(image, deployment)
    return jsonify({"message": "Inference completed", "results": results})
