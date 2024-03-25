from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)

DATABASE_PATH = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Projects (U_id, M_id, D_id) VALUES (?, ?, ?)',
                   (data['U_id'], data['M_id'], data['D_id']))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Project created successfully"}), 201

@app.route('/projects/<int:p_id>', methods=['GET'])
def get_project(p_id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM Projects WHERE P_id = ?', (p_id,)).fetchone()
    conn.close()
    if project is None:
        abort(404)
    return jsonify(dict(project)), 200

@app.route('/projects/<int:p_id>', methods=['PUT'])
def update_project(p_id):
    data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE Projects SET U_id = ?, M_id = ?, D_id = ? WHERE P_id = ?',
                 (data['U_id'], data['M_id'], data['D_id'], p_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Project updated successfully"}), 200

@app.route('/projects/<int:p_id>', methods=['DELETE'])
def delete_project(p_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Projects WHERE P_id = ?', (p_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Project deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)