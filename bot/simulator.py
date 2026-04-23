import json
import os
import requests
from datetime import datetime
from .logging_config import logger

class Simulator:
    """
    A mock Binance client for Paper Trading.
    Uses public Binance API for live prices and manages a local virtual balance.
    """
    DATA_FILE = "paper_account.json"
    PUBLIC_API_URL = "https://api.binance.com/api/v3/ticker/price"

    def __init__(self):
        self.account = self._load_account()
        logger.info(f"Simulator initialized. Current Balance: ${self.account['balance']}")

    def _load_account(self):
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            # Initial state
            initial_data = {
                "balance": 10000.0,  # $10,000 virtual cash
                "positions": {},      # { "BTCUSDT": 0.001 }
                "history": []
            }
            self._save_account(initial_data)
            return initial_data

    def _save_account(self, data):
        with open(self.DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def get_price(self, symbol):
        """Fetches live price from public Binance API (No Key Required)."""
        try:
            response = requests.get(f"{self.PUBLIC_API_URL}?symbol={symbol}")
            response.raise_for_status()
            return float(response.json()['price'])
        except Exception as e:
            logger.error(f"Failed to fetch price for {symbol}: {str(e)}")
            raise ConnectionError(f"Could not connect to price feed for {symbol}")

    def futures_create_order(self, **params):
        """
        Simulates the Binance futures_create_order method.
        """
        symbol = params['symbol']
        side = params['side']
        order_type = params['type']
        quantity = float(params['quantity'])
        
        # Get live price for execution
        current_price = self.get_price(symbol)
        order_price = float(params.get('price', current_price))
        
        # Cost calculation
        total_cost = quantity * order_price
        
        if side == 'BUY':
            if self.account['balance'] < total_cost:
                raise ValueError(f"Insufficient virtual balance! Need ${total_cost:.2f}, Have ${self.account['balance']:.2f}")
            
            self.account['balance'] -= total_cost
            self.account['positions'][symbol] = self.account['positions'].get(symbol, 0.0) + quantity
        else: # SELL
            current_pos = self.account['positions'].get(symbol, 0.0)
            if current_pos < quantity:
                 raise ValueError(f"Insufficient position to sell! Have {current_pos} {symbol}")
            
            self.account['balance'] += total_cost
            self.account['positions'][symbol] = current_pos - quantity

        # Log history
        order_id = f"SIM-{int(datetime.now().timestamp())}"
        history_entry = {
            "orderId": order_id,
            "timestamp": str(datetime.now()),
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "price": order_price,
            "status": "FILLED"
        }
        self.account['history'].append(history_entry)
        self._save_account(self.account)

        return {
            "orderId": order_id,
            "status": "FILLED",
            "symbol": symbol,
            "executedQty": str(quantity),
            "avgPrice": str(order_price),
            "type": order_type,
            "side": side
        }

    def get_account_summary(self):
        return {
            "balance": self.account['balance'],
            "positions": self.account['positions']
        }
