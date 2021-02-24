from debate._helper import async_function, LOGGER
from debate.commands import CommandMiddleware
from debate.options import options
from ssl import wrap_socket, PROTOCOL_TLSv1_2
import socket


class Server(CommandMiddleware):
    '''Matchmaking class'''

    def __init__(self, title="Debate Game Server", desc="Vanilla Server", ip='127.0.0.1', port=1313):
        self.host_title = title
        self.host_desc = desc
        self.host_ip = ip
        self.host_port = port
        
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = wrap_socket(sk, ssl_version=PROTOCOL_TLSv1_2, certfile=options.CERTFILE, keyfile=options.KEYFILE)
        self.server.bind((self.host_ip, self.host_port))
        self.server.listen()
        LOGGER.info(f">>INF: Server listening")

    @async_function
    def handle_connection(self, connection, address):
        '''Handle new participant connection'''
        buffer = 1024
        connection.sendall(f">> You're connected to server {self.host_title}!\r\n".encode())
        
        while True:
            try:
                data = connection.recv(buffer)

                # Close connection if client hard quit
                if not data:    
                    LOGGER.info(f'Hard Disconected: {str(address[0])} : {str(address[1])}')
                    connection.close()
                    break

                else:
                    self.command_handler(command=data, connection=connection)

            except Exception as e:
                LOGGER.error(f'ERR: Error handling connection: {str(e)}')

        return None

    def main_loop(self):
        '''Main server loop. Listen for new connections'''
        while True:
            client, addr = self.server.accept()
            self.handle_connection(client, addr)

