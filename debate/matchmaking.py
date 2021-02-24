from debate.options import OptionSingleton
from debate.participants import Participant
from debate._helper import async_function, LOGGER, check_carriage_return
import socket


class Server:
    '''Matchmaking class'''
    
    options = OptionSingleton
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
                if not data:    
                    LOGGER.info(f'Hard Disconected: {str(address[0])} : {str(address[1])}')
                    connection.close()
                    break
                elif data == b'\x11':
                    LOGGER.info(f'Gracefully Disconected: {str(address[0])} : {str(address[1])}')
                    connection.close()
                    break
                else:
                    print(data)
            except Exception as e:
                LOGGER.error(f'ERR: Error handling connection: {str(e)}')
                break
        return None

    def main_loop(self):
        '''Main server loop. Listen for new connections'''
        while True:
            client, addr = self.server.accept()
            self.handle_connection(client, addr)


    def new_participand(self, participant):
        '''Add new participant to server'''
        self.participants.add(participant)

    def remove_participant(self, participant):
        '''Remove a participant from server'''
        try:
            self.participants.remove(participant)
        except:
            LOGGER.error(f"Cant remove {participant} from matchmaking")
