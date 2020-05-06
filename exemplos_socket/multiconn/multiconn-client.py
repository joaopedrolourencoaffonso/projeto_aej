import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

def start_connections(host, port, num_conns):
    server_addr = (host, port)

    for i in range(0, num_conns):
        connid = i + 1
        print("starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(

            connid=connid,

            msg_total=sum(len(m) for m in messages),

            recv_total=0,

            messages=list(messages),

            outb=b"",

        )

        sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print("received", repr(recv_data), "from connection", data.connid)
            data.recv_total += len(recv_data)

        if not recv_data or data.recv_total == data.msg_total:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:

        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)

        if data.outb:
            print("sending", repr(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]





if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)


host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns))



try:
    while True:
        events = sel.select(timeout=1)

        if events:
            for key, mask in events:
                service_connection(key, mask)

        # Check for a socket being monitored to continue.

        if not sel.get_map():
            break

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
