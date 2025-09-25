import streamlit as st
import requests

# Your n8n production webhook URL (replace with yours later)
WEBHOOK_URL = "https://sandhyanarwade.app.n8n.cloud/webhook/ad4a5feb-8298-4250-a7a2-a78b1f7f4b8a"

st.set_page_config(page_title="Competitor Insights", page_icon="📊", layout="centered")

st.title("📊 Industry Competitor Insights")
st.write("Enter an industry name and get AI-powered competitor analysis from n8n + OpenAI backend.")

# User input
industry = st.text_input("Enter Industry Name:", "EdTech")

# Button to fetch results
if st.button("🔍 Get Competitors"):
    if industry.strip() == "":
        st.warning("Please enter an industry first!")
    else:
        try:
            # Send request to n8n webhook
            payload = {"industry": industry}
            response = requests.post(WEBHOOK_URL, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()

                # If backend returns a JSON array of competitors
                st.subheader(f"Top Competitors in {industry}")
                if isinstance(data, list):
                    for comp in data:
                        st.markdown(f"### {comp.get('name', 'Unknown')}")
                        st.write(f"Founded: {comp.get('founded_year', 'N/A')}")
                        st.write("**Partnerships:**", ", ".join(comp.get("major_partnerships", [])))
                        st.write("**Upcoming Events:**", ", ".join(comp.get("upcoming_events", [])))
                        st.write("---")
                else:
                    st.json(data)

            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")
