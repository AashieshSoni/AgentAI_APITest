# FastAPI application entry point
import uvicorn
from fastapi import FastAPI
from scheduler import start_scheduler, autonomous_qa_job, scheduler

app = FastAPI(title="AutoAgent QA Service")

@app.on_event("startup")
async def startup_event():
    """Start the scheduler when the FastAPI application starts."""
    start_scheduler()

@app.get("/")
def read_root():
    return {"message": "AutoAgent QA Service Running. Scheduler is active."}

@app.post("/run-now")
def trigger_test():
    """Endpoint to manually trigger an immediate test run."""
    result = autonomous_qa_job()
    return {"message": "Test triggered manually.", "result": result}

@app.get("/jobs")
def get_jobs():
    """Get a list of currently scheduled jobs."""
    jobs = [
        {"id": job.id, "trigger": str(job.trigger), "next_run": str(job.next_run_time)}
        for job in scheduler.get_jobs()
    ]
    return {"jobs": jobs}

if __name__ == "__main__":
    # To run this, you need to set your OPENAI_API_KEY environment variable
    print("Starting FastAPI and APScheduler...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
# To run the code:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Run the application: python main.py