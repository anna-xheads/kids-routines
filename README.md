# Kids Morning Routines - WhatsApp Bot 🌅

Automated morning routine notifications for kids via WhatsApp using Green API.

## Overview

This bot reads breakfast and vegetable options from a Google Sheet and sends personalized WhatsApp messages to each kid with randomly selected items from their menu.

## Features

- 📊 Reads from Google Sheets (Morning_food worksheet)
- 🎲 Randomly selects breakfast and vegetable for each kid
- 📱 Sends WhatsApp messages via Green API
- ⏰ Runs daily via GitHub Actions
- 🇮🇱 Supports Hebrew text

## Setup

### Prerequisites

1. **Google Sheets API**
   - Service account JSON file with access to the spreadsheet
   - Spreadsheet ID: `1MZ6NRdtndGjcitSR3qKT250Ni5TPjDyinI-1o_1OcKA`

2. **Green API (WhatsApp)**
   - Instance ID: `7105233428`
   - API Token: `01be127289a24d33871059257b7c6ac6fac9a551f1e5425db7`
   - Target: WhatsApp Group "Feldman mornings" (`120363404296654202@g.us`)

### Installation

```bash
# Clone the repository
git clone https://github.com/anna-xheads/kids-routines.git
cd kids-routines

# Install dependencies
pip install -r requirements.txt

# Add service account credentials
mkdir -p secrets
# Copy your service_account.json to secrets/
```

### Local Testing

```bash
python send_morning_routine.py
```

## Sheet Structure

The `Morning_food` sheet should have the following columns:

| A (ארוחת בוקר) | B (ירקות) | C (שם הילד) | D (מתוק) |
|----------------|-----------|-------------|----------|
| פיתה עם זעתר   | מלפפונים   | ליה         |          |
| כריך חביתה      | זיתים     | ליה         |          |

- **Column A**: Breakfast options
- **Column B**: Vegetable options
- **Column C**: Kid's name
- **Column D**: Sweet indicator (optional)

## GitHub Actions

The workflow runs daily at 7:00 AM Israel time (5:00 AM UTC) and sends morning routine messages.

### Secrets Required

- `SERVICE_ACCOUNT_JSON`: Google service account credentials
- `GREEN_API_INSTANCE_ID`: Green API instance ID (7105233428)
- `GREEN_API_TOKEN`: Green API token

## Message Format

Each kid receives a personalized message:

```
🌅 *בוקר טוב ליה!*

🍽️ *ארוחת בוקר:* פיתה עם זעתר
🥒 *ירקות:* מלפפונים

😋 בתאבון!
```

## Files

- `send_morning_routine.py` - Main script
- `sheets_client.py` - Google Sheets integration
- `whatsapp_client.py` - Green API WhatsApp client
- `requirements.txt` - Python dependencies
- `.github/workflows/morning-routine.yml` - GitHub Actions workflow

## License

MIT
