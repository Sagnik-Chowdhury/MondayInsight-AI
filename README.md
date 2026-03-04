# Quantm BI: Intelligent Analytical Engine
**Developer:** Sagnik Chowdhury

**Deployment:** https://mondayinsight-ai-kqto3mvcfqqqfignwmjhuv.streamlit.app/~/+/YOUR_DEALS_PUBLIC_LINK 
## Overview
Quantm BI is an AI-driven Business Intelligence (BI) agent designed for startup founders. It bridges the gap between raw operational data in Monday.com and executive-level decision-making. Using Gemini 2.5 Flash, the agent performs real-time data retrieval, cleaning, and strategic synthesis.

---

## Architecture
The system is built on a Modular Retrieval-Augmented Generation (RAG) pattern:

1. **Data Layer:** Live connection to Monday.com boards via GraphQL API v2023-10.
2. **Processing Layer:** A Python-based normalization engine that cleans nested JSON and handles null values using Pandas.
3. **Intelligence Layer:** Google Gemini 2.5 Flash acts as the reasoning core, performing entity resolution and anomaly detection.
4. **Interface Layer:** A minimalist Streamlit UI optimized for conversational data exploration.



---

## Setup and Configuration

### 1. Monday.com Configuration
To replicate this environment, two boards are required on Monday.com:
* **Sales Pipeline Board:** Used to track deals, values, and stages.
* **Operations Board:** Used to track work orders, owners, and timelines.

### 2. Environment Variables (Secrets)
The application requires the following keys in the Streamlit Cloud Secrets:
```toml
LLM_API_KEY = "my_google_gemini_api_key"
MONDAY_API_KEY = "my_monday_dot_com_api_key"
DEALS_BOARD_ID = "my_sales_board_id"
WORK_ORDERS_BOARD_ID = "my_work_orders_board_id"
```
## Core Features
* **Action Trace (Visible Reasoning):** The agent provides a step-by-step trace of its tool-calls (Action Trace), allowing the evaluator to observe the data retrieval, normalization, and reasoning phases in real-time. This ensures transparency in the agent's decision-making process.
* **Strategic Leadership Updates:** Optimized system prompts enable the agent to identify statistical outliers and operational bottlenecks, delivering executive-ready summaries rather than raw data lists.
* **Schema Agnosticism:** The agent utilizes LLM inference to map natural language queries to board columns, making the system resilient to changes in column naming conventions on the Monday.com interface.
* **Data Integrity Layer:** Includes a custom Python pre-processor that strips null values and metadata noise to minimize model hallucination.

## Testing the Prototype
The hosted version is pre-configured for immediate testing. To evaluate the agent's analytical and leadership capabilities, the following queries are recommended:

* **For Sales Insights:** "Provide a high-level update on current revenue risk and identify any significant deal anomalies."
* **For Operational Insights:** "Identify work orders that are currently stalled or lacking ownership."
* **For Strategic Planning:** "Summarize the sales pipeline and suggest a strategic next step for the founder."
