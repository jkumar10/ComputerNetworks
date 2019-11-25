
'''************************************************************************************
  SOURCE FILE - Jainendra Kumar (jaikumar)
  CREATED: 11/12/2019
  This is an Networks assignment 3 Task 1, Task 2, Task 3 and Task 4
  This code provides reliable UDP file transfer functionality using Go-Back-n and 
  alternate bit(stop and wait) protocols
  RUN INSTRUCTIONS:
  TO START TCP:
  Server: $python3 netster.py -p <portnumber>
  Client: $python3 netster.py <hostip> -p <portnumber>
 
  TO START UDP:
  Server: $python3 netster.py -p <portnumber> -u
  Client: $python3 netster.py <hostip> -p <portnumber> -u

  TO START RUDP STOP AND WAIT PROTOCOL
  Receiver: $python3 netster.py -r 1 -p <portnumber> -f <outputfilename>
  Sender: $python3 netster.py <host> -r 1 -p <portnumber> -f <inputfilename>

  TO START RUDP GO BACK N PROTOCOL
  Receiver: $python3 netster.py -r 2 -p <portnumber> -f <outputfilename>
  Sender: $python3 netster.py <host> -r 2 -p <portnumber> -f <inputfilename>
  
*************************************************************************************'''
import socket
import logging as log
import time

sender_chunk_size=1024
receiver_chunk_size=2000
Timeout=100
HOST_IP = '10.10.2.10'
window_size=5
window=[]
rttdict={}
senttimedict={}
receivetimedict={}
expectedrtt=50

# Method for RUDP STOP and WAIT or ALTERNATE-BIT client or sender
def rudp_alternatebit_sender(HOST,PORT,filename):
    global window_size
    global expectedrtt
    try:
        l=[]
        seqnum=0
        print("---------------RUDP SENDER-----ALTERNATING-BIT-PROTOCOL----------------")
        # Creating a socket 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Binding the socket pot and the host address
        server_address = (HOST, PORT)
        f=open(filename,"rb")
        complete = False

        # Here we are reading the data from the file in chunks whose size is defined as
        # a global variable. The data is then sent to a method make_packet() which creates
        # the packet by appending sequence number, data length, and a bit called finish bit 
        # that acknowledges the receiver if no more data is to be read. Once the packet is 
        # made the packet is then returned by the method. The packet is of the format:
        # <sequence_number>&&<data_length>&&<file_data>&&<finsih_bit>
        while not complete:
            data = f.read(sender_chunk_size)
            packet=make_packet(data,seqnum)
            l= packet.split('&&')
            seqnum=str(l[0])

            # Once the packet is received it is then sent to the method rdt_send() along 
            # with socket object and server address which is responsible for sending the 
            # packet. Once the packet is sent it returns the packet sent time.
            sent_time=rdt_send(packet,s,server_address)
            ack_received=None

            # Here we wait for the acknowledgements. The method wait_for_ACK is responsible
            # for receiving ACKS.
            ack_received=receive_ACK_alternatebit(s,sent_time)
            if not data:
                complete = True

            # If acknowledgement is not received within the packet timeout then the packet
            # along with the sequence number is again sent to the receiver.
            while ack_received==None:
                print("Did not receive ACK, resending data for sequence number: ",seqnum)
                send_time = rdt_send(packet, s, server_address)
                ack_received = receive_ACK_alternatebit(s, send_time)

            # If incorrect sequence number is received then the packet along with the 
            # sequence number is sent again.
            while ack_received.decode('utf-8') != seqnum:
                print("Received incorrect ACK, for sequence number: ",seqnum)
                print("Resending the data")
                send_time = rdt_send(packet, s, server_address)
                ack_received = receive_ACK_alternatebit(s, send_time)

            if ack_received.decode('utf-8') == seqnum and ack_received.decode('utf-8') == str(0):
                seqnum=str(1)
            if ack_received.decode('utf-8') == seqnum and ack_received.decode('utf-8') == str(1):
                seqnum=str(0)

    except Exception as e:
        log.info(e)


