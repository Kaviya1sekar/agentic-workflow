from crewai_tools import tool
import json
from datetime import datetime

@tool("Error deterministic tool")
def error_deterministic_tool(data: str):
    """
    Error deterministic tool accepts 1 parameter which is a string in pipe (|) separated text format.
    Input should have id, load_creation_timestamp, pickup_appointment_timestamp, delivery_appointment_timestamp in pipe-separated text format.
    id|load_creation_timestamp|pickup_appointment_timestamp|delivery_appointment_timestamp

    It determines the error in the data and returns the error in a particular entry.

    Errors can be:
        - Load created after delivery appointment 
        - Load created after pickup appointment 
        - Load delivery appointment is before pickup appointment 
        - Pickup and delivery appointments are scheduled at the same time
        - Load missing appointment times
        - Time between pickup and delivery appointments is too broad
        - Load created with appointment Times in Night
    """
    try:
        id, load_creation_timestamp, pickup_appointment_timestamp, delivery_appointment_timestamp = data.split("|")

        if any(timestamp in ["", None, "None"] for timestamp in [load_creation_timestamp, pickup_appointment_timestamp, delivery_appointment_timestamp]):
            return "Load missing appointment times"

        load_creation_time = datetime.strptime(load_creation_timestamp, '%Y-%m-%dT%H:%M:%SZ')
        pickup_appointment_time = datetime.strptime(pickup_appointment_timestamp, '%Y-%m-%dT%H:%M:%SZ')
        delivery_appointment_time = datetime.strptime(delivery_appointment_timestamp, '%Y-%m-%dT%H:%M:%SZ')

        if load_creation_time > delivery_appointment_time:
            return "Load created after delivery appointment"
        if load_creation_time > pickup_appointment_time:
            return "Load created after pickup appointment"
        if pickup_appointment_time > delivery_appointment_time:
            return "Load delivery appointment is before pickup appointment"
        if pickup_appointment_time == delivery_appointment_time:
            return "Pickup and delivery appointments are scheduled at the same time"
        if (delivery_appointment_time - pickup_appointment_time).days > 30:
            return "Time between pickup and delivery appointments is too broad"
        if pickup_appointment_time.hour < 6 or delivery_appointment_time.hour < 6:
            return "Load created with appointment Times in Night"

        return "No error found"
    
    except ValueError as ve:
        return f"Error: Invalid input format. {ve}"
    
    except Exception as e:
        return f"An error occurred: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "error_deterministic_tool",
            "description": "Determine the error in the data and return the error in a particular entry.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "A string which is pipe (|) separated text format. Each input should have id, load_creation_timestamp, pickup_appointment_timestamp, delivery_appointment_timestamp.",
                    },
                },
                "required": ["data"],
            },
        }
    }
]
