import os
import time
import random
import sys
import requests
import json
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import warnings

os.system('clear' if os.name == 'posix' else 'cls')
warnings.filterwarnings('ignore')

if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class UltimatePredictBayBot:
    def __init__(self):
        self.min_bet = 100
        self.max_bet = 200
        self.check_interval = 10
        self.min_confidence = 2
        
        self.markets_config = {
            "1": {"name": "BTC", "api_id": "1", "whale_threshold": 3000, "price_threshold_strong": 30.0, "price_threshold_normal": 10.0, "precision": 2},
            "2": {"name": "ETH", "api_id": "2", "whale_threshold": 1000, "price_threshold_strong": 2.0, "price_threshold_normal": 0.5, "precision": 4},
            "3": {"name": "SOL", "api_id": "3", "whale_threshold": 1500, "price_threshold_strong": 0.25, "price_threshold_normal": 0.10, "precision": 4},
            "4": {"name": "DOGE", "api_id": "4", "whale_threshold": 800, "price_threshold_strong": 0.0005, "price_threshold_normal": 0.0002, "precision": 8},
            "5": {"name": "XRP", "api_id": "5", "whale_threshold": 1500, "price_threshold_strong": 0.005, "price_threshold_normal": 0.002, "precision": 8},
            "6": {"name": "SUI", "api_id": "6", "whale_threshold": 1200, "price_threshold_strong": 0.010, "price_threshold_normal": 0.005, "precision": 6}
        }
        
        self.stats = {'total_trades': 0, 'wins': 0, 'losses': 0}

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')

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

    def show_menu(self):
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        while True:
            choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
            if choice in ['1', '2']: return choice

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def get_headers(self, token, is_post=False):
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {token}",
            "referer": "https://predictbay.io/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }
        if is_post:
            headers["content-type"] = "application/json"
            headers["origin"] = "https://predictbay.io"
        return headers

    def get_hermes_price(self, pyth_id, proxy=None):
        if not pyth_id: return None
        clean_id = pyth_id if pyth_id.startswith("0x") else f"0x{pyth_id}"
        url = f"https://hermes.pyth.network/v2/updates/price/latest?ids[]={clean_id}&parsed=true"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, proxies=proxies, timeout=5)
            if res.status_code == 200:
                data = res.json()
                price_info = data['parsed'][0]['price']
                return float(price_info['price']) * (10 ** price_info['expo'])
        except: pass
        return None

    def get_active_market(self, token, market_api_id, proxy=None):
        url = f"https://api.predictbay.io/api/v1/markets/simple-mode/{market_api_id}?frequency=10m"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=10)
            if res.status_code == 200: return res.json()
        except: pass
        return None

    def get_live_bets(self, token, market_id, proxy=None):
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/bets/live?limit=80"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=10)
            if res.status_code == 200: return res.json()
        except: pass
        return None

    def get_balance(self, token, proxy=None):
        url = "https://api.predictbay.io/api/v1/users/profile"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=10)
            if res.status_code == 200: return float(res.json()["data"]["balance"]["available"])
        except: return 0.0

    def place_trade(self, token, market_id, side, amount, proxy=None):
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/trades"
        payload = {"side": side, "amount": amount}
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json=payload, proxies=proxies, timeout=10)
            return res.json()
        except: return None

    def claim_quest(self, token, quest_id, proxy=None):
        url = f"https://api.predictbay.io/api/v1/quests/{quest_id}/claim"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json={}, proxies=proxies, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get("success"):
                    points = data["data"].get("pointsEarned", 0)
                    self.log(f"Quest {quest_id} Claimed! Reward: +{points} Points", "SUCCESS")
        except: pass

    def advanced_analysis(self, market_info, live_price, bets_data, pool_data, config):
        open_price = float(market_info['openPrice'])
        price_diff = live_price - open_price
        bets = bets_data.get("bets", []) if bets_data else []
        
        self.log(f"Analysis {config['name']} | Diff: {price_diff:.{config['precision']}f}", "INFO")
        
        price_signal, price_confidence = None, 0
        if abs(price_diff) > config['price_threshold_strong']:
            price_signal = "above" if price_diff > 0 else "below"
            price_confidence = 2
        elif abs(price_diff) > config['price_threshold_normal']:
            price_signal = "above" if price_diff > 0 else "below"
            price_confidence = 1

        whale_signal, whale_confidence = None, 0
        whales = [b for b in bets if b['amount'] >= config['whale_threshold']]
        if whales:
            w_above = sum(b['amount'] for b in whales if b['side'] == 'above')
            w_below = sum(b['amount'] for b in whales if b['side'] == 'below')
            self.log(f"Whale detected: {len(whales)} | Above: ${w_above:,.0f} | Below: ${w_below:,.0f}", "INFO")
            if w_above > w_below * 1.5: whale_signal, whale_confidence = "above", 2
            elif w_below > w_above * 1.5: whale_signal, whale_confidence = "below", 2

        con_signal, con_confidence = None, 0
        if pool_data['belowPercentage'] > 75: con_signal, con_confidence = "above", 1
        elif pool_data['abovePercentage'] > 75: con_signal, con_confidence = "below", 1

        signals = {'above': 0, 'below': 0}
        reasons = []
        for s, c, name in [(price_signal, price_confidence, "Price"), (whale_signal, whale_confidence, "Whale"), (con_signal, con_confidence, "Sentiment")]:
            if s:
                signals[s] += c
                reasons.append(f"{name}:{s.upper()}")

        final_signal = None
        if signals['above'] > signals['below'] and signals['above'] >= self.min_confidence:
            final_signal, final_conf = "above", signals['above']
        elif signals['below'] > signals['above'] and signals['below'] >= self.min_confidence:
            final_signal, final_conf = "below", signals['below']
        else:
            final_conf = max(signals['above'], signals['below'])

        if final_signal:
            self.log(f"Decision: {final_signal.upper()} | Confidence: {final_conf}/5 | Factors: {' + '.join(reasons)}", "SUCCESS")
        else:
            self.log(f"Skip Trade | Confidence Low ({final_conf}/{self.min_confidence})", "WARNING")

        return {'signal': final_signal, 'confidence': final_conf}

    def run(self):
        self.print_banner()
        choice = self.show_menu()
        use_proxy = True if choice == '1' else False
        
        if not os.path.exists("accounts.txt"):
            self.log("accounts.txt not found!", "ERROR")
            return
            
        tokens = [l.strip() for l in open("accounts.txt", "r") if l.strip()]
        proxies = [l.strip() for l in open("proxy.txt", "r") if l.strip()] if os.path.exists("proxy.txt") else []
        
        self.log(f"Loaded {len(tokens)} accounts successfully", "INFO")
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        market_ids = ["1", "2", "3", "4", "5", "6"]
        
        while True:
            current_market_id = market_ids[(cycle - 1) % 6]
            config = self.markets_config[current_market_id]
            
            self.log(f"Cycle #{cycle} Started | Target: {config['name']}", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            main_p = proxies[0] if use_proxy and proxies else None
            active_market = self.get_active_market(tokens[0], config['api_id'], main_p)
            
            if not active_market or not active_market.get("success"):
                self.log(f"{config['name']} Market unavailable", "WARNING")
                time.sleep(5)
                cycle += 1
                continue

            market_info = active_market["data"]["market"]
            pool_data = active_market["data"]["pool"]
            pyth_id = market_info.get('pythAddress')
            live_price = self.get_hermes_price(pyth_id, main_p)
            
            if not live_price:
                self.log(f"Price feed failed for {config['name']}", "ERROR")
                time.sleep(5)
                cycle += 1
                continue

            bets_data = self.get_live_bets(tokens[0], market_info['id'], main_p)
            analysis = self.advanced_analysis(market_info, live_price, bets_data.get("data"), pool_data, config)
            
            success_count = 0
            for i, t in enumerate(tokens):
                self.log(f"Account #{i+1}/{len(tokens)}", "INFO")
                p = proxies[i % len(proxies)] if use_proxy and proxies else None
                self.log(f"Proxy: {p if p else 'No Proxy'}", "INFO")
                
                balance = self.get_balance(t, p)
                if analysis['signal'] and balance >= self.min_bet:
                    amount = max(self.min_bet, min(int(self.max_bet if analysis['confidence'] >= 3 else self.min_bet), int(balance)))
                    trade = self.place_trade(t, market_info['id'], analysis['signal'], amount, p)
                    
                    if trade and trade.get("success"):
                        self.log(f"Trade {analysis['signal'].upper()} Success! | Amount: ${amount} | ID: {trade['data']['trade']['id'][:8]}...", "SUCCESS")
                        time.sleep(1)
                        self.claim_quest(t, "daily-prediction", p)
                        self.claim_quest(t, "daily-volume", p)
                        success_count += 1
                    else:
                        self.log(f"Trade failed: {trade.get('message') if trade else 'Unknown Error'}", "ERROR")
                else:
                    self.log(f"Skip Account | No signal or balance: ${balance:.0f}", "WARNING")
                
                if i < len(tokens) - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(1)

            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{len(tokens)}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(self.check_interval)

if __name__ == "__main__":
    try:
        bot = UltimatePredictBayBot()
        bot.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
