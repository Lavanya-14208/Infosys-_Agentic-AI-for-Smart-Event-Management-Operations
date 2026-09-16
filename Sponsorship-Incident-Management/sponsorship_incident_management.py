import streamlit as st
import pandas as pd
import datetime
import random
import string

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Event Management Operations Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED GLASSMORPHIC STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #ffffff 100%);
        color: #0f172a;
    }
    div[data-testid="stMetric"], .stDataFrame, div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #bae6fd !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08) !important;
    }
    h1, h2, h3, p, label {
        color: #0f172a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    div[data-testid="stMetricValue"] {
        color: #0284c7 !important;
        font-weight: 800 !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #e0f2fe;
        border-radius: 10px;
        color: #0369a1 !important;
        padding: 10px 20px;
        font-weight: 700;
        border: 1px solid #bae6fd;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #f0f9ff !important;
        border-right: 1px solid #bae6fd !important;
    }
    .status-banner {
        padding: 12px 20px;
        border-radius: 10px;
        background: #0284c7;
        color: white;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "🛡️ Event Admin Hub"

if "authenticated_sponsor" not in st.session_state:
    st.session_state.authenticated_sponsor = None

if "credentials_modal" not in st.session_state:
    st.session_state.credentials_modal = None

if "sponsors" not in st.session_state:
    st.session_state.sponsors = [
        {
            "Sponsor": "TechCorp Global",
            "Category": "Technology & IT",
            "Contact Email": "sponsorships@techcorp.com",
            "Password": "pass",
            "Budget Capacity ($)": 15000,
            "Engagement Rate (%)": 92,
            "Leads Generated": 450,
            "Deliverables Met (%)": 100,
            "Performance Status": "Collaborated Partner",
            "Rating Numerator": 4.9,
            "Rating Count": 10,
            "Reviews": ["Outstanding technical booth setup during TechCon. Highly engaged audience!"],
            "Image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&q=80",
            "AI Match Score": "98% Match",
            "Collaborated Events": [
                {
                    "Event Name": "TechCon 2025",
                    "Tasks": [
                        {"Task": "Booth Space Setup & Branding", "Status": "Completed"},
                        {"Task": "Keynote Presentation Slot", "Status": "Completed"},
                        {"Task": "Attendee Lead Scan Integration", "Status": "Completed"}
                    ]
                }
            ]
        },
        {
            "Sponsor": "BioHealth Solutions",
            "Category": "Health & Wellness",
            "Contact Email": "events@biohealth.org",
            "Password": "pass",
            "Budget Capacity ($)": 10000,
            "Engagement Rate (%)": 76,
            "Leads Generated": 280,
            "Deliverables Met (%)": 90,
            "Performance Status": "Good",
            "Rating Numerator": 4.2,
            "Rating Count": 5,
            "Reviews": ["Great product sampling setup. Very professional staff and quick communication."],
            "Image": "https://images.unsplash.com/photo-1511578314322-379afb476865?w=500&q=80",
            "AI Match Score": "85% Match",
            "Collaborated Events": []
        },
        {
            "Sponsor": "Apex Financial",
            "Category": "Finance & Banking",
            "Contact Email": "grants@apexfin.com",
            "Password": "pass",
            "Budget Capacity ($)": 20000,
            "Engagement Rate (%)": 88,
            "Leads Generated": 390,
            "Deliverables Met (%)": 95,
            "Performance Status": "Collaborated Partner",
            "Rating Numerator": 4.8,
            "Rating Count": 8,
            "Reviews": ["Sponsored our VIP lounge and provided seamless fintech branding."],
            "Image": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=500&q=80",
            "AI Match Score": "91% Match",
            "Collaborated Events": [
                {
                    "Event Name": "Fintech Summit 2025",
                    "Tasks": [
                        {"Task": "VIP Lounge Branding", "Status": "Completed"},
                        {"Task": "Panelist Desk Banners", "Status": "Completed"},
                        {"Task": "Digital Ad Screens", "Status": "In Progress"}
                    ]
                }
            ]
        },
        {
            "Sponsor": "EcoVolt Motors",
            "Category": "Automotive & EV",
            "Contact Email": "events@ecovolt.com",
            "Password": "pass",
            "Budget Capacity ($)": 18000,
            "Engagement Rate (%)": 95,
            "Leads Generated": 520,
            "Deliverables Met (%)": 100,
            "Performance Status": "Collaborated Partner",
            "Rating Numerator": 5.0,
            "Rating Count": 12,
            "Reviews": ["Brought interactive EV vehicles to the main lobby. Massive attendee interest!"],
            "Image": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=500&q=80",
            "AI Match Score": "96% Match",
            "Collaborated Events": [
                {
                    "Event Name": "AutoExpo 2025",
                    "Tasks": [
                        {"Task": "EV Lobby Display Vehicle Setup", "Status": "Completed"},
                        {"Task": "Brochure Distribution Desk", "Status": "Completed"}
                    ]
                }
            ]
        }
    ]

if "incidents" not in st.session_state:
    st.session_state.incidents = pd.DataFrame([
        {
            "ID": "INC-101",
            "Title": "Main Stage Power Surge",
            "Category": "Electrical & Hardware",
            "Priority": "Critical Alerts",
            "Assigned Team": "Emergency Ops Center",
            "Status": "INVESTIGATING",
            "Root Cause": "Grid overload from high-wattage sound rig",
            "Solution": "Switched to backup generator circuit B",
            "Time": "13:45",
            "Reporter": "Stage Crew A",
            "PIR Summary": "Upgrade power breaker capacity before Main Keynote.",
            "SLA Remaining": 0.25
        }
    ])

if "activity_logs" not in st.session_state:
    st.session_state.activity_logs = [
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] System initialized with active monitoring nodes."
    ]

