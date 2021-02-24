from debate._helper import LOGGER, socket_command
from debate.participants import Participant


class CommandMiddleware:
    '''Middleware Common Command Class'''

    def __init__(self):
        self.participants = set()
        self.command_dict = {
            '/help': self.list_commands,
            '/connect': self.new_participant,
            '/quit': self.remove_participant,
            '/broadcast': self.broadcast_msg,
            '/msg': self.send_msg, 
            '/nick': self.change_nickname,
            '/list': self.list_rooms,
            '/join':self.join_room
        }

    def command_handler(self, *args, **kwargs):
        '''Handle commands received over socket'''
        
        command = kwargs['command'].decode("utf8", "ignore").split()
       
        # Verify command health
        if len(command) < 1 or not command[0].startswith('/'):
            kwargs['connection'].sendall(f'>> This is not a command: {command[0]}\r\n'.encode())
            return

        # Execute command
        try:
            func = self.command_dict[command[0]]
            args = command[1:]
            func(*args, connection=kwargs['connection'])
        except:
            kwargs['connection'].sendall(f'>> Invalid command: {command}\r\n'.encode())

    @socket_command
    def new_participant(self, *args, **kwargs):
        '''Join Server: /connect'''

        # Verify if its already connected
        f = [x for x in self.participants if x.connection == kwargs['connection']]
        if len(f) > 0:
            kwargs['connection'].sendall(b'>> Already connected\r\n')
            return
        
        # Add participant to the list 
        try:
            p = Participant(name=' '.join(args), connection=kwargs['connection'])
            self.participants.add(p)
        except:
            kwargs['connection'].sendall(b'>> Need a valid name\r\n')
        return

    @socket_command
    def remove_participant(self, *args, **kwargs):
        '''Quit Server: /quit'''
        try:
            f = [x for x in self.participants if x.connection == kwargs['connection']]
            if len(f) > 0:
                self.participants.remove(f[0])
                kwargs['connection'].close()

        except Exception as e:
            LOGGER.error(f"ERR: Can't remove client: {str(e)}")

    @socket_command
    def list_commands(self, *args, **kwargs):
        '''List commands: /help'''
        result = []
        for key, value in self.command_dict.items():
            result.append((key, value.__doc__))

        kwargs['connection'].sendall(str(result).decode())

    @socket_command
    def broadcast_msg(self, *args, **kwargs):
        '''Brodcast message: /broadcast <Message>'''
        pass

    @socket_command
    def change_nickname(self, *args, **kwargs):
        '''Brodcast message: /nick <Message>'''
        pass

    @socket_command
    def list_rooms(self, *args, **kwargs):
        '''List Rooms: /list'''
        pass

    @socket_command
    def join_room(self, *args, **kwargs):
        '''Join room: /join <room_uuid>'''
        pass

    @socket_command
    def send_msg(self, *args, **kwargs):
        '''Send message: /msg <-r Room> <-p Participant>'''
        pass