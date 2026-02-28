from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

#ip url registration
@app.route('/register', methods=['PUT'])
def register():
    #parse data from request
    data = request.json
    hostname = data.get('hostname')
    fs_ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    dns_message = f"TYPE=A\nNAME={hostname} VALUE={fs_ip} TTL=10"

    #create udp socket and register url and ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_message.encode(), (as_ip, int(as_port)))
    sock.close()

    return "Registered", 201

@app.route('/fibonacci', methods=['GET'])
def calculate_fibonacci():
    num_str = request.args.get('number')
    
    try:
        n = int(num_str)
        if n < 0: raise ValueError
    except (ValueError, TypeError):
        return "Bad Request: 'number' must be a non-negative integer", 400


    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    
    return str(a), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)