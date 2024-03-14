import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from dramatiq.results import Results
from dramatiq.middleware import AsyncIO
from bunnet import PydanticObjectId
from src.models import Task, Wallet, TimeWalletSummary
from src.config import init_db, REDIS_BROKER_DB, REDIS_HOSTNAME, REDIS_PORT, dramatiq_logger, BASE_DIR, logs_dir, current_utc_timestamp
from src.transactions import TransactionManager
from src.exceptions import NoPopupDataFound
from dramatiq_abort.abort_manager import Abort
import logging
import os
import redis
import time
from dramatiq_abort import Abortable, backends


abortable = Abortable(backend=backends.RedisBackend(client=redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, db=REDIS_BROKER_DB)))
redis_broker = RedisBroker(url=f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_BROKER_DB}")
redis_broker.add_middleware(abortable)
dramatiq.set_broker(redis_broker)


init_db([Task, Wallet])

def startup():
    print("Startup ...analyzing tasks ...")
    tasks = Task.find(Task.status == "running").to_list()
    for task in tasks:
        n_task = Task(
            wallet_id=task.wallet_id,
            is_update_task=task.is_update_task
        )
        n_task.create()
        res = new_task.send(str(n_task.id))
        n_task.task_id = res.message_id
        n_task.save_changes()
        task.delete()

 
@dramatiq.actor(max_retries=0, time_limit=5000000)
def new_task(task_id: str):
    task_id = PydanticObjectId(task_id)
    task = Task.find(Task.id == task_id).first_or_none()
    if not task:
        return
    
    res = Task.find(Task.wallet_id == task.wallet_id).sort(-Task.id).to_list()
    for i,t in enumerate(res):
        if i > 0:
            t.status = "aborted"
            t.save_changes()
            if task_id == t.id:
                dramatiq_logger.warning(f"Aborting task for [{task.wallet_id}]")
                return
        
    task.status = "running"
    task.save_changes()
    
    wallet = Wallet.find(Wallet.wallet_id == task.wallet_id).first_or_none()
    wallet.status = "running"
    wallet.started_at = current_utc_timestamp()
    wallet.status_percent = 0
    wallet.duration = 0
    wallet.save_changes()
    
    try:
        dramatiq_logger.info(f"Running task => {task.id} for [{wallet.wallet_id}] wallet")
        t_manager = TransactionManager(wallet.wallet_id, wallet)
        
        tokens_all_time, wallet_summary = t_manager.get_wallet_summary_birdeye()
        
        _yesterday = wallet_summary.get("yesterday")
        _today = wallet_summary.get("today")
        _7d =wallet_summary.get("7D")
        _30d = wallet_summary.get("30D")
        _60d = wallet_summary.get("60D")
        _90d = wallet_summary.get("90D")
        
        if _7d:
            wallet.trade_7D = TimeWalletSummary.model_validate(_7d)
        if _yesterday:
            wallet.trade_yesterday = TimeWalletSummary.model_validate(_yesterday)
        if _today:
            wallet.trade_today = TimeWalletSummary.model_validate(_today)
        if _30d:
            wallet.trade_30D = TimeWalletSummary.model_validate(_30d)
        if _60d:
            wallet.trade_60D = TimeWalletSummary.model_validate(_60d)
        if _90d:
            wallet.trade_90D = TimeWalletSummary.model_validate(_90d)
            wallet.pnl_90days = _90d.get("pnl")
        
        wallet.status_percent = 0.1
        wallet.save()
        
        # Get token info of all tokens traded all time
        
        if tokens_all_time:
            total_items = len(tokens_all_time)
            status_increment = 1 / total_items

            for ind,token in enumerate(tokens_all_time):
                dex_data = t_manager.get_token_dexscreener_summary(token)
                wallet.tokens_dex_data[token["mint"]] = dex_data
                wallet.status_percent += status_increment
                wallet.save_changes()
        else:
            wallet.status_percent = 1

        wallet.status = "completed"
        wallet.save_changes()
        
        task.status = "completed"
        task.result = wallet.model_dump(by_alias=True)
        task.save_changes()
        
        dramatiq_logger.info(f"All traded data saved successfully ...")
    except Abort:
        pass
    except Exception as e:
        dramatiq_logger.error(f"Wallet task [{task.wallet_id}] failed with error => {e}")
        task.status = "failed"
        wallet.status ="failed"
        wallet.save_changes()
        task.save_changes()

startup()
