import random
import pyautogui
import os
import time

from selectolax.parser import HTMLParser
from pprint import pprint
from src.config import logger, BASE_DIR
from typing import List
import subprocess
import threading
import psutil
import numpy as np
import cv2
import pyperclip

"""
Automation steps:

- Get random task from queue
- Open browser or new tab
- Go to dex screener and search for token address and for radyium pool
- Filter transactions by wallet id.
- Get last 7 days of account transactions
- Close tab or browser and save results
"""


class WindowManager:
    def __init__(self, account_hash, tokens_traded: List = []):
        """ Initializes the manager for automation """

        # Initialize important variables for calculation
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pyautogui.size()
        self.CHROME_EXECUTABLE_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"

        self.account_hash = account_hash
        self.tokens_traded = tokens_traded
        self.logger = logger

        self.window_name = "test_automation"
        self.target_url = "https://dexscreener.com"

        # Start Chrome browser
        self.command = f"chrome --start-maximized --window-name='{self.window_name}' {self.target_url} --incognito"
        # self.start_browser_thread = threading.Thread(target=self.start_browser_service)

        # Start browser manager thread
        threading.Thread(target=self.browser_manager).start()

    def browser_manager(self):
        # This loop always checks the browser
        is_running = False
        while True:
            x_times = 0
            # Get all processes and check if chrome is running
            for process in psutil.process_iter():

                try:
                    if process.name() == "chrome.exe":
                        if x_times > 0:
                            break
                        x_times += 1
                        if not process.is_running():
                            process.resume()
                        is_running = True
                        self.logger.info("Browser is already running")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Ignore exceptions for processes that are not accessible or have terminated
                    pass

            if not is_running:
                self.logger.info("Starting chrome browser ...")
                threading.Thread(target=lambda: subprocess.call(self.command, shell=True)).start()
                self.logger.debug("Browser is running ...")
                is_running = True
            else:
                is_running = False

            time.sleep(30)

    def locate_image(self, image_path):
        # Take a screenshot of the entire screen
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # Load the image to locate
        image_to_locate = cv2.imread(image_path)

        h, w = image_to_locate.shape[:2]

        # Use template matching to find the image within the screenshot
        result = cv2.matchTemplate(screenshot, image_to_locate, cv2.TM_CCOEFF_NORMED)

        # Threshold to find the location(s) with sufficiently high match scores
        threshold = 0.8
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        return locations, w, h

    def random_mouse_movement(self):
        """ Simulates actual mouse movements """

        for i in range(random.randint(4, 7)):
            pyautogui.moveTo(random.randint(10, self.SCREEN_WIDTH), random.randint(200, self.SCREEN_HEIGHT - 100),
                             duration=random.randint(1, 3))

    def run(self):
        waiting_for_verification = True

        self.logger.info("Waiting for cloudflare bypass ...")

        while waiting_for_verification:
            cloudflare_captcha_button_location, _, _ = self.locate_image("assets/cloudflare_verify_image.png")
            dex_screener_logo_location, _, _ = self.locate_image("assets/dex_screener_logo.png")

            if cloudflare_captcha_button_location:
                x, y = cloudflare_captcha_button_location[0]
                pyautogui.click(x + 20, y + 8)
            elif dex_screener_logo_location:
                waiting_for_verification = False

            self.random_mouse_movement()

        self.logger.info("Cloudflare successfully bypassed")

        refined_results = []

        for token in self.tokens_traded:
            token_address, token_name = token.split("_____")

            pyautogui.press("/")
            self.random_mouse_movement()
            pyautogui.typewrite(token_address)

            self.logger.info("Waiting for token search results ...")
            idle_time = 0
            start_time = time.time()
            while True:
                locations, w, h = self.locate_image("assets/favourite_icon.png")
                if locations:
                    idle_time = 0
                    break
                idle_time = int(abs(time.time() - start_time))
                if idle_time > 30:
                    pyautogui.press("/")
                    pyautogui.typewrite(token_address)
                    idle_time = 0
                time.sleep(3)

            # Save page

            random_file_name = r"C:\Users\bengabp\Documents\IT\UKTeam\SolanaScan\datasets\dex_screener_sr.html"

            try:
                os.remove(random_file_name)
            except:
                pass
            try:
                os.remove(r"C:\Users\bengabp\Documents\IT\UKTeam\SolanaScan\datasets\dex_screener_sr_files")
            except:
                pass

            pyautogui.hotkey("ctrl", "s")

            # Wait for file explorer to open
            self.logger.info("Opening file explorer to save file ...a")
            while True:
                locations, w, h = self.locate_image("assets/save_file_explorer_buttons.png")
                if locations:
                    break
                time.sleep(2)

            pyautogui.typewrite(random_file_name)
            pyautogui.press("enter")

            # Wait for file to download
            self.logger.info("Saving page to file...")
            html_content = ""
            while True:
                if os.path.exists(random_file_name):
                    time.sleep(4)
                    with open(random_file_name, "rb") as f:
                        html_content = f.read()
                        break
                time.sleep(5)

            parser = HTMLParser(html_content)
            os.remove(random_file_name)
            link =None

            self.logger.info("Parsing html results ... extract raydium link ...")
            for node in parser.css('div[id^="chakra-modal--body"]  div.chakra-stack > div[class^="custom"] a.chakra-link[href^="https://dexscreener.com"]'):
                for img in node.css("img.chakra-image"):
                    title = img.attrs.get("title")
                    if title == "Raydium":
                        link = node.attrs.get("href")

            refined_results.append({
                "tokenName": token_name,
                "tokenAddress": token_address,
                "dexScreenerRaydiumPoolLink": link
            })

            time.sleep(random.randint(1,5))
            pyautogui.press("esc")

        self.logger.info("Successfully got token data from dexscreener")
        pprint(refined_results)


manager = WindowManager("2bhkQ6uVn32ddiG4Fe3DVbLsrExdb3ubaY6i1G4szEmq", [
    "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3_____PYTH",
    "HbxiDXQxBKMNJqDsTavQE7LVwrTR36wjV2EaYEqUw6qH_____GH0ST",
    "8HGyAAB1yoM1ttS7pXjHMa3dukTFGQggnFFH3hJZgzQh_____COPE"
])
manager.run()
