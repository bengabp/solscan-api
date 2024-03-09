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
        pre=True,
        check_fields=False
    )
    def dash_to_null(cls, v):
        if isinstance(v, str):
            if v.strip() == "-":
                return None
        return v
    
class Token(BaseModel):
    model_config = simple_pydantic_model_config
    
    mint: str
    ui_amount: float
    price: float
    name: str
    symbol: str
    icon: OptionalString
    value: float
    
class TokenWithDexData(Token):
    dex_data: Optional[TokenDexscreenerData] = Field(default=None)
    
class TimeWalletSummary(BaseModel):
    model_config = simple_pydantic_model_config
    pnl: float = Field(default=0)
    token_change: List[Token]
    trade_count: int
    volume: float
    
    
OptionalTimeWalletSummary = Optional[TimeWalletSummary]

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
    
    trade_yesterday: OptionalTimeWalletSummary = Field(default=None)
    trade_today: OptionalTimeWalletSummary = Field(default=None)
    trade_7D:  OptionalTimeWalletSummary = Field(default=None)
    trade_30D: OptionalTimeWalletSummary = Field(default=None)
    trade_60D: OptionalTimeWalletSummary = Field(default=None)
    trade_90D: OptionalTimeWalletSummary = Field(default=None)
    
    started_at: int = Field(default_factory=current_utc_timestamp)
    duration: float = Field(default=0)
    wallet_id: str = Field(description = "wallet id")
    status: Literal["running", "queued", "completed"] = Field(default = "queued")
    tokens_dex_data: Dict = Field(default={})
    status_percent: float = Field(default=0)
    
    
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
    status: Literal["running", "queued", "completed", "aborted"] = Field(default = "queued")
    wallet_id: str = Field()
    task_id: OptionalString = Field(default=None)
    result: Dict = Field(default={})
    