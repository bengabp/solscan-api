from typing import Optional, List, Dict, Annotated, Literal
from uuid import UUID
from datetime import datetime
import pymongo
from bunnet import Document, PydanticObjectId, Indexed
from pydantic import Field, BaseModel
from pymongo import IndexModel

from src.config import simple_pydantic_model_config, current_utc_timestamp

OptionalString = Optional[str]


class Wallet(Document):
    class Settings:
        name = "wallets"
        use_state_management = True
        
        indexes = [
            IndexModel("walletId", name="signature_unique_1", unique=True)
        ]
    
    model_config = simple_pydantic_model_config
    
    id: PydanticObjectId = Field(
        description = "Document Id",
        default_factory = lambda: PydanticObjectId(),
        alias = "_id",
    )
    
    wallet_id: str = Field(description = "wallet id")
    status: Literal["running", "queued", "completed"] = Field(default = "queued")
    data: Dict = Field(default={})
    tokens_traded: List = Field(default=[])

class Task(Document):
    class Settings:
        name = "tasks"
        use_state_management = True
    
    model_config = simple_pydantic_model_config
    
    id: PydanticObjectId = Field(
        description = "Document Id",
        default_factory = lambda: PydanticObjectId(),
        alias = "_id",
    )
    
    is_update_task: bool = Field(default=False)
    queued_at: int = Field(default_factory= current_utc_timestamp)
    status: Literal["running", "queued", "completed"] = Field(default = "queued")
    wallet_id: str = Field()
    result: Dict = Field(default={})
    
class Transaction(Document):
    class Settings:
        name = "transactions"
        use_state_management = True
        
        indexes = [
            IndexModel("txHash", name="signature_unique_1", unique=True)
        ]
    
    model_config = simple_pydantic_model_config
    
    id: PydanticObjectId = Field(
        description = "Document Id",
        default_factory = lambda: PydanticObjectId(),
        alias = "_id",
    )
    
    tx_hash: str = Field(description = "Transaction signature", alias="txHash")
    account: str = Field(description = "Account ID")
    