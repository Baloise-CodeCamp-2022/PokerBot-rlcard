''' A toy example of playing against rule-based bot on UNO
'''

import rlcard
from rlcard import models
from rlcard.utils.utils import print_card
from rlcard.agents.human_agents.maumau_human_agent import HumanAgent
import torch

# Make environment
env = rlcard.make('maumau')
human_agent = HumanAgent(env.num_actions)
#cfr_agent = models.load('maumau-rule-v1').agents[0]
agent = torch.load('/home/markus/Code/PokerBot/PokerBot-rlcard/examples/tournament/dqn_vs_dmc.pth', map_location=None)
env.set_agents([
    human_agent,
    agent,
])

print(">> MauMau rule model V1")

while (True):
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action
    final_state = trajectories[0][-1]
    action_record = final_state['action_record']
    state = final_state['raw_obs']
    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses ', end='')
        print('')
        print('')
        print_card(pair[1])
        print('')

    print('===============     Result     ===============')
    if payoffs[0] > 0:
        print('You win!')
    else:
        print('You lose!')
    print('')
    input("Press any key to continue...")
