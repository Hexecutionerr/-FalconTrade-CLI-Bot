import argparse
import sys
from tabulate import tabulate
from colorama import init, Fore, Style

from .client import get_binance_client
from .orders import OrderManager
from .validators import validate_order_params, ValidationError
from .logging_config import logger

# Initialize colorama for Windows support
init(autoreset=True)

def print_summary(params):
    """Prints a clear summary of the order before execution."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- Order Summary ---")
    table = [
        ["Symbol", params['symbol']],
        ["Side", f"{Fore.GREEN if params['side'] == 'BUY' else Fore.RED}{params['side']}"],
        ["Type", params['order_type']],
        ["Quantity", params['quantity']],
    ]
    if params['price']:
        table.append(["Price", params['price']])
    
    print(tabulate(table, tablefmt="grid"))
    print(f"{Style.RESET_ALL}")

def print_result(response):
    """Prints a formatted response after execution."""
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Execution Successful")
    
    result_data = [
        ["Order ID", response.get('orderId')],
        ["Status", response.get('status')],
        ["Executed Qty", response.get('executedQty')],
        ["Avg Price", response.get('avgPrice', 'N/A')],
        ["Type", response.get('type')],
        ["Side", response.get('side')]
    ]
    
    print(tabulate(result_data, tablefmt="grid"))
    print("-" * 30)

def main():
    parser = argparse.ArgumentParser(
        description="FalconTrade - High-Performance Binance Futures Trading Bot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m bot.cli BTCUSDT BUY MARKET 0.001
  python -m bot.cli ETHUSDT SELL LIMIT 0.05 --price 2500
        """
    )
    
    parser.add_argument("symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("type", choices=["MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"], help="Order type")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price (required for LIMIT orders)")
    parser.add_argument("--stop-price", type=float, help="Stop price (required for STOP orders)")
    parser.add_argument("--paper", action="store_true", help="Force Paper Trading mode (No keys needed)")
    parser.add_argument("--balance", action="store_true", help="Check virtual balance (Paper mode only)")
    
    args = parser.parse_args()

    try:
        # 0. Initialize Client
        client = get_binance_client(paper_trading=args.paper)
        
        # 1. Handle Balance Check
        if args.balance:
            if hasattr(client, 'get_account_summary'):
                summary = client.get_account_summary()
                print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Virtual Wallet (Paper) ---")
                print(f"Balance: ${summary['balance']:.2f}")
                print(f"Positions: {summary['positions']}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Balance check only available in Paper Trading mode.")
                sys.exit(1)

        # 2. Validate Inputs
        validated_params = validate_order_params(
            symbol=args.symbol.upper(),
            side=args.side.upper(),
            order_type=args.type.upper(),
            quantity=args.quantity,
            price=args.price
        )
        
        # 3. Show Summary
        print_summary(validated_params)
        
        # 4. Confirm
        confirm = input(f"{Fore.YELLOW}Confirm execution? (y/n): {Style.RESET_ALL}")
        if confirm.lower() != 'y':
            print(f"{Fore.YELLOW}Order cancelled by user.")
            sys.exit(0)

        # 5. Initialize Manager & Place Order
        manager = OrderManager(client)
        
        response = manager.place_order(
            symbol=validated_params['symbol'],
            side=validated_params['side'],
            order_type=validated_params['order_type'],
            quantity=validated_params['quantity'],
            price=validated_params['price'],
            stop_price=args.stop_price
        )
        
        # 6. Show Result
        print_result(response)

    except ValidationError as e:
        print(f"\n{Fore.RED}Validation Error: {str(e)}")
        logger.error(f"Validation failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}")
        # Logging handled in the component layers
        sys.exit(1)

if __name__ == "__main__":
    main()
