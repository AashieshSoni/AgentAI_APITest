# LangChain/OpenAI logic for test generation
import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field

# Set up your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

class TestSpec(BaseModel):
    """Pydantic model for the AI-generated test case."""
    test_name: str = Field(description="A descriptive name for the test.")
    http_method: str = Field(description="The HTTP method (GET, POST, PUT, DELETE).")
    endpoint: str = Field(description="The API endpoint path (e.g., /users).")
    payload: dict = Field(description="The JSON body for POST/PUT requests (empty dict if not needed).")
    expected_status_code: int = Field(description="The expected HTTP status code.")
    expected_response_key: str = Field(description="A key expected to be present in the response body.")

def generate_test_case(api_description: str) -> TestSpec:
    """
    Generates a structured API test case using an LLM.
    """
    try:
        llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.5)

        # 💡 Prompt to guide the AI to generate a structured JSON output
        template = """
        You are an autonomous API testing agent. Based on the following API description,
        generate a single, detailed, and structured test case.
        
        API Description: {description}
        
        Generate the output in a JSON format that strictly adheres to the provided schema:
        {{
          "test_name": "...",
          "http_method": "...",
          "endpoint": "...",
          "payload": {{...}},
          "expected_status_code": 200,
          "expected_response_key": "id"
        }}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["description"]
        )
        
        # We'd typically use a Structured Output Parser in a real LangChain app,
        # but for simplicity, we'll ask the model for raw JSON here.
        
        chain = prompt | llm
        
        raw_response = chain.invoke({"description": api_description})
        
        # --- Simplified Parsing ---
        # In a real app, you'd robustly parse the JSON output from the model.
        import json
        json_str = raw_response.strip().replace('\n', '')
        # Simple attempt to find and parse the JSON block
        start = json_str.find('{')
        end = json_str.rfind('}') + 1
        test_data = json.loads(json_str[start:end])
        
        return TestSpec(**test_data)
    
    except Exception as e:
        print(f"Error generating test: {e}")
        # Return a fallback or raise the exception
        return TestSpec(
            test_name="Fallback Test", 
            http_method="GET", 
            endpoint="/health", 
            payload={}, 
            expected_status_code=200, 
            expected_response_key="status"
        )

if __name__ == '__main__':
    # Example usage:
    desc = "API to fetch user details by ID at /api/v1/users/{id} and should return 200."
    test_case = generate_test_case(desc)
    print(f"Generated Test: {test_case.model_dump_json(indent=2)}")