import random
import socket
import time
import os
from _thread import *
import sys


ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = int(sys.argv[1])
SEED = int(sys.argv[2])
random.seed(SEED)

ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

# print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    global ThreadCount
        
    data=connection.recv(2048).decode('utf-8')
    randomNumber = random.randint(0, 14)
    if data=="0":
        #open the file and randomly choose the word, based on the length words, send message
        file = open("hangman_words.txt")
        # read the content of the file opened
        content = file.readlines()
        # read 10th line from the file
        word = content[randomNumber]
        word_length = len(word)-1
        word_print = word[0]
        for x in range(1, word_length):
            word_print = word_print + ' ' + word[x]
         
        word_been_guessed = '_'
        for x in range(word_length-1):
            word_been_guessed += ' _'
    else:
        # connection.close()
        ThreadCount -= 1
        return    
    
    guess_wrong_count=0
    first_wrong_guess_token=0
    incorrect_guess="Incorrect Guesses: "
    message=">>>"+word_been_guessed+"\n>>>"+incorrect_guess+"\n>>>"
    connection.send(str.encode(message))
    while guess_wrong_count<6:
        data = connection.recv(2048).decode('utf-8')
        
        guess_token=0
        
        for x in range(word_length):
            if word[x]==data:
                word_been_guessed=word_been_guessed[:2*x]+data+word_been_guessed[2*x+1:]
                guess_token=1
        
        if guess_token==0 and first_wrong_guess_token==0:
            incorrect_guess=incorrect_guess+data
            first_wrong_guess_token=1
            guess_wrong_count+=1
        else:
            if guess_token==0:
                incorrect_guess=incorrect_guess+" "+data
                guess_wrong_count+=1
            
        
        gameover_token=0
        
        for x in range(2*word_length-1):
            if word_been_guessed[x]=="_":
                gameover_token=1

        if gameover_token==0:
            message=">>>The word was "+word+">>>You Win!"+"\n"+">>>Game Over!"
            connection.send(str.encode(message))
            break
        else:
            message=">>>"+word_been_guessed+"\n>>>"+incorrect_guess+"\n>>>"
            

            if guess_wrong_count==6:
                message=">>>The word was "+word+">>>You Lose."+"\n"+">>>Game Over!"
                connection.send(str.encode(message))
            else:
                connection.send(str.encode(message))

    # connection.close()
    time.sleep(2)
    ThreadCount -= 1

while True:

    Client, address = ServerSocket.accept()
    
    if ThreadCount==3:
        message=">>>server-overloaded"
        Client.send(str.encode(message))
        # Client.close()
    else:
        message="Able to connect"
        Client.send(str.encode(message))
        time.sleep(0.1)
        ThreadCount +=1
        start_new_thread(threaded_client, (Client, ))        