# This method is used to make the packet. The packet is of the format:
# <sequence_number>&&<data_length>&&<file_data>&&<finish_bit>
def make_packet(data,seq_num=0):
    try:
        msg=data.decode(encoding='UTF-8')
        msg=str(msg)
        msglen = str(len(msg))
        finish_bit = 1 if not data else 0
        header = str(seq_num) + '&&' + str(msglen)
        packet = header + '&&' + msg + '&&' + str(finish_bit)
        return(packet)

    except Exception as e:
        log.info(e)

# This method is used to send the packet. It returns the packet
# sent time.
def rdt_send(packet,s,server_address):
    try:
        newlist=packet.split('&&')
        print("SEQ NO. SENT:",newlist[0])
        message_bytes = str.encode(packet)
        s.sendto(message_bytes, server_address)
        msg_sent_time = int((time.time() * 1000))
        return (msg_sent_time)

    except Exception as e:
        log.info(e)

# This method is used to receive the acknowledgements. It maintains
# the timeout for each packet. If the acknowledgement is not 
# received then the packet is resent.
def receive_ACK_alternatebit(s,sent_time):
    try:
        current_time = int((time.time() * 1000))
        time_elapsed = current_time - sent_time
        while(time_elapsed<Timeout):
            s.setblocking(False)
            try:
                ACK=s.recv(2000)
                print("ACK received = ", ACK.decode('utf-8'))
                print("---------------------------------------------------")
                if ACK!=None:
                    return ACK
            except socket.error:
                pass
            current_time = int((time.time() * 1000))
            time_elapsed = current_time - sent_time
        return None

    except Exception as err:
        log.info(err)

# This is the method for rudp alternatebit or stop and wait receiver/server.
def rudp_alternatebit_receiver(PORT,filename):
    try:
        print("---------------RUDP--RECEIVER------ALTERNATING-BIT-PROTOCOL-------------")
        # Creating the UDP Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("UDP Socket created sucessfully")
        server_address = (HOST_IP, PORT)
        print("Starting the UDP server on:", server_address)
        print("------------------------------------------------------------------------")
        # Binding the socket with the port
        s.bind(server_address)
        # Opening the file
        f=open(filename,"w")
        store=[]
        # temp is the temporary variable that stores the value of the last sequence number
        # received. It is initially set to None but will be updated accordingly.
        temp=None
        while True:
            data,address = s.recvfrom(receiver_chunk_size)
            decoded_data = data.decode()
            store=decoded_data.split('&&')
            print("Received Sequence number:- ", store[0])
            seq=store[0]
            msg=store[2]
            ACK=store[0]
            finish_bit=store[3]

            # Here we check the value of the finish bit. If the finish bit is 1 then
            # it means it is the last packet received and end of file has been reached.
            # The control will break and the client will proceed to close the connection.
            if int(finish_bit) == 1:
                print("End of file sequence no. received")
                break
            # The received sequence number is checked with last sequence number received.
            # If it is different then it is in sequence otherwise we reject the packet
            # as it is duplicate.
            if store[0] == '0' and temp != store[0]:
                s.sendto(str.encode("0"), address)
                f.write(msg)
                print("Sent ACK: 0")
                print("---------------------------------------------------------------")
            elif store[0] == '0' and temp == store[0]:
                s.sendto(str.encode("0"), address)
                print("Duplicate packet received. Discard the packet and send ack")
                print("Sent ACK: 0")
                print("---------------------------------------------------------------")
            elif store[0] == '1' and temp != store[0]:
                s.sendto(str.encode("1"), address)
                f.write(msg)
                print("Sent ACK: 1")
                print("---------------------------------------------------------------")
            else:
                s.sendto(str.encode("1"), address)
                print("Duplicate packet received. Discard the packet and send ack")
                print("sending ACK-1 to client")
                print("---------------------------------------------------------------")
            temp=ACK
        
        k=0
        while k<25:
            s.sendto(str.encode(str(seq)), address)
            k+=1
        print("End of file ACK sent: ", str(seq))
        f.close()
        s.close()
        

    except Exception as e:
        log.info(e)

