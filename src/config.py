import logging
from colorlog import ColoredFormatter
import os
import motor.motor_asyncio
from beanie import init_beanie
from bunnet import init_bunnet
from pymongo import MongoClient
from pydantic import ConfigDict
from typing import List

BASE_DIR = "C:/Users/bengabp/Documents/IT/UKTeam/SolanaScan"


def create_dir(name):
    fullpath = os.path.join(BASE_DIR, name)
    os.makedirs(fullpath, exist_ok=True)
    return fullpath


HEADERS = {
    "authority": "planning.adur-worthing.gov.uk",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}

MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DB_NAME = "SolanaScan"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = ColoredFormatter(
    "SolanaScan -> %(log_color)s%(asctime)s%(reset)s - %(process)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
    datefmt="%B %d, %Y : %I:%M:%S%p",
    log_colors={
        "DEBUG": "green",
        "INFO": "blue",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

# Create a console handler
console_handler = logging.StreamHandler()

# Set the formatter for the console handler
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def to_camel_case(snake_str: str):
    """
    Converts a string in snake case to camel case
    :param snake_str: A string in snake case
    :return: A string in camel case"""

    components = snake_str.split("_")
    components = [components[0]] + [x.capitalize() for x in components[1:]]
    camel_case_str = "".join(components)
    return camel_case_str


simple_pydantic_model_config = ConfigDict(
    str_strip_whitespace=True,
    # alias_generator=to_camel_case,
    populate_by_name=True,
    extra="allow",
)


def init_db(models: List):
    """
    Initializes the database connection using async motor driver
    :param models: A list of models to add
    """
    
    # client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
    # await init_beanie(
    #     database=client.get_default_database(MONGODB_DB_NAME), document_models=models
    # )
    
    client = MongoClient(MONGODB_URI)
    init_bunnet(database = client.get_default_database(MONGODB_DB_NAME), document_models = models)
    