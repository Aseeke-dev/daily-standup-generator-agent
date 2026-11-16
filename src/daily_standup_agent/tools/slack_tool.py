import requests
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def post_to_slack(standup_text):
    if not SLACK_WEBHOOK_URL:
        return "Error: Slack webhook url missing in .env file"
    
    paylod = {
        "text": standup_text
    }
    
    response = requests.post(SLACK_WEBHOOK_URL, json=paylod)
    
    if response.status_code == 200:
        return "Successfully posted standup to slack"
    
    else:
        return f"Failed to post to slack: {response.status_code} - {response.text}"
    
if __name__ == "__main__":
    print("Testing Slack Webhook Tool...")
    print(post_to_slack("🧪 Test message from Daily Stand-Up Agent!"))