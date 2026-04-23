from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException
from .logging_config import logger

class OrderManager:
    def __init__(self, client):
        self.client = client

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generic method to place orders on Binance Futures.
        """
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
            }
            
            if order_type == "LIMIT":
                params["price"] = str(price)
                params["timeInForce"] = "GTC"  # Good Till Cancelled
            
            elif order_type == "STOP_MARKET":
                if stop_price is None:
                    raise ValueError("stop_price is required for STOP_MARKET orders")
                params["stopPrice"] = str(stop_price)
                
            elif order_type == "STOP_LIMIT":
                if stop_price is None or price is None:
                    raise ValueError("stop_price and price are required for STOP_LIMIT orders")
                params["price"] = str(price)
                params["stopPrice"] = str(stop_price)
                params["timeInForce"] = "GTC"

            logger.info(f"Attempting to place {order_type} {side} order for {symbol} (Qty: {quantity})")
            logger.debug(f"Order params: {params}")
            
            # Execute on Futures
            response = self.client.futures_create_order(**params)
            
            logger.info(f"Order successfully placed! Order ID: {response.get('orderId')}")
            logger.debug(f"API Response: {response}")
            
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while placing order: {str(e)}")
            raise
