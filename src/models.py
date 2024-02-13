from typing import Optional, List, Dict, Annotated
from uuid import UUID

import pymongo
from bunnet import Document, PydanticObjectId, Indexed
from pydantic import Field, BaseModel
from pymongo import IndexModel

from src.config import simple_pydantic_model_config

OptionalString = Optional[str]


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
    