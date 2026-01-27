# PredictBay Auto Bot

🔗 **[Join PredictBay Now!](https://predictbay.io/?r=QVYL9HXQOW)**

---

## 📋 Overview

PredictBay Auto Bot is an automated trading bot designed for the PredictBay prediction market platform. It automatically analyzes Bitcoin price movements and places strategic trades based on market trends.

## ✨ Features

- 🤖 **Automated Trading** - Places trades automatically based on price analysis
- 📊 **Real-time Price Tracking** - Monitors live BTC/USD prices from Pyth Network
- 🎯 **Smart Signal Detection** - Identifies strong market trends (Above/Below)
- 💰 **Balance Management** - Automatic balance checking and bet sizing
- 🎁 **Auto Quest Claiming** - Claims daily login and prediction rewards
- 🔄 **Multi-Account Support** - Manage multiple accounts simultaneously
- 🌐 **Proxy Support** - Optional proxy configuration for enhanced privacy
- ⏰ **WIB Timezone** - Uses Indonesia Western Time (WIB) for logging
- 🎨 **Colorful Console Output** - Easy-to-read colored terminal interface

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/febriyan9346/Predictbay-Auto-Bot.git
   cd Predictbay-Auto-Bot
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your accounts:**
   - Create `accounts.txt` in the root directory
   - Add your PredictBay authorization tokens (one per line)
   
   Example:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

4. **(Optional) Configure proxies:**
   - Create `proxy.txt` in the root directory
   - Add your proxy addresses (one per line)
   
   Example:
   ```
   http://user:pass@proxy1.example.com:8080
   http://user:pass@proxy2.example.com:8080
   ```

### 🔑 How to Get Your Authorization Token

1. Visit [PredictBay](https://predictbay.io/?r=QVYL9HXQOW) and log in
2. Open your browser's Developer Tools (F12)
3. Go to the **Network** tab
4. Refresh the page or perform any action
5. Look for requests to `api.predictbay.io`
6. Find the **Authorization** header (starts with "Bearer ")
7. Copy the token (everything after "Bearer ")
8. Paste it into `accounts.txt`

## 💻 Usage

Run the bot:

```bash
python bot.py
```

### Menu Options

When you start the bot, you'll be presented with a menu:

```
1. Run with proxy
2. Run without proxy
```

Select your preferred mode by entering `1` or `2`.

### Configuration

You can adjust the following parameters in the `PredictBayBot` class:

```python
self.min_bet = 100              # Minimum bet amount
self.max_bet = 200              # Maximum bet amount
self.price_threshold = 3.0      # Price difference threshold for trading
self.check_interval = 10        # Seconds between cycles
```

## 📊 Trading Logic

The bot uses a simple but effective trading strategy:

1. **Price Monitoring**: Fetches real-time BTC/USD prices from Pyth Network
2. **Trend Detection**: Compares live price with market open price
3. **Signal Generation**:
   - **ABOVE**: When live price is $3+ higher than open price
   - **BELOW**: When live price is $3+ lower than open price
4. **Trade Execution**: Places trades based on detected signals
5. **Quest Claiming**: Automatically claims daily rewards

## 📁 File Structure

```
Predictbay-Auto-Bot/
│
├── bot.py              # Main bot script
├── accounts.txt        # Your authorization tokens (one per line)
├── proxy.txt          # Optional proxy list (one per line)
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── .gitignore        # Git ignore rules
```

## ⚙️ Features in Detail

### Multi-Account Management
- Process multiple accounts in sequence
- Individual balance tracking
- Automatic login and authentication

### Smart Trading
- Random bet amounts within configured range
- Balance-aware betting (won't bet more than available)
- Automatic retry on failed trades

### Quest System
- Auto-claims daily login rewards (after 7 AM WIB)
- Auto-claims daily prediction rewards
- Tracks claimed status per account

### Safety Features
- Error handling for network issues
- Balance verification before trading
- Configurable delays between actions
- Proxy rotation support

## 🛡️ Security & Privacy

- Your tokens are stored locally in `accounts.txt`
- Never share your `accounts.txt` file
- The bot does not send your credentials anywhere except PredictBay API
- Use proxies for additional privacy if needed

## ⚠️ Disclaimer

- This bot is for educational purposes only
- Use at your own risk
- Always be aware of the risks involved in trading
- The author is not responsible for any losses incurred
- Make sure to comply with PredictBay's Terms of Service

## 🐛 Troubleshooting

### "File accounts.txt not found or empty!"
- Make sure you've created `accounts.txt` in the same directory as `bot.py`
- Ensure the file contains at least one valid token

### "Insufficient Balance"
- Check your PredictBay account balance
- Lower the `min_bet` value in the code if needed

### "Market data not available"
- Check your internet connection
- Verify that PredictBay API is accessible
- If using proxies, ensure they're working correctly

### Connection Issues
- Try running without proxies first
- Check if your proxies are active and properly formatted
- Verify your authorization tokens are still valid

## 📝 Changelog

### Version 1.0.0
- Initial release
- Multi-account support
- Proxy support
- Auto quest claiming
- Real-time price tracking
- Colored console output

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/febriyan9346/Predictbay-Auto-Bot/issues).

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**FEBRIYAN**

- GitHub: [@febriyan9346](https://github.com/febriyan9346)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

## 💰 Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|----------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

---

**Made with ❤️ by FEBRIYAN**
