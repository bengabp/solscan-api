from fastapi import FastAPI, Request, Response, status, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Optional
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from src.models import Task, Wallet
from src.config import init_db, simple_pydantic_model_config, current_utc_timestamp
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError
from src.tasks import new_task as add_new_task
from fastapi.middleware.cors import CORSMiddleware
from dramatiq_abort import abort as abort_task

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
    init_db([Task, Wallet])


@api.post("/track")
def track_new_wallet(request: Request,  response: Response, create_request: TrackWalletRequest):
    wallet = Wallet.find(Wallet.wallet_id == create_request.wallet_id).first_or_none()
    new_task = Task(
        wallet_id = create_request.wallet_id,
    )
    
    # if wallet exists, then update wallet, else create wallet
    if wallet:
        new_task.is_update_task = True
        wallet.status = new_task.status
        wallet.save_changes()
    else:
        new_task.is_update_task = False
        wallet = Wallet(
            wallet_id = new_task.wallet_id,
            status = new_task.status
        )
        wallet.create()

    new_task.create()
    r = add_new_task.send(str(new_task.id))
    new_task.task_id = r.message_id
    new_task.save()
    
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


@api.delete("/wallets/{wallet_id}")
def delete_wallet(request: Request, response: Response, wallet_id: str = Path()):
    wallet = Wallet.find(Wallet.wallet_id == wallet_id).first_or_none()
    if wallet:
        wallet_tasks = Task.find(Task.wallet_id == wallet.wallet_id).to_list()
        for task in wallet_tasks:
            abort_task(task.task_id)
            task.delete()   
        wallet.delete()
    
    response.status_code =  status.HTTP_200_OK
    return
