from uuid import uuid4
from enum import Enum


class Participant:
    '''Base Participant Class'''
    is_player = False
    is_audience = False
    in_matchmaking = True

    def __init__(self, name, connection):
        self.uid = uuid4()
        self.name = name
        self.connection = connection  # Receive a Socket object
