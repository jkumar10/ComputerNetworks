'''*********************************************************************************
  a2 thread SOURCE FILE - Jainendra Kumar (jaikumar)
  CREATED: 09/22/2018
  This is an Networks assignment 2 Task 3
  This code provides Server and multi client socket functionality with threading
  Run instructions:
  TO START TCP SERVER:
  $python3 netster_multithread.py -p <portnumber>
  or
  $python3 netster_multithread.py (will start on default port)
  TO START TCP CLIENT:
  $python3 netster_multithread.py <hostip> -p <portnumber>
  or
  $python3 netster_multithread.py <hostip> (will start on default port)
  TO START UDP SERVER:
  $python3 netster_multithread.py -p <portnumber> -u
  or
  $python3 netster_multithread.py -u (will start on default port)
  TO START UDP CLIENT:
  $python3 netster_multithread.py <hostip> -p <portnumber> -u
  or
  $python3 netster_multithread.py <hostip> -u (will start on default port)
*************************************************************************************'''
import sys
import socket
import threading

HOST_IP = '127.0.0.1'

# This is a tcp_server method which is invoked by tcp_thread()
# For each client tcp_thread() will create a separate thread
# and invoke the tcp_server
TCP_ON=True
def tcp_server(connection,s,client_address):
    global TCP_ON
    while True:
        try:
            # Receiving the data
            data = connection.recv(255)
            decoded_data = data.decode()
            print("Client Message: ", decoded_data)
            # Condition based responses
            if decoded_data.strip() == "hello":
                response = str.encode("world"+"\r\n")
                connection.send(response)
                print("Replied: world"+"\r\n")
            elif decoded_data.strip() == "goodbye":
                response = str.encode("farewell"+"\r\n")
                connection.send(response)
                print("Replied: farewell"+"\r\n")
                connection.close()
                break
            elif decoded_data.strip() == "exit":
                response = str.encode("ok")
                connection.send(response)
                print("Replied: ok")
                print("Terminating Connection: Server Closed")
                TCP_ON=False
                s.close()
                break
            else:
                connection.send(data)
                print("Replied: ", decoded_data)
        except s.timeout as error:
            var = error.args
            print(var)



# This method will create a separate thread for each
# TCP client. It will then invoke the tcp_server()
# method for condition based responses
def tcp_thread(PORT):
    print("***********TCP SERVER*********************")
    # Creating the TCP Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("TCP Socket created sucessfully")
    server_address = (HOST_IP, PORT)
    print("Starting the TCP server on:",server_address)
    # Binding the TCP Socket and the port
    s.bind(server_address)
    # Starting the TCP Socket to listen
    s.listen(1)
    while True:
        try:
            if not TCP_ON:
                break
            connection, client_address = s.accept()
            s.settimeout(2.0)
            print("Connected with", client_address)
            # Creating a thread object, passing the connection, socket object and client
            # objects. Keeping the daemon as True so if server closes all the clients are
            # shut down.
            t=threading.Thread(target=tcp_server,args=(connection,s,client_address),daemon=True)
            t.start()
        except:
            pass
    exit(0)



# Method to invoke tcp client
# Accepts host and port as an argument
def tcp_client(HOST,PORT):
    print("***********TCP CLIENT*********************")
    # Creating the clinet socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    server_address = (HOST,PORT)
    print("Waiting to connect to:",server_address)
    try:
        # Connecting the client to the socket
        s.connect(server_address)
        print("Connected! Start chatting with the server")
    except:
        print("Connection failed")
    try:
        while True:
            message = input("Type message:")
            message_bytes=str.encode(message)
            s.sendall(message_bytes)
            # Creating the buffer size of 255 to receive data
            data = s.recv(255)
            decoded_data = data.decode()
            print("Server Response:",decoded_data)
            if message.strip()=="goodbye":
                exit(0)
            if message.strip()=="exit":
                exit(0)
        s.close()
    except:
        print("Exited")


# This is a udp_server method which is invoked by udp_thread()
# For each client, udp_thread() will create a separate thread
# and invoke the udp_server for condition based responses.
UDP_ON=True
def udp_server(s,data,address):
    global UDP_ON
    try:
        # Decoding the data
        decoded_data = data.decode()
        print("Client Message: ", decoded_data)
        if decoded_data.strip() == "hello":
            response = str.encode("world" + "\r\n")
            s.sendto(response, address)
            print("Replied: world" + "\r\n")
        elif decoded_data.strip() == "goodbye":
            response = str.encode("farewell" + "\r\n")
            s.sendto(response, address)
            print("Replied: farewell" + "\r\n")
        elif decoded_data.strip() == "exit":
            UDP_ON = False
            response = str.encode("ok" + "\r\n")
            s.sendto(response, address)
            print("Replied: ok" + "\r\n")
            print("Terminating Connection: Server Closed")
            s.close()
            return
        elif data:
            s.sendto(data, address)
            print("Replied:", decoded_data + "\r\n")
    except:
        pass




# This method will create a separate thread for each
# UDP client. It will then invoke the udp_server()
# method for condition based responses.
def udp_thread(PORT):
    global UDP_ON
    print("***********UDP SERVER*********************")
    # Creating the UDP Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    print("UDP Socket created sucessfully")
    server_address = (HOST_IP, PORT)
    print("Starting the UDP server on:", server_address)
    # Binding the Host IP and the port
    s.bind(server_address)
    print("Waiting for a new client")
    while True:
        try:
            if not UDP_ON:
                s.close()
                break
            # Creating the buffer of 255 and receiving the data
            data, address = s.recvfrom(255)
            # Creating a thread object, passing the connection, socket object and client
            # objects. Keeping the daemon as True so if server closes all the clients are
            # shut down.
            t=threading.Thread(target=udp_server,args=(s,data,address),daemon=True)
            t.daemon=True
            t.start()
        except:
            pass
    exit(0)



# Method to invoke udp client
# Accepts host and port as an argument
def udp_client(HOST,PORT):
    print("***********UDP CLIENT*********************")
    # Creating the UDP Client Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    # Binding the HOST and the PORT
    server_address = (HOST,PORT)
    print("Waiting to connect to:",server_address)
    try:
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
    except:
        print("Exited")