#--------------------------------------GO-BACK-N--------------------------------------
# Method for RUDP GO-BACK-N Protocol
def rudp_gobackn_sender(HOST, PORT,filename):
    global window_size
    global expectedrtt
    try:
        print("--------------------------RUDP SENDER-----GO-BACK-N-------------------")

        # Creating the UDP socket and binding the host and the port
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (HOST, PORT)
        seqnum = 0
        f = open(filename, "rb")
        complete = False

        # Here the window acts like a queue and the window size is defined at the top as 5
        # i.e. here we are reading the 1024 bytes of data from the file
        #  and then making the packet using make_packet() method.
        # Each made packet is then returned by the method and then appended to the window.
        # This will continue till the time the window is completely filled. The loop runs from
        # length of window to window size because if the window becomes empty then new packet will
        # be appended from the empty index.
        while len(window) > 0 or not complete:
            if not complete:
                for i in range(len(window), window_size):
                    data = f.read(sender_chunk_size)
                    packet = make_packet_gobackn(data, seqnum)
                    window.append(packet)
                    seqnum += 1
                    if not data:
                        complete = True
                        break

            # Once the window is completely filled we sent all the packets at once to the
            # receiver without waiting for the acknowledgement. This is implemented by
            # the rdt_send() method. We then store the oldest sent time.
            i = 0
            oldest_sent_time = 0
            while i < len(window):
                packet = window[i]
                sent_time = rdt_send_gobackn(packet, s, server_address)
                if (i == 0):
                    oldest_sent_time = sent_time
                i += 1

            # If the packet times out i.e. no acknowledgement is received within
            # the timeout specified then all the packets which are sent after the
            # unacknowledged packet are re-sent
            decoded_ack = None
            current_time = int((time.time() * 1000))
            time_elapsed = current_time - oldest_sent_time
            while time_elapsed < Timeout and len(window) > 0:
                s.setblocking(False)
                try:
                    ack, address = s.recvfrom(3000)
                    decoded_ack = ack.decode('utf-8')
                    print("ACK received: ", decoded_ack)
                    print("----------------------------------------------------")
                    decoded_ack = int(decoded_ack)
                except socket.error:
                    pass

                # When the ACK is received the ACK number is decoded and matched.
                # The ACK is a cumulative acknowledgement for all the packets sent
                # before it. So, all the packets pending from the queue or window
                # are then removed.
                if decoded_ack is not None:
                    for packet in window:
                        newlist = packet.split('&&')
                        acknum = int(newlist[0])
                        if acknum <= int(decoded_ack):
                            window.pop(0)
                        else:
                            break

                current_time = int((time.time() * 1000))
                time_elapsed = current_time - oldest_sent_time
    
            for key in senttimedict:
                if key in receivetimedict:
                    rttdict[key]=receivetimedict[key]-senttimedict[key]
                else:
                    pass
            # Here congestion control is implemented i.e. the window size
            # and the number of packets broadcasted will dynamically change 
            # with respect to the congestion in the channel. The rtt of 
            # each packet sent is calculated and the average rtt upto that
            # time is calulated. If the average rtt exceeeds the expected
            # rtt value then the window size is halved otherwise the 
            # window size is increased by one.
            if (len(rttdict)) !=0:
                avgrtt=sum(rttdict.values())/len(rttdict)
            else:
                avgrtt=0
            if avgrtt>expectedrtt+10:
                window_size=max(window_size//2,1)
            else:
                window_size=window_size+1
            expectedrtt=avgrtt
        time.sleep(5)


    except Exception as e:
        print(e)


# This method is used to make a packet. It receives the
# data from the file and the sequence number.
# The packet is of the format:
# <seqnum>&&<data length>&&<data>&&<finishbit>
# After the last data is read an empty packet with finish
# bit set to 1 is sent which tells the receiver that it
# can close the connection and exit.
def make_packet_gobackn(data, seq_num):
    try:
        finish_bit = 0
        msg = data.decode(encoding='UTF-8')
        msg = str(msg)
        msglen = str(len(msg))
        finish_bit = 1 if not data else 0
        header = str(seq_num) + '&&' + str(msglen)
        packet = header + '&&' + msg + '&&' + str(finish_bit)
        return (packet)

    except Exception as e:
        print(e)


# This method is used to send the packet to the receiver.
# It returns the message sent time.
def rdt_send_gobackn(packet, s, server_address):
    try:
        newlist = packet.split('&&')
        print("SEQ NO. SENT:", newlist[0])
        message_bytes = str.encode(packet)
        s.sendto(message_bytes, server_address)
        msg_sent_time = int((time.time() * 1000))
        return (msg_sent_time)

    except Exception as e:
        print(e)



# Method for RUDP Go-Back-N receiver
def rudp_gobackn_receiver(PORT,filename):
    try:
        print("---------------RUDP RECEIVER------------GO-BACK-N-----------------------")
        # Creating the RUDP Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("UDP Socket created sucessfully")
        server_address = (HOST_IP, PORT)
        print("Starting the RUDP server on:", server_address)
        print("-------------------------------------------------------------------------")
        # Binding the socket with the port
        s.bind(server_address)
        f=open(filename,"w")
        store = []
        last_seq = None
        i=0

        # Here in the while loop we receive the packet from the sender.
        # The packet which is of the form <seqnum>&&<msglen>&&<data>&&<finishbit>
        # when received is split into corresponding fields are decoded. Then the
        # sequence number of each packet is checked to see if packets arrive in
        # order and corresponding ACK is sent. If a dummy packet with finish bit
        # set to 1 is received then it means the file is completely read. An ACK
        # is sent and the client closes itself.
        while True:
            data, address = s.recvfrom(2000)
            decoded_data = data.decode()
            if decoded_data is not None:
                store = decoded_data.split('&&')
                seq = store[0]
                msg=store[2]
                finish_bit=store[3]
                if int(finish_bit)==1 and int(seq)==last_seq+1:
                    print("End of file sequence no. received")
                    break
                print("Sequence no. received:", seq)

                # Case 0: This case takes care of sequence number zero i.e.
                # the first packet. It initializes the value of previous_seq.
                if int(seq)==0:
                    ACK=seq
                    last_seq=int(seq)
                    s.sendto(str.encode(ACK), address)
                    print("ACK sent: ",ACK)
                    print("----------------------------------------------------------")
                    f.write(msg)

                # Case1: Here the received sequence number is matched and checked with the
                # last sequence number received to determine if the packet is in correct
                # sequence. If the packet is in correct sequence an ACK is sent to the
                # sender.
                elif last_seq is not None and int(seq)==last_seq+1:
                    ACK=seq
                    last_seq=int(seq)
                    s.sendto(str.encode(ACK), address)
                    print("ACK sent: ", ACK)
                    print("----------------------------------------------------------")
                    f.write(msg)

                # Case2: This case will only run if the last_seq is not set which means
                # the first packet with sequence number zero is not received.
                elif last_seq is None:
                    print("Out of order sequence number received, Discard message")
                    print("----------------------------------------------------------")

                # Case3: This will run when the first packet has arrived and last sequence
                # number is set however, the current packet received is out of sequence.
                else:
                    ACK=str(last_seq)
                    print("Out of order sequence number received, Discard message")
                    s.sendto(str.encode(ACK), address)
                    print("ACK sent: ", ACK)
                    print("----------------------------------------------------------")

            else:
                break
            i+=1
        k=0
        while k<25:
            s.sendto(str.encode(str(seq)), address)
            k+=1
        print("End of file ACK sent")
        time.sleep(5)

        f.close()
        s.close()
        exit(0)

    except Exception as e:
        print(e)

