from debate._helper import LOGGER, socket_command
from debate.participants import Participant


class CommandMiddleware:
    '''Middleware Common Command Class'''

    def __init__(self):
        self.participants = set() # Dummy declaration to stop acusing self.participant of undefined
        self.command_dict = {
            '/join': self.new_participant,
            '/quit': self.remove_participant
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
        '''Add new participant to server'''

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
        '''Remove a participant from server'''
        try:
            f = [x for x in self.participants if x.connection == kwargs['connection']]
            if len(f) > 0:
                self.participants.remove(f[0])
                kwargs['connection'].close()

        except Exception as e:
            LOGGER.error(f"ERR: Can't remove client: {str(e)}")
