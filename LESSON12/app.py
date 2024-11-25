from flask import Flask, jsonify, request
from celery_config import celery  # Import Celery instance
import logging_config             # Import logging configuration

# Initialize Flask app
app = Flask(__name__)

# In-memory data store
data = []

# Home route
@app.route('/')
def home():
    return "Welcome to the Flask + Celery application!"

# Route: Get all items (GET)
@app.route('/items', methods=['GET'])
def get_items():
    print(f"Requested URL: {request.url}")
    return jsonify({"items": data})

# Route: Add an item (POST)
@app.route('/item', methods=['POST'])
def add_item():
    new_item = request.json.get('name')
    if new_item:
        data.append(new_item)
        return jsonify({"message": "Item added", "item": new_item}), 201
    return jsonify({"error": "Name is required"}), 400

# Route: Update an item (PUT)
@app.route('/item/<int:index>', methods=['PUT'])
def update_item(index):
    if index < len(data):
        updated_item = request.json.get('name')
        if updated_item:
            data[index] = updated_item
            return jsonify({"message": "Item updated", "item": updated_item}), 200
        return jsonify({"error": "Name is required"}), 400
    return jsonify({"error": "Item not found"}), 404

# Route: Delete an item (DELETE)
@app.route('/item/<int:index>', methods=['DELETE'])
def delete_item(index):
    if index < len(data):
        removed_item = data.pop(index)
        return jsonify({"message": "Item deleted", "item": removed_item}), 200
    return jsonify({"error": "Item not found"}), 404

# Route: Trigger a Celery task
@app.route('/task/add', methods=['POST'])
def trigger_task():
    numbers = request.json
    if 'x' in numbers and 'y' in numbers:
        task = celery.send_task('celery_config.long_running_task', args=[numbers['x'], numbers['y']])
        return jsonify({"task_id": task.id, "status": "Task submitted"}), 202
    return jsonify({"error": "Invalid input, 'x' and 'y' are required"}), 400

# Error handler: 404
@app.errorhandler(404)
def not_found(error):
    logging_config.logger.error(f"404 Error: {error}")
    return jsonify({"error": "Resource not found"}), 404

# Error handler: 500
@app.errorhandler(500)
def internal_error(error):
    logging_config.logger.error(f"500 Error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
