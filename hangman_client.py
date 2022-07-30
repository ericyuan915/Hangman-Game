import socket
import sys

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = sys.argv[1]
port = int(sys.argv[2])

# print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024).decode('utf-8')
if Response==">>>server-overloaded":
    # ClientSocket.close()
    print(Response)
else:
    while True:
        Input = input('>>>Ready to start game? (y/n): ')      
        if  Input == 'y':            
            ClientSocket.send(str.encode("0"))
        else:
            break
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
        while True:
            while True:
                try:
                    guess_letter=input('>>>Letter to guess: ')
                except EOFError:
                    exit()
                if (guess_letter.isnumeric()) or (len(guess_letter) > 1):
                    print('>>>Error! Please guess one letter.')
                else:
                    break
            guess_letter=guess_letter.lower()
            ClientSocket.send(str.encode(guess_letter))
            Response = ClientSocket.recv(1024).decode('utf-8')
            print(Response)       
            if Response[-1]=="!":
                break

        break
    # ClientSocket.close()
