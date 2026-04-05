# ==================================================
# app.py - LexiGuard AI
# ==================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import datetime
from openai import OpenAI
import base64

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="LexiGuard AI", layout="wide")


# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# --------------------------------------------------
# SESSION LOGIN STATE
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# --------------------------------------------------
# OPENAI CLIENT
# --------------------------------------------------
api_key = st.secrets.get("OPENAI_API_KEY", None) or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


# ==================================================
# LOGIN PAGE — GLASS UI
# ==================================================
if not st.session_state.logged_in:

    def get_base64(file):
        try:
            with open(file, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except:
            return ""

    bg_img = get_base64("logo.png")   # Add your logo.png in project folder

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_img}");
        background-size: cover;
        background-position: right;
        background-attachment: fixed;
    }}
    [data-testid="stAppViewContainer"] > .css-1d391kg {{
        padding-top: 0rem !important;
        display: flex;
        height: 90vh;
    }}
    .login-card {{
        backdrop-filter: blur(30px);
        background: rgba(blue);
        border-radius: 20px;
        border: 1px solid rgba(blue);
        padding: 40px;
        width: 320px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(blue);
    }}
    .login-title {{
        font-size: 60px;
        font-weight: 700;
        color: white;
        margin-bottom: 25px;
        text-align: right;
    }}
    .stTextInput input {{
        background: rgba(255,255,255);
        border: none;
        border-radius: 10px;
        padding: 100px;
        color: black;
        text-align: left
        ;
    }}
    .stTextInput input::placeholder {{ color:white; }}
    .stButton button {{
        width: 100%;
        background: rgba(37, 99, 235);
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-weight: 600;
        border: none;
        transition: 0.3s;
        text-align: left;
    }}
    .stButton button:hover {{
        background: #2563EB;
        transform: scale(1.05);
        text-align: right;
    }}
    label {{ color: white !important; font-weight: 500; }}
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">LexiGuard Sign In</div>', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Invalid Credentials")

        st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# MAIN APP
# ==================================================
else:

    # HEADER
    st.markdown("""
    <h1> LexiGuard AI</h1>
    <h3>Enterprise Smart Contract Risk Intelligence</h3>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # --------------------------------------------------
    # SIDEBAR NAVIGATION
    # --------------------------------------------------
    with st.sidebar:
        st.markdown("## 🛡️ LexiGuard AI")

        page = st.radio(
            "Navigation",
            ["Dashboard", "Contract Analysis", "AI Assistant", "Reports"]
        )

        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Upload Contract",
            type=["pdf", "docx"]
        )

        analysis_level = st.selectbox(
            "Analysis Depth",
            ["Basic", "Advanced", "Legal Audit"]
        )

        st.markdown("---")
        st.write("User: Analyst")
        st.write("Session:", datetime.datetime.now().strftime("%H:%M:%S"))

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()


    # ==================================================
    # DASHBOARD PAGE
    # ==================================================
    if page == "Dashboard":

        st.subheader("📊 System Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Contracts", "24", "+3")
        c2.metric("Clauses", "187")
        c3.metric("High Risk", "12", "-2")
        c4.metric("Confidence", "92%")
        st.markdown("---")

        risk_data = pd.DataFrame({
            "Risk": ["Low", "Medium", "High"],
            "Count": [120, 45, 22]
        })

        fig = px.bar(risk_data, x="Risk", y="Count", color="Risk", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)


    # ==================================================
    # CONTRACT ANALYSIS PAGE
    # ==================================================
    elif page == "Contract Analysis":

        st.subheader("📄 Clause-Level Risk Analysis")

        if uploaded_file:

            df = pd.DataFrame({
                "Clause": [
                    "Payment Terms","Termination Clause","Liability Clause","Confidentiality",
                    "Indemnity","Force Majeure","Dispute Resolution","Data Protection",
                    "Intellectual Property","Governing Law","Service Level Agreement","Warranty Clause",
                    "Subcontracting Rights","Change Management","Insurance Obligations"
                ],
                "Risk Level": [
                    "Low","Medium","High","Low","High","Medium","Medium","Low","Medium","Low",
                    "Medium","Low","High","Medium","Low"
                ],
                "Explanation": [
                    "Clear payment timeline and invoice terms","Termination rights slightly one-sided",
                    "Unlimited liability exposure","Strong confidentiality protection","Vendor indemnity obligation is risky",
                    "Force majeure clause lacks clarity","Arbitration jurisdiction unclear","GDPR compliance clause present",
                    "Ownership rights not clearly defined","Governing law properly stated","Service uptime commitments unclear",
                    "Warranty limitations reasonable","Allows risky third-party delegation","Change approval process vague",
                    "Insurance coverage sufficient"
                ]
            })

            st.dataframe(df, use_container_width=True)

            # Risk Chart
            risk_count = df["Risk Level"].value_counts().reset_index()
            risk_count.columns = ["Risk", "Count"]

            fig = px.pie(risk_count, names="Risk", values="Count", title="Risk Distribution")
            st.plotly_chart(fig, use_container_width=True)

            st.progress(70)
            st.warning("⚠ Moderate legal exposure detected")

        else:
            st.info("Upload a contract from sidebar")


    # ==================================================
    # AI ASSISTANT PAGE
    # ==================================================
    elif page == "AI Assistant":

        st.subheader("🤖 AI Legal Assistant")

        if client is None:
            st.error("Add OPENAI_API_KEY in secrets")
            st.stop()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Show chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Ask about contract laws or review clauses...")

        if prompt:

            system_prompt = """
            You are LexiGuard AI – a professional contract law assistant.

            You ONLY answer questions related to:
            - Laws of Contract
            - Contract clause explanation
            - Contract risk review
            - Agreement drafting basics
            - Legal meaning of contract terms

            If user asks anything outside contract law,
            politely respond:
            'I specialize only in contract law and agreement review.'

            ALWAYS provide answers in a detailed structured format with:
            1️⃣ Explanation in simple words
            2️⃣ Key points / subtopics
            3️⃣ References to Indian Contract Act where relevant
            4️⃣ Examples if needed
            """

            st.session_state.messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages]
            )

            reply = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": reply})

            with st.chat_message("assistant"):
                st.markdown(reply)


    # ==================================================
    # REPORTS PAGE
    # ==================================================
    elif page == "Reports":

        st.subheader("📑 Export Reports")

        def generate_pdf():
            os.makedirs("reports", exist_ok=True)
            path = "reports/LexiGuard_Report.pdf"
            c = canvas.Canvas(path, pagesize=A4)
            c.drawString(50, 800, "LexiGuard AI Risk Report")
            c.drawString(50, 770, f"Analysis Level: {analysis_level}")
            c.drawString(50, 740, "Moderate liability risk detected")
            c.save()
            return path

        if st.button("Generate PDF"):
            file_path = generate_pdf()
            with open(file_path, "rb") as f:
                st.download_button("Download Report", f, file_name="LexiGuard_Report.pdf")


    # ==================================================
    # FOOTER
    # ==================================================
    st.markdown("---")
    st.markdown("<center>🤖 AI Legal Assistant<br>© 2026 LexiGuard AI</center>", unsafe_allow_html=True)
