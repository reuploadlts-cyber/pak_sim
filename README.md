# Telegram Coin Bot

A modular Telegram bot built with Python and aiogram.

## Features
- Force join system
- User account panel
- Coins system
- Referral system
- Promo code redeem
- Search validation
- Admin commands
- Broadcast
- Force join management
- Promo management
- Database backup
- Logging

## Requirements
- Python 3.10+
- Telegram Bot Token

## Installation

### 1. Create virtual environment
```bash
python -m venv venv
```

### 2. Activate virtual environment
Windows:
```bash
venv\Scripts\activate
```
Linux / macOS:
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Copy `.env.example` to `.env` and fill your values.

## Run bot
```bash
python app.py
```

## Main API integration file
`bot/services/api_client.py`

## Search behavior
- Valid mobile format: `3123456789`
- Invalid mobile format: `03123456789`
- Valid CNIC format: `3460112345678`
- Successful response with records -> 1 coin deduct
- No result -> no coin deduct
- API failure -> no coin deduct

## Main admin commands
```text
/admin
/stats
/userinfo <telegram_id>
/addcoins <telegram_id> <amount>
/removecoins <telegram_id> <amount>
/ban <telegram_id>
/unban <telegram_id>
/broadcast <message>
/addforce <title> | <url> | <chat_id optional>
/listforce
/removeforce <link_id>
/createpromo <code> <coins> <max_uses>
/disablepromo <code>
/promoinfo <code>
/health
/backup
```
