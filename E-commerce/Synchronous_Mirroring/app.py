from flask import Flask, jsonify, request , render_template 
import json
import os

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

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    products = read_data(PRIMARY_DB)
    products.append(data)
    write_data(PRIMARY_DB, products)  # Update primary database
    write_data(SECONDARY_DB, products)  # Update secondary database synchronously
    return jsonify(data)

# Similar implementation for PUT, DELETE...
@app.route('/')
def home():
    return render_template('Frontend/templates/index.html')
if __name__ == '__main__':
    app.run(debug=True)