# HELPER FUNCTION TO RENDER WORK DELIVERABLE TRACKER
def render_event_deliverables_tracker(sponsor_obj, is_admin=False):
    if not sponsor_obj["Collaborated Events"]:
        return

    # If rendered in Event Admin Hub, display clean minimal text
    if is_admin:
        st.markdown("### 📋 Event Deliverables & Operational Work Status")
        for ev_data in sponsor_obj["Collaborated Events"]:
            event_title = ev_data["Event Name"]
            tasks = ev_data["Tasks"]
            st.markdown(f"**Event:** {event_title}")
            for t in tasks:
                st.write(f"• **{t['Task']}** — `{t['Status']}`")
        return

    # Detailed Interactive Dashboard for Sponsor Portal View
    st.markdown("### 📋 Event Deliverables & Operational Work Status")
    for ev_idx, ev_data in enumerate(sponsor_obj["Collaborated Events"]):
        event_title = ev_data["Event Name"]
        tasks = ev_data["Tasks"]
        
        with st.expander(f"🎉 Event: {event_title} ({len(tasks)} Deliverables)", expanded=True):
            if tasks:
                comp_count = sum(1 for t in tasks if t["Status"] == "Completed")
                prog_count = sum(1 for t in tasks if t["Status"] == "In Progress")
                not_start_count = sum(1 for t in tasks if t["Status"] == "Not Started Yet")
                
                progress_pct = int((comp_count / len(tasks)) * 100) if tasks else 0
                st.write(f"**Overall Event Progress:** `{progress_pct}% Completed`")
                st.progress(progress_pct / 100)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Completed", comp_count, delta="🟢 Finalized")
                c2.metric("In Progress", prog_count, delta="🟡 Ongoing")
                c3.metric("Not Started Yet", not_start_count, delta="🔴 Pending")
                
                st.markdown("---")
                st.markdown("**Deliverables Checklist & Status Updates:**")
                
                for t_idx, task_item in enumerate(tasks):
                    tc1, tc2, tc3 = st.columns([2.5, 1.5, 1])
                    with tc1:
                        st.write(f"• **{task_item['Task']}**")
                    with tc2:
                        status_options = ["Completed", "In Progress", "Not Started Yet"]
                        current_status_idx = status_options.index(task_item["Status"]) if task_item["Status"] in status_options else 2
                        
                        new_st = st.selectbox(
                            "Status", 
                            status_options, 
                            index=current_status_idx, 
                            key=f"status_sel_{sponsor_obj['Sponsor']}_{ev_idx}_{t_idx}_sp",
                            label_visibility="collapsed"
                        )
                        if new_st != task_item["Status"]:
                            task_item["Status"] = new_st
                            st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Task '{task_item['Task']}' updated to '{new_st}' for {sponsor_obj['Sponsor']}.")
                            st.rerun()
                            
                    with tc3:
                        if task_item["Status"] == "Completed":
                            st.success("✅ Completed")
                        elif task_item["Status"] == "In Progress":
                            st.warning("⏳ In Progress")
                        else:
                            st.error("🛑 Not Started")
            else:
                st.info("No work deliverables configured yet.")
                
            with st.form(key=f"add_task_form_{sponsor_obj['Sponsor']}_{ev_idx}_sp"):
                st.markdown("**Add New Work Deliverable / Task**")
                col_nt1, col_nt2 = st.columns([3, 1])
                with col_nt1:
                    new_task_title = st.text_input("Task Title", placeholder="e.g., LED Screen Media Clip Playback", label_visibility="collapsed")
                with col_nt2:
                    add_task_btn = st.form_submit_button("➕ Add Task")
                    
                if add_task_btn and new_task_title:
                    ev_data["Tasks"].append({"Task": new_task_title, "Status": "Not Started Yet"})
                    st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Added task '{new_task_title}' to {event_title}.")
                    st.success(f"Added deliverable: '{new_task_title}'")
                    st.rerun()

