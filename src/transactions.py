import json
import time
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions, WebElement
import httpx
from datetime import datetime, timedelta
from pymongo.errors import DuplicateKeyError
from src.models import Transaction
from src.config import init_db, logger
import platform
from seleniumbase import Driver
from playwright.sync_api import sync_playwright


class TransactionManager:
    def __init__(self, account_hash):
        self.account_hash = account_hash
        self.last_x_days = 7

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
        current_date = datetime.today()
        last_x_days_date = current_date - timedelta(days=self.last_x_days + 1)

        loop = True
        offset = 0
        limit = 30

        tokens_traded = set()

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
            response = httpx.get(url, params=params, headers=headers, timeout=timeout)
            if response.status_code in [200]:
                json_data = response.json()
                if json_data:
                    if json_data.get("statusCode") == 200 and json_data.get("success"):
                        _data = json_data.get("data", {})
                        if _data:
                            has_next = _data.get("hasNext", False)
                            transactions = _data.get("items", [])
                            logger.info(f"Saving {len(transactions)} transactions for {self.account_hash} [{offset}]")
                            for transaction in transactions:
                                block_time = transaction["blockTime"]
                                _transaction_datetime, _timestamp = self.compute_timestamp(block_time)

                                # Only process transactions within last_x_days :
                                if _transaction_datetime - timedelta(days=2) >= last_x_days_date:
                                    transaction["timestamp"] = _timestamp
                                    transaction["account"] = self.account_hash
                                    transaction.pop("blockTime", None)
                                    sorted_int = transaction.pop("sortedIns", [])
                                    for token in transaction.pop("tokenChange", []):
                                        tokens_traded.add(f"{token['address']}_____{token['symbol']}")
                                else:
                                    loop = False
                                    logger.info(f"All transactions for last {self.last_x_days} days complete")
                                    break
                            if has_next:
                                offset += limit
                            else:
                                logger.info("No next results ...")
                                loop = False
                    else:
                        logger.info(f"Request unsuccessful => {json_data}")
                        loop = True
            elif response.status_code == 429:
                logger.info("Too many requests .. sleeping for some time ...")
                time.sleep(60)

        logger.info(
            f"Total tokens traded within last {self.last_x_days} days for account [{self.account_hash} => {len(list(tokens_traded))}")

        # Save tokens traded

    @staticmethod
    def create_driver():
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
        driver = Chrome(use_subprocess=False, options=chrome_options)

        driver.execute_script('''window.open("http://nowsecure.nl","_blank");''')  # open page in new tab
        time.sleep(5)  # wait until page has loaded
        driver.switch_to.window(window_name=driver.window_handles[0])  # switch to first tab
        driver.close()  # close first tab
        driver.switch_to.window(window_name=driver.window_handles[0])  # switch back to new tab
        time.sleep(2)
        driver.get("https://google.com")
        time.sleep(2)
        driver.get("https://dexscreener.com/")  # this should pass cloudflare captchas now

        return driver

    def lookup_tokens(self):
        with open("tokens_traded.txt") as f:
            _tokens_traded = f.readlines()

        logger.info(f"Loaded {len(_tokens_traded)} tokens ...")
        # Get transaction data of each token filtering by account hash on radium pool:

        with sync_playwright() as playwright_sync:
            browser = playwright_sync.chromium.launch(proxy={
                "server": "datacenter.proxyempire.io:9000",
                "username": "a0f76e18a0;any",
                "password": "ddfb4e1b18"
            }, headless=False)
            context = browser.new_context()
            page = context.new_page()

            for token in _tokens_traded:
                address, symbol = token.strip().split("_____")
                page.goto("https://dexscreener.com/")
                print(_tokens_traded)


if __name__ == "__main__":
    account_hash = "2bhkQ6uVn32ddiG4Fe3DVbLsrExdb3ubaY6i1G4szEmq"
    manager = TransactionManager(account_hash)
    manager.lookup_tokens()
