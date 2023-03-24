import socket
import time

server_address = ('localhost', 8000)

# Send some requests to the load balancer
for i in range(10):
    client_socket = socket.socket()
    client_socket.connect(server_address)
    message = f'Request {i+1}'
    client_socket.sendall(message.encode())
    response = client_socket.recv(1024)
    print(f'Response from server: {response.decode()}')
    time.sleep(1)

client_socket.close()