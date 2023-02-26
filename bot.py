import websocket, json, pprint, numpy as np, talib, config
from binance.enums import *
from binance.client import Client

# Create a socket that retrives data on ETHUSDT pair every 1 minute
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

# RSI over a 14 day period
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70 # Execute SELL
RSI_OVERSOLD = 30   # Execute BUY
TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

def order(side, symbol, quantity, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending Order:")
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        print(order)
    except Exception as e:
        return False        
    return True

def on_open(ws):
    print("Connection Opened")

def on_close(ws):
    print("Connection Closed")
    
def on_message(ws, message):
    print("Message Recieved")
    json_message = json.loads(message)
    pprint.pprint(json_message)
    
    candle = json_message['k']
    is_candle_closed = candle['x']
    close_price = candle['c']
    
    if is_candle_closed:
        print(f"Candle closed at {close_price}")
        closes.append(float(closes))
        print(f"Closes: {closes}")
        
        if (len(closes) > RSI_PERIOD):
            np_closes = np.array(closes)
            # Calculates RSI Values
            rsi = talib.RSI(np_closes, RSI_PERIOD) 
            print(f"RSI's calculated so far: {rsi}")
            
            last_rsi = rsi[-1]
            print(f"Current RSI: {last_rsi}")
            if (last_rsi > RSI_OVERBOUGHT):
                if in_position:
                    print("Overbought: SELL!")
                    # Insert Binance Logic
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("Overbought, but we have no position")
    
            elif (last_rsi < RSI_OVERSOLD):
                if (in_position):
                    print("It is oversold, but you already own it!")
                print("Oversold: BUY!")
                # Insert Binance Logic
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = True
    

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

try:
    ws.run_forever()
except KeyboardInterrupt:
    on_close(ws)