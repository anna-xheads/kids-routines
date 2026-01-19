#!/usr/bin/env python3
"""
Send weekly shopping list from SuperList sheet to WhatsApp group.
Organizes items by category for easy shopping.
"""

import os
import sys
from collections import defaultdict
from sheets_client import GoogleSheetsClient
from whatsapp_client import WhatsAppClient

# Target group
SHOPPING_GROUP_ID = "120363408230160930@g.us"  # קניות סופר 🛒


def get_shopping_list():
    """Get all shopping items grouped by category."""
    sheets_client = GoogleSheetsClient(
        service_account_file='secrets/service_account.json',
        spreadsheet_id='1MZ6NRdtndGjcitSR3qKT250Ni5TPjDyinI-1o_1OcKA',
        worksheet_name='SuperList'
    )
    
    # Get all values (skip header row)
    values = sheets_client.worksheet.get_all_values()
    
    # Group items by category
    items_by_category = defaultdict(list)
    
    for row in values[1:]:  # Skip header
        if len(row) >= 3 and row[0].strip():  # Has product name
            product = row[0].strip()
            quantity = row[1].strip() if len(row) > 1 else ""
            category = row[2].strip() if len(row) > 2 else "אחר"
            
            # Format item with quantity if specified
            if quantity:
                item = f"{product} - {quantity}"
            else:
                item = product
            
            items_by_category[category].append(item)
    
    return dict(items_by_category)


def format_shopping_message(items_by_category):
    """Format shopping list message with categories."""
    message = "🛒 *רשימת קניות שבועית*\n\n"
    
    # Sort categories for consistent ordering
    categories = sorted(items_by_category.keys())
    
    for category in categories:
        if not category:
            continue
            
        message += f"📌 *{category}*\n"
        
        for item in items_by_category[category]:
            message += f"• {item}\n"
        
        message += "\n"
    
    message += "בהצלחה בקניות! 🎯"
    
    return message


def main():
    try:
        print("📊 Getting shopping list from SuperList sheet...")
        items_by_category = get_shopping_list()
        
        if not items_by_category:
            print("❌ No items found in SuperList")
            return
        
        # Count total items
        total_items = sum(len(items) for items in items_by_category.values())
        print(f"✅ Found {total_items} items in {len(items_by_category)} categories")
        
        # Format message
        message = format_shopping_message(items_by_category)
        
        print("\n📝 Shopping list message:")
        print("=" * 50)
        print(message)
        print("=" * 50)
        
        # Send to WhatsApp
        print(f"\n📤 Sending to קניות סופר group...")
        whatsapp_client = WhatsAppClient(
            instance_id=os.environ.get('GREEN_API_INSTANCE_ID', '7105233428'),
            api_token=os.environ.get('GREEN_API_TOKEN', '01be127289a24d33871059257b7c6ac6fac9a551f1e5425db7')
        )
        
        result = whatsapp_client.send_message(SHOPPING_GROUP_ID, message)
        
        if result:
            print("✅ Shopping list sent successfully!")
        else:
            print("❌ Failed to send shopping list")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
