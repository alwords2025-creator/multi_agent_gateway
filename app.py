# Copyright (c) 2026 AI Software Innovation Infotech And Hardware Enterprises. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.

"""
AI Software Innovation Infotech And Hardware Enterprises Multi-Agent Gateway - Web Application
Includes: Multi-Agent System + About Us + Admin Panel
"""

import streamlit as st
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime
import asyncio
from gateway import APIGateway

# ====================== CONFIG ======================
DATA_FILE = Path("data/company_info.json")
USERS_FILE = Path("data/users.json")
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)

# Default admin users (CEO + Team)
DEFAULT_USERS = {
    "ceo": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@CEO2026".encode()).hexdigest(),
        "role": "Founder & CEO",
        "name": "Alex Rivera",
        "full_access": True
    },
    "priya": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@CTO2026".encode()).hexdigest(),
        "role": "CTO",
        "name": "Priya Sharma",
        "full_access": True
    },
    "jordan": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@Research2026".encode()).hexdigest(),
        "role": "Head of AI Research",
        "name": "Jordan Lee",
        "full_access": True
    },
    "sam": {
        "password_hash": hashlib.sha256("AI Software Innovation Infotech And Hardware Enterprises@Product2026".encode()).hexdigest(),
        "role": "Product Lead",
        "name": "Sam Patel",
        "full_access": True
    }
}

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            return json.load(f)
    else:
        save_users(DEFAULT_USERS)
        return DEFAULT_USERS

