import socket
import time             
def create_socket():
    s = socket.socket()       
    port = 12345
    s.connect(('', port))                
    return s

def send_data(s,data):
    s.send(bytes(data,'utf-8'))

def receive_data(s):
    return s.recv(1024)

def close_connection(s):
    s.close()

expected_frame=1
############main###############
sock=create_socket()
flag_error=0
count=0
while(1):
        recev_data=receive_data(sock).decode('utf-8')
        if (recev_data == ''):
            break
        if(flag_error==1) and expected_frame!=int(recev_data.split(':')[0]) :
            send_data(sock,'discarded')
        elif(expected_frame==int(recev_data.split(':')[0])):
            time.sleep(1)
            print('Received ' + recev_data.split(':')[0] + ' successfully')
            send_data(sock,'acknowledge ' + recev_data.split(':')[0])
            expected_frame+=1
            flag_error=0
        else:
            time.sleep(1)
            print('error')
            send_data(sock,'error')
            flag_error=1
    

              
  
  
  
