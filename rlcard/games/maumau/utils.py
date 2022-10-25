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

WILD = ['H', 'S', 'D', 'C']

def cards2list(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of UnoCards objects

    Returns:
        (string): string representation of cards
    '''
    cards_list = []
    for card in cards:
        cards_list.append(card.get_str())
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
        plane (array): 3*4*15 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 3*4*15 numpy array
    '''
    # plane = np.zeros((3, 4, 15), dtype=int)
    plane[0] = np.ones((4, 15), dtype=int)
    hand = hand2dict(hand)
    for card, count in hand.items():
        if card.rank >= 13:
            if plane[1][0][card.rank] == 0:
                for index in range(4):
                    plane[0][index][card.rank] = 0
                    plane[1][index][card.rank] = 1
        else:
            plane[0][card.suit][card.rank] = 0
            plane[count][card.suit][card.rank] = 1
    return plane

def encode_target(plane, target):
    ''' Encode target and represerve it into plane

    Args:
        plane (array): 1*4*15 numpy array
        target(str): string of target card

    Returns:
        (array): 1*4*15 numpy array
    '''
    suit = target[0]
    rank = target[1]
    plane[suit][rank] = 1
    return plane
