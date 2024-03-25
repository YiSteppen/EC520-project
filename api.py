from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

DIYML = Flask(__name__)


# Assuming a directory for saving uploaded files
UPLOAD_FOLDER = 'uploads'
projects = {}
User = {}
upload_data = {}
trainingresult = {}
testingresult = {}
training_stats = {}
DIYML.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
User_id_g = 1
Data_id = 1
project_id_counter= 1
training_points= 1

# Create project
@DIYML.route('/user', methods=['POST'])
def create_project():
    User_id = request.json
    User_name = request.json
    User_password = request.json
    User_email = request.json
    User[User_id] = {
        'User_id':User_id,
        'User_name': User_name,
        'User_password': User_password,
        'User_email': User_email,
    }
    global User_id_g
    User_id_g = User_id
    return jsonify({"message": "User login", "User_id": User_id}), 200

# Create project
@DIYML.route('/projects', methods=['POST'])
def create_project():
    global project_id_counter
    project_model_id = request.json
    project_data_id = request.json
    projects[project_id_counter] = {
        'id': project_id_counter,
        'User_id': User_id_g,
        'model_id': project_model_id,
        'data_id': project_data_id,
        'training_points': training_points,
    }
    project_id_counter += 1
    return jsonify({"message": "Project created successfully", "project_id": 1}), 200

# Upload data
@DIYML.route('/upload_data/<int:Data_id>', methods=['POST'])
def upload_data(project_id):
    global Data_id
    data = request.files
    train_data = data.get('train_data')
    test_data = data.get('test_data')
    label = data.get('label')
    upload_data[Data_id] = {
        'User_id': User_id_g,
        'Data_id': Data_id,
        'train_data': train_data,
        'test_data': test_data,
        'label': label,
    }
    Data_id += 1
    

# Analyze data
@DIYML.route('/projects/<int:project_id>/analyze', methods=['POST'])
def analyze_data(project_id, Data_id):
    analysis_results = {
        "message": "Data analysis completed",
        "project_id": project_id,
        "data_id": Data_id,
        "analysis": {
            "total_samples": 100,
            "missing_values": False,
            "class_distribution": {
                "class_1": 50,
                "class_2": 50
            }
        }
    }
    return jsonify(analysis_results), 200

# Training model
@DIYML.route('/Training/<int:project_id>', methods=['POST'])
def Training(project_id, Data_id):
        train_data = upload_data[Data_id].get('train_data')
        train_project = projects[project_id].get('model_id')
        project_model_id = projects[project_id].get('model_id')
        project_data_id = projects[project_id].get('data_id')
        result = train_model(train_data, train_project);
        trainingresult[project_id] = {
        'project_id': project_id,
        'User_id': User_id_g,
        'model_id': project_model_id,
        'data_id': project_data_id,
        'training_points': training_points,
        'result': result
    }
        training_stats[project_id] = {
        'accuracy': result['accuracy'],
        'loss': result['loss'],
        'time': result['time']
    }
        project_model_id.save(f'models/model_{project_id}.h5')
    

# Test model
@DIYML.route('/Testing/<int:project_id>', methods=['POST'])
def Testing(project_id, Data_id):
        test_data = upload_data[Data_id].get('test_data')
        train_project = projects[project_id].get('model_id')
        project_model_id = projects[project_id].get('model_id')
        project_data_id = projects[project_id].get('data_id')
        result = test_model(test_data, train_project);
        testingresult[project_id] = {
        'project_id': project_id,
        'User_id': User_id_g,
        'model_id': project_model_id,
        'data_id': project_data_id,
        'training_points': training_points,
        'result': result
    }



# Add or remove training points
@DIYML.route('/projects/<int:project_id>/training_points', methods=['Put'])
def add_training_point(project_id):
    training_point_update = request.get_json()
    training_points = training_points + training_point_update
    return jsonify({"message": "Data point added successfully", "total_training_points": training_points}), 200

@DIYML.route('/projects/<int:project_id>/training_points', methods=['Put'])
def remove_data_point(project_id):
    data_point = request.get_json()
    training_points = training_points - training_point_update
    return jsonify({"message": "Data point delete successfully", "total_data_points": training_points}), 200


# Add training points
@DIYML.route('/add_data/<project_id>', methods=['POST'])
def add_data(project_id):
    return jsonify({"message": "Data added successfully"}), 200


# Remove training points
@DIYML.route('/remove_data/<project_id>', methods=['POST'])
def remove_data(project_id):
    data_ids = request.json.get('data_ids')
    return jsonify({"message": "Data removed successfully", "removed_ids": data_ids}), 200


# Configure training parameters
@DIYML.route('/configure_parameters/<project_id>', methods=['POST'])
def configure_training(project_id):
    training_params = request.json
    return jsonify({"message": "Training parameters", "params": training_params}), 200


# Get training states
@DIYML.route('/training_stats/<project_id>', methods=['GET'])
def get_training_stats(project_id):
    return jsonify(training_stats[project_id])

# Inference
@DIYML.route('/inference', methods=['POST'])
def perform_inference():
    data = request.get_json()
    project_id = data['project_id']
    iteration = data['iteration']
    data_inference = data['inference_data']

    model = load_model_for_inference(project_id, iteration) 
    result = model_predict(model, data)

    return jsonify({"result": result}), 200