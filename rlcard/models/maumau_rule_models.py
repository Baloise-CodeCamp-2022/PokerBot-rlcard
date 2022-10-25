''' MauMau rule models
'''

import numpy as np

import rlcard
from rlcard.models.model import Model

class MauMauRuleAgentV1(object):
    ''' MauMau Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    def step(self, state):
        ''' Predict the action given raw state. A naive rule. Choose the color
            that appears least in the hand from legal actions. Try to keep wild
            cards as long as it can.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''

        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        if 'draw' in legal_actions:
            return 'draw'

        hand = state['hand']

        # we randomly choose one
        action = np.random.choice(self.filter_wild(legal_actions))
        return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

    @staticmethod
    def filter_wild(hand):
        ''' Filter the wild cards. If all are wild cards, we do not filter

        Args:
            hand (list): A list of MauMau card string

        Returns:
            filtered_hand (list): A filtered list of MauMau string
        '''
        filtered_hand = []
        for card in hand:
            if not card[1] == 'J':
                filtered_hand.append(card)

        if len(filtered_hand) == 0:
            filtered_hand = hand

        return filtered_hand

    @staticmethod
    def count_colors(hand):
        ''' Count the number of cards in each color in hand

        Args:
            hand (list): A list of MauMau card string

        Returns:
            color_nums (dict): The number cards of each color
        '''
        color_nums = {}
        for card in hand:
            color = card[0]
            if color not in color_nums:
                color_nums[color] = 0
            color_nums[color] += 1

        return color_nums

class MauMauRuleModelV1(Model):
    ''' MauMau Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('maumau')

        rule_agent = MauMauRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate wether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True



