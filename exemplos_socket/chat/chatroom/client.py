import socket, select, errno,  sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 45000

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode("utf-8"))
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue
        
    except Exception as e:
        print('General error', str(e))
        sys.exit()






















#import socket, random

#def main():

 #   string1 = "Olá Lua"
 #   string2 = "Olá Sol"
 #   string3 = "Olá Mercúrio"
    
 #   z = random.randint(1,3)

 #   if z == 1:
 #       print(string1)
 #   if z == 2:
 #       print(string2)
 #   if z == 3:
 #       print(string3)
    
    
#if __name__ == '__main__':
#    main()

    
#exemplo de entry point





























#import PySimpleGUI as sg

## layout the Window
#layout = [[sg.Text('A custom progress meter')],
#          [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
#          [sg.Cancel()]]

## create the Window
#window = sg.Window('Custom Progress Meter', layout)
## loop that would normally do something useful
#for i in range(1000):
#    # check to see if the cancel button was clicked and exit loop if clicked
#    event, values = window.read(timeout=0)
#    if event == 'Cancel' or event is None:
#        break
#        # update bar with loop value +1 so that bar eventually reaches the maximum
#    window['progbar'].update_bar(i + 1)
## done with loop... need to destroy the window as it's still open
#window.close()
