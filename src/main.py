import os
import sys
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from loguru import logger
from fastapi import FastAPI, Request, Response, status, Path
from pydantic import BaseModel, Field
from src.config import (init_db,
                        simple_pydantic_model_config,
                        ENVIRONMENT, SENTRY_ENABLED, BASE_DIR, SENTRY_DSN
                        )

# Add src package to PYTHONPATH
sys.path.append(os.path.join(BASE_DIR, "src"))

from src.models import Task, Wallet
from src.tasks import new_task as add_new_task


api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class TrackWalletRequest(BaseModel):
    model_config = simple_pydantic_model_config

    wallet_id: str = Field()


@api.on_event("startup")
def on_start():
    """ Fastapi startup event, configure logging, database and sentry """

    logger.add(os.path.join(BASE_DIR, "logs/api.log"), encoding="utf-8", rotation="10 MB", retention="10 days", enqueue=True)

    if SENTRY_ENABLED:
        logger.info("SENTRY IS ACTIVE ✅")
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=ENVIRONMENT,
            traces_sample_rate=1.0,
        )
    # Configure logging

    init_db([Task, Wallet])
    logger.info("APP STARTUP COMPLETED ✅")


@api.post("/track")
def track_new_wallet(request: Request, response: Response, create_request: TrackWalletRequest):
    wallet = Wallet.find(Wallet.wallet_id == create_request.wallet_id).first_or_none()
    new_task = Task(
        wallet_id=create_request.wallet_id,
    )

    # if wallet exists, then update wallet, else create wallet
    if wallet:
        new_task.is_update_task = True
        wallet.status = new_task.status
        wallet.save_changes()
    else:
        new_task.is_update_task = False
        wallet = Wallet(
            wallet_id=new_task.wallet_id,
            status=new_task.status
        )
        wallet.create()

    new_task.create()
    r = add_new_task.send(str(new_task.id))

    response.status_code = status.HTTP_201_CREATED
    return wallet


@api.get("/wallets/{wallet_id}")
def get_wallet(request: Request, response: Response, wallet_id: str = Path()):
    wallet = Wallet.find(Wallet.wallet_id == wallet_id).first_or_none()
    if wallet:
        response.status_code == status.HTTP_200_OK
    else:
        response.status_code == status.HTTP_404_NOT_FOUND
    return wallet


@api.get("/wallets")
def get_all_wallets(request: Request, response: Response):
    wallets = Wallet.find().to_list()

    return wallets
