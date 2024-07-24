from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    return jsonify({"message": "Register endpoint reached!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
