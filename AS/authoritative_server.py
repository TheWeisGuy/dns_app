import socket
import json
import os

AS_PORT = 53533
DNS_DB = "dns_database.json"

def run_as():
    # 1. Ensure DB file exists
    if not os.path.exists(DNS_DB):
        with open(DNS_DB, 'w') as f:
            json.dump({}, f)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', AS_PORT))
    print(f"Authoritative Server listening on port {AS_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        print(f"Received raw:\n{message}") # Debug print
        
        if "VALUE=" in message:
            try:
                parts = message.split()
                
                name = parts[1].split('=')[1]
                value = parts[2].split('=')[1]
                ttl = parts[3].split('=')[1]
               
                with open(DNS_DB, 'r+') as f:
                    try:
                        db = json.load(f)
                    except json.JSONDecodeError:
                        db = {} 
                    
                    db[name] = {"ip": value, "ttl": ttl}
                    f.seek(0)
                    json.dump(db, f)
                    f.truncate()
                print(f"Successfully Registered {name} -> {value}")
            except Exception as e:
                print(f"Registration Error: {e}")

        else:
            
            try:
                parts = message.split()
            
                name = parts[1].split('=')[1]
                
                with open(DNS_DB, 'r') as f:
                    try:
                        db = json.load(f)
                    except json.JSONDecodeError:
                        db = {} 
                
                print(f"Looking up {name} in DB: {db}") 
                
                if name in db:
                    response = f"TYPE=A\nNAME={name} VALUE={db[name]['ip']} TTL={db[name]['ttl']}"
                    sock.sendto(response.encode(), addr)
                    print(f"Sent response for {name}")
                else:
                    print(f"Host {name} not found in database")
                    response = f"TYPE=A\nNAME={name} ERROR=NotFound"
                    sock.sendto(response.encode(), addr)
            except Exception as e:
                print(f"Query Error: {e}")

if __name__ == '__main__':
    run_as()