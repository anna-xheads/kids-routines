"""Green API WhatsApp client for sending messages."""

import requests
import time


class WhatsAppClient:
    """Client for sending WhatsApp messages via Green API."""
    
    def __init__(self, instance_id, api_token):
        """
        Initialize the WhatsApp client.
        
        Args:
            instance_id: Green API instance ID
            api_token: Green API token
        """
        self.instance_id = instance_id
        self.api_token = api_token
        self.base_url = f"https://api.green-api.com/waInstance{instance_id}"
    
    def send_message(self, phone_number, message):
        """
        Send a WhatsApp message.
        
        Args:
            phone_number: Phone number in international format (e.g., '972528798977')
            message: Text message to send
            
        Returns:
            dict: API response
        """
        url = f"{self.base_url}/sendMessage/{self.api_token}"
        
        payload = {
            "chatId": f"{phone_number}@c.us",
            "message": message
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_messages_with_delay(self, phone_number, messages, delay=2):
        """
        Send multiple messages with a delay between them.
        
        Args:
            phone_number: Phone number to send to
            messages: List of message strings
            delay: Seconds to wait between messages
            
        Returns:
            list: Results for each message
        """
        results = []
        
        for i, message in enumerate(messages):
            print(f"📤 Sending message {i+1}/{len(messages)}...")
            result = self.send_message(phone_number, message)
            results.append(result)
            
            if result['success']:
                print(f"   ✅ Message sent successfully")
            else:
                print(f"   ❌ Failed to send message: {result.get('error')}")
            
            # Wait before sending next message (except for the last one)
            if i < len(messages) - 1:
                print(f"   ⏳ Waiting {delay} seconds...")
                time.sleep(delay)
        
        return results
