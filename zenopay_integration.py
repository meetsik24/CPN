import requests
import json
from fastapi import FastAPI, HTTPException

def check_order_status(order_id):
    # The endpoint URL where the request will be sent
    endpoint_url = "https://api.zeno.africa/order-status"
    
    # Data to be sent in the POST request
    post_data = {
        'check_status': 1,
        'order_id': order_id,
        'api_key': 'reyfyfufu',
        'secret_key': 'YOUR SECRET KEY'
    }
    
    try:
        # Send the POST request
        response = requests.post(endpoint_url, data=post_data)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Decode the JSON response
        response_data = response.json()
        
        # Format the response to match the desired structure
        if response_data.get('status') == 'success':
            result = {
                "status": "success",
                "order_id": response_data.get('order_id'),
                "message": response_data.get('message'),
                "payment_status": response_data.get('payment_status')
            }
        else:
            result = {
                "status": "error",
                "message": response_data.get('message')
            }
        
        # Print the result in JSON format
        print(json.dumps(result, indent=4))
        return result

    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        result = {
            "status": "error",
            "message": f"Request error: {str(e)}"
        }
        print(json.dumps(result, indent=4))
        return result

# Example usage
check_order_status(order_id="123456789")