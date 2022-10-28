#!/usr/bin/env python3

import os
from torch import get_device
import rlcard
from rlcard.agents import (
  DQNAgent,
  RandomAgent,
)
from rlcard.utils import (
  get_device,
  set_seed,
  tournament
)

def load_model(model_path, env=None, position=None, device=None):
  if os.path.isfile(model_path):  # Torch model
    import torch
    agent = torch.load(model_path, map_location=device)
    agent.set_device(device)
  elif os.path.isdir(model_path):  # CFR model
    from rlcard.agents import CFRAgent
    agent = CFRAgent(env, model_path)
    agent.load()
  elif model_path == 'random':  # Random model
    from rlcard.agents import RandomAgent
    agent = RandomAgent(num_actions=env.num_actions)
  else:  # A model in the model zoo
    from rlcard import models
    agent = models.load(model_path).agents[position]

  return agent

device = get_device()
set_seed(42)
env = rlcard.make('maumau', config={'seed': 42})

files = [f for f in os.listdir("./") if f.endswith(".pth")]
files.append("random")
for o in files:
  for i in files:
    print("Playing: ", o, " vs. ", i)

    env.set_agents([load_model(o, env, 0, device), load_model(i, env, 1, device)])

    rewards = tournament(env, 5000)
    for position, reward in enumerate(rewards):
      print(position, reward)
