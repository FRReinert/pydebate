from debate.participants import Participant
from debate._helper import async_function, LOGGER, socket_command
import socket


class Server:
    '''Matchmaking class'''
    
    room_list = set()
    participants = set()

    def __init__(self, title="Debate Game Server", desc="Vanilla Server", ip='127.0.0.1', port=1313):
        self.host_title = title
        self.host_desc = desc
        self.host_ip = ip
        self.host_port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_ip, self.host_port))
        self.server.listen()
        LOGGER.info(f">>INF: Server listening")

    @async_function
    def handle_connection(self, connection, address):
        '''Handle new participant connection'''
        buffer = 1024
        connection.sendall(f"You're connected to server {self.host_title}".encode())
        while True:
            try:
                data = connection.recv(buffer)

                # Close connection if client hard quit
                if not data:    
                    LOGGER.info(f'Hard Disconected: {str(address[0])} : {str(address[1])}')
                    connection.close()
                    break

                # TODO: implement command receiver
                else:
                    self.handle_command(command=data, connection=connection)

            except Exception as e:
                LOGGER.error(f'ERR: Error handling connection: {str(e)}')
                break

        return None

    def main_loop(self):
        '''Main server loop. Listen for new connections'''
        while True:
            client, addr = self.server.accept()
            self.handle_connection(client, addr)

    @socket_command
    def new_participand(self, command, connection):
        '''Add new participant to server'''
        try:
            name = command.decode().split('JOIN')[1]
        except:
            connection.sendall('Need a valid name')
            return

        p = Participant(name=name, connection=connection)
        self.participants.add(p)

    @socket_command
    def remove_participant(self, command, connection):
        '''Remove a participant from server'''
        try:
            f = [x for x in self.participants if x.connection == connection]
            if len(f) > 0:
                self.participants.remove(f[0])
                connection.close()

        except Exception as e:
            LOGGER.error(f"ERR: Cant remove client: {str(e)}")

    def handle_command(self, *args, **kwargs):
        '''Handle commands received over socket'''
        
        # No command handler
        if not kwargs['command']:
            return
        
        # ^Q handler
        elif kwargs['command'] == b'\x11':
            self.remove_participant(*args, **kwargs)
        
        elif b'JOIN' in kwargs['command']:
            self.new_participand(*args, **kwargs)

        # Unrecognized command
        else:
            print(kwargs['command'])

