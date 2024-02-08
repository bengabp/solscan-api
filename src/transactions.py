import json
import httpx
from pymongo.errors import DuplicateKeyError

from src.models import Transaction
from src.config import init_db

init_db([Transaction])


def get_transactions(account_hash: str):
    loop = True
    cursor = None
    cookies = {
        '_ga': 'GA1.1.945626448.1707306938',
        '_ga_F96PEY6C7C': 'GS1.1.1707394598.3.1.1707394779.0.0.0',
        'ph_phc_H66gRNy1uok5uPmsul2kpbRynt6h9L74f5BlPJ4RMqE_posthog': '%7B%22distinct_id%22%3A%22018d8388-7612-7e5c-8954-d8dc0cfd9e42%22%2C%22%24sesid%22%3A%5B1707394783623%2C%22018d88a4-01f1-7410-bea1-56532ce2aa2c%22%2C1707394466289%5D%7D',
        '_ga_XGVFBFP3B4': 'GS1.1.1707392706.4.1.1707395031.0.0.0',
    }
    
    headers = {
        'authority': 'xray.helius.xyz',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        # 'cookie': '_ga=GA1.1.945626448.1707306938; _ga_F96PEY6C7C=GS1.1.1707394598.3.1.1707394779.0.0.0; ph_phc_H66gRNy1uok5uPmsul2kpbRynt6h9L74f5BlPJ4RMqE_posthog=%7B%22distinct_id%22%3A%22018d8388-7612-7e5c-8954-d8dc0cfd9e42%22%2C%22%24sesid%22%3A%5B1707394783623%2C%22018d88a4-01f1-7410-bea1-56532ce2aa2c%22%2C1707394466289%5D%7D; _ga_XGVFBFP3B4=GS1.1.1707392706.4.1.1707395031.0.0.0',
        'referer': 'https://xray.helius.xyz/account/2bhkQ6uVn32ddiG4Fe3DVbLsrExdb3ubaY6i1G4szEmq?network=mainnet',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    
    while loop:
        params = {
            'batch': '1',
            'input': json.dumps({"0": {"account": account_hash, "filter": "SWAP", "isMainnet": True, "user": account_hash}}),
        }
        if cursor:
            params["cursor"] = cursor
        
        response = httpx.get('https://xray.helius.xyz/trpc/transactions', params = params, cookies = cookies, headers = headers)
        if response.status_code in [200]:
            json_data = response.json()
            if json_data:
                result = json_data[0]["result"]
                _data = result["data"]
                next_cursor = _data.get("oldest")
                if next_cursor:
                    cursor = next_cursor
                else:
                    loop = False
                
                transactions = _data.get("result",[])
                for transaction in transactions:
                    _timestamp = transaction["timestamp"]
                    # Convert and compare timestamps
                    
                    transac = Transaction.model_validate(transaction)
                    try:
                        transac.create()
                    except DuplicateKeyError:
                        pass
    
get_transactions("2bhkQ6uVn32ddiG4Fe3DVbLsrExdb3ubaY6i1G4szEmq")