# --- SIDEBAR CONTROL PANEL & VIEW ROUTER ---
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=64)
    st.title("System Control")
    st.caption("Agentic AI Operations Platform")
    st.divider()
    
    st.markdown("**🔐 Access Mode**")
    selected_view = st.radio("Select Portal View:", ["🛡️ Event Admin Hub", "🤝 Sponsor Login Portal"], index=0 if st.session_state.view_mode == "🛡️ Event Admin Hub" else 1)
    
    if selected_view != st.session_state.view_mode:
        st.session_state.view_mode = selected_view
        st.rerun()

    st.divider()
    if st.session_state.view_mode == "🤝 Sponsor Login Portal" and st.session_state.authenticated_sponsor:
        st.success(f"Authenticated as:\n**{st.session_state.authenticated_sponsor['Sponsor']}**")
        if st.button("🚪 Logout Sponsor"):
            st.session_state.authenticated_sponsor = None
            st.rerun()

    st.divider()
    st.markdown("**📜 Live Activity Stream**")
    for log in st.session_state.activity_logs[-4:]:
        st.caption(f"• {log}")

# ==========================================
# VIEW ROUTE 1: SPONSOR DEDICATED LOGIN PORTAL
# ==========================================
if st.session_state.view_mode == "🤝 Sponsor Login Portal":
    if not st.session_state.authenticated_sponsor:
        st.title("🔑 Sponsor Partner Login Portal")
        st.caption("Dedicated authentication portal for collaborated sponsors to track real-time performance, deliverables, and event status.")
        
        col_l1, col_l2 = st.columns([1, 1])
        with col_l1:
            with st.form("sponsor_login_form"):
                st.subheader("Partner Authentication")
                
                default_email = st.session_state.credentials_modal["email"] if st.session_state.credentials_modal else ""
                default_pass = st.session_state.credentials_modal["password"] if st.session_state.credentials_modal else ""
                
                email_input = st.text_input("Sponsor Contact Email", value=default_email, placeholder="e.g., sponsorships@techcorp.com")
                pass_input = st.text_input("Access Key / Password", value=default_pass, type="password")
                
                login_btn = st.form_submit_button("Authenticate & Access Dashboard")
                if login_btn:
                    matched = [
                        sp for sp in st.session_state.sponsors 
                        if sp["Contact Email"].strip().lower() == email_input.strip().lower() and sp["Password"] == pass_input.strip()
                    ]
                    if matched:
                        st.session_state.authenticated_sponsor = matched[0]
                        st.session_state.credentials_modal = None
                        st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Sponsor {matched[0]['Sponsor']} logged into portal.")
                        st.success(f"Welcome back, {matched[0]['Sponsor']}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please check your Email and Access Key.")
                        
        with col_l2:
            st.info("💡 **Generated Credentials Info:**\n\nWhen you collaborate with a sponsor in the Admin Hub, unique login credentials are generated here to view real-time event tracking and task deliverables.")
    else:
        sp_data = st.session_state.authenticated_sponsor
        avg_rating = round(sp_data["Rating Numerator"] / sp_data["Rating Count"], 1) if sp_data["Rating Count"] > 0 else 5.0
        
        st.title(f"🏢 {sp_data['Sponsor']} — Performance & Collaboration Portal")
        st.caption(f"Category: **{sp_data['Category']}** | Status: **{sp_data['Performance Status']}** | Contact: `{sp_data['Contact Email']}`")
        
        st.divider()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Leads Generated", sp_data["Leads Generated"], delta="▲ Live Sync Active")
        m2.metric("Audience Engagement Rate", f"{sp_data['Engagement Rate (%)']}%", delta="▲ High Benchmark")
        m3.metric("Deliverables Completed", f"{sp_data['Deliverables Met (%)']}%", delta="100% Target")
        m4.metric("Partner Performance Score", f"⭐ {avg_rating} / 5.0", delta=f"{sp_data['Rating Count']} Organizer Reviews")
        
        st.divider()
        
        col_p1, col_p2 = st.columns([1.5, 1])
        with col_p1:
            render_event_deliverables_tracker(sp_data, is_admin=False)
            
            st.divider()
            st.subheader("💬 Event Organizer Reviews & Feedback")
            for rev in sp_data["Reviews"]:
                st.info(f"\"{rev}\"")
                
        with col_p2:
            st.subheader("📈 Sponsorship ROI Benchmarks")
            df_perf = pd.DataFrame({
                "Metric": ["Leads Generated", "Engagement Rate (%)", "Deliverables (%)"],
                "Value": [sp_data["Leads Generated"], sp_data["Engagement Rate (%)"], sp_data["Deliverables Met (%)"]]
            })
            st.bar_chart(df_perf.set_index("Metric"))

