import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 8001)

# Bind the socket to the address and port
server_socket.bind(server_address)

# Listen for incoming connections (backlog argument specifies the maximum number of queued connections)
server_socket.listen(5)

# Accept incoming connections
while True:
    print('Waiting for a connection...')
    client_socket, client_address = server_socket.accept()
    # data contains data take from load balancer
    data = client_socket.recv(1024)
    print(f'Accepted connection from {client_address}')
    print(f'Data from {client_address}: {data}')
    

    # Handle the connection
    message = 'Welcome to the server ' + str(server_address)
    client_socket.sendall(message.encode())
    client_socket.close()





