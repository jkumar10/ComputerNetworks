'''*********************************************************************************
  a2 SOURCE FILE - Jainendra Kumar (jaikumar)
  CREATED: 09/30/2018
  This is an Networks assignment 2 Task 1 and Task 2
  This code provides Server and Client socket functionality with TCP and UDP protocol
  Run instructions:
  TO START TCP SERVER:
  $python3 netster.py -p <portnumber>
  or
  $python3 netster.py (will start on default port)
  TO START TCP CLIENT:
  $python3 netster.py <hostip> -p <portnumber>
  or
  $python3 netster.py <hostip> (will start on default port)
  TO START UDP SERVER:
  $python3 netster.py -p <portnumber> -u
  or
  $python3 netster.py -u (will start on default port)
  TO START UDP CLIENT:
  $python3 netster.py <hostip> -p <portnumber> -u
  or
  $python3 netster.py <hostip> -u (will start on default port)
*************************************************************************************'''
import socket
import logging as log


HOST_IP = '10.10.2.10'

# Method to invoke TCP server
# Accepts PORT as an argument
def tcp_server(PORT):
    print("**************TCP SERVER***********************")
    # Creating a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("TCP Socket for server created sucessfully")
    server_address = (HOST_IP, PORT)
    print("Starting the TCP server on:",server_address)
    # Binding the socket and the port
    s.bind(server_address)
    # Invoking the socket to start the listening
    s.listen(1)
    while True:
      print("Waiting for a new client")
      connection, client_address = s.accept()
      try:
        print("Connected with", client_address)
        while True:
          # Receiving the data, buffer size is given as 255
          data = connection.recv(255)
          decoded_data = data.decode()
          print("Client Message: ",decoded_data)
          if decoded_data.strip()=="hello":
            response=str.encode("world"+"\r\n")
            connection.send(response)
            print("Replied: world")
          elif decoded_data.strip()=="goodbye":
            response=str.encode("farewell"+"\r\n")
            connection.send(response)
            print("Replied: farewell"+"\r\n")
            break
          elif decoded_data.strip()=="exit":
            response=str.encode("ok"+"\r\n")
            connection.send(response)
            print("Replied: ok"+"\r\n")
            exit(0)
          else:
            connection.send(data)
            print("Replied: ",decoded_data+"\r\n")
      finally:
        connection.close()

# Method to invoke tcp client
# Accepts host and port as an argument
def tcp_client(HOST,PORT):
    print("**************TCP CLIENT***********************")
    # creating the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST,PORT)
    print("Waiting to connect to:",server_address)
    try:
      s.connect(server_address)
      print("Connected! Start chatting with the server")
    except:
      print("Connection failed")
    while True:
      message = input("Type message:")
      message_bytes=str.encode(message)
      s.sendall(message_bytes)
      data = s.recv(255)
      decoded_data = data.decode()
      print("Server Response:",decoded_data)
      if message.strip()=="goodbye":
        exit(0)
      if message.strip()=="exit":
        exit(0)
    s.close()


# Method to invoke UDP Server
# Accepts port as an argument
def udp_server(PORT):
    print("**************UDP SERVER***********************")
    # Creating the UDP Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP Socket created sucessfully")
    server_address = (HOST_IP, PORT)
    print("Starting the UDP server on:", server_address)
    # Binding the socket with the port
    s.bind(server_address)
    while True:
      print("Waiting for a new client")
      try:
        while True:
          data,address = s.recvfrom(255)
          decoded_data = data.decode()
          print("Client Message: ", decoded_data)
          if decoded_data.strip()=="hello":
            response=str.encode("world"+"\r\n")
            s.sendto(response,address)
            print("Replied: world"+"\r\n")
          elif decoded_data.strip()=="goodbye":
            response=str.encode("farewell"+"\r\n")
            s.sendto(response,address)
            print("Replied: farewell"+"\r\n")
            break
          elif decoded_data.strip()=="exit":
            response=str.encode("ok"+"\r\n")
            s.sendto(response,address)
            print("Replied: ok"+"\r\n")
            s.close()
            exit(0)
          elif data:
            s.sendto(data,address)
            print("Replied:",decoded_data+"\r\n")
      except Exception as err:
        log.info(err)
    s.close()


# Method to invoke udp client
# Accepts host and port as an argument
def udp_client(HOST,PORT):
    print("**************UDP CLIENT***********************")
    # Creating the UDP Client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (HOST,PORT)
    print("Waiting to connect to:",server_address)
    while True:
        message = input("Type message:")
        message_bytes=str.encode(message)
        s.sendto(message_bytes,server_address)
        data,server = s.recvfrom(255)
        decoded_data = data.decode()
        print("Server Response:", decoded_data)
        if message.strip()=="goodbye":
            exit(0)
        if message.strip()=="exit":
            exit(0)
    s.close()