# ==========================================
# VIEW ROUTE 2: MAIN ADMIN HUB
# ==========================================
else:
    st.title("⚡ Smart Event Management Operations Hub")
    st.caption("Agentic AI Platform for Sponsorship Matchmaking, Incident Automation & Real-time Operations")

    st.markdown("""
        <div class="status-banner">
            <span>🟢 <b>ALL SYSTEMS OPERATIONAL</b> | 4 Active Dispatch Nodes | Network Latency: 12ms</span>
            <span><b>Server Time:</b> """ + datetime.datetime.now().strftime("%H:%M:%S") + """ IST</span>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.credentials_modal:
        cred = st.session_state.credentials_modal
        st.success("🎉 **Collaboration Established & Access Granted!**")
        
        with st.expander("🔑 **Sponsor Generated Credentials & Direct Access**", expanded=True):
            st.write(f"Collaboration with **{cred['sponsor']}** for **'{cred['event']}'** has been initialized.")
            
            mc1, mc2 = st.columns(2)
            with mc1:
                st.info(f"📧 **Login Email:** `{cred['email']}`")
            with mc2:
                st.info(f"🔑 **Generated Access Key:** `{cred['password']}`")
                
            st.markdown("Share these credentials with the sponsor team, or login directly to view the event deliverable status.")
            
            col_m1, col_m2 = st.columns([1, 3])
            with col_m1:
                if st.button("🚀 Go to Sponsor Portal Login"):
                    st.session_state.view_mode = "🤝 Sponsor Login Portal"
                    st.rerun()
            with col_m2:
                if st.button("Close Modal"):
                    st.session_state.credentials_modal = None
                    st.rerun()

    st.markdown("### 📊 Real-Time Operations & Performance Analytics")
    open_count = len(st.session_state.incidents[st.session_state.incidents["Status"] != "RESOLVED"])
    critical_count = len(st.session_state.incidents[st.session_state.incidents["Priority"] == "Critical Alerts"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Active Sponsor Portfolio", value=len(st.session_state.sponsors), delta="🟢 Tracking Active")
    m2.metric(label="Active Incident Tickets", value=open_count, delta=f"🔴 {critical_count} Critical", delta_color="inverse")
    m3.metric(label="Sponsor Engagement Avg", value="82.4%", delta="▲ +4.2%")
    m4.metric(label="System Health", value="98.1%", delta="🟢 Optimal")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🤝 AI Sponsorship Agent", 
        "🚨 AI Incident Workflows", 
        "🔔 Operational Alert Streams", 
        "📈 Analytics & Reports"
    ])

    with tab1:
        st.header("🤝 AI Sponsorship Agent & Performance Tracking")
        
        st.subheader("📊 Sponsor Performance & Collaboration Tracking")
        
        filter_collab_only = st.checkbox("Show Only Active Collaborations", value=False)
        
        tracked_sponsors = [
            sp for sp in st.session_state.sponsors 
            if not filter_collab_only or len(sp["Collaborated Events"]) > 0
        ]
        
        if tracked_sponsors:
            perf_rows = []
            for sp in tracked_sponsors:
                avg_r = round(sp["Rating Numerator"] / sp["Rating Count"], 1) if sp["Rating Count"] > 0 else 5.0
                event_names = [ev["Event Name"] for ev in sp["Collaborated Events"]]
                collab_events_str = ", ".join(event_names) if event_names else "None (Pending)"
                
                perf_rows.append({
                    "Sponsor Name": sp["Sponsor"],
                    "Category": sp["Category"],
                    "Status": sp["Performance Status"],
                    "Collaborated Events": collab_events_str,
                    "Rating": f"⭐ {avg_r} / 5.0",
                    "Leads Generated": sp["Leads Generated"],
                    "Engagement Rate": f"{sp['Engagement Rate (%)']}%",
                    "Deliverables Met": f"{sp['Deliverables Met (%)']}%",
                    "Budget": f"${sp['Budget Capacity ($)']:,}"
                })
            
            st.dataframe(pd.DataFrame(perf_rows), use_container_width=True)
        else:
            st.info("No collaborated sponsors found based on selected filter.")

        st.divider()

        with st.expander("➕ Register & Add New Sponsor", expanded=False):
            with st.form("add_sponsor_form"):
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    new_sname = st.text_input("Sponsor / Company Name*", placeholder="e.g., Nova Tech")
                    new_scat = st.selectbox("Category*", ["Technology & IT", "Health & Wellness", "Finance & Banking", "Automotive & EV", "Media & Promotion", "Education"])
                    new_semail = st.text_input("Contact Email*", placeholder="contact@novatech.com")
                with col_s2:
                    new_sbudget = st.number_input("Budget Capacity ($)", min_value=1000, value=10000, step=1000)
                    new_simg = st.text_input("Banner / Logo Image URL", value="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&q=80")
                
                submit_sp = st.form_submit_button("Register Sponsor")
                if submit_sp:
                    if new_sname and new_semail:
                        gen_pass = "".join(random.choices(string.ascii_letters + string.digits, k=8))
                        new_entry = {
                            "Sponsor": new_sname,
                            "Category": new_scat,
                            "Contact Email": new_semail,
                            "Password": gen_pass,
                            "Budget Capacity ($)": new_sbudget,
                            "Engagement Rate (%)": 0,
                            "Leads Generated": 0,
                            "Deliverables Met (%)": 100,
                            "Performance Status": "New Partner",
                            "Rating Numerator": 5.0,
                            "Rating Count": 1,
                            "Reviews": ["Newly onboarded sponsor."],
                            "Image": new_simg,
                            "AI Match Score": "90% Match",
                            "Collaborated Events": []
                        }
                        st.session_state.sponsors.append(new_entry)
                        st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] New sponsor '{new_sname}' added.")
                        st.success(f"✅ Successfully onboarded **{new_sname}**! Generated Access Key: `{gen_pass}`")
                        st.rerun()
                    else:
                        st.error("Please fill in required fields (Name & Email).")

        st.subheader("🔍 AI Matchmaker & Filter")
        col_req1, col_req2 = st.columns(2)
        categories = ["All Categories"] + sorted(list(set([sp["Category"] for sp in st.session_state.sponsors])))
        
        with col_req1:
            req_category = st.selectbox("Select Event Domain / Category:", categories)
        with col_req2:
            req_budget = st.slider("Minimum Budget Capacity ($):", min_value=1000, max_value=25000, value=5000, step=1000)

        st.divider()

        st.subheader("🏢 All Sponsor Portfolios & Direct Engagement")
        matched_sponsors = [
            sp for sp in st.session_state.sponsors 
            if (req_category == "All Categories" or sp["Category"] == req_category) and sp["Budget Capacity ($)"] >= req_budget
        ]

        for idx, sp in enumerate(matched_sponsors):
            with st.container():
                col_img, col_info, col_action = st.columns([1.2, 2, 1.5])
                avg_rating = round(sp["Rating Numerator"] / sp["Rating Count"], 1) if sp["Rating Count"] > 0 else 5.0
                
                with col_img:
                    st.image(sp["Image"], caption="Activation Photo", use_container_width=True)
                
                with col_info:
                    st.markdown(f"### **{sp['Sponsor']}** `{sp['AI Match Score']}`")
                    st.write(f"**Category:** {sp['Category']} | **Budget:** ${sp['Budget Capacity ($)']:,}")
                    st.write(f"**Performance Status:** `{sp['Performance Status']}` | **Rating:** ⭐ {avg_rating}/5.0 ({sp['Rating Count']} reviews)")
                    
                    event_names = [ev["Event Name"] for ev in sp["Collaborated Events"]]
                    if event_names:
                        st.write(f"🤝 **Collaborated Events:** `{', '.join(event_names)}`")
                    else:
                        st.write("🤝 **Collaborated Events:** *No active events yet*")
                    
                    with st.expander("💬 View All Feedback & Reviews"):
                        for rev in sp["Reviews"]:
                            st.caption(f"• \"{rev}\"")
                    
                    # Clean Read-Only Display inside Admin Hub
                    if sp["Collaborated Events"]:
                        render_event_deliverables_tracker(sp, is_admin=True)

                with col_action:
                    st.markdown("**✉️ Collaborate & Outreach**")
                    user_event_name = st.text_input("Event Name:", value="Tech Expo 2026", key=f"ev_{idx}")
                    custom_msg = st.text_area("Outreach Message:", value=f"Hi {sp['Sponsor']} team, we reviewed your performance track record and would love to partner with you.", key=f"msg_{idx}")
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button("Send Email", key=f"btn_email_{idx}"):
                            st.success(f"📧 **Email Sent!**")
                            st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Email dispatched to {sp['Sponsor']}.")
                    
                    with col_b2:
                        if st.button("🤝 Collaborate", key=f"btn_collab_{idx}"):
                            existing_events = [ev["Event Name"] for ev in sp["Collaborated Events"]]
                            if user_event_name not in existing_events:
                                sp["Collaborated Events"].append({
                                    "Event Name": user_event_name,
                                    "Tasks": [
                                        {"Task": "Initial Sponsorship Agreement Signed", "Status": "Completed"},
                                        {"Task": "Booth Space & Logistics Allocation", "Status": "In Progress"},
                                        {"Task": "Marketing Banner & Digital Ad Assets", "Status": "Not Started Yet"},
                                        {"Task": "On-Site Lead Generation Setup", "Status": "Not Started Yet"}
                                    ]
                                })
                                sp["Performance Status"] = "Collaborated Partner"
                            
                            gen_pass = sp["Password"] if sp["Password"] != "pass" else "Sponsor" + str(random.randint(100, 999))
                            sp["Password"] = gen_pass
                            
                            st.session_state.credentials_modal = {
                                "sponsor": sp["Sponsor"],
                                "event": user_event_name,
                                "email": sp["Contact Email"],
                                "password": gen_pass
                            }
                            
                            st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Collaborated with {sp['Sponsor']} for {user_event_name}. Credentials generated.")
                            st.rerun()

        st.divider()

        st.subheader("📝 Submit Feedback & Update Sponsor Performance")
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.markdown("**Submit Event Feedback for Sponsor**")
            target_sponsor_name = st.selectbox("Select Sponsor to Review:", [sp["Sponsor"] for sp in st.session_state.sponsors])
            rating_val = st.slider("Rating (1 to 5 Stars):", 1.0, 5.0, 4.5, 0.5)
            review_text = st.text_area("Event Host / Attendee Review Comments:", placeholder="Share your experience working with this sponsor...")
            
            if st.button("Submit Sponsor Review"):
                for sp in st.session_state.sponsors:
                    if sp["Sponsor"] == target_sponsor_name:
                        sp["Rating Numerator"] += rating_val
                        sp["Rating Count"] += 1
                        if review_text:
                            sp["Reviews"].append(review_text)
                        st.success(f"⭐ Review recorded for **{target_sponsor_name}**!")
                        st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Review submitted for {target_sponsor_name}.")
                        st.rerun()

        with col_f2:
            st.markdown("**Sponsor Metrics Snapshot**")
            perf_data = []
            for sp in st.session_state.sponsors:
                avg_r = round(sp["Rating Numerator"] / sp["Rating Count"], 1) if sp["Rating Count"] > 0 else 5.0
                perf_data.append({
                    "Sponsor": sp["Sponsor"],
                    "Rating": f"⭐ {avg_r}/5.0",
                    "Leads": sp["Leads Generated"],
                    "Engagement Rate": f"{sp['Engagement Rate (%)']}%",
                    "Status": sp["Performance Status"]
                })
            st.dataframe(pd.DataFrame(perf_data), use_container_width=True)

    with tab2:
        st.header("🚨 AI Incident Agent & Workflow Automation")

        col_create, col_manage = st.columns([1, 1.2])

        with col_create:
            st.subheader("📌 Log & Route New Incident")
            with st.form("incident_logging_form"):
                inc_title = st.text_input("1. Identify Incident", placeholder="e.g., VIP Gate Scanner Failure")
                inc_reporter = st.text_input("2. Record Reporter Details", placeholder="e.g., Gate Supervisor")
                inc_category = st.selectbox("3. Categorize Domain", ["Electrical & Hardware", "Network & IT", "Logistics & Facility", "Guest Relations & VIP"])
                inc_priority = st.selectbox("4. Prioritize Severity", ["Critical Alerts", "High-Priority Alerts", "Medium-Priority Alerts", "Informational Alerts"])
                
                auto_team = "Emergency Operations Center" if inc_priority == "Critical Alerts" else "On-Site Security & IT" if inc_priority == "High-Priority Alerts" else "Logistics & Facility Crew" if inc_priority == "Medium-Priority Alerts" else "Guest Relations Team"
                st.info(f"5. Escalate Destination: `{auto_team}`")
                
                submit_log = st.form_submit_button("Log Incident Ticket")
                if submit_log and inc_title:
                    new_id = f"INC-{101 + len(st.session_state.incidents)}"
                    new_row = {
                        "ID": new_id, "Title": inc_title, "Category": inc_category, "Priority": inc_priority,
                        "Assigned Team": auto_team, "Status": "INVESTIGATING", "Root Cause": "Pending Diagnostics",
                        "Solution": "Pending Resolution", "Time": datetime.datetime.now().strftime("%H:%M"),
                        "Reporter": inc_reporter, "PIR Summary": "Pending PIR", "SLA Remaining": 0.90
                    }
                    st.session_state.incidents = pd.concat([st.session_state.incidents, pd.DataFrame([new_row])], ignore_index=True)
                    st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] New incident {new_id} logged.")
                    st.success(f"Logged {new_id}! Escalated to {auto_team}.")
                    st.rerun()

        with col_manage:
            st.subheader("⚙️ Investigate, Resolve & Review (PIR)")
            if not st.session_state.incidents.empty:
                selected_id = st.selectbox("Select Incident Ticket:", st.session_state.incidents["ID"].tolist())
                inc_idx = st.session_state.incidents[st.session_state.incidents["ID"] == selected_id].index[0]
                curr_item = st.session_state.incidents.loc[inc_idx]

                st.write(f"**Title:** {curr_item['Title']} | **Category:** {curr_item['Category']}")
                st.write(f"**Current Status:** `{curr_item['Status']}` | **Assigned Team:** `{curr_item['Assigned Team']}`")

                with st.form("incident_resolution_form"):
                    rca_input = st.text_input("Root Cause Analysis (RCA):", value=curr_item["Root Cause"])
                    sol_input = st.text_input("Solution Applied:", value=curr_item["Solution"])
                    status_input = st.selectbox("Update Status:", ["INVESTIGATING", "RESOLVED", "CLOSED"], index=1 if curr_item["Status"] == "RESOLVED" else 0)
                    pir_input = st.text_area("Post Incident Review (PIR):", value=curr_item["PIR Summary"])

                    if st.form_submit_button("Update Incident Lifecycle"):
                        st.session_state.incidents.at[inc_idx, "Root Cause"] = rca_input
                        st.session_state.incidents.at[inc_idx, "Solution"] = sol_input
                        st.session_state.incidents.at[inc_idx, "Status"] = status_input
                        st.session_state.incidents.at[inc_idx, "PIR Summary"] = pir_input
                        st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Ticket {selected_id} updated to {status_input}.")
                        st.success(f"Updated ticket {selected_id}!")
                        st.rerun()

    with tab3:
        st.header("🔔 Live Operational Command Center & Alert Dispatch")

        f_col1, f_col2 = st.columns([1, 2])
        with f_col1:
            status_filter = st.radio("Filter Alerts by Status:", ["All Active", "INVESTIGATING", "RESOLVED"], horizontal=True)

        c_crit = len(st.session_state.incidents[st.session_state.incidents["Priority"] == "Critical Alerts"])
        c_high = len(st.session_state.incidents[st.session_state.incidents["Priority"] == "High-Priority Alerts"])
        c_med = len(st.session_state.incidents[st.session_state.incidents["Priority"] == "Medium-Priority Alerts"])
        c_info = len(st.session_state.incidents[st.session_state.incidents["Priority"] == "Informational Alerts"])

        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.markdown(f"🔴 **Critical:** `{c_crit} Active`")
        sc2.markdown(f"🟡 **High Priority:** `{c_high} Active`")
        sc3.markdown(f"🔵 **Medium Priority:** `{c_med} Active`")
        sc4.markdown(f"🟢 **Informational:** `{c_info} Active`")

        st.divider()

        col_a1, col_a2 = st.columns(2)

        def render_alert_card(item, alert_type="error"):
            if status_filter != "All Active" and item["Status"] != status_filter:
                return
                
            with st.expander(f"[{item['ID']}] {item['Title']} — Status: {item['Status']}", expanded=True):
                if alert_type == "error":
                    st.error(f"📍 **Target:** `{item['Assigned Team']}` | 🕒 **Logged:** `{item['Time']}`")
                elif alert_type == "warning":
                    st.warning(f"📍 **Target:** `{item['Assigned Team']}` | 🕒 **Logged:** `{item['Time']}`")
                else:
                    st.info(f"📍 **Target:** `{item['Assigned Team']}` | 🕒 **Logged:** `{item['Time']}`")
                    
                st.caption(f"👤 **Reporter:** {item['Reporter']}")
                st.write("⏱️ **SLA Expiration Remaining:**")
                st.progress(float(item.get("SLA Remaining", 0.5)))
                
                st.markdown("---")
                st.markdown(f"**RCA Diagnostics:** {item['Root Cause']}")
                st.markdown(f"**Applied Solution:** {item['Solution']}")
                
                btn_1, btn_2 = st.columns(2)
                if btn_1.button("✅ Mark Resolved", key=f"res_{item['ID']}"):
                    st.session_state.incidents.loc[st.session_state.incidents["ID"] == item["ID"], "Status"] = "RESOLVED"
                    st.session_state.activity_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Ticket {item['ID']} resolved via Command Center.")
                    st.success(f"Ticket {item['ID']} resolved!")
                    st.rerun()
                if btn_2.button("📢 Broadcast Alert", key=f"bc_{item['ID']}"):
                    st.warning(f"Broadcast sent for {item['ID']}!")

        with col_a1:
            st.markdown("### 🔴 Critical Alerts Matrix")
            crit_items = st.session_state.incidents[st.session_state.incidents["Priority"] == "Critical Alerts"]
            for _, item in crit_items.iterrows():
                render_alert_card(item, "error")

            st.divider()

            st.markdown("### 🟡 High-Priority Alerts Matrix")
            high_items = st.session_state.incidents[st.session_state.incidents["Priority"] == "High-Priority Alerts"]
            for _, item in high_items.iterrows():
                render_alert_card(item, "warning")

        with col_a2:
            st.markdown("### 🔵 Medium-Priority Alerts Matrix")
            med_items = st.session_state.incidents[st.session_state.incidents["Priority"] == "Medium-Priority Alerts"]
            for _, item in med_items.iterrows():
                render_alert_card(item, "info")

            st.divider()

            st.markdown("### 🟢 Informational Alerts Stream")
            info_items = st.session_state.incidents[st.session_state.incidents["Priority"] == "Informational Alerts"]
            for _, item in info_items.iterrows():
                render_alert_card(item, "info")

    with tab4:
        st.header("📈 AI Analytics, Visual Dashboards & Reports")
        
        st.subheader("📊 Visual Operations & Sponsor Performance Charts")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("**Incidents Volume by Category**")
            if not st.session_state.incidents.empty:
                inc_counts = st.session_state.incidents["Category"].value_counts()
                st.bar_chart(inc_counts)
                
        with chart_col2:
            st.markdown("**Sponsor Lead Generation Benchmarks**")
            if st.session_state.sponsors:
                sp_df = pd.DataFrame(st.session_state.sponsors)
                st.bar_chart(data=sp_df, x="Sponsor", y="Leads Generated")

        st.divider()

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("### 🤖 Predictive Crowd Analytics")
            selected_venue = st.selectbox("Select Event Venue / Zone:", ["Main Auditorium", "Hall A (Exhibition)", "Hall B (Keynote Zone)", "Outdoor Arena"])
            hall_capacity = st.slider(f"{selected_venue} Occupancy Level (%)", min_value=10, max_value=100, value=80)
            st.progress(hall_capacity / 100)
            
        with col_p2:
            st.markdown("### ⚡ AI Recommendation Engine")
            if hall_capacity >= 80:
                st.error(f'🤖 **Intervention Alert:** {selected_venue} capacity is at {hall_capacity}%. AI recommends opening overflow gates immediately.')
            else:
                st.success(f'🤖 **Status:** {selected_venue} crowd flow parameters operating normally.')

        st.divider()

        st.markdown("### 📋 Incident Audit Log & Export")
        st.dataframe(st.session_state.incidents, use_container_width=True)
        st.download_button(
            label="📥 Export Full Incident Analytical Report (CSV)",
            data=st.session_state.incidents.to_csv(index=False),
            file_name="Incident_Analytical_Report.csv",
            mime="text/csv"
        )