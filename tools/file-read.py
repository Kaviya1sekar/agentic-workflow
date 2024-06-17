from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain_community.tools.gmail.send_message import GmailSendMessage
from langchain.tools import tool

class EmailTools:
    
    @tool("Create Draft")
    def create_draft(data):
        """
        Create an email draft.
        The input should be a pipe (|) separated string of length three, representing:
        - recipient's email address
        - subject of the email
        - message content
        
        Example: `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`
        """
        try:
            email, subject, message = data.split('|')
            gmail = GmailToolkit()
            draft = GmailCreateDraft(api_resource=gmail.api_resource)
            result = draft({
                'to': [email],
                'subject': subject,
                'message': message
            })
            return f"\nDraft created: {result}\n"
        
        except ValueError:
            return "Error: Input should be a pipe-separated string with exactly three parts."
        
        except Exception as e:
            return f"An error occurred: {e}"

    @tool("Send Mail")
    def send_mail(data):
        """
        Create an email draft.
        The input should be a pipe (|) separated string of length three, representing:
        - recipient's email address.
        - subject of the email 
        - message content
        
        Example: `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`
        """
        try:
            email, subject, message = data.split('|')
            gmail = GmailToolkit()
            draft= GmailSendMessage(api_resource=gmail.api_resource)
            result = draft({
                'to': [email],
                'subject': subject,
                'message': message
            })
            return f"\nMail sent: {result}\n"
        
        except ValueError:
            return "Error: Input should be a pipe-separated string with exactly three parts."
        
        except Exception as e:
            return f"An error occurred: {e}"

