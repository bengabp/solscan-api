import logging
from colorlog import ColoredFormatter
import os
import motor.motor_asyncio
from beanie import init_beanie
from bunnet import init_bunnet
from pymongo import MongoClient
from pydantic import ConfigDict
from typing import List
from datetime import datetime
from starlette.config import Config


BASE_DIR = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])


def create_dir(name):
    fullpath = os.path.join(BASE_DIR, name)
    os.makedirs(fullpath, exist_ok=True)
    return fullpath

try:
    config = Config(".env")
except:
    config = Config()

logs_dir = create_dir("logs")

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

MONGODB_DB_NAME = "SolanaScan"

MONGODB_URI = config("MONGODB_URI")#,default= "mongodb://localhost:27017")
BROKER_URI = config("BROKER_URI")#, default="redis://127.0.0.1:6379/0")
DEXSCREENER_API_URI = config("DEXSCREENER_API_URI")#, default="http://localhost:3000")

dramatiq_logger = logging.getLogger("dramatiq")
file_handler = logging.FileHandler(
    filename=os.path.join(logs_dir,"drmatiq.log"),
    mode="a",
)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] [PID %(process)d] [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s'))
dramatiq_logger.addHandler(file_handler)

def current_utc_timestamp() -> int:
    return int(datetime.now().timestamp())

def to_camel_case(snake_str: str):
    components = snake_str.split("_")
    components = [components[0]] + [x.capitalize() for x in components[1:]]
    camel_case_str = "".join(components)
    return camel_case_str

simple_pydantic_model_config = ConfigDict(
    str_strip_whitespace=True,
    alias_generator=to_camel_case,
    populate_by_name=True,
    extra="ignore",
)

def init_db(models: List):
    client = MongoClient(MONGODB_URI)
    init_bunnet(database = client.get_default_database(MONGODB_DB_NAME), document_models = models)
