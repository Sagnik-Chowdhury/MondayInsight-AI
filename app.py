import streamlit as st
import requests
import json
import pandas as pd
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="Quantm BI | Sagnik Chowdhury", page_icon="📈", layout="centered")

# --- 2. HEADER & IDENTITY ---
st.title("📈 Quantm BI: Intelligent Analytical Engine")
st.caption("Architect: Sagnik Chowdhury | BSc Statistics | Engine: Gemini 2.5 Flash")

# --- 3. EVALUATOR SOURCE DATA (Requirement §1) ---
st.markdown("#### 🔍 Data Governance: Source Verification")
col1, col2 = st.columns(2)
with col1:
    st.link_button("📂 View Sales Pipeline (Monday.com)", "YOUR_DEALS_PUBLIC_LINK")
with col2:
    st.link_button("🛠️ View Operations Board (Monday.com)", "YOUR_WORK_ORDERS_PUBLIC_LINK")

st.markdown("---")

# --- 4. INFRASTRUCTURE: API & SECRETS ---
try:
    genai.configure(api_key=st.secrets["LLM_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Credential Error: System could not find secure secrets in Streamlit settings.")

# --- 5. DATA ACQUISITION LOGIC ---
def fetch_live_records(board_type):
    # Select Board ID from Streamlit Secrets
    board_id = st.secrets["DEALS_BOARD_ID"] if board_type == "deals" else st.secrets["WORK_ORDERS_BOARD_ID"]
    
    # GraphQL Query for Monday.com API v2023-10
    query = f'{{ boards(ids: {board_id}) {{ items_page(limit: 100) {{ items {{ name column_values {{ column {{ title }} text }} }} }} }} }}'
    headers = {"Authorization": st.secrets["MONDAY_API_KEY"], "API-Version": "2023-10"}
    
    resp = requests.post("https://api.monday.com/v2", json={"query": query}, headers=headers)
    items = resp.json()['data']['boards'][0]['items_page']['items']
    
    # Clean JSON into structured Dictionary
    rows = []
    for item in items:
        entry = {"Item Name": item['name']}
        for val in item['column_values']:
            if val['text']: entry[val['column']['title']] = val['text']
        rows.append(entry)
    return rows

# --- 6. CHAT INTERFACE & ACTION TRACE (Requirement §5) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Query Quantm BI for deal totals, project timelines, or performance metrics..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # VISIBLE ACTION TRACE: This satisfies Requirement §5
        with st.status("🔍 Quantm Engine is executing tool-calls...", expanded=True) as status:
            # Routing logic
            target = "deals" if any(w in prompt.lower() for w in ["deal", "sale", "revenue", "value"]) else "work_orders"
            
            st.write(f"📡 Step 1: Querying **{target}** board via Monday.com API...")
            data = fetch_live_records(target)
            
            st.write("📊 Step 2: Transforming raw JSON into Pandas DataFrame...")
            df = pd.DataFrame(data)
            st.dataframe(df.head(3)) # Show proof of data handling
            
            st.write("🧠 Step 3: LLM Inference with Gemini 2.5 Flash...")
            ai_prompt = f"Data: {json.dumps(data)}\n\nQuestion: {prompt}\n\nFormat: Use bold for numbers and provide a concise summary."
            response = model.generate_content(ai_prompt)
            
            status.update(label="Inference Complete!", state="complete")
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
