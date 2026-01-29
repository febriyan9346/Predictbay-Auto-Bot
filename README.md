# PredictBay Auto Bot

[Join PredictBay Now!](https://predictbay.io/)

An automated trading bot for PredictBay cryptocurrency prediction platform with advanced market analysis.

## Features

- 🤖 **Automated Trading**: Execute trades automatically based on market analysis
- 📊 **Multi-Market Support**: Trade BTC, ETH, SOL, DOGE, XRP, and SUI
- 🐋 **Whale Detection**: Track large trades and follow smart money
- 📈 **Advanced Analysis**: Multi-factor signal generation with confidence scoring
- 🔄 **Rotating Markets**: Automatically cycles through different markets
- 🌐 **Proxy Support**: Run with or without proxy for enhanced privacy
- 🎯 **Quest Auto-Claim**: Automatically claims daily prediction and volume quests
- 📱 **Multi-Account**: Support for multiple accounts management

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/febriyan9346/Predictbay-Auto-Bot.git
cd Predictbay-Auto-Bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create configuration files:

**accounts.txt** - Add your bearer tokens (one per line):
```
Bearer_token_1
Bearer_token_2
Bearer_token_3
```

**proxy.txt** (optional) - Add your proxies (one per line):
```
http://user:pass@host:port
http://user:pass@host:port
```

## Usage

Run the bot:
```bash
python bot.py
```

Select your preferred mode:
- **Option 1**: Run with proxy
- **Option 2**: Run without proxy

The bot will:
1. Cycle through different cryptocurrency markets (BTC, ETH, SOL, DOGE, XRP, SUI)
2. Analyze market conditions using multiple factors
3. Place trades based on confidence signals
4. Automatically claim daily quests
5. Repeat the cycle with configurable intervals

## Configuration

You can modify these parameters in the code:

```python
self.min_bet = 7000          # Minimum bet amount
self.max_bet = 9000          # Maximum bet amount
self.check_interval = 10      # Seconds between cycles
self.min_confidence = 2       # Minimum confidence score to trade
```

### Market-Specific Settings

Each market has customizable parameters:
- Whale detection threshold
- Price movement thresholds (strong/normal)
- Price precision for display

## Analysis Factors

The bot uses multiple signals for decision making:

1. **Price Movement**: Compares current price vs market open price
2. **Whale Activity**: Tracks large bets and their direction
3. **Sentiment Analysis**: Analyzes pool distribution percentages

Each factor contributes to a confidence score that determines trade execution.

## Requirements

```
requests
colorama
pytz
```

## How to Get Bearer Token

1. Visit [PredictBay](https://predictbay.io/)
2. Open Browser Developer Tools (F12)
3. Go to Application/Storage → Local Storage
4. Find and copy your authentication token
5. Add to `accounts.txt` file

## Disclaimer

⚠️ **Important Notice**:
- This bot is for educational purposes only
- Cryptocurrency trading involves substantial risk
- Past performance does not guarantee future results
- Use at your own risk
- The developer is not responsible for any financial losses

## Features in Detail

### Advanced Market Analysis
- Real-time price feed from Pyth Network
- Multi-signal confidence scoring system
- Adaptive bet sizing based on confidence level

### Whale Detection
- Monitors large transactions in real-time
- Identifies dominant market direction from whales
- Adjustable threshold per cryptocurrency

### Auto Quest Claiming
- Daily prediction quest
- Daily volume quest
- Automatic reward collection

### Smart Risk Management
- Balance checking before each trade
- Configurable min/max bet amounts
- Skip trading on low confidence signals

## Troubleshooting

**Issue**: Bot can't connect to API
- Check your internet connection
- Verify your bearer token is valid
- Try using a proxy

**Issue**: Trades not executing
- Ensure sufficient balance
- Check minimum confidence threshold
- Verify market is active

**Issue**: Price feed unavailable
- Check Pyth Network status
- Verify market's Pyth address is correct

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License.

## Credits

**Developer**: FEBRIYAN

---

## Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |
