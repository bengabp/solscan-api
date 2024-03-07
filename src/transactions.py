import json
import time
from typing import List, Dict, Optional
import httpx
from curl_cffi import requests
from requests.auth import HTTPProxyAuth
from datetime import datetime, timedelta
from src.models import TokenBase, TokenDexscreenerData
from src.config import init_db, DEXSCREENER_API_URI, dramatiq_logger
import logging
import requests as generic_requests
from src.exceptions import NoPopupDataFound
import platform
from pprint import pprint
from src.utils import get_random_ua


class TransactionManager:
    def __init__(self, account_hash):
        self.account_hash = account_hash
        self.platform = platform.system()
        self.trader_overview_url = 'https://multichain-api.birdeye.so/solana/trader_profile/trader_overview'
        
    def parse_avro_bytes(self, url, content: bytes) -> Dict:
        files=[
            ('file',('output', content, 'application/octet-stream'))
        ]
    
        r = generic_requests.request("POST", url, files=files).json()
        return r

    def compute_timestamp(self, timestamp: int):
        if self.platform == "Windows":
            time_convert_exception_class = OSError
        else:
            time_convert_exception_class = ValueError
        try:
            _timestamp = timestamp
            _date = datetime.fromtimestamp(_timestamp)
        except time_convert_exception_class:
            _timestamp = timestamp / 1000
            _date = datetime.fromtimestamp(_timestamp)
        
        return _date, _timestamp
    
    def get_token_dexscreener_summary(self, token: Dict) -> Optional[TokenDexscreenerData]:
        address = token["mint"]
        symbol = token["symbol"]
        
        cookies = {
            '__cuid': 'c75f8923aa8d4190aafc36620b96e2fa',
            'amp_fef1e8': '478ebb49-619e-49ff-bae2-9517c76ad8bcR...1hn5od2lh.1hn5oemhg.f.5.k',
            '_ga_RD6VMQDXZ6': 'GS1.1.1708516586.6.1.1708517039.0.0.0',
            '_ga': 'GA1.1.1539199066.1707302013',
            'cf_clearance': 'kMmBbhNKyO5OZ4ilsF.jPBkdgMJL9zXpX4F4KPOxcGc-1709561360-1.0.1.1-ryT70.h2vsOAji2uaWqsA0OJk4EL6ZJeznxGnJBEvXN9Vuur9e2g_IM.AjL4.SmugHxO4V.Ae0VYSVhRHL__1g',
            '__cflb': '0H28vzQ7jjUXq92cxrPQi3FxzcKVhBVoVZJapc7Tu1o',
            '__cf_bm': 'LRhPSjXuU5t6YLrzuynWhQMWjHcRvi_28qmiXlGUnso-1709565388-1.0.1.1-IHkR0Pnst_2xkzRS.wUlxz7WuOGZBJ7UVN3DeFRIR__sSUKC9S0FyAx7wNXxxCdYOlg.U06jB_MIAo2hrPL5YDYws5dzALo1eMZDmuN5c3c',
            '_ga_532KFVB4WT': 'GS1.1.1709565378.21.1.1709565653.41.0.0',
        }

        headers = {
            'authority': 'io.dexscreener.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'if-none-match': 'W/"10e3-YeF0RRckjY+hyZg4rAz5wOVF1Do"',
            'origin': 'https://dexscreener.com',
            'referer': 'https://dexscreener.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        
        params = {
            'q': address,
        }

        value = self.dexscreener_send_until_ok(
            'https://io.dexscreener.com/dex/search/v4/pairs', 
            f'{DEXSCREENER_API_URI}/pairs',
            params=params, 
            cookies=cookies, 
            headers=headers
        )
        
        raydium_pair_address = None
        quote_token = {}
        quote_token_address = None
        
        for pair in value["pairs"]:
            if pair["dexId"] == "raydium" and pair["chainId"] == "solana":
                raydium_pair_address = pair["pairAddress"]
                quote_token =pair["quoteToken"]
                quote_token_address = quote_token["address"]
                break
        
        if not raydium_pair_address:
            return None
        
        headers = {
            'authority': 'io.dexscreener.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'origin': 'https://dexscreener.com',
            'referer': 'https://dexscreener.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        transaction_logs = []
        token_dexscreener_data = None

        params = {
            'q': quote_token_address,
            'm': self.account_hash,
            'c': '1',
        }
        _logs = self.dexscreener_send_until_ok(
            f'https://io.dexscreener.com/dex/log/amm/v2/solamm/all/solana/{raydium_pair_address}',
            f"{DEXSCREENER_API_URI}/logs",
            params=params,
            headers=headers,
            cookies={}
        )
        logs = _logs.get("logs", [])
        if logs:
            # Extract popup data from last log
            try:
                _details = logs[-1]["makerScreener"]
                _details.update({
                    "pairAddress": raydium_pair_address
                })
                token_dexscreener_data = TokenDexscreenerData.model_validate(_details)
                token_dexscreener_data.pnl = "$ " + str(token_dexscreener_data.volume_usd_buy - token_dexscreener_data.volume_usd_sell)
            except KeyError:
                return None
        return token_dexscreener_data
        
    def dexscreener_send_until_ok(self, url, parser_url, headers, params, cookies):
        while True:
            headers['user-agent'] = get_random_ua()
            try:
                response = requests.get(url, headers=headers, params=params, cookies=cookies)
                if response.status_code in [200]:
                    _json = self.parse_avro_bytes(parser_url, response.content)
                    if _json.get("ok", False):
                        value = _json["value"]
                        return value
                elif response.status_code in [429]:
                    dramatiq_logger.info("too many requests.. sleeping ...")
                    time.sleep(60)
                else:
                    dramatiq_logger.info(f"Request failed ... with status {response.status_code}")
            except (json.JSONDecodeError, generic_requests.JSONDecodeError) as err:
                dramatiq_logger.info("falied to decode data")
    def birdeye_send_until_ok(self, url, headers, params):
        timeout = 60 * 10
        
        while True:
            headers['user-agent'] = get_random_ua()
            try:
                response = requests.get(url, params=params, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data:
                        if json_data.get("success"):
                            _data = json_data.get("data", {})
                            return _data
            except requests.errors.RequestsError:
                dramatiq_logger.warning(f"Failed to perform, curl 23: Retrying ...")
                time.sleep(1)
                continue
    
    def get_wallet_summary_birdeye(self):
        _times = ["yesterday", "today", "7D", "30D", "60D", "90D"]
        token_datas = {}
        unique_token_list = set()
        
        headers = {
            'authority': 'multichain-api.birdeye.so',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'agent-id': '18b2d1c0-e2fc-46ca-8a25-9ea14378e9e0',
            'cf-be': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDk4MjE0MDQsImV4cCI6MTcwOTgyMTcwNH0.q8BNLCT2t6ea_b4cMZ8TiMYG8cv7rzYuVTScyinimPM',
            'origin': 'https://birdeye.so',
            'referer': 'https://birdeye.so/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'token': 'undefined',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        wallet_summary = {}
        for _time in _times:
            params = {
                'address': self.account_hash,
                'time': _time,
            }
            data = self.birdeye_send_until_ok(
                url = self.trader_overview_url,
                params=params,
                headers=headers,
            )
            keys = ["pnl","tokenChange","tradeCount", "volume"]
            _wallet_summary = {}
            for key in keys:
                full_key = f"{key}{_time.title()}"
                value = data[full_key]
                _wallet_summary[key] = value
            wallet_summary[_time] = _wallet_summary
            for token in _wallet_summary.get("tokenChange", []):
                addr_symbol = f"{token['mint']}_____{token['symbol']}"
                unique_token_list.add(addr_symbol)
                token_datas[addr_symbol] = token
        
        _tokens_all_time = [token_datas[addr_symb] for addr_symb in unique_token_list]
        dramatiq_logger.info(f"{len(token_datas)} tokens found for all time trades [{self.account_hash}] ... Getting dexscreener token data ...")
        return _tokens_all_time, wallet_summary
        
        
if __name__ == "__main__":
    class Clogger:
        def __init__(self):
            pass
        def info(self, msg):
            print(f"[INFO] => {msg}")
        def warning(self, msg):
            print(f"[WARNING] => {msg}")
        def error(self, msg):
            print(f"[ERROR] => {msg}")  
            
    dramatiq_logger = Clogger()
    account_hash = "71WDyyCsZwyEYDV91Qrb212rdg6woCHYQhFnmZUBxiJ6"
    manager = TransactionManager(account_hash)
    
    start_time = time.time()
    tokens_all_time, wallet_summary = manager.get_wallet_summary_birdeye()
    tokens_dex_data = {}
    print(f"Getting dex data for {len(tokens_all_time)} tokens ...")
    for ind,token in enumerate(tokens_all_time):
        dex_data = manager.get_token_dexscreener_summary(token)
        tokens_dex_data[token["mint"]] = dex_data
        print(f"Processed {ind+1}/{len(tokens_all_time)}")
    stop_time = time.time()
    duration = abs(start_time-stop_time)
    print(tokens_dex_data)
