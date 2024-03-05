import json
import time
from typing import List, Dict
import httpx
from curl_cffi import requests
from datetime import datetime, timedelta
from src.models import TokenBase, TokenTradeData
from src.config import init_db, DEXSCREENER_API_URI, dramatiq_logger
import logging
import requests as generic_requests
from src.exceptions import NoPopupDataFound



class TransactionManager:
    def __init__(self, account_hash, last_x_days=7):
        self.account_hash = account_hash
        self.last_x_days = last_x_days
        self.last_x_days_date = datetime.today() - timedelta(days=self.last_x_days + 1)
        
    def parse_avro_bytes(self, url, content: bytes) -> Dict:
        files=[
            ('file',('output', content, 'application/octet-stream'))
        ]
    
        r = generic_requests.request("POST", url, files=files).json()
        return r

    @staticmethod
    def compute_timestamp(timestamp: int):
        try:
            _timestamp = timestamp
            _date = datetime.fromtimestamp(_timestamp)
        except OSError:
            _timestamp = timestamp / 1000
            _date = datetime.fromtimestamp(_timestamp)
        return _date, _timestamp

    def get_transaction_coins_for_x_days(self):
        timeout = 60 * 10
        
        loop = True
        offset = 0
        limit = 30

        tokens_traded = set()
        symbol_data = {}

        headers = {
            'authority': 'multichain-api.birdeye.so',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'agent-id': '18b2d1c0-e2fc-46ca-8a25-9ea14378e9e0',
            'cf-be': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDc3NjE3MDMsImV4cCI6MTcwNzc2MjAwM30.xBDaGBD4403Ozcfya3bhCBFOMu6wipbiFSZE8-FXu7c',
            'origin': 'https://birdeye.so',
            'referer': 'https://birdeye.so/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

        while loop:
            params = {
                'address': self.account_hash,
                "offset": offset,
                "limit": limit
            }

            url = "https://multichain-api.birdeye.so/solana/trader_profile/trader_txs"
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            if response.status_code in [200]:
                json_data = response.json()
                if json_data:
                    if json_data.get("statusCode") == 200 and json_data.get("success"):
                        _data = json_data.get("data", {})
                        if _data:
                            has_next = _data.get("hasNext", False)
                            transactions = _data.get("items", [])
                            dramatiq_logger.info(f"Saving {len(transactions)} transactions for {self.account_hash} [{offset}]")
                            for transaction in transactions:
                                block_time = transaction["blockTime"]
                                _transaction_datetime, _timestamp = self.compute_timestamp(block_time)

                                # Only process transactions within last_x_days :
                                if _transaction_datetime - timedelta(days=2) >= self.last_x_days_date:
                                    transaction["timestamp"] = _timestamp
                                    transaction["account"] = self.account_hash
                                    transaction.pop("blockTime", None)
                                    sorted_int = transaction.pop("tokenChange", [])
                                    for token in transaction.pop("sortedIns", []):
                                        for _type in ["from", "to"]:
                                            symbol = token[_type]["symbol"]
                                            address = token[_type]["address"]
                                            logo = token[_type]["icon"]
                                            symb_addr = f"{address}_____{symbol}"
                                            tokens_traded.add(symb_addr)
                                            symbol_data[symb_addr] = {
                                                "symbol": symbol,
                                                "logo": logo,
                                                "address": address
                                            }
                                else:
                                    loop = False
                                    dramatiq_logger.info(f"All transactions for last {self.last_x_days} days complete")
                                    break
                            if has_next:
                                offset += limit
                            else:
                                dramatiq_logger.info("No next results ...")
                                loop = False
                    else:
                        dramatiq_logger.info(f"Request unsuccessful => {json_data}")
                        loop = True
            elif response.status_code == 429:
                dramatiq_logger.info("Too many requests .. sleeping for some time ...")
                time.sleep(60)
            else:
                pass
        
        tokens_traded = list(tokens_traded) 
        tokens_traded_full_data = [
            TokenBase.model_validate(symbol_data[symb_addr])
            for symb_addr in tokens_traded
        ]
        dramatiq_logger.info(
            f"Total tokens traded within last {self.last_x_days} days for account [{self.account_hash} => {len(tokens_traded_full_data)}")

        # Save tokens traded
        return tokens_traded_full_data
    
    def get_token_raydium_data(self, token):
        
        headers = {}
        
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
            'q': token.address,
        }

        value = self.send_until_ok(
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
        
        # Get transaction logs for last 7 days

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

        loop = True
        page = 1
        bbn = None
        
        transaction_logs = []
        
        token_trade_data = None
        popup_data_extracted = False
        
        while loop:
            params = {
                'q': quote_token_address,
                'm': self.account_hash,
                'c': '1',
            }
            if page > 1:
                params["bbn"] = bbn

            _logs = self.send_until_ok(
                f'https://io.dexscreener.com/dex/log/amm/v2/solamm/all/solana/{raydium_pair_address}',
                f"{DEXSCREENER_API_URI}/logs",
                params=params,
                headers=headers,
                cookies={}
            )
            logs = _logs.get("logs")
            if logs:
                for log in logs:
                    block_timestamp = log["blockTimestamp"]
                    _transaction_datetime, _timestamp = self.compute_timestamp(block_timestamp)
                    
                    # Extract popup data
                    if not popup_data_extracted:
                        try:
                            _details = log["makerScreener"]
                            _details.update({
                                "symbol": token.symbol,
                                "logo": token.logo,
                                "address": token.address
                            })
                            token_trade_data = TokenTradeData.model_validate(_details)
                            popup_data_extracted = True
                        except KeyError:
                            raise NoPopupDataFound("No popup data found !")

                    # Only process transactions within last_x_days :
                    if _transaction_datetime >= self.last_x_days_date:
                        transaction_logs.append(log)
                
                bbn = log["blockNumber"]
                block_timestamp = log["blockTimestamp"]
                _transaction_datetime, _timestamp = self.compute_timestamp(block_timestamp)
                page += 1
                if _transaction_datetime < self.last_x_days_date:
                    loop = False
                    break       
            else:
                loop = False
                
        if token_trade_data:
            token_trade_data.transaction_logs = transaction_logs
            return token_trade_data
        return None
        
        
    def send_until_ok(self, url, parser_url, headers, params, cookies):
        while True:
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
        
        
# if __name__ == "__main__":
#     account_hash = "2bhkQ6uVn32ddiG4Fe3DVbLsrExdb3ubaY6i1G4szEmq"
#     manager = TransactionManager(account_hash)
#     # manager.get_transaction_coins_for_x_days()
#     manager.get_token_raydium_data(TokenBase.model_validate({
#       "symbol": "ZERO",
#       "logo": "https://img.fotofolio.xyz/?url=https%3A%2F%2Fgateway.irys.xyz%2F0qYdLixPAk4cYEpaf3ylqZ-JIbw8Vqg6R9xXZrH9SCc",
#       "address": "93RC484oMK5T9H89rzT5qiAXKHGP9jscXfFfrihNbe57"
#     }))
