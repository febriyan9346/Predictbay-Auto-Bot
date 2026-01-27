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

class PredictBayBot:
    def __init__(self):
        self.min_bet = 100
        self.max_bet = 200
        self.price_threshold = 3.0  
        self.check_interval = 10
        self.traded_history = {}
        self.last_login_claim = {}

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
            res = requests.get(url, headers=self.get_headers(token, is_post=False), proxies=proxies, timeout=10)
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None

    def get_balance(self, token, proxy=None):
        url = "https://api.predictbay.io/api/v1/users/profile"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token, is_post=False), proxies=proxies, timeout=10)
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
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Claim Success! Reward: +{points} Points{Style.RESET_ALL}")
                    return "success"
            elif res.status_code == 400:
                return "already_claimed"
        except:
            pass
        return "error"

    def run(self):
        self.print_banner()
        choice = self.show_menu()
        
        use_proxy = True if choice == '1' else False
        tokens = self.load_file("accounts.txt")
        proxies = self.load_file("proxy.txt")
        
        if not tokens:
            self.log("File accounts.txt not found or empty!", "ERROR")
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
            open_price = float(market_info["openPrice"])
            
            price_diff = live_price - open_price if live_price else 0
            
            self.log(f"Market: {market_info['title'][:40]}...", "INFO")
            self.log(f"Price: Open {open_price} | Live {live_price} (Diff: {price_diff:.2f})", "INFO")
            
            signal = None
            if live_price:
                if price_diff > self.price_threshold:
                    signal = "above"
                    self.log(f"Signal: ABOVE (Strong Trend Detected: +{price_diff:.2f})", "INFO")
                elif price_diff < -self.price_threshold:
                    signal = "below"
                    self.log(f"Signal: BELOW (Strong Trend Detected: {price_diff:.2f})", "INFO")
                else:
                    self.log("Price flat/sideways, skipping...", "WARNING")
            else:
                self.log("Waiting for live price data...", "WARNING")
            
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
                        self.log(f"Insufficient Balance ({balance}) - Skip", "ERROR")
                        continue
                    
                    self.random_delay()
                    
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
                    
                    self.log(f"Processing Task:", "INFO")
                    
                    safe_max = min(self.max_bet, int(balance))
                    amount = random.randint(self.min_bet, safe_max)
                    
                    self.random_delay()
                    
                    trade = self.place_trade(token, market_id, signal, amount, proxy)
                    
                    if trade and trade.get("success"):
                        time_str = self.get_wib_time()
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Trade Success! ID: {trade['data']['trade']['id']}{Style.RESET_ALL}")
                        self.random_delay()
                        self.claim_quest(token, "daily-prediction", proxy)
                        success_count += 1
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
                print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(self.check_interval)

if __name__ == "__main__":
    bot = PredictBayBot()
    bot.run()
