from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load products and orders from JSON files
with open('products.json') as f:
    products = json.load(f)

with open('orders.json') as f:
    orders = json.load(f)


# Products Routes
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    data['id'] = max(p['id'] for p in products) + 1  # Assign new ID to product
    products.append(data)
    return jsonify(data), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        product.update(data)
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        products.remove(product)
        return jsonify({"message": "Product deleted"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404


# Orders Routes
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    data['id'] = max(o['id'] for o in orders) + 1  # Assign new ID to order
    orders.append(data)
    return jsonify(data), 201

@app.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    user_orders = [order for order in orders if order.get('user_id') == user_id]
    if user_orders:
        return jsonify(user_orders)
    else:
        return jsonify({"error": "No orders found for user"}), 404


@app.route('/')
def home():
    return render_template('Frontend/templates/index.html')

if __name__ == '__main__':
    app.run(debug=True)
