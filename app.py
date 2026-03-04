import streamlit as st
import requests
import json
import google.generativeai as genai

# 1. Setup - Using Streamlit's Secret manager (similar to Colab's)
try:
    genai.configure(api_key=st.secrets["LLM_API_KEY"])
    # Using the Gemini model your environment confirmed works
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Keys missing! Please add them to the Streamlit Sidebar or Secrets.")

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
    return json.dumps(data_list)

# --- Streamlit UI ---
st.set_page_config(page_title="Founder BI Agent", page_icon="📈")
st.title("🚀 Founder BI Agent")
st.markdown("Ask questions about your Monday.com Pipeline and Work Orders.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is my total pipeline value?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Agent thinking...", expanded=True) as status:
            board = "deals" if "deal" in prompt.lower() else "work_orders"
            st.write(f"📡 Fetching live data from **{board}**...")
            raw_data = fetch_live_data(board)
            
            st.write("📊 Analyzing business metrics...")
            ai_instruction = f"Data: {raw_data}\n\nQuestion: {prompt}\nRespond with clear sections and bold numbers."
            response = model.generate_content(ai_instruction)
            
            status.update(label="Analysis Complete!", state="complete")
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
