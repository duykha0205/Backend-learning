import socket

server_socket = socket.socket()
server_socket.bind(('localhost', 8000))
server_socket.listen()

backend_servers = ['localhost:8001', 'localhost:8002', 'localhost:8003']

current_server = 0
while True:
    client_socket, address = server_socket.accept()
    backend_server = backend_servers[current_server]
    current_server = (current_server + 1) % len(backend_servers)
    backend_host, backend_port = backend_server.split(':')
    
    backend_socket = socket.socket()
    backend_socket.connect((backend_host, int(backend_port)))
    backend_socket.sendall('Hello from load balancer!'.encode())
    response = backend_socket.recv(1024)
    client_socket.sendall(response)
    backend_socket.close()
    
    print("from " + str(client_socket) + ": " + str(address))
    print("to " + str(backend_host) + ": " + str(backend_port))
    print("-----")
    
    client_socket.close()