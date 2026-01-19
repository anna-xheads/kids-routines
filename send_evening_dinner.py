"""Evening dinner lottery - sends dinner suggestions via WhatsApp with countdown."""

import random
import time
from datetime import datetime
from sheets_client import GoogleSheetsClient
from whatsapp_client import WhatsAppClient


# Configuration
INSTANCE_ID = "7105233428"
API_TOKEN = "01be127289a24d33871059257b7c6ac6fac9a551f1e5425db7"
GROUP_CHAT_ID = "120363404296654202@g.us"  # WhatsApp group "Feldman mornings"


def get_dinner_options():
    """
    Get dinner options from Food sheet.
    
    Returns:
        dict with 'main_dishes', 'vegetables', and 'extras' lists
    """
    client = GoogleSheetsClient()
    all_values = client.worksheet.get_all_values()
    
    main_dishes = []  # Column F
    vegetables = []   # Column I (always include)
    extras = []       # Column J (include if Column G = true)
    
    for row in all_values[1:]:  # Skip header
        # Pad row to have at least 10 columns
        row = row + [''] * (10 - len(row))
        
        # Column F (index 5) - Main dishes
        if row[5] and row[5].strip():
            main_dish = row[5].strip()
            # Check if G (index 6) has "true" to include extra from J
            has_extra = row[6] and row[6].strip().lower() in ['true', 'תוספת']
            main_dishes.append({
                'name': main_dish,
                'has_extra': has_extra
            })
        
        # Column I (index 8) - Vegetables (always)
        if row[8] and row[8].strip():
            vegetables.append(row[8].strip())
        
        # Column J (index 9) - Extras
        if row[9] and row[9].strip():
            extras.append(row[9].strip())
    
    return {
        'main_dishes': main_dishes,
        'vegetables': vegetables,
        'extras': extras
    }


def format_dinner_message(main_dish, vegetable, extra=None):
    """
    Format the dinner announcement message.
    
    Args:
        main_dish: Selected main dish name
        vegetable: Selected vegetable
        extra: Selected extra (can be None)
        
    Returns:
        str: Formatted message
    """
    message = f"🍽️ *{main_dish}*"
    
    if vegetable:
        message += f"\n🥗 {vegetable}"
    
    if extra:
        message += f"\n➕ {extra}"
    
    return message


def send_evening_dinner():
    """Main function to send evening dinner with countdown."""
    print("=" * 80)
    print("🌆 Evening Dinner Lottery - WhatsApp Notifications")
    print("=" * 80)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Initialize clients
        print("🔧 Initializing clients...")
        whatsapp_client = WhatsAppClient(INSTANCE_ID, API_TOKEN)
        print("   ✅ WhatsApp client initialized")
        print()
        
        # Get dinner options
        print("📊 Getting dinner options from Food sheet...")
        options = get_dinner_options()
        print(f"   ✅ Found {len(options['main_dishes'])} main dishes")
        print(f"   ✅ Found {len(options['vegetables'])} vegetables")
        print(f"   ✅ Found {len(options['extras'])} extras")
        print()
        
        # Select random options
        print("🎲 Selecting random dinner...")
        main_dish_obj = random.choice(options['main_dishes'])
        main_dish = main_dish_obj['name']
        vegetable = random.choice(options['vegetables']) if options['vegetables'] else None
        extra = random.choice(options['extras']) if main_dish_obj['has_extra'] and options['extras'] else None
        
        print(f"   🍽️  Main dish: {main_dish}")
        if vegetable:
            print(f"   🥗 Vegetable: {vegetable}")
        if extra:
            print(f"   ➕ Extra: {extra}")
        print()
        
        # Prepare messages
        intro_message = "🌆 משפחת פלדמן, הארוחת ערב המוגרלת היא..."
        countdown_messages = ["5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣"]
        result_message = format_dinner_message(main_dish, vegetable, extra)
        
        # Send intro
        print("📤 Sending intro message...")
        result = whatsapp_client.send_message(GROUP_CHAT_ID, intro_message)
        if result['success']:
            print("   ✅ Intro sent")
        time.sleep(2)
        
        # Send countdown
        print("⏳ Sending countdown...")
        for i, count_msg in enumerate(countdown_messages, 1):
            print(f"   {count_msg}")
            result = whatsapp_client.send_message(GROUP_CHAT_ID, count_msg)
            if result['success']:
                print(f"   ✅ Countdown {i}/5 sent")
            time.sleep(5)  # 5 seconds between countdown messages
        
        # Send result
        print()
        print("🎉 Sending result...")
        result = whatsapp_client.send_message(GROUP_CHAT_ID, result_message)
        if result['success']:
            print("   ✅ Result sent!")
        
        print()
        print("=" * 80)
        print("✅ Evening dinner lottery complete!")
        print("=" * 80)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    send_evening_dinner()
