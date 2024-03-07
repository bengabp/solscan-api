from typing import Optional, List, Dict, Annotated, Literal, Optional
from uuid import UUID
from datetime import datetime
import pymongo
from bunnet import Document, PydanticObjectId, Indexed
from pydantic import Field, BaseModel, validator
from pymongo import IndexModel

from src.config import simple_pydantic_model_config, current_utc_timestamp

OptionalString = Optional[str]
OptionalInt = Optional[int]
OptionalFloat = Optional[float]

class TokenBase(BaseModel):
    model_config = simple_pydantic_model_config
    
    symbol: str = Field(description = "Token symbol")
    logo: OptionalString = Field(description="Token logo")
    address: str = Field(description=  "Token address")

class TokenDexscreenerData(BaseModel):
    model_config = simple_pydantic_model_config

    buys:OptionalInt = Field(description="Total number of buy transactions")
    sells: OptionalInt = Field(description="Total number of sell transactions")
    volume_usd_sell: OptionalFloat = Field(description="Sell volume in usd")
    volume_usd_buy: OptionalFloat = Field(description="Buy volume in usd")
    amount_buy: OptionalString = Field(description= "Number of buy transactions")
    amount_sell: OptionalString = Field(description= "Number of sell transactions")
    balance_amount: OptionalString = Field(description="Balance amount")
    balance_percentage: OptionalFloat = Field(description="Balance percentage")
    first_swap: OptionalInt = Field(description="First swap -> UTC TIMESTAMP")
    pair_address: str = Field(description="Raydium pair address")
    pnl: OptionalString = Field(description="PNL", default=None)
    
    @validator(
        'volume_usd_sell', 
        'volume_usd_buy', 
        "amount_buy",
        "amount_sell",
        "balance_amount",
        "buys",
        "sells",
        "balance_percentage",
        "first_swap",
        pre=True,
        check_fields=False
    )
    def dash_to_null(cls, v):
        if isinstance(v, str):
            if v.strip() == "-":
                return None
        return v
    
class TokenTradeData(TokenBase):
    model_config = simple_pydantic_model_config

    buys:OptionalInt = Field(description="Total number of buy transactions")
    sells: OptionalInt = Field(description="Total number of sell transactions")
    volume_usd_sell: OptionalFloat = Field(description="Sell volume in usd")
    volume_usd_buy: OptionalFloat = Field(description="Buy volume in usd")
    amount_buy: OptionalString = Field(description= "Number of buy transactions")
    amount_sell: OptionalString = Field(description= "Number of sell transactions")
    balance_amount: OptionalString = Field(description="Balance amount")
    balance_percentage: OptionalFloat = Field(description="Balance percentage")
    first_swap: OptionalInt = Field(description="First swap -> UTC TIMESTAMP")

    transaction_logs: List = Field(description="Historical transaction logs", default=[])
    
    
    
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
    