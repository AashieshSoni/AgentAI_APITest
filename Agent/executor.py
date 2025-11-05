# Handles API execution (using requests) 
#This file executes the test case and checks the results.
import requests
from agent.ai_generator import TestSpec

def execute_api_test(base_url: str, test_spec: TestSpec) -> dict:
    """
    Executes the API test based on the TestSpec and performs basic validation.
    """
    full_url = f"{base_url}{test_spec.endpoint}"
    
    # 1. Execute the request
    try:
        response = requests.request(
            method=test_spec.http_method,
            url=full_url,
            json=test_spec.payload,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        return {
            "test_name": test_spec.test_name,
            "status": "FAILURE",
            "log": f"Request failed: {e}",
            "http_status": None
        }

    # 2. Perform validation
    passed = True
    log_messages = []

    # Check Status Code
    if response.status_code != test_spec.expected_status_code:
        passed = False
        log_messages.append(
            f"Status Code Mismatch: Expected {test_spec.expected_status_code}, Got {response.status_code}"
        )

    # Check Response Content (Key presence)
    try:
        response_json = response.json()
        if test_spec.expected_response_key and test_spec.expected_response_key not in response_json:
            passed = False
            log_messages.append(
                f"Content Mismatch: Expected key '{test_spec.expected_response_key}' not found in response."
            )
    except requests.exceptions.JSONDecodeError:
        if response.content and test_spec.expected_status_code == 200:
             passed = False
             log_messages.append("Response was not valid JSON.")
    except Exception as e:
        log_messages.append(f"Validation Error: {e}")


    # 3. Compile results and send alert (simplified)
    status = "SUCCESS" if passed else "FAILURE"
    
    if status == "FAILURE":
        # In a real system, this is where you'd integrate with Slack/Email alerting
        print(f"🚨 ALERT! Test Failure: {test_spec.test_name} at {full_url}")

    return {
        "test_name": test_spec.test_name,
        "status": status,
        "log": "; ".join(log_messages) if log_messages else "Test passed all assertions.",
        "http_status": response.status_code,
        "response_body": response_json if 'response_json' in locals() else response.text[:200]
    }

# Note: The `base_url` is configured in `main.py` or `scheduler.py`