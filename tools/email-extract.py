from langchain.tools import tool
import json

@tool("JSON Writer")
def json_writer(data):
    """
    Write the entries to a JSON file.
    The input should be a pipe (|) separated string of length four (4), representing:
    - threadId
    - email_id
    - summary
    - sender's email address
    
    Example: `35ef654e4|76fg65hj32|Nice To Meet You|lorem@ipsum.com`
    """
    try:
        thread_id, email_id, summary, sender = data.split('|')
        
        # Validate IDs
        if len(thread_id) != 16:
            return "Thread ID is invalid. Please fetch the data again and retry."
        if len(email_id) != 16:
            return "Email ID is invalid. Please fetch the data again and retry."
        
        # Load existing data
        try:
            with open('output.json', 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}
        
        # Update data
        if thread_id in existing_data:
            if email_id not in existing_data[thread_id]["id_of_email"]:
                existing_data[thread_id]["email_id"].append(email_id)
                existing_data[thread_id]["summary"].append(summary)
        else:
            existing_data[thread_id] = {
                "email_id": [email_id],
                "summary": [summary],
                "sender": sender
            }
        
        # Write updated data to file
        with open('output.json', 'w') as f:
            json.dump(existing_data, f, indent=4)
        
        return f"Data updated in output.json: {existing_data}"
    
    except ValueError:
        return "Error: Input should be a pipe-separated string with exactly four parts."
    
    except Exception as e:
        return f"An error occurred: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "json_writer",
            "description": "Write the entries to a JSON file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Pipe (|) separated text of length 4 (four), representing the threadId, email_id, summary, and sender's email address.",
                    },
                },
                "required": ["data"],
            },
        }
    }
]
