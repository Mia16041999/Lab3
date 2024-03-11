from flask import Flask, jsonify, request , render_template
import json
import os
from threading import Thread

app = Flask(__name__)

PRIMARY_DB = 'primary_db.json'
SECONDARY_DB = 'secondary_db.json'

def read_data(db_file):
    if not os.path.exists(db_file):
        return {}
    with open(db_file, 'r') as file:
        return json.load(file)

def write_data(db_file, data):
    with open(db_file, 'w') as file:
        json.dump(data, file, indent=4)

def replicate_data(data):
    write_data(SECONDARY_DB, data)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    products = read_data(PRIMARY_DB)
    products.append(data)
    write_data(PRIMARY_DB, products)  # Update primary database
    # Asynchronously replicate changes to the secondary database
    Thread(target=replicate_data, args=(products,)).start()
    return jsonify(data)
@app.route('/')
def home():
    # The path 'frontend/templates/index.html' is relative to the root directory
    # and points to the index.html file inside the templates directory.
    return render_template('frontend/templates/index.html')
# Similar implementation for PUT, DELETE...

if __name__ == '__main__':
    app.run(debug=True)
