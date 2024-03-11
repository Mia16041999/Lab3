from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/getServer')
def get_server():
    server_url = request.host_url
    return jsonify({"code": 200, "server": server_url})
@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
