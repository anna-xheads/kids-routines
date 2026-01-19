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
    
    def send_message(self, chat_id, message):
        """
        Send a WhatsApp message.
        
        Args:
            chat_id: Chat ID (phone number like '972528798977@c.us' or group like '120363404296654202@g.us')
            message: Text message to send
            
        Returns:
            dict: API response
        """
        url = f"{self.base_url}/sendMessage/{self.api_token}"
        
        # If chat_id doesn't contain @, assume it's a phone number and add @c.us
        if '@' not in chat_id:
            chat_id = f"{chat_id}@c.us"
        
        payload = {
            "chatId": chat_id,
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
    
    def send_messages_with_delay(self, chat_id, messages, delay=2):
        """
        Send multiple messages with a delay between them.
        
        Args:
            chat_id: Chat ID (phone number or group)
            messages: List of message strings
            delay: Seconds to wait between messages
            
        Returns:
            list: Results for each message
        """
        results = []
        
        for i, message in enumerate(messages):
            print(f"📤 Sending message {i+1}/{len(messages)}...")
            result = self.send_message(chat_id, message)
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
