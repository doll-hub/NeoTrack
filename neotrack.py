#!/usr/bin/env python3
"""
NeoTrack - Competitor Price Tracker
Version: 2.0.0
Developed by: NEO
License: Proprietary
"""

import requests
from bs4 import BeautifulSoup
import json
import hashlib
from datetime import datetime
import os
import sys
import time
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich import box

# Initialize
init(autoreset=True)
console = Console()

# ============ CONSTANTS ============
CONFIG_FILE = 'config.json'
DATA_FILE = 'data.json'
VERSION = "2.0.0"
DEVELOPER = "NEO"

# ============ MAIN CLASS ============
class NeoTrack:
    def __init__(self):
        self.config = self.load_config()
        self.data = self.load_data()
        self.results = []
        self.app_name = self.config.get('app', {}).get('name', 'NeoTrack')
        self.version = self.config.get('app', {}).get('version', VERSION)
        self.developer = self.config.get('app', {}).get('developer', DEVELOPER)
    
    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            console.print(f"[red]Error: {CONFIG_FILE} not found[/red]")
            sys.exit(1)
        except json.JSONDecodeError:
            console.print(f"[red]Error: Invalid JSON in {CONFIG_FILE}[/red]")
            sys.exit(1)
    
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self):
        data = {}
        for r in self.results:
            data[r['id']] = {
                'title': r['title'],
                'price': r['price'],
                'fingerprint': r['fingerprint'],
                'checked': r['checked']
            }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def scrape(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        title = soup.find('h1')
        title = title.text.strip() if title else "Unknown"
        
        price = None
        for sel in ['p.price_color', '.price', '.product-price', '.current-price']:
            el = soup.select_one(sel)
            if el:
                price = el.text.strip()
                break
        price = price or "N/A"
        
        fp = hashlib.sha256(f"{title}|{price}".encode()).hexdigest()[:16]
        
        return {'title': title, 'price': price, 'fingerprint': fp}
    
    def check_product(self, pid, info):
        name = info.get('name', pid)
        url = info.get('url', '')
        
        try:
            current = self.scrape(url)
            checked = datetime.now().isoformat()
            
            status = 0
            old_price = None
            
            if pid in self.data:
                prev = self.data[pid]
                if current['fingerprint'] != prev.get('fingerprint', ''):
                    status = 2
                    old_price = prev.get('price')
                else:
                    status = 1
            
            return {
                'id': pid,
                'name': name,
                'title': current['title'],
                'price': current['price'],
                'fingerprint': current['fingerprint'],
                'status': status,
                'old_price': old_price,
                'checked': checked,
                'error': None
            }
        except Exception as e:
            return {
                'id': pid,
                'name': name,
                'title': 'Error',
                'price': 'N/A',
                'fingerprint': '',
                'status': 3,
                'old_price': None,
                'checked': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def send_email(self, changes):
        email = self.config.get('email', {})
        if not email.get('enabled', False):
            return
        
        try:
            msg = MIMEMultipart()
            msg['Subject'] = f"NeoTrack Alert - {len(changes)} changes"
            msg['From'] = email['sender']
            msg['To'] = email['recipient']
            
            body = f"NeoTrack v{self.version} - Alert\n"
            body += "="*50 + "\n\n"
            
            for c in changes:
                body += f"Product: {c['name']}\n"
                if c['status'] == 2:
                    body += f"  Price changed: {c['old_price']} → {c['price']}\n"
                elif c['status'] == 0:
                    body += f"  New product detected: {c['price']}\n"
                body += f"  Title: {c['title']}\n\n"
            
            body += "="*50 + "\n"
            body += f"NeoTrack v{self.version} | Developed by {self.developer}"
            
            msg.attach(MIMEText(body, 'plain'))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(email['smtp_server'], email['smtp_port']) as server:
                server.starttls(context=context)
                server.login(email['sender'], email['password'])
                server.send_message(msg)
            
            console.print("[green]✓ Email alert sent[/green]")
        except Exception as e:
            console.print(f"[yellow]Email failed: {e}[/yellow]")
    
    def display_header(self):
        header = Panel(
            f"[bold cyan]{self.app_name}[/bold cyan] v{self.version}\n"
            f"[dim]Developed by {self.developer}[/dim]",
            border_style="cyan",
            padding=(1, 2),
            box=box.ROUNDED
        )
        console.print(header)
        console.print()
    
    def display_results(self):
        table = Table(
            title="[bold]Scan Results[/bold]",
            box=box.HEAVY_HEAD,
            header_style="bold cyan"
        )
        table.add_column("#", width=4)
        table.add_column("Product", style="white", no_wrap=False)
        table.add_column("Status", style="bold")
        table.add_column("Price", style="yellow")
        table.add_column("Previous", style="dim")
        table.add_column("Checked", style="dim")
        
        status_labels = {0: "NEW", 1: "OK", 2: "CHANGED", 3: "ERROR"}
        status_colors = {0: "green", 1: "blue", 2: "red", 3: "yellow"}
        
        for i, r in enumerate(self.results, 1):
            status = r['status']
            price_display = r['price']
            old_display = r['old_price'] or "—"
            
            if status == 2:
                price_display = f"[green]{r['price']}[/green]"
                old_display = f"[red]{r['old_price']}[/red]"
            elif status == 3:
                price_display = "[red]ERROR[/red]"
            
            checked = r['checked'][:16] if r['checked'] else "—"
            
            table.add_row(
                str(i),
                r['name'][:35],
                f"[{status_colors[status]}]{status_labels[status]}[/{status_colors[status]}]",
                price_display,
                old_display,
                checked
            )
        
        console.print(table)
    
    def display_summary(self):
        total = len(self.results)
        changed = sum(1 for r in self.results if r['status'] == 2)
        new = sum(1 for r in self.results if r['status'] == 0)
        ok = sum(1 for r in self.results if r['status'] == 1)
        errors = sum(1 for r in self.results if r['status'] == 3)
        
        summary = Panel(
            f"[bold]Scan Summary[/bold]\n"
            f"  Total Products:  {total}\n"
            f"  [green]New:         {new}[/green]\n"
            f"  [blue]Unchanged:   {ok}[/blue]\n"
            f"  [red]Changed:     {changed}[/red]\n"
            f"  [yellow]Errors:      {errors}[/yellow]",
            border_style="bright_blue",
            padding=(1, 2),
            box=box.ROUNDED
        )
        console.print(summary)
    
    def display_footer(self, start_time):
        elapsed = time.time() - start_time
        footer = Panel(
            f"[dim]Completed in {elapsed:.2f}s  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  {self.app_name} v{self.version}[/dim]",
            border_style="dim",
            padding=(0, 1)
        )
        console.print(footer)
    
    def run(self):
        import time
        start_time = time.time()
        
        console.clear()
        self.display_header()
        
        products = self.config.get('products', {})
        if not products:
            console.print("[red]No products configured in config.json[/red]")
            return
        
        console.print(f"[cyan]Monitoring {len(products)} products...[/cyan]")
        console.print("[dim]Press Ctrl+C to stop[/dim]")
        console.print()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning...", total=len(products))
            for pid, info in products.items():
                result = self.check_product(pid, info)
                self.results.append(result)
                progress.update(task, advance=1)
        
        self.save_data()
        
        console.print()
        self.display_results()
        self.display_summary()
        
        changes = [r for r in self.results if r['status'] in [0, 2]]
        if changes:
            self.send_email(changes)
        
        self.display_footer(start_time)

# ============ MAIN EXECUTION ============
if __name__ == "__main__":
    try:
        NeoTrack().run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Scan interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)
