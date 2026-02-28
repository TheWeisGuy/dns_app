from flask import Flask, request
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():

    #parse query params
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    fib_number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

   #check no missing params
    if not all([hostname, fs_port, fib_number, as_ip, as_port]):
        return "Bad Request: Missing parameters", 400

    try:
       
       #build query string
        dns_query = f"TYPE=A\nNAME={hostname}" 
        
      #build socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(dns_query.encode(), (as_ip, int(as_port)))
        
       #call auth server and get response
        data, addr = sock.recvfrom(1024)
        response_str = data.decode()
        print(f"Received from AS: {response_str}") 
        sock.close()

        
        try:
            #interpret response
            parts = response_str.split()
            fs_ip = None
            for part in parts:
                if part.startswith("VALUE="):
                    fs_ip = part.split('=')[1]
                    break
            #if no value returned
            if not fs_ip:
                raise ValueError("VALUE not found in DNS response")
                
        except Exception as e:
            return f"DNS Parsing Failed: {str(e)}", 500

        #build and send query to FS
        fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={fib_number}"
        print(f"Querying FS: {fs_url}")
        response = requests.get(fs_url)
        
        return response.text, response.status_code

    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)