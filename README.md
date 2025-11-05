AI-Powered API Testing Agent :-
It's is an intelligent testing automation system that simulates a proactive QA engineer. It autonomously generates test cases using AI, executes scheduled API tests, logs results, and alerts your team about failures. Built with Python library.

Features
•	🔁 Automated API testing on intervals using APScheduler
•	🧠 AI-generated test scenarios via LangChain or OpenAI
•	📊 Interactive Streamlit dashboard for monitoring
•	⚙️ Modular Python-based architecture
•	✅ CI/CD integration using GitHub Actions

________________________________________
📁 Project Structure
autoagent-qa/
├── agent/             # LLM logic for test generation
├── api/               # FastAPI endpoints




1.	Clone repo and Install Python Dependencies
pip install -r requirements.txt
2.	Start the Test Agent (Scheduler)
python scheduler/scheduler.py
3.	Run Streamlit Dashboard
streamlit run dashboard/app.py


Set of REST APIs for a testing before every release. If any test fails (e.g., slow response or wrong data , incorrect output), it logs the result, visualizes it on the Streamlit dashboard, and sends a Slack alert. Developers can view summaries or detailed error traces directly.

📌 Roadmap
•	 FastAPI + Streamlit integration
•	 Slack alert integration
•	 Retrieval-Augmented Generation (RAG) enhancement
•	 Prometheus/Grafana for deep observability
•	 Support for external API documentation import
