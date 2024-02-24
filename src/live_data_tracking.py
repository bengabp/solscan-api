from websockets.sync.client import connect # pip install websockets

headers = {
    'Pragma': 'no-cache',
    'Origin': 'https://dexscreener.com',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Sec-WebSocket-Key': 'o8nYF5szG57kchVS/OhPpg==',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Upgrade': 'websocket',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Sec-WebSocket-Version': '13',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
}

def hello():
    with connect("wss://io.dexscreener.com/dex/screener/pair/solana/8d4ed1uc96qcvtrzx68e3swrznv5jzqpmth3gwyy7xwa",
                  additional_headers=headers) as websocket:
        while True:
            message = websocket.recv()
            print(f"Received: {message}")

hello()