# Decision Log: Quantm BI
**Architect:** Sagnik Chowdhury  
**Date:** 04.03.2026

### 1. Key Assumptions

* **Schema-Agnostic Reasoning:** I assumed that business data structures on Monday.com are fluid. Rather than hard-coding column IDs, I utilized the Gemini 2.5 Flash reasoning layer to perform entity resolution, allowing the agent to map synonyms (e.g., "Revenue" vs. "Deal Value") dynamically.
* **Founder Persona Priorities:** I assumed the primary user values strategic synthesis over raw data dumps. The agent is optimized to provide "Bottom Line" metrics and executive summaries rather than standard tabular outputs.
* **Real-Time Fidelity:** I assumed that live API polling is essential for business intelligence. Static data exports are insufficient for an agent that must monitor a shifting operational pipeline.

---

### 2. Trade-offs and Justifications

#### Framework Selection (Streamlit)
* **Decision:** Utilized Streamlit for the frontend.
* **Justification:** Streamlit allows for native Pandas integration, which is critical for a statistics-driven project. It also ensures the "no local setup" requirement is met through a seamless cloud deployment.

#### Integration Architecture (Direct API)
* **Decision:** Chose direct Monday.com GraphQL API over Model Context Protocol (MCP).
* **Justification:** To ensure the evaluator can access the hosted prototype immediately via Streamlit Secrets without configuring local environment variables or servers.

#### Model Selection (Gemini 2.5 Flash)
* **Decision:** Utilized Flash over Pro.
* **Justification:** In a conversational BI context, latency is a primary UX metric. Flash provides the necessary sub-3-second response times for tool-calling and data synthesis.

---

### 3. Data Cleaning & Integrity (The "Data Science" Layer)

* **Hybrid Normalization:** I implemented a Python-based normalization layer to flatten nested JSON structures from the Monday.com API. This converts complex responses into structured dictionaries, facilitating accurate manipulation by the LLM.
* **Pre-Processing Filters:** To ensure data quality, I explicitly stripped null values, empty strings, and metadata "noise" at the API level. This prevents model "hallucinations" by ensuring the agent only reasons over populated, high-fidelity data points.
* **Graceful Handling:** The system is designed to catch API exceptions and provide user-friendly feedback (e.g., "Board connection unavailable") to prevent application crashes during connectivity failures.

---

### 4. Leadership Updates (Bonus Feature Implementation)

* **Interpretation:** I interpreted "Leadership Updates" as a Strategic Synthesis Layer.
* **Implementation:** Within the system prompt, I implemented a "Strategic Reasoning" instruction. The agent does not merely list records; it performs Anomaly Detection. It identifies statistical outliers (e.g., deal values significantly above the board mean) and operational bottlenecks (e.g., stalled work orders) and flags them as "Critical Strategic Updates" for the founder.

---

### 5. Future Roadmap

With additional development time, I would implement:

* **Predictive Modeling:** Regression-based forecasting to predict quarterly revenue based on current pipeline velocity.
* **Visual Analytics:** Automated generation of Plotly charts for real-time data distribution analysis.
* **Multi-Board RAG:** Cross-functional indexing for insights spanning multiple operational boards simultaneously.
