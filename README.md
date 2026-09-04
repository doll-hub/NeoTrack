# NeoTrack - Competitor Price Tracker

**Version:** 2.0.0  
**Developed by:** NEO

Monitor competitor prices and get real-time alerts when they change.

## Features

- Track multiple products simultaneously
- Automatic change detection
- Email alerts on price changes
- Beautiful CLI interface
- No API keys required

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure your products
nano config.json

# Run
python adspy.py
```

Configuration

Edit config.json:

```json
{
    "products": {
        "product_id": {
            "name": "Product Name",
            "url": "https://example.com/product"
        }
    },
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender": "your_email@gmail.com",
        "password": "your_app_password",
        "recipient": "your_email@gmail.com"
    }
}
```

Requirements

· Python 3.7+
· requests, beautifulsoup4, rich

License

Proprietary - All rights reserved

Support

Contact: doll-hub
```
