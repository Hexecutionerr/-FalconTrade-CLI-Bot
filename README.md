# 🦅 FalconTrade CLI Bot

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Binance API](https://img.shields.io/badge/Binance-API-F3BA2F.svg)](https://binance-docs.github.io/apidocs/futures/en/)
[![Paper Trading](https://img.shields.io/badge/Trading-Paper%20Mode-green.svg)](#-paper-trading-no-api-keys-needed)

A production-grade, modular Python CLI application for high-performance trading on the **Binance Futures Testnet**. This bot is engineered with clean architecture principles, robust validation, and a built-in **zero-config simulator** for paper trading.

---

## ✨ Key Features

- 🛠 **Multi-Order Engine**: Seamlessly execute `MARKET`, `LIMIT`, `STOP_MARKET`, and `STOP_LIMIT` orders.
- 🧪 **Paper Trading Mode**: Zero-setup simulator that uses live market prices with a local virtual wallet ($10,000).
- 🛡 **Robust Validation**: Pre-flight checks for symbols, quantities, and price parameters to prevent API errors.
- 📊 **Professional UI**: Beautifully formatted terminal output using `tabulate` and `colorama`.
- 🕵️ **Audit Logging**: Comprehensive rotating logs stored in `trading.log` for debugging and transparency.
- 🔒 **Secure**: Credentials managed strictly via environment variables.

---

## 🏗 Project Architecture

```text
trading_bot/
├── bot/
│   ├── client.py          # Dual-mode Client (Real vs Simulator)
│   ├── simulator.py       # Paper Trading Logic & Local Wallet
│   ├── orders.py          # Order Execution Layer
│   ├── validators.py      # Input & Schema Validation
│   ├── logging_config.py  # Centralized Audit Logs
│   └── cli.py             # User Command-Line Interface
├── .env.example           # Environment template
├── requirements.txt       # System dependencies
└── README.md              # Project Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 or higher.
- [Optional] Binance Futures Testnet API Keys.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/hasnainkhan/trading-bot.git
cd trading-bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy the template and add your credentials (if using real testnet):
```bash
cp .env.example .env
```

---

## 🧪 Paper Trading (No API Keys Needed)

The bot defaults to **Paper Trading** if no API keys are found. It uses live prices from Binance's public API.

| Feature | Command |
| :--- | :--- |
| **Check Balance** | `python -m bot.cli BTCUSDT BUY MARKET 0 --balance` |
| **Place Order** | `python -m bot.cli BTCUSDT BUY MARKET 0.01` |
| **Force Paper Mode** | Add `--paper` flag to any command |

---

## ⚡ Usage Examples

### Market Order (Quick Buy/Sell)
```bash
python -m bot.cli BTCUSDT BUY MARKET 0.001
```

### Limit Order (Price Sensitive)
```bash
python -m bot.cli ETHUSDT SELL LIMIT 0.05 --price 2500
```

### Stop Market (Risk Management)
```bash
python -m bot.cli BTCUSDT SELL STOP_MARKET 0.001 --stop-price 60000
```

---

## 📈 Logging
All activities are recorded in `trading.log`. Monitor your bot's health:
```bash
tail -f trading.log
```

---

## 👨‍💻 Author

**Hasnain Khan**  
*Lead Developer & Architect*

- [GitHub](https://github.com/Hexecutionerr)
- [LinkedIn](https://www.linkedin.com/in/hasnain-khan-0ab3b2320)

---
...
---

## 🗺 Roadmap

- [ ] **Risk Management Engine**: Daily loss limits and max drawdown.
- [ ] **Technical Analysis**: RSI, Moving Averages, and MACD indicators.
- [ ] **Web Dashboard**: A React-based UI for real-time monitoring.
- [ ] **Notification System**: Telegram/Discord alerts for executed trades.

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork** the Project
2. Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the Branch (`git push origin

--

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.

*Built with ❤️ by Hasnain Khan for FalconTrade.*
