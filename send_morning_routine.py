"""Daily kids' morning routine - sends random breakfast options via WhatsApp."""

import random
from datetime import datetime
from sheets_client import GoogleSheetsClient
from whatsapp_client import WhatsAppClient


# Configuration
INSTANCE_ID = "7105233428"
API_TOKEN = "01be127289a24d33871059257b7c6ac6fac9a551f1e5425db7"
GROUP_CHAT_ID = "120363404296654202@g.us"  # WhatsApp group "Feldman mornings"


def format_routine_message(kid_name, breakfast, vegetable):
    """
    Format a morning routine message for a kid.
    
    Args:
        kid_name: Name of the kid
        breakfast: Selected breakfast item
        vegetable: Selected vegetable (can be None)
        
    Returns:
        str: Formatted message
    """
    message = f"🌅 *בוקר טוב {kid_name}!*\n\n"
    message += f"🍽️ *ארוחת בוקר:* {breakfast}\n"
    
    if vegetable:
        message += f"🥒 *ירקות:* {vegetable}\n"
    
    message += f"\n😋 בתאבון!"
    
    return message


def send_morning_routines():
    """Main function to send morning routines to all kids."""
    print("=" * 80)
    print("🌅 Kids Morning Routine - WhatsApp Notifications")
    print("=" * 80)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if today is Friday (weekday() returns 4 for Friday)
    is_friday = datetime.now().weekday() == 4
    if is_friday:
        print("🎉 Today is Friday - Sweet items enabled!")
    print()
    
    try:
        # Initialize clients
        print("🔧 Initializing clients...")
        sheets_client = GoogleSheetsClient()
        whatsapp_client = WhatsAppClient(INSTANCE_ID, API_TOKEN)
        print("   ✅ Sheets client initialized")
        print("   ✅ WhatsApp client initialized")
        print()
        
        # Get all kids
        print("👶 Getting kids list...")
        kids = sheets_client.get_all_kids()
        print(f"   ✅ Found {len(kids)} kids: {', '.join(kids)}")
        print()
        
        # Prepare messages for each kid
        messages = []
        
        for kid_name in kids:
            print(f"🎲 Selecting options for {kid_name}...")
            
            # Get options for this kid
            options = sheets_client.get_kid_options(kid_name, include_sweet=is_friday)
            
            # Combine regular and sweet breakfast options based on day
            all_breakfast_options = options['breakfast'].copy()
            if is_friday and options['sweet_breakfast']:
                all_breakfast_options.extend(options['sweet_breakfast'])
                print(f"   🍰 Added {len(options['sweet_breakfast'])} sweet options for Friday!")
            
            if not all_breakfast_options:
                print(f"   ⚠️  No breakfast options found for {kid_name}, skipping...")
                continue
            
            # Randomly select breakfast
            breakfast = random.choice(all_breakfast_options)
            
            # Check if selected item is sweet
            is_sweet_item = breakfast in options['sweet_breakfast']
            if is_sweet_item:
                print(f"   🍽️  Breakfast: {breakfast} 🍰 (Sweet)")
            else:
                print(f"   🍽️  Breakfast: {breakfast}")
            
            # Randomly select vegetable (if available)
            vegetable = None
            if options['vegetables']:
                vegetable = random.choice(options['vegetables'])
                print(f"   🥒 Vegetable: {vegetable}")
            else:
                print(f"   ℹ️  No vegetables available")
            
            # Format message
            message = format_routine_message(kid_name, breakfast, vegetable)
            messages.append(message)
            print()
        
        # Send all messages
        if messages:
            print(f"📤 Sending {len(messages)} WhatsApp messages to group 'Feldman mornings'...")
            print()
            
            results = whatsapp_client.send_messages_with_delay(
                GROUP_CHAT_ID, 
                messages, 
                delay=3  # 3 seconds between messages
            )
            
            # Summary
            print()
            print("=" * 80)
            print("📊 Summary:")
            successful = sum(1 for r in results if r['success'])
            print(f"   ✅ Messages sent successfully: {successful}/{len(results)}")
            
            if successful < len(results):
                print(f"   ❌ Failed messages: {len(results) - successful}")
            
            print("=" * 80)
            print("✅ Morning routine complete!")
            print("=" * 80)
        else:
            print("⚠️  No messages to send")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    send_morning_routines()
