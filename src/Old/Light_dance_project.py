import socket

# Create a socket object.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port.
server_socket.bind('127.0.0.1', 5000)

# Listen for connections.
server_socket.listen(1)

# Accept a connection.
client_socket, address = server_socket.accept()

# Send the array of floats.
data = [0.9, 120000, 0.85, 12.8, 0.1, 28, 16, 124565, 0.72, 3.9]
client_socket.send(data)

# Close the connection.
client_socket.close()

# Close the server socket.
server_socket.close()
