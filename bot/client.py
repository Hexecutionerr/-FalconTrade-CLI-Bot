import os
from binance.client import Client
from dotenv import load_dotenv
from .logging_config import logger
from .simulator import Simulator

# Load environment variables
load_dotenv()

def get_binance_client(paper_trading=False):
    """
    Initializes and returns a client. 
    Returns a Simulator if paper_trading=True or keys are missing.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    # Check if we should use Paper Trading
    if paper_trading or not api_key or not api_secret:
        if not api_key or not api_secret:
            logger.info("API Keys missing. Falling back to Paper Trading (Simulator).")
        else:
            logger.info("Paper Trading mode explicitly requested.")
        return Simulator()
    
    try:
        # Initialize client for Testnet
        client = Client(api_key, api_secret, testnet=True)
        logger.info("Successfully initialized Binance Futures Testnet client.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Binance client: {str(e)}")
        logger.info("Falling back to Paper Trading due to connection error.")
        return Simulator()
