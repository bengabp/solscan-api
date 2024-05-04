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

config = Config(".env")

logs_dir = create_dir("logs")

MONGODB_DB_NAME = "SolanaScan"
MONGODB_URI = config("MONGODB_URI")#,default= "mongodb://localhost:27017")
BROKER_URI = config("BROKER_URI")#, default="redis://127.0.0.1:6379/0")
DEXSCREENER_API_URI = config("DEXSCREENER_API_URI")#, default="http://localhost:3000")
SENTRY_ENABLED = config("SENTRY_ENABLED", cast=bool, default=False)
DEBUG = config("DEBUG", cast=bool, default=False)
ENVIRONMENT = "development" if DEBUG else "production"
SENTRY_DSN = config("SENTRY_DSN")

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
