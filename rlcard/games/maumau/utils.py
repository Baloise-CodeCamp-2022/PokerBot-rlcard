import os
import json
import numpy as np
from collections import OrderedDict

import rlcard
from rlcard.games.base import Card

# Read required docs
ROOT_PATH = rlcard.__path__[0]

# a map of abstract action to its index and a list of abstract action
with open(os.path.join(ROOT_PATH, 'games/maumau/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())

WILD = ['HJ', 'SJ', 'DJ', 'CJ']

# a map of color to its index
SUIT_MAP = {'S': 0, 'C': 1, 'H': 2, 'D': 3}

# a map of trait to its index
RANK_MAP = {'7': 0, '8': 1, '9': 2, 'T': 3, 'J': 4, 'Q': 5,
             'K': 6, 'A': 7}

def cards2list(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of UnoCards objects

    Returns:
        (string): string representation of cards
    '''
    cards_list = []
    for card in cards:
        cards_list.append(card.get_index())
    return cards_list

def hand2dict(hand):
    ''' Get the corresponding dict representation of hand

    Args:
        hand (list): list of string of hand's card

    Returns:
        (dict): dict of hand
    '''
    hand_dict = {}
    for card in hand:
        if card not in hand_dict:
            hand_dict[card] = 1
        else:
            hand_dict[card] += 1
    return hand_dict

def encode_hand(plane, hand):
    ''' Encode hand and represerve it into plane

    Args:
        plane (array): 4*8 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 4*8 numpy array
    '''
    plane[0] = np.ones((4, 8), dtype=int)
    hand = hand2dict(hand)
    for card, count in hand.items():
        suit = SUIT_MAP[card[0]]
        rank = RANK_MAP[card[1]]
        if rank == 'J':
            if plane[1][0][rank] == 0:
                for index in range(4):
                    plane[0][index][rank] = 0
                    plane[1][index][rank] = 1
        else:
            plane[0][suit][rank] = 0
            plane[count][suit][rank] = 1
    return plane

def encode_target(plane, target):
    ''' Encode target and represerve it into plane

    Args:
        plane (array): 1*4*15 numpy array
        target(str): string of target card

    Returns:
        (array): 1*4*15 numpy array
    '''
    suit = SUIT_MAP[target[0]]
    rank = RANK_MAP[target[1]]
    plane[suit][rank] = 1
    return plane
