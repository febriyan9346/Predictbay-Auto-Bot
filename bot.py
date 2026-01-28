import os
import time
import random
import sys
import requests
from datetime import datetime, timedelta
import pytz
from colorama import Fore, Style, init
import warnings
os.system('clear' if os.name == 'posix' else 'cls')
warnings.filterwarnings('ignore')
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"
init(autoreset=True)
class AdvancedPredictBayBot:
    def __init__(self):
        self.min_bet = 7000
        self.max_bet = 9000
        self.check_interval = 10
        self.whale_threshold = 5000
        self.min_confidence = 3
        self.volume_ratio_threshold = 2.5
        self.traded_history = {}
        self.last_login_claim = {}
        self.stats = {
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'skipped': 0
        }
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    def get_wib_datetime(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib)
    def print_banner(self):
        banner = f"""
{Fore.CYAN}PREDICTBAY AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        elif level == "ANALYSIS":
            color = Fore.BLUE
            symbol = "[ANALYSIS]"
        elif level == "WHALE":
            color = Fore.YELLOW
            symbol = "[WHALE]"
        elif level == "SIGNAL":
            color = Fore.GREEN
            symbol = "[SIGNAL]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    def random_delay(self):
        delay = random.randint(1, 10)
        time.sleep(delay)
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    def load_file(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    def get_headers(self, token, is_post=False):
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {token}",
            "referer": "https://predictbay.io/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        if is_post:
            headers["content-type"] = "application/json"
            headers["origin"] = "https://predictbay.io"
        return headers
    def get_live_price(self, proxy=None):
        now = int(time.time())
        url = f"https://benchmarks.pyth.network/v1/shims/tradingview/history?symbol=Crypto.BTC%2FUSD&resolution=1&from={now-300}&to={now}"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, proxies=proxies, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if "c" in data and len(data["c"]) > 0:
                    return float(data["c"][-1])
        except:
            pass
        return None
    def get_active_market(self, token, proxy=None):
        url = "https://api.predictbay.io/api/v1/markets/simple-mode/1?frequency=10m"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=10)
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None
    def get_live_bets(self, token, market_id, proxy=None):
        """Fetch live bets data for whale tracking and sentiment analysis"""
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/bets/live?limit=80"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=10)
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None
    def get_balance(self, token, proxy=None):
        url = "https://api.predictbay.io/api/v1/users/profile"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=10)
            if res.status_code == 200:
                return float(res.json()["data"]["balance"]["available"])
        except:
            return 0.0
    def place_trade(self, token, market_id, side, amount, proxy=None):
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/trades"
        payload = {"side": side, "amount": amount}
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json=payload, proxies=proxies, timeout=10)
            return res.json()
        except:
            return None
    def claim_quest(self, token, quest_id, proxy=None):
        url = f"https://api.predictbay.io/api/v1/quests/{quest_id}/claim"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json={}, proxies=proxies, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get("success"):
                    points = data["data"].get("pointsEarned", 0)
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[✓] Claim Success! Reward: +{points} Points{Style.RESET_ALL}")
                    return "success"
            elif res.status_code == 400:
                return "already_claimed"
        except:
            pass
        return "error"
    def analyze_whale_activity(self, bets):
        """Analyze whale betting patterns"""
        if not bets:
            return {"whale_signal": None, "whale_confidence": 0}
        whales = [b for b in bets if b['amount'] >= self.whale_threshold]
        if not whales:
            return {"whale_signal": None, "whale_confidence": 0}
        whale_above = sum(b['amount'] for b in whales if b['side'] == 'above')
        whale_below = sum(b['amount'] for b in whales if b['side'] == 'below')
        total_whale_volume = whale_above + whale_below
        self.log(f"Whale Activity: {len(whales)} whales | Above: ${whale_above:,.0f} | Below: ${whale_below:,.0f}", "WHALE")
        if whale_above > whale_below * 2:
            return {"whale_signal": "above", "whale_confidence": 2, "whale_volume": whale_above}
        elif whale_below > whale_above * 2:
            return {"whale_signal": "below", "whale_confidence": 2, "whale_volume": whale_below}
        elif whale_above > whale_below * 1.5:
            return {"whale_signal": "above", "whale_confidence": 1, "whale_volume": whale_above}
        elif whale_below > whale_above * 1.5:
            return {"whale_signal": "below", "whale_confidence": 1, "whale_volume": whale_below}
        else:
            return {"whale_signal": None, "whale_confidence": 0}
    def analyze_momentum(self, bets):
        """Analyze recent betting momentum"""
        if not bets or len(bets) < 10:
            return {"momentum_signal": None, "momentum_confidence": 0}
        recent = bets[:20]
        recent_above = sum(b['amount'] for b in recent if b['side'] == 'above')
        recent_below = sum(b['amount'] for b in recent if b['side'] == 'below')
        self.log(f"Recent Momentum (20 bets): Above: ${recent_above:,.0f} | Below: ${recent_below:,.0f}", "ANALYSIS")
        if recent_above > recent_below * 2:
            return {"momentum_signal": "above", "momentum_confidence": 2}
        elif recent_below > recent_above * 2:
            return {"momentum_signal": "below", "momentum_confidence": 2}
        elif recent_above > recent_below * 1.3:
            return {"momentum_signal": "above", "momentum_confidence": 1}
        elif recent_below > recent_above * 1.3:
            return {"momentum_signal": "below", "momentum_confidence": 1}
        else:
            return {"momentum_signal": None, "momentum_confidence": 0}
    def analyze_contrarian(self, totals, pool):
        """Apply contrarian strategy when market is too lopsided"""
        if totals['above'] == 0 or totals['below'] == 0:
            return {"contrarian_signal": None, "contrarian_confidence": 0}
        ratio_below_to_above = totals['below'] / totals['above']
        ratio_above_to_below = totals['above'] / totals['below']
        below_percentage = pool['belowPercentage']
        above_percentage = pool['abovePercentage']
        self.log(f"Market Sentiment: Above: {above_percentage:.1f}% | Below: {below_percentage:.1f}%", "ANALYSIS")
        if below_percentage > 75:
            self.log(f"Contrarian Signal: Market too bearish ({below_percentage:.1f}%)", "WARNING")
            return {"contrarian_signal": "above", "contrarian_confidence": 1}
        elif above_percentage > 75:
            self.log(f"Contrarian Signal: Market too bullish ({above_percentage:.1f}%)", "WARNING")
            return {"contrarian_signal": "below", "contrarian_confidence": 1}
        else:
            return {"contrarian_signal": None, "contrarian_confidence": 0}
    def analyze_multiplier_value(self, pool):
        """Check if multiplier provides good value"""
        above_mult = pool['aboveMultiplier']
        below_mult = pool['belowMultiplier']
        if above_mult > 3.0:
            return {"value_signal": "above", "value_confidence": 1}
        elif below_mult > 3.0:
            return {"value_signal": "below", "value_confidence": 1}
        else:
            return {"value_signal": None, "value_confidence": 0}
    def advanced_analysis(self, market_info, live_price, bets_data, pool_data):
        """
        Comprehensive multi-factor analysis
        Returns: {signal, confidence (0-5), reasons}
        """
        open_price = float(market_info['openPrice'])
        price_diff = live_price - open_price if live_price else 0
        bets = bets_data.get("bets", []) if bets_data else []
        totals = bets_data.get("totals", {"above": 0, "below": 0}) if bets_data else {"above": 0, "below": 0}
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        self.log("ADVANCED MARKET ANALYSIS", "ANALYSIS")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        price_signal = None
        price_confidence = 0
        if price_diff > 50:
            price_signal = "above"
            price_confidence = 2
            self.log(f"Price Signal: STRONG BULLISH (+${price_diff:.2f})", "SIGNAL")
        elif price_diff > 20:
            price_signal = "above"
            price_confidence = 1
            self.log(f"Price Signal: BULLISH (+${price_diff:.2f})", "SIGNAL")
        elif price_diff < -50:
            price_signal = "below"
            price_confidence = 2
            self.log(f"Price Signal: STRONG BEARISH (${price_diff:.2f})", "SIGNAL")
        elif price_diff < -20:
            price_signal = "below"
            price_confidence = 1
            self.log(f"Price Signal: BEARISH (${price_diff:.2f})", "SIGNAL")
        else:
            self.log(f"Price Signal: NEUTRAL (${price_diff:.2f})", "WARNING")
        whale_analysis = self.analyze_whale_activity(bets)
        momentum_analysis = self.analyze_momentum(bets)
        contrarian_analysis = self.analyze_contrarian(totals, pool_data)
        value_analysis = self.analyze_multiplier_value(pool_data)
        signals = {
            'above': 0,
            'below': 0
        }
        total_confidence = 0
        reasons = []
        if price_signal:
            signals[price_signal] += price_confidence
            total_confidence += price_confidence
            reasons.append(f"Price: {price_signal.upper()} ({price_confidence})")
        if whale_analysis['whale_signal']:
            signals[whale_analysis['whale_signal']] += whale_analysis['whale_confidence']
            total_confidence += whale_analysis['whale_confidence']
            reasons.append(f"Whale: {whale_analysis['whale_signal'].upper()} ({whale_analysis['whale_confidence']})")
        if momentum_analysis['momentum_signal']:
            signals[momentum_analysis['momentum_signal']] += momentum_analysis['momentum_confidence']
            total_confidence += momentum_analysis['momentum_confidence']
            reasons.append(f"Momentum: {momentum_analysis['momentum_signal'].upper()} ({momentum_analysis['momentum_confidence']})")
        if contrarian_analysis['contrarian_signal']:
            signals[contrarian_analysis['contrarian_signal']] += contrarian_analysis['contrarian_confidence']
            total_confidence += contrarian_analysis['contrarian_confidence']
            reasons.append(f"Contrarian: {contrarian_analysis['contrarian_signal'].upper()} ({contrarian_analysis['contrarian_confidence']})")
        if value_analysis['value_signal']:
            signals[value_analysis['value_signal']] += value_analysis['value_confidence']
            total_confidence += value_analysis['value_confidence']
            reasons.append(f"Value: {value_analysis['value_signal'].upper()} ({value_analysis['value_confidence']})")
        if signals['above'] > signals['below'] and signals['above'] >= self.min_confidence:
            final_signal = "above"
            final_confidence = signals['above']
        elif signals['below'] > signals['above'] and signals['below'] >= self.min_confidence:
            final_signal = "below"
            final_confidence = signals['below']
        else:
            final_signal = None
            final_confidence = max(signals['above'], signals['below'])
        print(f"\n{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
        if final_signal:
            self.log(f"FINAL DECISION: {final_signal.upper()} | Confidence: {final_confidence}/5 ⭐", "SUCCESS")
            self.log(f"Factors: {' + '.join(reasons)}", "INFO")
        else:
            self.log(f"DECISION: SKIP | Confidence too low ({final_confidence}/{self.min_confidence} required)", "WARNING")
            if reasons:
                self.log(f"Conflicting signals: {' | '.join(reasons)}", "INFO")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        return {
            'signal': final_signal,
            'confidence': final_confidence,
            'reasons': reasons,
            'price_diff': price_diff
        }
    def calculate_dynamic_bet_size(self, balance, confidence, pool_data, signal):
        """Calculate bet size based on confidence and risk/reward"""
        multiplier = pool_data['aboveMultiplier'] if signal == 'above' else pool_data['belowMultiplier']
        base_bet = self.min_bet
        if confidence >= 4:
            base_bet = min(self.max_bet * 1.5, balance * 0.02)
        elif confidence >= 3:
            base_bet = min(self.max_bet, balance * 0.015)
        else:
            base_bet = self.min_bet
        if multiplier > 3:
            base_bet = base_bet * 0.8
        final_bet = max(self.min_bet, min(int(base_bet), self.max_bet, int(balance)))
        return final_bet
    def run(self):
        self.print_banner()
        choice = self.show_menu()
        use_proxy = True if choice == '1' else False
        tokens = self.load_file("accounts.txt")
        proxies = self.load_file("proxy.txt")
        if not tokens:
            self.log("File accounts.txt not foundor empty!", "ERROR")
            return
        self.log(f"Loaded {len(tokens)} accounts successfully", "INFO")
        for token in tokens:
            self.traded_history[token] = []
            self.last_login_claim[token] = ""
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            wib_now = self.get_wib_datetime()
            current_date = wib_now.strftime("%Y-%m-%d")
            if wib_now.hour >= 7:
                for i, token in enumerate(tokens):
                    if self.last_login_claim[token] != current_date:
                        proxy = proxies[i % len(proxies)] if use_proxy and proxies else None
                        status = self.claim_quest(token, "daily-login", proxy)
                        if status in ["success", "already_claimed"]:
                            self.last_login_claim[token] = current_date
            main_proxy = proxies[0] if use_proxy and proxies else None
            active_market = self.get_active_market(tokens[0], main_proxy)
            live_price = self.get_live_price(main_proxy)
            if not active_market or not active_market.get("success"):
                self.log("Market data not available, waiting...", "WARNING")
                self.countdown(5)
                continue
            market_info = active_market["data"]["market"]
            market_id = market_info["id"]
            pool_data = active_market["data"]["pool"]
            self.log(f"Market: {market_info['title'][:50]}...", "INFO")
            self.log(f"Open Price: ${float(market_info['openPrice']):,.2f} | Live: ${live_price:,.2f}", "INFO")
            bets_data = self.get_live_bets(tokens[0], market_id, main_proxy)
            if live_price and bets_data:
                analysis = self.advanced_analysis(market_info, live_price, bets_data.get("data"), pool_data)
                signal = analysis['signal']
                confidence = analysis['confidence']
            else:
                self.log("Insufficient data for analysis, skipping...", "WARNING")
                signal = None
                confidence = 0
            if signal:
                print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                success_count = 0
                for i, token in enumerate(tokens):
                    proxy = proxies[i % len(proxies)] if use_proxy and proxies else None
                    proxy_text = proxy if proxy else "No Proxy"
                    self.log(f"Account #{i+1}/{len(tokens)}", "INFO")
                    self.log(f"Proxy: {proxy_text}", "INFO")
                    balance = self.get_balance(token, proxy)
                    if balance < self.min_bet:
                        self.log(f"Insufficient Balance (${balance:.2f}) - Skip", "ERROR")
                        continue
                    self.random_delay()
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
                    amount = self.calculate_dynamic_bet_size(balance, confidence, pool_data, signal)
                    self.log(f"Executing Trade: {signal.upper()} | Amount: ${amount} | Confidence: {confidence}⭐", "INFO")
                    self.random_delay()
                    trade = self.place_trade(token, market_id, signal, amount, proxy)
                    if trade and trade.get("success"):
                        time_str = self.get_wib_time()
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Trade Success! ID: {trade['data']['trade']['id']}{Style.RESET_ALL}")
                        self.random_delay()
                        self.claim_quest(token, "daily-prediction", proxy)
                        self.random_delay()
                        self.claim_quest(token, "daily-volume", proxy)
                        success_count += 1
                        self.stats['total_trades'] += 1
                    else:
                        msg = trade.get("message") if trade else "Request Failed"
                        self.log(f"Trade Failed: {msg}", "ERROR")
                    self.random_delay()
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Balance: ${balance:.2f} | Bet: ${amount}{Style.RESET_ALL}")
                    if i < len(tokens) - 1:
                        print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                        time.sleep(2)
                print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{len(tokens)}", "CYCLE")
                if self.stats['total_trades'] > 0:
                    winrate = (self.stats['wins'] / self.stats['total_trades'] * 100) if self.stats['total_trades'] > 0 else 0
                    self.log(f"Session Stats: {self.stats['total_trades']} trades | Winrate: {winrate:.1f}%", "INFO")
                print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            else:
                self.stats['skipped'] += 1
                self.log(f"No trade signal (skipped: {self.stats['skipped']} this session)", "WARNING")
                print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            cycle += 1
            self.countdown(self.check_interval)
if __name__ == "__main__":
    bot = AdvancedPredictBayBot()
    bot.run()
