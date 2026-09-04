# 🚀 NeoTrack

**Professional Competitor Price Intelligence System**

Track competitor prices, get instant email alerts, and make data-driven decisions.

---

## ✨ Features

- 🔍 Track multiple competitor products
- 📧 Instant email alerts on price changes
- 📊 Beautiful CLI interface with colors and tables
- 🎯 No API keys required - 100% free to use
- 💰 Save money by making informed pricing decisions
- 📈 Track price history and trends

---

## 🎯 Perfect For

- **E-commerce store owners** - Monitor competitor pricing
- **Dropshippers** - Find winning products and track margins
- **Product managers** - Stay ahead of market trends
- **Marketing agencies** - Provide competitive intelligence to clients
- **Small business owners** - Make data-driven decisions

---

## 📦 Quick Start

### 1. Setup Your Configuration

Open the setup wizard:
👉 **https://doll-hub.github.io/neotrack/

Add your products and download `config.json`

### 2. Install Dependencies

```bash
pip install -r requirements.txt

3. Place Config File

Put your downloaded config.json in the NeoTrack folder.

4. Start Monitoring

```bash
python neotrack.py
```

---

📸 Example Output

```
┌─────────────────────────────────┐
│  NeoTrack v2.0.0                │
│  Developed by NEO               │
└─────────────────────────────────┘

Monitoring 3 products...
Press Ctrl+C to stop

Scanning... ████████████████████ 100%

┌──────────────────────────────────────────────────────────────┐
│ Scan Results                                                │
├───┬───────────────┬─────────┬──────────┬──────────┬────────┤
│ # │ Product       │ Status  │ Price    │ Previous │ Checked│
├───┼───────────────┼─────────┼──────────┼──────────┼────────┤
│ 1 │ Apple Watch   │ CHANGED │ $349.00  │ $399.00  │ 2026-..│
│ 2 │ Samsung Buds  │ OK      │ $129.99  │ —        │ 2026-..│
│ 3 │ Sony Headph.  │ NEW     │ $199.00  │ —        │ 2026-..│
└───┴───────────────┴─────────┴──────────┴──────────┴────────┘

┌─────────────────────────────────┐
│ Scan Summary                    │
│   Total Products:  3            │
│   New:             1            │
│   Unchanged:       1            │
│   Changed:         1            │
│   Errors:          0            │
└─────────────────────────────────┘

✓ Email alert sent
Completed in 3.45s | 2026-09-04 12:00:00
```

---

📧 Email Alerts

When a price changes, you'll receive a professional email alert:

```
Subject: NeoTrack Alert - 1 product(s) changed

Product: Apple Watch
  Price changed: $399.00 → $349.00
  Title: Apple Watch Series 9
```

---

🛠️ Requirements

· Python 3.7+
· requests
· beautifulsoup4
· lxml
· colorama
· rich

---

📂 Project Structure

```
neotrack/
├── neotrack.py          # Main application
├── config.json          # Your configuration
├── data.json            # Price history (auto-generated)
├── requirements.txt     # Dependencies
├── README.md            # This file
└── index.html           # Setup wizard
```

---

🔧 Configuration Example

```json
{
    "products": {
        "product_1": {
            "name": "Apple Watch Series 9",
            "url": "https://amazon.com/dp/B0CHX7R8KJ"
        },
        "product_2": {
            "name": "Samsung Galaxy Buds",
            "url": "https://bestbuy.com/samsung-buds"
        }
    },
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender": "your_email@gmail.com",
        "password": "your_app_password",
        "recipient": "your_email@gmail.com"
    },
    "app": {
        "name": "NeoTrack",
        "version": "2.0.0",
        "developer": "NEO"
    }
}
```

---

🤝 Contributing

Contributions are welcome! Please submit a Pull Request.

---

📄 License

Proprietary - All rights reserved

---

👨‍💻 Developed By

NEO

· GitHub: doll-hub
· Project: NeoTrack

---

🌟 Support

If you find NeoTrack useful:

· ⭐ Star the repository
· 🐛 Report issues
· 💡 Suggest features

---

📞 Contact

For support or inquiries: duckduckcomme@proton.me
--- 
                 
Made with love  by NEO

```
