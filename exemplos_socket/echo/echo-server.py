import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

























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
