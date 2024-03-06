import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from dramatiq.results import Results
from dramatiq.middleware import AsyncIO
from bunnet import PydanticObjectId
from src.models import Task, Wallet
from src.config import init_db, BROKER_URI, dramatiq_logger, BASE_DIR, logs_dir
from src.transactions import TransactionManager
from src.exceptions import NoPopupDataFound
import logging
import os


redis_broker = RedisBroker(url=BROKER_URI)
dramatiq.set_broker(redis_broker)

init_db([Task, Wallet])

@dramatiq.actor(max_retries=1, time_limit=5000000)
def new_task(task_id: str):
    
    task_id = PydanticObjectId(task_id)
    
    task = Task.find(Task.id == task_id).first_or_none()
    if not task:
        return
    
    task.status = "running"
    task.save_changes()
    
    wallet = Wallet.find(Wallet.wallet_id == task.wallet_id).first_or_none()
    wallet.status = "running"
    wallet.save_changes()
    
    # Get traded tokens in last 7 days
    dramatiq_logger.info(f"Running task => {task.id} for [{wallet.wallet_id}] wallet")
    
    t_manager = TransactionManager(wallet.wallet_id, last_x_days=7)
    tokens_traded = t_manager.get_transaction_coins_for_x_days()
    
    wallet.tokens_traded_list = tokens_traded
    wallet.status = "completed"
    wallet.save_changes()
    
    trade_datas = []
    # Get raydium links for each token
    for token in wallet.tokens_traded_list:
        try:
            trade_data = t_manager.get_token_raydium_data(token)
            if trade_data:
                trade_datas.append(trade_data)
        except NoPopupDataFound:
            pass
    
    wallet.tokens_traded_data = trade_datas
    task.status = "completed"
    task.result = {
        "tokenList": wallet.tokens_traded_list,
        "tokenData": wallet.tokens_traded_data
    }
    wallet.status = "completed"
    wallet.save_changes()
    task.save_changes()
    dramatiq_logger.info(f"All traded data saved successfully ...")

