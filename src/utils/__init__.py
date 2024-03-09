import os
from src.config import BASE_DIR
import random
from datetime import datetime


with open(os.path.join(BASE_DIR, "datasets/user_agents.txt")) as ua_file:
    agents = [agn.strip() for agn in ua_file.readlines()]

def get_random_ua():
    choice = random.choice(agents)
    return choice

def calculate_duration(start_time):
    start_datetime = datetime.utcfromtimestamp(start_time)
    current_datetime = datetime.utcnow()
    duration_seconds = (current_datetime - start_datetime).total_seconds()
    return duration_seconds