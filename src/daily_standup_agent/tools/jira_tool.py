# tools/jira_tool.py
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def fetch_jira_tickets():
    if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN]):
        return "Jira credentials missing in .env file."
        
    url = f"https://{JIRA_DOMAIN}/rest/api/3/search/jql"

    jql = 'assignee = currentUser() AND status IN ("In Progress", "Done") ORDER BY updated DESC'
    
    params = {
        'jql': jql,
        'fields': ['summary', 'status', 'updated'],
        'maxResults': 50
    }
    
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    
    print(f"Connecting to Jira Domain: {JIRA_DOMAIN} via new search/jql API...")
    response = requests.get(url, headers=headers, params=params, auth=auth)
    
    if response.status_code != 200:
        return f"Error fetching Jira tickets: {response.status_code} - {response.text}"
        
    data = response.json()
    issues = data.get('issues', [])
    
    if not issues:
        return "No Jira tickets found. Make sure you have created at least one ticket on your board!"
        
    formatted_tickets = []
    for issue in issues:
        summary = issue['fields'].get('summary', 'No summary')
        status = issue['fields'].get('status', {}).get('name', 'Unknown')
        assignee = issue['fields'].get('assignee')
        assignee_name = assignee.get('displayName') if assignee else 'Unassigned'
        formatted_tickets.append(f"- [{status.upper()}] {summary} (Assignee: {assignee_name})")
        
    return "\n".join(formatted_tickets)

if __name__ == "__main__":
    print("Testing Jira API Tool (Updated Endpoint)...")
    print(fetch_jira_tickets())