from uuid import uuid4
from enum import Enum


class Participant:
    '''Base Participant Class'''
    is_player = False
    is_audience = False

    def __init__(self, name):
        self.uid = uuid4()
        self.name = name


class Player(Participant):
    '''Player Class'''
    is_player = True 


class Audience(Participant):
    '''Audience Class'''
    is_audience = True
