To build, cd to /dns_app and run: docker compose up --build 

This will run every server at once, but to run each one individually, run: python3 <serverName>_server.py

Testing curl commands:


Registering:

curl -X PUT -H "Content-Type: application/json"      -d '{"hostname": "fibonacci.com", "ip": "10.9.10.3", "as_ip": "10.9.10.2", "as_port": "53533"}'      http://localhost:9090/register

This adds the json entry {"fibonacci.com": {"ip": "10.9.10.3", "ttl": "10"}} to dns_app/dns_database.json


Testing /fibonacci:

For the user server:
curl "http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=10.9.10.2&as_port=53533"

This tests the fibonacci path with a value of 10. It should return 55. To test other numbers, change the number= query param


For the fibonacci server:
curl "http://localhost:9090/fibonacci?number=10"

Again change the number query param for different values


To deploy with kubernetes:
kubectl apply -f deploy_dns.yml