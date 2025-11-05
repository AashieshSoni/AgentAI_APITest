# APScheduler setup and jobs
#This file sets up the scheduled job using APScheduler.
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from agent.ai_generator import generate_test_case
from agent.executor import execute_api_test

# Configuration for the API being tested
TARGET_API_BASE_URL = "http://api.example.com"
API_TO_TEST_DESCRIPTION = "The primary /users API that returns a list of active users."

def autonomous_qa_job():
    """
    The main job that runs on a schedule.
    1. Generates a new test case (AI).
    2. Executes the test (Executor).
    3. Logs/reports the result.
    """
    print("\n--- Running AutoAgent QA Autonomous Job ---")
    
    # 1. Generate Test Case
    print("Step 1: AI Generating Test Spec...")
    test_spec = generate_test_case(API_TO_TEST_DESCRIPTION)
    print(f"Generated Spec: {test_spec.test_name}")

    # 2. Execute Test
    print("Step 2: Executing Test...")
    result = execute_api_test(TARGET_API_BASE_URL, test_spec)
    
    # 3. Log Result
    print(f"Step 3: Result Logged ({result['status']})")
    print(f"  Test: {result['test_name']}")
    print(f"  Log: {result['log']}")
    print("------------------------------------------\n")
    
    return result

# Initialize the scheduler
scheduler = AsyncIOScheduler()

# Add the job to run every 15 minutes
# In a real app, this would be dynamic and configurable via the FastAPI endpoint
scheduler.add_job(
    autonomous_qa_job,
    'interval',
    minutes=15,
    id='api_health_check_job'
)

def start_scheduler():
    """Starts the APScheduler instance."""
    if not scheduler.running:
        scheduler.start()
        print("APScheduler started: Autonomous QA Agent is active.")