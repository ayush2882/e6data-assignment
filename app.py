from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/ip', methods=['GET'])
def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return jsonify({"pod_ip": ip_address})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)