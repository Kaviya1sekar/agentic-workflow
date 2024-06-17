from langchain.tools import tool
import requests
import json

class JiraFilterTools:
    
    @tool("Fetch Jira Ticket Data")
    def fetch_jira_data(jira_ticket_number):
        """
        Fetch Jira ticket data for the provided Jira ticket number.
        
        The input should be a string representing the Jira ticket number.
        Example: `ABC-1234`.
        """
        print(f"Fetching Jira ticket data for {jira_ticket_number}")
        fields = "description"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic cmFrc2hpdC5iaGFzaW5AZm91cmtpdGVzLmNvbTpoeDhkSGpXMkoxYnE3RmhhcXY3UDI3QzM='
        }
        url = f'https://fourkites.atlassian.net/rest/api/2/search?jql=key%20in%20({jira_ticket_number})&fields={fields}'
        print(url)
        jira_response = requests.get(url, headers=headers)
            
        if jira_response.status_code == 200:
            jira_data = jira_response.json().get("issues", [])[0].get("fields", {}).get("description", "No description available")
            return jira_data
        else:
            return f"Failed to get Jira ticket data. Error: {jira_response.text}"
    
    @tool("Write to File")
    def write_to_file(jira_ticket_data):
        """
        Write the extracted details of all the Jira tickets to a file.
        
        The input should be a string representing the extracted details of all the Jira tickets.
        Example:
        `1. Jira Ticket Number: PNG-2903
        - **API Endpoints**:
        - https://example.com/api/v1/endpoint
        - **Credentials**:
        - Token: example_api_token1234556789
        - **Headers**: Not explicitly mentioned, but the use of a token suggests Authorization headers would be used.
        - **Category**: Complex due to multiple API endpoints.`
        """

        print(f"Writing the following extracted details of all the Jira tickets to a file: {jira_ticket_data}")
        file_path = '/Users/rakshit.bhasin/Desktop/files/jira_tickets_data.json'
        with open(file_path, 'w') as file:
            json.dump(jira_ticket_data, file)
        return "Details written to file successfully."
        


