import socket
import time
def create_socket():
    s = socket.socket()       
    print ("Socket successfully created") 
    port = 12345                
    s.bind(('', port))          
    s.listen(1)   
    print ("socket is listening")
    # Establish connection with client.  
    c, addr = s.accept()      
    print ('Got connection from', addr ) 
    return s , c
 
def close_connection(connection):
    connection.close()

def send_data(connection,data):
    connection.send(bytes(data,'utf-8'))

def receive_data(connection):
    return connection.recv(1024)
 
def swapPositions(list, pos1, pos2): 
      
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def get_data():
    data=input('Enter your Data : ')
    if(data == 'exit'):
        return data
    data_list=list()
    y=0
    for i in range(len(data)):
        if len(data)-y-4 > 0:
            data_list.append((str(i+1),data[y:y+4]))
            y+=4
        elif len(data)-y-4 == 0:
            data_list.append((str(i+1),data[y:]))
            break
        else :
            data_list.append((str(i+1),data[y:]))
            break
    return data_list
###############main###########
data_sent=list()     #store frames that have been sent
data_notsent=list()  #store frames that have not been sent
sock,conn=create_socket()    #create socket
data=get_data()              #divide data into frames each frame has 4 bytes
print('There are ' + str(len(data)) + 'Frames')
retrans_flag=0               #check if there is retransmission for data
error_flag=0                 #check if there is an error
counter=0
while(1):
    if (error_flag) and (retrans_flag) and counter == 3 :
        time.sleep(1)
        print('Timeout')
        for i in data_notsent:
            send_data(conn,i[0]+':'+i[1])
            time.sleep(1)
            print('Re-Sending :'+ i[0] + ' ' + i[1])
            time.sleep(1)
            recv_data=(receive_data(conn).decode('utf-8'))
            print(recv_data)
        error_flag=0
        retrans_flag=0
        counter=0
        data=[i for i in data if i not in data_notsent]  #remove data that has been sent
        data_notsent.clear()
    for i in data:
        if (counter == 3):
            break
        print('Sending :'+ i[0] + ' ' + i[1])
        if(i[0]=='3') :
            send_data(conn,'0none')
        else :
            send_data(conn,i[0]+':'+i[1])
        recv_data=(receive_data(conn).decode('utf-8'))
        if recv_data != 'discarded' and recv_data != 'error':    #check if data was sent successfully or not
            data_sent.append(i)       # store data that has been sent successfully to datasent
        elif recv_data == 'discarded' or recv_data == 'error':
            data_notsent.append(i)
            error_flag=1
            retrans_flag=1
            counter+=1
            if(recv_data == 'error'):
                continue
        time.sleep(1)                                               
        print(recv_data)
    data=[i for i in data if i not in data_sent]  #remove data that has been sent
    data_sent.clear()    #clear all data that 
    if not data:
        break

close_connection(conn)


