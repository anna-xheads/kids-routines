# Kids Routines - Project Summary

## ✅ Project Complete!

**Repository**: https://github.com/anna-xheads/kids-routines

---

## 📋 What Was Created

### 1. **Repository Structure**
```
kids-routines/
├── .github/workflows/
│   └── morning-routine.yml      # Daily workflow at 7:00 AM
├── secrets/
│   └── service_account.json     # Google Sheets credentials (gitignored)
├── send_morning_routine.py      # Main script
├── sheets_client.py             # Google Sheets integration
├── whatsapp_client.py           # Green API WhatsApp client
├── requirements.txt             # Python dependencies
├── setup_secrets.sh            # GitHub secrets setup script
├── .gitignore                   # Git ignore rules
└── README.md                    # Documentation
```

### 2. **Features Implemented**

✅ **Google Sheets Integration**
- Reads from `Morning_food` worksheet
- Spreadsheet ID: `1MZ6NRdtndGjcitSR3qKT250Ni5TPjDyinI-1o_1OcKA`
- Extracts breakfast options (Column A) and vegetables (Column B)
- Identifies kids by name (Column C)

✅ **WhatsApp Messaging via Green API**
- Instance ID: `7105233428`
- API Token: `01be127289a24d33871059257b7c6ac6fac9a551f1e5425db7`
- Target Phone: `972528798977`
- Sends one message per kid with:
  - Kid's name
  - Random breakfast item
  - Random vegetable item

✅ **Daily Automation**
- GitHub Actions workflow runs every day at 7:00 AM Israel time (5:00 AM UTC)
- Can be manually triggered anytime
- Automatic failure notifications

### 3. **Test Results**

**Local Test** (2026-01-19 15:50:46):
- דן: בורקס תפוח אדמה + תפוחים ✅
- ליה: פיתה עם שוקולד + סלט חתוך ✅
- 2/2 messages sent successfully

**GitHub Actions Test** (2026-01-19 13:52:10):
- דן: פיתה עם זעתר + פלפל ✅
- ליה: בורקס תפוח אדמה + סלט חתוך ✅
- 2/2 messages sent successfully
- Workflow completed in 20 seconds

---

## 🔧 Configuration

### GitHub Secrets (Already Set Up)
- ✅ `SERVICE_ACCOUNT_JSON` - Google Sheets service account
- ✅ `GREEN_API_INSTANCE_ID` - 7105233428
- ✅ `GREEN_API_TOKEN` - 01be127289a24d33871059257b7c6ac6fac9a551f1e5425db7

### Morning_food Sheet Structure
The script reads data where Column C (שם הילד) contains the kid's name:
- **Column A (ארוחת בוקר)**: Breakfast options
- **Column B (ירקות)**: Vegetable options
- **Column C (שם הילד)**: Kid's name (ליה or דן)

Current kids detected:
- דן - 7 breakfast options, 6 vegetable options
- ליה - 7 breakfast options, 3 vegetable options

---

## 📱 Message Format

Each kid receives a message like this:

```
🌅 *בוקר טוב ליה!*

🍽️ *ארוחת בוקר:* פיתה עם זעתר
🥒 *ירקות:* מלפפונים

😋 בתאבון!
```

---

## 🚀 Usage

### Manual Trigger
```bash
cd /Users/annafeldman/kids-routines
python3 send_morning_routine.py
```

Or via GitHub Actions:
```bash
gh workflow run morning-routine.yml
```

### Automatic Daily Run
The workflow runs automatically every day at **7:00 AM Israel time**.

---

## 📊 Next Steps

1. **Monitor Messages**: Check your WhatsApp (972528798977) to verify messages are received
2. **Adjust Schedule**: Edit `.github/workflows/morning-routine.yml` if you want different timing
3. **Add More Kids**: Simply add more rows in the Morning_food sheet with new names in Column C
4. **Customize Messages**: Edit `format_routine_message()` in `send_morning_routine.py`

---

## 🎉 Success Metrics

- ✅ Repository created and pushed to GitHub
- ✅ GitHub Actions workflow configured and tested
- ✅ All secrets properly configured
- ✅ Successfully sent test messages via WhatsApp
- ✅ Random selection working correctly
- ✅ Hebrew text displayed correctly
- ✅ Ready for daily automated runs

---

## 📞 Support

**Repository**: https://github.com/anna-xheads/kids-routines
**Workflow Status**: https://github.com/anna-xheads/kids-routines/actions
**Secrets**: https://github.com/anna-xheads/kids-routines/settings/secrets/actions

The system is now fully operational and will send morning routine messages automatically every day at 7:00 AM! 🌅
