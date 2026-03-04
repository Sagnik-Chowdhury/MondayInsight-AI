

import streamlit as st
import requests
import json
import pandas as pd
import google.generativeai as genai

# --- 1. CONFIGURATION & SECRETS ---
st.set_page_config(page_title="StatFlow BI | Monday.com AI", page_icon="📈", layout="wide")

try:
    genai.configure(api_key=st.secrets["LLM_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Missing API Keys! Please check Streamlit Secrets.")

# --- 2. SIDEBAR (The 'Data Scientist' Touch) ---
with st.sidebar:
    st.title("📈 StatFlow BI")
    st.subheader("BSc Statistics Project")
    st.markdown("---")
    st.write("**Agent Status:** ✅ Online")
    st.write("**Model:** Gemini 2.5 Flash")
    st.write("**Data Source:** Monday.com Live API")
    st.markdown("---")
    st.info("Built by Sagnik Chowdhury")

# --- 3. DATA FETCHING LOGIC ---
def fetch_live_data(target_board):
    board_id = st.secrets["DEALS_BOARD_ID"] if target_board == "deals" else st.secrets["WORK_ORDERS_BOARD_ID"]
    query = f'{{ boards(ids: {board_id}) {{ items_page(limit: 100) {{ items {{ name column_values {{ column {{ title }} text }} }} }} }} }}'
    headers = {"Authorization": st.secrets["MONDAY_API_KEY"], "API-Version": "2023-10"}
    
    resp = requests.post("https://api.monday.com/v2", json={"query": query}, headers=headers)
    items = resp.json()['data']['boards'][0]['items_page']['items']
    
    data_list = []
    for item in items:
        row = {"Name": item['name']}
        for v in item['column_values']:
            if v['text']: row[v['column']['title']] = v['text']
        data_list.append(row)
    return data_list

# --- 4. USER INTERFACE ---
st.title("🚀 Founder BI Agent")
st.markdown("Analyze your **Sales Pipeline** and **Work Orders** using Generative AI.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: What is the total value of our deals?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🔍 Agent is analyzing live data...", expanded=True) as status:
            board_type = "deals" if "deal" in prompt.lower() else "work_orders"
            
            st.write(f"📡 Accessing **{board_type}** board...")
            raw_data = fetch_live_data(board_type)
            
            # Show a data preview for transparency
            df = pd.DataFrame(raw_data)
            st.write("📊 Data Preview:", df.head(3))
            
            st.write("🧠 Consulting Gemini 2.5 Flash...")
            ai_instruction = f"""
            You are a Senior Business Analyst. 
            Data: {json.dumps(raw_data)}
            User Question: {prompt}
            
            Provide a professional response with:
            1. A clear summary.
            2. Bold numbers (e.g., **$50,000**).
            3. A 'Statistical Note' regarding the data distribution if relevant.
            """
            response = model.generate_content(ai_instruction)
            status.update(label="Analysis Complete!", state="complete")
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
