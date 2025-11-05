'''#  -Pydantic models for data Pydantic Data Models)
This file defines the structured formats for two main things:

Test Specification (TestSpec): The input/format for the AI to generate or for a user to define a test.

Test Result (TestResult): The output/format after the executor.py runs a test.
'''
from pydantic import BaseModel, Field
from typing import Optional, Dict

# --- 1. Model for AI Generation and Test Definition ---
class TestSpec(BaseModel):
    """
    Defines the structure for an API Test Case.
    Used by the AI generator and the executor.
    """
    test_name: str = Field(..., description="A unique, descriptive name for the test.")
    http_method: str = Field(..., description="The HTTP method (GET, POST, PUT, DELETE).")
    endpoint: str = Field(..., description="The API endpoint path (e.g., /api/v1/users).")
    payload: Optional[Dict] = Field(default={}, description="The JSON body for POST/PUT requests.")
    expected_status_code: int = Field(..., description="The expected HTTP status code (e.g., 200, 201).")
    expected_response_key: Optional[str] = Field(default=None, description="A critical key expected in the response body (e.g., 'id', 'status').")

    # Example:
    # {
    #   "test_name": "Create new user",
    #   "http_method": "POST",
    #   "endpoint": "/users",
    #   "payload": {"name": "Test User", "email": "test@example.com"},
    #   "expected_status_code": 201,
    #   "expected_response_key": "user_id"
    # }

# --- 2. Model for Test Execution Results ---
class TestResult(BaseModel):
    """
    Defines the structure for the results returned after test execution.
    """
    test_name: str = Field(..., description="The name of the test that was executed.")
    status: str = Field(..., description="The result status: 'SUCCESS' or 'FAILURE'.")
    http_status: Optional[int] = Field(default=None, description="The actual HTTP status code returned.")
    url: str = Field(..., description="The full URL that was tested.")
    log: str = Field(..., description="Detailed log messages regarding failures or success.")
    response_sample: Optional[str] = Field(default=None, description="A truncated sample of the response body for debugging.")

    # Example:
    # {
    #   "test_name": "Fetch user info",
    #   "status": "FAILURE",
    #   "http_status": 404,
    #   "url": "http://api.example.com/users/123",
    #   "log": "Status Code Mismatch: Expected 200, Got 404",
    #   "response_sample": "{'error': 'User not found'}"
    # }