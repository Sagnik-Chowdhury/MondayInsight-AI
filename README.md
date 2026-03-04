Quantm BI: Intelligent Analytical Engine
Developer: Sagnik Chowdhury

Major: BSc Statistics

Deployment: [Link to your Streamlit App]

Overview
Quantm BI is an AI-driven Business Intelligence (BI) agent designed for startup founders. It bridges the gap between raw operational data in Monday.com and executive-level decision-making. Using Gemini 2.5 Flash, the agent performs real-time data retrieval, cleaning, and strategic synthesis.

Architecture
The system is built on a Modular Retrieval-Augmented Generation (RAG) pattern:

Data Layer: Live connection to Monday.com boards via GraphQL API v2023-10.

Processing Layer: A Python-based normalization engine that cleans nested JSON and handles null values using Pandas.

Intelligence Layer: Google Gemini 2.5 Flash acts as the reasoning core, performing entity resolution and anomaly detection.

Interface Layer: A minimalist Streamlit UI optimized for conversational data exploration.

Setup and Configuration
1. Monday.com Configuration
To replicate this environment, two boards are required on Monday.com:

Sales Pipeline Board: Used to track deals, values, and stages.

Operations Board: Used to track work orders, owners, and timelines.

2. Environment Variables (Secrets)
The application requires the following keys in the Streamlit Cloud Secrets:

Ini, TOML
LLM_API_KEY = "your_google_gemini_api_key"
MONDAY_API_KEY = "your_monday_dot_com_api_key"
DEALS_BOARD_ID = "your_sales_board_id"
WORK_ORDERS_BOARD_ID = "your_work_orders_board_id"
Core Features
Action Trace (Visible Reasoning): The agent provides a step-by-step trace of its tool-calls, allowing the evaluator to observe the data retrieval and processing phases.

Strategic Leadership Updates: Optimized prompts enable the agent to identify statistical outliers and operational bottlenecks, delivering executive-ready summaries.

Schema Agnosticism: The agent utilizes LLM inference to map natural language queries to board columns, independent of specific naming conventions.

Testing the Prototype
The hosted version is pre-configured for immediate testing. Recommended queries for evaluating leadership features include:

"Give me a high-level update on our current revenue risk."

"Which work orders are currently stalled?"

"Summarize the sales pipeline and suggest a strategic next step."
