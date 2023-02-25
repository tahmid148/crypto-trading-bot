import websocket, json, pprint

# Create a socket that retrives data on ETHUSDT pair every 1 minute
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

def on_open(ws):
    print("Connection Opened")

def on_close(ws):
    print("Connection Closed")
    
def on_message(ws, message):
    print("Message Recieved")
    json_message = json.loads(message)
    pprint.pprint(json_message)

    

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

try:
    ws.run_forever()
except KeyboardInterrupt:
    on_close(ws)