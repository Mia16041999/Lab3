from flask import Flask, jsonify, request , render_template

app = Flask(__name__)

# Dummy data for products and orders (you can replace with actual database or JSON file)
products = [
    {"id": 1, "name": "Product 1", "price": 10.0, "category": "Category 1", "stock": 100},
    {"id": 2, "name": "Product 2", "price": 20.0, "category": "Category 2", "stock": 50},
]

orders = []

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
    products.append(data)
    return jsonify(data)

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
    products = [p for p in products if p['id'] != product_id]
    return jsonify({"message": "Product deleted"})

# Orders Routes
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    orders.append(data)
    return jsonify(data)

@app.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    user_orders = [order for order in orders if order.get('user_id') == user_id]
    return jsonify(user_orders)
@app.route('/')
def home():
    # The path 'frontend/templates/index.html' is relative to the root directory
    # and points to the index.html file inside the templates directory.
    return render_template('Frontend/templates/index.html')
if __name__ == '__main__':
    app.run(debug=True)
