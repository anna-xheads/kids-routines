"""Google Sheets client for reading morning food options."""

import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsClient:
    """Client for interacting with Google Sheets."""
    
    def __init__(self, service_account_file='secrets/service_account.json', 
                 spreadsheet_id='1MZ6NRdtndGjcitSR3qKT250Ni5TPjDyinI-1o_1OcKA',
                 worksheet_name='Food'):
        """
        Initialize the Google Sheets client.
        
        Args:
            service_account_file: Path to service account JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
            worksheet_name: Name of the worksheet to access
        """
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name
        
        # Set up credentials
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(
            service_account_file,
            scopes=scopes
        )
        
        # Initialize gspread client
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)
        self.worksheet = self.spreadsheet.worksheet(worksheet_name)
    
    def get_kid_options(self, kid_name, include_sweet=False):
        """
        Get breakfast and vegetable options for a specific kid.
        
        Args:
            kid_name: Name of the kid (e.g., 'ליה' or 'דן')
            include_sweet: If True, include sweet items (Column D = מתוק/true)
            
        Returns:
            dict with 'breakfast', 'vegetables', and 'sweet_breakfast' lists
        """
        all_values = self.worksheet.get_all_values()
        
        breakfast_options = []
        vegetable_options = []
        sweet_breakfast_options = []
        
        for row in all_values:
            # Skip header rows
            if row[2] == 'שם הילד ' or not row[2]:
                continue
            
            # Check if this row is for the specified kid
            if row[2].strip() == kid_name:
                # Check if Column D (index 3) indicates sweet item
                is_sweet = len(row) > 3 and row[3] and row[3].strip() in ['מתוק', 'true', 'True', 'TRUE']
                
                # Column A (index 0) - breakfast
                if row[0] and row[0].strip():
                    if is_sweet:
                        sweet_breakfast_options.append(row[0].strip())
                    else:
                        breakfast_options.append(row[0].strip())
                
                # Column B (index 1) - vegetables
                if row[1] and row[1].strip():
                    vegetable_options.append(row[1].strip())
        
        return {
            'breakfast': breakfast_options,
            'vegetables': vegetable_options,
            'sweet_breakfast': sweet_breakfast_options
        }
    
    def get_all_kids(self):
        """
        Get list of all kids' names from the sheet.
        
        Returns:
            list of unique kid names
        """
        all_values = self.worksheet.get_all_values()
        kids = set()
        
        for row in all_values:
            # Column C (index 2) contains kid names
            if len(row) > 2 and row[2] and row[2].strip() and row[2] != 'שם הילד ':
                kids.add(row[2].strip())
        
        return sorted(list(kids))
