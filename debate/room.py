from uuid import uuid4
from time import time
from debate.chat import MsgChat
from debate.options import options
from debate._helper import LOGGER

class Room:
    '''Game Room'''

    uid = uuid4()
    participants = set()
    players = set()
    chat = MsgChat()
    subject_keyword = ""
    timestamp = time()  # EPOCH time since midnight 1970
    LEFT_SIDE = None
    RIGHT_SIDE = None

    def __len__(self):
        '''Return the amount of participants''' 
        return len(self.participants)

    def __str__(self):
        return f"Game Room #{self.uid}"

    @property
    def is_game_ready_to_start(self):
        '''Return True if game is ready to start''' 
        players_ready = self.RIGHT_SIDE and self.LEFT_SIDE  # True if we have two players
        have_audience = len(self.participants) > options.AUDIENCE_MIN # True if we have the requested amount of audience
        
        return players_ready and have_audience

    def player_in(self, player):
        '''Add player to the game'''
        if not self.LEFT_SIDE:
            self.LEFT_SIDE = player
        elif not self.RIGHT_SIDE:
            self.RIGHT_SIDE = player
        else:
            LOGGER.error(f"ERR: Player list filled at room {self.uid}")

    def player_out(self, player):
        '''Remove player from Room'''
        if player in self.RIGHT_SIDE:
            self.RIGHT_SIDE = None
        elif player in self.LEFT_SIDE:
            self.LEFT_SIDE = None

    def espectator_in(self, espectator):
        '''Add one participant to game room espectator'''
        if options.AUDIENCE_MAX:
            self.participants.add(espectator)

    def espectator_out(self, espectator):
        '''Remove an participant from the game room espectator'''
        try:
            self.participants.remove(espectator)
            self.chat.broadcast(f"Espectator {espectator} left the room.")
        except:
            LOGGER.error(f"ERR: Can't remove {espectator} from room {self.uid}")

    def close_room(self):
        '''Close room'''
        pass