def save_users(users):
    USERS_FILE.parent.mkdir(exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_company():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def save_company(data):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_login(username, password):
    users = load_users()
    if username in users:
        hash_pw = hashlib.sha256(password.encode()).hexdigest()
        if users[username]["password_hash"] == hash_pw:
            return users[username]
    return None

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="AI Software Innovation Infotech And Hardware Enterprises | Multi-Agent Gateway",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0f172a, #1e1b4b);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #8b5cf6;
    }
    .stButton>button {
        background: linear-gradient(90deg, #7c3aed, #8b5cf6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
    }
    .info-card {
        background: #1e293b;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ====================== SIDEBAR ======================
with st.sidebar:
    st.image("assets/logo.svg", width=220)
    st.markdown("### AISIH Enterprises")
    st.caption("Multi-Agent AI Systems")
    st.divider()

    menu = st.radio(
        "Navigation",
        ["🏠 Home", "🤖 Multi-Agent System", "📄 About Us", "🔐 Admin Login", "⚙️ Admin Panel"],
        label_visibility="collapsed"
    )

    st.divider()
    if st.session_state.logged_in:
        st.success(f"Logged in as: **{st.session_state.user['name']}**")
        st.caption(st.session_state.user['role'])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    else:
        st.info("Login for full access")

# ====================== HOME PAGE ======================
if menu == "🏠 Home":
    company = load_company()
    st.markdown(f"""
    <div class="main-header">
        <h1 style="color:white;margin:0;">🚀 {company.get('company_name', 'AI Software Innovation Infotech And Hardware Enterprises')}</h1>
        <p style="color:#a78bfa;margin:0.3rem 0 0 0;">{company.get('tagline', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Agents", "6 Specialized")
    with col2:
        st.metric("Architecture", "API Gateway")
    with col3:
        st.metric("Quality Gate", "Enabled")

    st.markdown("### Welcome to AI Software Innovation Infotech And Hardware Enterprises Multi-Agent Gateway")
    st.write(company.get("about", ""))
    st.info("Go to **Multi-Agent System** to run tasks, or **About Us** to know more about the company.")

# ====================== MULTI-AGENT SYSTEM ======================
elif menu == "🤖 Multi-Agent System":
    st.header("🤖 Multi-Agent Gateway")
    st.caption("Powered by AI Software Innovation Infotech And Hardware Enterprises • Parallel Collaboration • Quality Gate")

    task = st.text_area("Enter your task", height=100, 
                        placeholder="Example: Design a scalable recommendation system using multi-agent collaboration")

    if st.button("🚀 Run Multi-Agent Pipeline", type="primary"):
        if not task.strip():
            st.warning("Please enter a task")
        else:
            with st.spinner("Agents collaborating..."):
                gateway = APIGateway()
                # Run async in sync context
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(gateway.process(task))
                loop.close()

            if response.success:
                st.success(f"✅ Completed in {response.total_time_ms:.0f} ms | Confidence: {response.confidence:.0%}")
                st.markdown("### Final Output")
                st.markdown(response.final_output)

                with st.expander("📊 Performance & Agent Breakdown"):
                    st.write(f"**Agents Used:** {', '.join(response.agents_used)}")
                    st.write(f"**Critic Approved:** {response.aggregation_details.get('critic_approved')}")
                    for r in response.individual_results:
                        st.write(f"- {r['agent']}: {r['confidence']:.0%} confidence, {r['execution_time_ms']:.0f}ms")
            else:
                st.error("Pipeline failed")

# ====================== ABOUT US PAGE ======================
elif menu == "📄 About Us":
    company = load_company()

    st.markdown(f"""
    <div class="main-header">
        <h1 style="color:white;margin:0;">About {company.get('company_name', 'AI Software Innovation Infotech And Hardware Enterprises')}</h1>
        <p style="color:#a78bfa;">{company.get('tagline', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Company Description
    st.subheader("Our Story")
    st.write(company.get("about", ""))

    st.divider()

    # Founder & CEO
    st.subheader("👨‍💼 Founder & CEO")
    ceo = company.get("founder_ceo", {})
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            st.image(ceo.get("photo", "assets/ceo_placeholder.svg"), width=150)
        except:
            st.image("assets/ceo_placeholder.svg", width=150)
    with col2:
        st.markdown(f"### {ceo.get('name', 'N/A')}")
        st.caption(ceo.get("title", "Founder & CEO"))
        st.write(ceo.get("bio", ""))
        st.write(f"📧 {ceo.get('email', '')}")
        st.write(f"📱 {ceo.get('mobile', '')}")

    st.divider()

    # Team
    st.subheader("👥 Our Team")
    team = company.get("team_members", [])
    cols = st.columns(3)
    for i, member in enumerate(team):
        with cols[i % 3]:
            try:
                st.image(member.get("photo", "assets/ceo_placeholder.svg"), width=120)
            except:
                st.image("assets/ceo_placeholder.svg", width=120)
            st.markdown(f"**{member.get('name')}**")
            st.caption(member.get("role"))
            st.write(member.get("bio", ""))

    st.divider()

    # Contact & Office
    st.subheader("📍 Head Office & Contact")
    office = company.get("head_office", {})
    contact = company.get("contact", {})

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Head Office Address**")
        st.write(office.get("address", ""))
        st.write(f"{office.get('city', '')}, {office.get('country', '')}")
    with c2:
        st.markdown("**Helpline & Support**")
        st.write(f"📞 Helpline: **{contact.get('helpline', '')}**")
        st.write(f"📧 Support: {contact.get('support_email', '')}")
        st.write(f"🌐 Website: {contact.get('website', '')}")

# ====================== ADMIN LOGIN ======================
elif menu == "🔐 Admin Login":
    st.header("🔐 Admin Login")
    st.caption("CEO and Team members only — Full Access")

    if st.session_state.logged_in:
        st.success(f"Already logged in as {st.session_state.user['name']}")
    else:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                user = check_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success(f"Welcome {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.info("""
        **Default Credentials (Change after first login):**
        - CEO: `ceo` / `AI Software Innovation Infotech And Hardware Enterprises@CEO2026`
        - CTO: `priya` / `AI Software Innovation Infotech And Hardware Enterprises@CTO2026`
        - Research: `jordan` / `AI Software Innovation Infotech And Hardware Enterprises@Research2026`
        - Product: `sam` / `AI Software Innovation Infotech And Hardware Enterprises@Product2026`
        """)

# ====================== ADMIN PANEL ======================
elif menu == "⚙️ Admin Panel":
    if not st.session_state.logged_in:
        st.warning("🔒 Please login first from **Admin Login** page")
        st.stop()

    st.header("⚙️ Admin Panel — Full Access")
    st.caption(f"Logged in as: {st.session_state.user['name']} ({st.session_state.user['role']})")

    company = load_company()
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Company Info", "CEO Profile", "Team Members", "Contact & Office", "Logo Upload"
    ])

    # --- Company Info ---
    with tab1:
        st.subheader("Edit Company Information")
        new_name = st.text_input("Company Name", value=company.get("company_name", ""))
        new_tagline = st.text_input("Tagline", value=company.get("tagline", ""))
        new_about = st.text_area("About Description", value=company.get("about", ""), height=150)

        if st.button("💾 Save Company Info"):
            company["company_name"] = new_name
            company["tagline"] = new_tagline
            company["about"] = new_about
            save_company(company)
            st.success("Company information updated!")

    # --- CEO Profile ---
    with tab2:
        st.subheader("Edit Founder & CEO")
        ceo = company.get("founder_ceo", {})
        ceo_name = st.text_input("CEO Full Name", value=ceo.get("name", ""))
        ceo_title = st.text_input("Title", value=ceo.get("title", "Founder & CEO"))
        ceo_bio = st.text_area("Bio", value=ceo.get("bio", ""), height=100)
        ceo_email = st.text_input("Email", value=ceo.get("email", ""))
        ceo_mobile = st.text_input("Mobile Number", value=ceo.get("mobile", ""))

        if st.button("💾 Save CEO Profile"):
            company["founder_ceo"] = {
                "name": ceo_name,
                "title": ceo_title,
                "bio": ceo_bio,
                "email": ceo_email,
                "mobile": ceo_mobile,
                "photo": ceo.get("photo", "assets/ceo_placeholder.svg")
            }
            save_company(company)
            st.success("CEO profile updated!")

    # --- Team Members ---
    with tab3:
        st.subheader("Edit Team Members")
        team = company.get("team_members", [])
        for i, member in enumerate(team):
            with st.expander(f"Member {i+1}: {member.get('name', 'Unnamed')}"):
                name = st.text_input(f"Name {i}", value=member.get("name", ""), key=f"name_{i}")
                role = st.text_input(f"Role {i}", value=member.get("role", ""), key=f"role_{i}")
                bio = st.text_area(f"Bio {i}", value=member.get("bio", ""), key=f"bio_{i}")
                if st.button(f"Save Member {i+1}", key=f"save_m_{i}"):
                    company["team_members"][i] = {
                        "name": name,
                        "role": role,
                        "bio": bio,
                        "photo": member.get("photo", "assets/ceo_placeholder.svg")
                    }
                    save_company(company)
                    st.success(f"Member {i+1} updated!")

    # --- Contact & Office ---
    with tab4:
        st.subheader("Edit Contact & Head Office")
        office = company.get("head_office", {})
        contact = company.get("contact", {})

        address = st.text_area("Head Office Address", value=office.get("address", ""))
        city = st.text_input("City", value=office.get("city", ""))
        country = st.text_input("Country", value=office.get("country", ""))
        helpline = st.text_input("Helpline Mobile Number", value=contact.get("helpline", ""))
        support_email = st.text_input("Support Email", value=contact.get("support_email", ""))
        website = st.text_input("Website", value=contact.get("website", ""))

        if st.button("💾 Save Contact & Office"):
            company["head_office"] = {"address": address, "city": city, "country": country}
            company["contact"] = {
                "helpline": helpline,
                "support_email": support_email,
                "website": website
            }
            save_company(company)
            st.success("Contact & Office details updated!")

    # --- Logo Upload ---
    with tab5:
        st.subheader("Company Logo Upload")
        st.write("Current logo:")
        try:
            st.image(company.get("logo", "assets/logo.svg"), width=250)
        except:
            st.write("No logo found")

        uploaded = st.file_uploader("Upload new logo (PNG, JPG, SVG)", type=["png", "jpg", "jpeg", "svg"])
        if uploaded:
            logo_path = ASSETS_DIR / f"logo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{uploaded.name.split('.')[-1]}"
            with open(logo_path, "wb") as f:
                f.write(uploaded.getbuffer())
            company["logo"] = str(logo_path)
            save_company(company)
            st.success(f"Logo uploaded successfully: {logo_path}")
            st.image(str(logo_path), width=250)

# Footer
st.markdown("---")
st.caption("© 2026 AI Software Innovation Infotech And Hardware Enterprises. All Rights Reserved. | Multi-Agent Gateway System")
