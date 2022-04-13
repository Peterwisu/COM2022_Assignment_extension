'''
This is COM2020 Computer Networking coursework assignment in years two second semster at University of Surrey 2022 

Author: Wish Suharitdamrong 

This is a client UDP file  

'''


#######################################################################################################################

"""
    IMPORT ALL IMPORTANT LIBRARIES
"""
import cv2, imutils, socket
import numpy as np
import time
import base64
import threading
import time
# buff size
BUFF_SIZE = 65536


# Empty list to contain all round trip time
RTT_list = np.array([])

'''
    Create UDP socket
'''
def create_udp_socket():
    # Declare global variable for socket
    global client_socket
    global host_name
    global host_ip
    global port 

    
    # try create socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        host_name = socket.gethostname()
        host_ip =  input('Enter Host IP') # socket.gethostbyname(host_name)
        port =       int(input('Port number'))   #9998
        # Set timeout
        client_socket.settimeout(3)
        print('Host ip: - ',host_ip)

    except socket.error as msg :

        print(f'Create Socket error {msg}')



'''
    Calculate RTT time
'''
def get_rtt():
    if len(RTT_list):
        avg = np.average(RTT_list)
        max = np.max(RTT_list)
        min = np.min(RTT_list)
    else:
        avg = None
        max = None
        min = None
    return avg , max , min



'''
    Receive broadcast from server
'''
def receive_broadcast(server):
    
    print('Start broadcast from server')
    
    try:
        
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        while True:
            # record a time before send data to server
            initial_time = time.time()
            client_socket.sendto(b'RTT::',(host_ip, port))
            # receive a packet containing data for vdo streaming
            packet, server_add = client_socket.recvfrom(BUFF_SIZE)
            # record a time after data to server
            ending_time  = time.time()
            # calculate a round trip time 
            delay_time = ending_time - initial_time
            # global variable
            global RTT_list 
            # append a rtt to a RTT_list
            RTT_list= np.append(RTT_list,delay_time)


            # unpack packet from datagram and decode it
            data = base64.b64decode(packet,b' /')
            # recovery the image data and store in numpy array
            npdata = np.fromstring(data, dtype=np.uint8)
            # decode streaming data into image
            frame = cv2.imdecode(npdata, 1)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("RECEIVING VIDEO from Server (q:quit)", frame)
            key = cv2.waitKey(1) & 0xFF
            # if client click q exit the streaming
            if key == ord('q'):
                # send message quit to server to let server know client have disconnect
                msg =b'QUIT::'
                client_socket.sendto(msg,server)
                print('Disconnected to server')
                # close socket
                client_socket.close()
                break
            # calculate frame rate
            if cnt == frames_to_count:
                    try:
                        fps = round(frames_to_count/(time.time()-st))
                        st=time.time()
                        cnt=0
                    except:
                        pass
            cnt+=1
    
    # exception for timeout waiting to receive packet from server
    except socket.timeout as err:
        print(f'Connection {err}to Server while receiving broadcast ')
        client_socket.close()
    # exception socket error
    except socket.error as err:
        print(f'Connection {err}to Server while receiving broadcast ')
        client_socket.close()
    



'''
    Requestion connection from server
'''
def request_connection():
    
    # let clietn input theirs username
    name =  input('input your name : type quit to exit\n')
    # let client input theirs password
    password = input('input your password: type quit to exit\n')
    # put username and passwor in format
    message = 'LOGIN::'+name+'::'+password
    # convert message into bytes
    message = bytes(message,'ascii')
    

  
    try:
            # send username to a server        
            client_socket.sendto(message, (host_ip, port))
            print('Yourname: ',str(message.decode('ascii')))
            print('Requeting broadcast from server')
            # receive respond from server
            packet, server_add =client_socket.recvfrom(BUFF_SIZE)
            # unpack packet
            packet = packet.decode()
            # Check if the message from packet is authorize or unauthorize
            if(packet == 'UNAUTHORIZE:'):

                print("Your username is not authorize or password is wrong please try again")

            elif(packet == 'AUTHORIZE:'):
                # if authorize  start receiveing broadcast    
                print('Login authorize')
                # call receive broadcast to receive video streaming form server
                receive_broadcast((host_ip, port))

     # exception for timeout waiting to receive packet from server       
    except socket.timeout as er:

            print(f"Connection Timeout to  Server :{er}")
            client_socket.close()
     # exception socket error
    except socket.error as er:
            print(f"Connection error to  Server :{er}")
            client_socket.close()



def start():
    create_udp_socket()
    request_connection()
    # call function get_rtt to ge average ,maximum and minimum rtt time occur while reciving broadcast
    Avg , Max , Min = get_rtt()
    print(f'RTT average : {Avg} , RTT max : {Max} , RTT min : {Min}')


    
start()






