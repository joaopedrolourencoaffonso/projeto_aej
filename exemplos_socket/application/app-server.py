import sys
import socket
import selectors
import traceback
import libserver



sel = selectors.DefaultSelector()

def accept_wrapper(sock):

    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)



host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(

                        "main: error: exception for",

                        f"{message.addr}:\n{traceback.format_exc()}",

                    )

                    message.close()

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()





















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
