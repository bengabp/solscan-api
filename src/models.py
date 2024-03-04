from typing import Optional, List, Dict, Annotated, Literal
from uuid import UUID
from datetime import datetime
import pymongo
from bunnet import Document, PydanticObjectId, Indexed
from pydantic import Field, BaseModel
from pymongo import IndexModel

from src.config import simple_pydantic_model_config, current_utc_timestamp

OptionalString = Optional[str]

class TokenBase(BaseModel):
    model_config = simple_pydantic_model_config
    
    symbol: str = Field(description = "Token symbol")
    logo: str = Field(description="Token logo")
    address: str = Field(description=  "Token address")

class TokenTradeData(TokenBase):
    model_config = simple_pydantic_model_config
    
    bought: int = Field(description="Total bought amount")
    sold: int = Field(description="Total sold amount")
    pnl: int = Field(description="Pnl")
    unrealized_amount: int = Field(description="Unrealized amount")
    unrealized_relative: int = Field(description="Unrealized relative")
    
    tnt_buy:int = Field(description="Total number of tokens bought")
    tnt_sell: int = Field(description="Total number of tokens sold")
    
    tnx_buy: int = Field("Number of buy transactions")
    tnx_sell: int = Field("Number of sell transactions")
    
    market_share_info: List = Field(description="List of important informations", default=[])
    
    

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
    tokens_traded_data: List[TokenTradeData] = Field(default=[])
    tokens_traded_list: List[TokenBase] = Field(default=[])

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
    