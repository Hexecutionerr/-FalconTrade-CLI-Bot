import re
from typing import Optional, Dict, Any

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Validates the order parameters.
    Returns a dictionary of validated parameters or raises ValidationError.
    """
    
    # Validate Symbol (Basic check: uppercase, 3-12 chars)
    if not re.match(r'^[A-Z0-9]{3,12}$', symbol):
        raise ValidationError(f"Invalid symbol format: {symbol}. Must be uppercase alphanumeric (e.g., BTCUSDT).")
    
    # Validate Side
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValidationError(f"Invalid side: {side}. Must be BUY or SELL.")
    
    # Validate Order Type
    order_type = order_type.upper()
    valid_types = ['MARKET', 'LIMIT', 'STOP_MARKET', 'STOP_LIMIT']
    if order_type not in valid_types:
        raise ValidationError(f"Invalid order type: {order_type}. Must be one of {valid_types}.")
    
    # Validate Quantity
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than zero. Got: {quantity}")
    
    # Validate Price for LIMIT and STOP_LIMIT orders
    if order_type in ['LIMIT', 'STOP_LIMIT']:
        if price is None or price <= 0:
            raise ValidationError(f"Price is required and must be greater than zero for {order_type} orders.")
            
    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price
    }
