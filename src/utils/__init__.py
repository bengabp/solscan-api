import os
from src.config import BASE_DIR
import random


with open(os.path.join(BASE_DIR, "datasets/user_agents.txt")) as ua_file:
    agents = [agn.strip() for agn in ua_file.readlines()]

def get_random_ua():
    choice = random.choice(agents)
    return choice
