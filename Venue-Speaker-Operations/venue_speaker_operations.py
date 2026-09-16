import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# -------------------------------------------------------------
# 1. PAGE CONFIGURATION & PREMIUM STYLING
# -------------------------------------------------------------
st.set_page_config(
    page_title="Venue & Speaker Hub",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for visual polish
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Hero Banner Styling */
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #ffffff;
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 6px;
        color: #f8fafc;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    /* Status Pill Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-green { background-color: #dcfce7; color: #15803d; }
    .badge-blue { background-color: #dbeafe; color: #1d4ed8; }
    .badge-purple { background-color: #f3e8ff; color: #7e22ce; }
    .badge-amber { background-color: #fef3c7; color: #b45309; }

    /* Amenity Tag Pill */
    .tag-pill {
        background-color: #f1f5f9;
        color: #475569;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        margin-right: 4px;
        border: 1px solid #e2e8f0;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. INITIALIZE SESSION STATE DATA (INR / RUPEES RATES)
# -------------------------------------------------------------
if 'venues' not in st.session_state:
    st.session_state.venues = pd.DataFrame([
        {
            "ID": "V101", 
            "Name": "Grand Horizon Hall", 
            "Capacity": 500, 
            "Location": "Main Campus", 
            "Hourly Rate (₹)": 15000,
            "Tag": "Flagship",
            "Amenities": ["📶 High-Speed Wi-Fi", "🎥 4K Projectors", "🔊 Surround Sound", "❄️ Central AC"],
            "Rating": 4.9,
            "Top Review": "Acoustics were amazing for our annual fest!",
            "Image": "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?w=400&q=80"
        },
        {
            "ID": "V102", 
            "Name": "Auditorium A", 
            "Capacity": 250, 
            "Location": "North Wing", 
            "Hourly Rate (₹)": 8000,
            "Tag": "Popular",
            "Amenities": ["📶 Wi-Fi", "🎤 Wireless Mics", "💡 Stage Lighting"],
            "Rating": 4.7,
            "Top Review": "Great seating layout and crisp AV setup.",
            "Image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=400&q=80"
        },
        {
            "ID": "V103", 
            "Name": "Tech Seminar Room", 
            "Capacity": 80, 
            "Location": "Innovation Hub", 
            "Hourly Rate (₹)": 3500,
            "Tag": "Interactive",
            "Amenities": ["📶 Wi-Fi", "🖥️ Smart Board", "🔌 Power at All Desks"],
            "Rating": 4.5,
            "Top Review": "Perfect for hands-on technical workshops.",
            "Image": "https://images.unsplash.com/photo-1431540015161-0bf868a2d407?w=400&q=80"
        },
        {
            "ID": "V104", 
            "Name": "Executive Boardroom", 
            "Capacity": 30, 
            "Location": "Admin Block", 
            "Hourly Rate (₹)": 2500,
            "Tag": "VIP Space",
            "Amenities": ["📺 75\" Display", "☕ Coffee Station", "📹 Video Conf Equipment"],
            "Rating": 4.8,
            "Top Review": "Very professional and quiet environment.",
            "Image": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400&q=80"
        },
        {
            "ID": "V105", 
            "Name": "Open-Air Amphitheatre", 
            "Capacity": 1200, 
            "Location": "Central Courtyard", 
            "Hourly Rate (₹)": 25000,
            "Tag": "Outdoor",
            "Amenities": ["🎪 Open Stage", "💡 Concert Lighting", "🍔 Food Stall Booths", "🔊 Line Array Audio"],
            "Rating": 4.8,
            "Top Review": "Incredible venue for evening cultural events and keynotes!",
            "Image": "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=400&q=80"
        },
        {
            "ID": "V106", 
            "Name": "Virtual XR & Broadcast Studio", 
            "Capacity": 40, 
            "Location": "Media Center", 
            "Hourly Rate (₹)": 10000,
            "Tag": "Virtual-Ready",
            "Amenities": ["🟢 Green Screen", "🎥 4K Live Stream Cameras", "🎙️ Studio Mics", "💡 Grid Lights"],
            "Rating": 4.9,
            "Top Review": "Top-notch setup for global hybrid streaming webinars.",
            "Image": "https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=400&q=80"
        },
        {
            "ID": "V107", 
            "Name": "Incubation Design Lab", 
            "Capacity": 60, 
            "Location": "Research Park", 
            "Hourly Rate (₹)": 4500,
            "Tag": "Collaborative",
            "Amenities": ["📶 Wi-Fi 6", "🖊️ Modular Whiteboards", "🛠️ Hardware Benches", "☕ Breakout Area"],
            "Rating": 4.6,
            "Top Review": "The movable furniture made hackathon group sessions effortless.",
            "Image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400&q=80"
        },
        {
            "ID": "V108", 
            "Name": "Grand Conference Center", 
            "Capacity": 800, 
            "Location": "South Campus Gate", 
            "Hourly Rate (₹)": 20000,
            "Tag": "Large Scale",
            "Amenities": ["📶 Multi-AP Wi-Fi", "🎤 8 Wireless Mics", "🚗 Underground Parking", "🍽️ Catering Room"],
            "Rating": 4.7,
            "Top Review": "Hosted our multi-track international conference with zero hiccups.",
            "Image": "https://images.unsplash.com/photo-1511578314322-379afb476865?w=400&q=80"
        }
    ])

if 'speakers' not in st.session_state:
    st.session_state.speakers = pd.DataFrame([
        {
            "ID": "S201", 
            "Name": "Dr. Aris Thorne", 
            "Expertise": "AI & Machine Learning", 
            "Rating": 4.9, 
            "Fee (₹/hr)": 20000, 
            "Available Time": "Morning (9 AM - 12 PM)",
            "Badges": ["Keynote Speaker", "Top Rated"],
            "Bio": "Published ML researcher with 10+ years industry consulting experience.",
            "Photo": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&q=80"
        },
        {
            "ID": "S202", 
            "Name": "Elena Rostova", 
            "Expertise": "Embedded Systems & IoT", 
            "Rating": 4.7, 
            "Fee (₹/hr)": 15000, 
            "Available Time": "Afternoon (1 PM - 5 PM)",
            "Badges": ["Hardware Specialist"],
            "Bio": "Hardware architect specializing in low-power microcontrollers & RTOS.",
            "Photo": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&q=80"
        },
        {
            "ID": "S203", 
            "Name": "Marcus Vance", 
            "Expertise": "VLSI & Hardware Design", 
            "Rating": 4.8, 
            "Fee (₹/hr)": 18000, 
            "Available Time": "Full Day",
            "Badges": ["Industry Expert"],
            "Bio": "Senior ASIC Engineer leading next-gen chip architectures and physical design.",
            "Photo": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&q=80"
        },
        {
            "ID": "S204", 
            "Name": "Siddharth Rao", 
            "Expertise": "Cybersecurity & Cloud", 
            "Rating": 4.6, 
            "Fee (₹/hr)": 12000, 
            "Available Time": "Evening (5 PM - 8 PM)",
            "Badges": ["Certified Ethical Hacker"],
            "Bio": "Cloud security auditor and active open-source security tool contributor.",
            "Photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&q=80"
        },
        {
            "ID": "S205", 
            "Name": "Dr. Priya Sundaram", 
            "Expertise": "Edge AI & TinyML", 
            "Rating": 4.9, 
            "Fee (₹/hr)": 22000, 
            "Available Time": "Morning (9 AM - 1 PM)",
            "Badges": ["IEEE Fellow", "Keynote Speaker"],
            "Bio": "Pioneer in optimizing deep neural networks for ultra-low-power microcontrollers.",
            "Photo": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&q=80"
        },
        {
            "ID": "S206", 
            "Name": "Vikram Malhotra", 
            "Expertise": "RF & Antenna Design", 
            "Rating": 4.8, 
            "Fee (₹/hr)": 16000, 
            "Available Time": "Afternoon (2 PM - 6 PM)",
            "Badges": ["5G/6G Consultant"],
            "Bio": "12+ years of experience designing high-frequency phased array antennas for satellites.",
            "Photo": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=300&q=80"
        },
        {
            "ID": "S207", 
            "Name": "Sarah Jenkins", 
            "Expertise": "Robotics & Automation", 
            "Rating": 4.7, 
            "Fee (₹/hr)": 14000, 
            "Available Time": "Full Day",
            "Badges": ["ROS Specialist"],
            "Bio": "Robotics lead building autonomous navigation algorithms for industrial drones.",
            "Photo": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&q=80"
        },
        {
            "ID": "S208", 
            "Name": "David Chen", 
            "Expertise": "VLSI Verification (SystemVerilog)", 
            "Rating": 4.9, 
            "Fee (₹/hr)": 18000, 
            "Available Time": "Evening (4 PM - 8 PM)",
            "Badges": ["UVM Expert"],
            "Bio": "Principal engineer specializing in formal verification and UVM testbench architectures.",
            "Photo": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&q=80"
        }
    ])

if 'venue_bookings' not in st.session_state:
    st.session_state.venue_bookings = pd.DataFrame(columns=[
        "Booking ID", "Event Title", "Venue Name", "Date", "Time Slot", "Capacity Reserved", "Total Cost (₹)"
    ])

if 'speaker_bookings' not in st.session_state:
    st.session_state.speaker_bookings = pd.DataFrame(columns=[
        "Booking ID", "Event Title", "Speaker Name", "Expertise Topic", "Date", "Time Slot", "Total Fee (₹)"
    ])

if 'reviews' not in st.session_state:
    st.session_state.reviews = pd.DataFrame([
        {"Review ID": "R301", "Target Type": "Venue", "Target Name": "Grand Horizon Hall", "Reviewer": "Ananya S.", "Rating": 5.0, "Comment": "Outstanding acoustics and spacious seating!", "Date": "2026-07-15"},
        {"Review ID": "R302", "Target Type": "Speaker", "Target Name": "Dr. Aris Thorne", "Reviewer": "Rahul V.", "Rating": 5.0, "Comment": "Captivating talk on Machine Learning models.", "Date": "2026-07-20"},
        {"Review ID": "R303", "Target Type": "Venue", "Target Name": "Open-Air Amphitheatre", "Reviewer": "Priya N.", "Rating": 5.0, "Comment": "Atmosphere during the evening talk was unmatched!", "Date": "2026-08-01"},
        {"Review ID": "R304", "Target Type": "Speaker", "Target Name": "Dr. Priya Sundaram", "Reviewer": "Karthik R.", "Rating": 5.0, "Comment": "Hands-down the best TinyML session I have attended.", "Date": "2026-08-05"}
    ])

# -------------------------------------------------------------
# 3. HELPER DIALOG MODALS
# -------------------------------------------------------------
@st.dialog("🏢 Reserve Venue")
def book_venue_dialog(venue):
    st.markdown(f"### Reserve **{venue['Name']}**")
    st.caption(f"📍 Location: {venue['Location']} | 👥 Capacity: {venue['Capacity']} Seats")
    
    with st.form("dialog_venue_form"):
        event_title = st.text_input("Event Name", placeholder="e.g., Annual Tech Symposium")
        booking_date = st.date_input("Event Date", datetime.date.today())
        time_slot = st.selectbox("Select Time Slot", ["Morning (9 AM - 1 PM)", "Afternoon (1 PM - 5 PM)", "Evening (5 PM - 9 PM)", "Full Day"])
        duration = st.number_input("Duration (Hours)", min_value=1, max_value=12, value=3)
        
        total_cost = venue["Hourly Rate (₹)"] * duration
        st.info(f"💰 **Total Cost:** `₹{total_cost:,.2f}` (₹{venue['Hourly Rate (₹)']:,}/hr × {duration} hrs)")
        
        submit = st.form_submit_button("Confirm Reservation", use_container_width=True)
        if submit:
            if not event_title.strip():
                st.error("Please enter an event title.")
            else:
                new_booking = {
                    "Booking ID": f"VB-{len(st.session_state.venue_bookings) + 101}",
                    "Event Title": event_title,
                    "Venue Name": venue["Name"],
                    "Date": str(booking_date),
                    "Time Slot": time_slot,
                    "Capacity Reserved": venue["Capacity"],
                    "Total Cost (₹)": total_cost
                }
                st.session_state.venue_bookings = pd.concat([st.session_state.venue_bookings, pd.DataFrame([new_booking])], ignore_index=True)
                st.toast(f"🎉 Reserved {venue['Name']} successfully!", icon="✅")
                st.rerun()

@st.dialog("🎤 Engage Speaker")
def book_speaker_dialog(speaker):
    st.markdown(f"### Engage **{speaker['Name']}**")
    st.caption(f"🎯 Domain: {speaker['Expertise']} | ⭐ Rating: {speaker['Rating']}")
    
    with st.form("dialog_speaker_form"):
        event_title = st.text_input("Session Title", placeholder="e.g., Keynote Speech")
        session_date = st.date_input("Session Date", datetime.date.today())
        duration = st.number_input("Duration (Hours)", min_value=1, max_value=8, value=2)
        
        total_fee = speaker["Fee (₹/hr)"] * duration
        st.info(f"💳 **Total Honorarium:** `₹{total_fee:,.2f}` (₹{speaker['Fee (₹/hr)']:,}/hr × {duration} hrs)")
        
        submit = st.form_submit_button("Confirm Engagement", use_container_width=True)
        if submit:
            if not event_title.strip():
                st.error("Please enter a session title.")
            else:
                new_booking = {
                    "Booking ID": f"SB-{len(st.session_state.speaker_bookings) + 201}",
                    "Event Title": event_title,
                    "Speaker Name": speaker["Name"],
                    "Expertise Topic": speaker["Expertise"],
                    "Date": str(session_date),
                    "Time Slot": speaker['Available Time'],
                    "Total Fee (₹)": total_fee
                }
                st.session_state.speaker_bookings = pd.concat([st.session_state.speaker_bookings, pd.DataFrame([new_booking])], ignore_index=True)
                st.toast(f"🎉 Engaged {speaker['Name']} successfully!", icon="✅")
                st.rerun()

@st.dialog("📄 Booking Confirmation Receipt")
def generate_invoice_dialog(row_data, b_type):
    st.markdown(f"### 🧾 Official Confirmation Receipt ({b_type})")
    st.divider()
    
    amount = row_data.get('Total Cost (₹)') if b_type=='Venue' else row_data.get('Total Fee (₹)')
    receipt_text = f"""
==================================================
           EVENT OPS HUB - RECEIPT              
==================================================
Booking ID:      {row_data.get('Booking ID')}
Date Generated:  {datetime.date.today()}
Event Title:     {row_data.get('Event Title')}
--------------------------------------------------
Resource:        {row_data.get('Venue Name') if b_type=='Venue' else row_data.get('Speaker Name')}
Scheduled Date:  {row_data.get('Date')}
Time Slot:       {row_data.get('Time Slot')}
Total Amount:    ₹{amount:,.2f}
Status:          CONFIRMED & RESERVED
==================================================
Thank you for using Event Ops Hub Platform!
"""
    st.code(receipt_text, language="text")
    st.download_button(
        label="📥 Download Receipt (.txt)",
        data=receipt_text,
        file_name=f"Receipt_{row_data.get('Booking ID')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# -------------------------------------------------------------
# 4. SIDEBAR NAVIGATION
# -------------------------------------------------------------
st.sidebar.markdown("### 🎪 **Event Ops Hub**")
st.sidebar.caption("Venue & Speaker Operations")

menu = st.sidebar.radio("Navigation", [
    "🏢 Venue Operations",
    "🎤 Speaker Directory",
    "💬 Community Reviews",
    "📊 Operations Analytics",
    "📋 Booking Log",
    "⚙️ Admin Control Panel"
])

# -------------------------------------------------------------
# HERO BANNER (TOP OF PAGE)
# -------------------------------------------------------------
st.markdown(f"""
    <div class="hero-container">
        <div class="hero-title">🎪 Operations Management Platform</div>
        <div class="hero-subtitle">
            Book top-tier venues and connect with leading subject experts • 
            <b>{len(st.session_state.venues)} Venues</b> Available • 
            <b>{len(st.session_state.speakers)} Speakers</b> Listed
        </div>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# MODULE 1: VENUE OPERATIONS
# -------------------------------------------------------------
if menu == "🏢 Venue Operations":
    st.subheader("🏢 Browse & Reserve Venues")

    col_s, col_f = st.columns([3, 1])
    with col_s:
        search_query = st.text_input("🔍 Quick Search venue name, tag, or location...", placeholder="e.g., Horizon, Amphitheatre, Studio, Main Campus")
    with col_f:
        min_cap = st.selectbox("Min Capacity", [0, 50, 100, 250, 500, 1000])

    filtered_venues = st.session_state.venues[st.session_state.venues["Capacity"] >= min_cap]
    if search_query.strip():
        filtered_venues = filtered_venues[
            filtered_venues["Name"].str.contains(search_query, case=False) | 
            filtered_venues["Location"].str.contains(search_query, case=False) |
            filtered_venues["Tag"].str.contains(search_query, case=False)
        ]

    st.markdown("---")

    for _, venue in filtered_venues.iterrows():
        with st.container(border=True):
            c1, c2, c3 = st.columns([1.2, 3, 1.2])
            with c1:
                st.image(venue["Image"], use_container_width=True)
            with c2:
                st.markdown(f"### {venue['Name']} <span class='badge badge-blue'>{venue['Tag']}</span> <span class='badge badge-green'>● Available</span>", unsafe_allow_html=True)
                st.markdown(f"📍 **Location:** {venue['Location']} &nbsp;&nbsp;|&nbsp;&nbsp; 👥 **Capacity:** {venue['Capacity']} Seats &nbsp;&nbsp;|&nbsp;&nbsp; ⭐ **{venue['Rating']}/5.0**")
                
                # Render Amenities Pills
                amenity_html = "".join([f"<span class='tag-pill'>{item}</span>" for item in venue["Amenities"]])
                st.markdown(f"<div style='margin-top:6px; margin-bottom:8px;'>{amenity_html}</div>", unsafe_allow_html=True)
                
                # Highlight Review Snippet
                st.caption(f"💬 *\"{venue['Top Review']}\"*")

            with c3:
                st.metric("Hourly Rate", f"₹{venue['Hourly Rate (₹)']:,}/hr")
                if st.button("Reserve Venue", key=f"btn_v_{venue['ID']}", use_container_width=True, type="primary"):
                    book_venue_dialog(venue)

# -------------------------------------------------------------
# MODULE 2: SPEAKER DIRECTORY
# -------------------------------------------------------------
elif menu == "🎤 Speaker Directory":
    st.subheader("🎤 Keynote Speakers & Experts")

    col_s, col_f = st.columns([3, 1])
    with col_s:
        search_spk = st.text_input("🔍 Search speaker name, domain, or keyword...", placeholder="e.g., AI, VLSI, TinyML, RF, Robotics")
    with col_f:
        topics = ["All Domains"] + sorted(list(set(st.session_state.speakers["Expertise"].tolist())))
        selected_topic = st.selectbox("Filter Domain", topics)

    filtered_speakers = st.session_state.speakers
    if selected_topic != "All Domains":
        filtered_speakers = filtered_speakers[filtered_speakers["Expertise"] == selected_topic]
    if search_spk.strip():
        filtered_speakers = filtered_speakers[
            filtered_speakers["Name"].str.contains(search_spk, case=False) | 
            filtered_speakers["Expertise"].str.contains(search_spk, case=False)
        ]

    st.markdown("---")

    for _, speaker in filtered_speakers.iterrows():
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 3, 1.2])
            with c1:
                st.image(speaker["Photo"], width=115)
            with c2:
                badges_html = "".join([f"<span class='badge badge-purple'>{b}</span>" for b in speaker["Badges"]])
                st.markdown(f"### {speaker['Name']} {badges_html}", unsafe_allow_html=True)
                st.markdown(f"🎯 **Expertise:** :blue[{speaker['Expertise']}] &nbsp;&nbsp;|&nbsp;&nbsp; ⭐ **Rating:** {speaker['Rating']} / 5.0")
                st.markdown(f"📝 *{speaker['Bio']}*")
                st.caption(f"⏰ **Preferred Slot:** {speaker['Available Time']}")
            with c3:
                st.metric("Honorarium", f"₹{speaker['Fee (₹/hr)']:,}/hr")
                if st.button("Engage Speaker", key=f"btn_s_{speaker['ID']}", use_container_width=True, type="primary"):
                    book_speaker_dialog(speaker)

# -------------------------------------------------------------
# MODULE 3: COMMUNITY REVIEWS
# -------------------------------------------------------------
elif menu == "💬 Community Reviews":
    st.subheader("💬 Reviews & Ratings")

    tab_view, tab_write = st.tabs(["⭐ All Reviews", "✍️ Submit Feedback"])

    with tab_view:
        reviews_df = st.session_state.reviews
        if not reviews_df.empty:
            avg_rating = reviews_df["Rating"].mean()
            
            r_col1, r_col2 = st.columns([1, 2])
            with r_col1:
                st.metric("Platform Rating Average", f"⭐ {avg_rating:.2f} / 5.0", delta=f"{len(reviews_df)} total reviews")
            with r_col2:
                st.write("**Rating Breakdown**")
                st.progress(0.90, text="5 Stars (90%)")
                st.progress(0.10, text="4 Stars (10%)")

            st.divider()

            for _, rev in reviews_df.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"**{rev['Target Name']}** <span class='badge badge-blue'>{rev['Target Type']}</span>", unsafe_allow_html=True)
                        st.write(f"\"{rev['Comment']}\"")
                        st.caption(f"Reviewed by **{rev['Reviewer']}** on {rev['Date']}")
                    with c2:
                        st.markdown(f"### ⭐ {rev['Rating']}")

    with tab_write:
        st.write("### Post Your Review")
        with st.form("submit_review_form"):
            r_type = st.radio("Target Category", ["Venue", "Speaker"], horizontal=True)
            target_list = st.session_state.venues["Name"].tolist() if r_type == "Venue" else st.session_state.speakers["Name"].tolist()
            r_target_name = st.selectbox("Select Target", target_list)
            
            r_reviewer = st.text_input("Your Name / Organization", placeholder="e.g., IEEE Student Branch")
            r_rating = st.slider("Rating", 1.0, 5.0, 5.0, 0.5)
            r_comment = st.text_area("Feedback Comments", placeholder="Describe stage setup, acoustics, or keynote content...")

            if st.form_submit_button("Post Review", use_container_width=True):
                if not r_reviewer or not r_comment:
                    st.error("Please fill in your name and comments.")
                else:
                    new_rev = {
                        "Review ID": f"R{len(st.session_state.reviews) + 301}",
                        "Target Type": r_type,
                        "Target Name": r_target_name,
                        "Reviewer": r_reviewer,
                        "Rating": r_rating,
                        "Comment": r_comment,
                        "Date": str(datetime.date.today())
                    }
                    st.session_state.reviews = pd.concat([st.session_state.reviews, pd.DataFrame([new_rev])], ignore_index=True)
                    st.toast("Thank you! Review posted successfully.", icon="⭐")
                    st.rerun()

# -------------------------------------------------------------
# MODULE 4: OPERATIONS ANALYTICS
# -------------------------------------------------------------
elif menu == "📊 Operations Analytics":
    st.subheader("📊 Financial & Utilization Overview")

    v_bookings = st.session_state.venue_bookings
    s_bookings = st.session_state.speaker_bookings

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Venue Reservations", len(v_bookings))
    k2.metric("Total Speaker Engagements", len(s_bookings))
    k3.metric("Total Venue Spend", f"₹{v_bookings['Total Cost (₹)'].sum():,.2f}" if not v_bookings.empty else "₹0")
    k4.metric("Total Speaker Fees", f"₹{s_bookings['Total Fee (₹)'].sum():,.2f}" if not s_bookings.empty else "₹0")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        if not v_bookings.empty:
            fig_v = px.pie(v_bookings, values="Total Cost (₹)", names="Venue Name", hole=0.4, title="<b>Venue Expenditure Share</b>")
            st.plotly_chart(fig_v, use_container_width=True)
        else:
            st.info("No venue booking data available for graphical analysis.")
    with col_b:
        if not s_bookings.empty:
            fig_s = px.bar(s_bookings, x="Speaker Name", y="Total Fee (₹)", color="Expertise Topic", title="<b>Speaker Honorarium Payouts</b>")
            st.plotly_chart(fig_s, use_container_width=True)
        else:
            st.info("No speaker booking data available for graphical analysis.")

# -------------------------------------------------------------
# MODULE 5: BOOKING LOG (WITH CSV EXPORT & RECEIPTS)
# -------------------------------------------------------------
elif menu == "📋 Booking Log":
    st.subheader("📋 Confirmed Reservations & Engagements")

    tab1, tab2 = st.tabs(["🏢 Venue Reservations", "🎤 Speaker Engagements"])
    
    with tab1:
        if not st.session_state.venue_bookings.empty:
            col_tbl, col_act = st.columns([4, 1])
            with col_tbl:
                st.dataframe(st.session_state.venue_bookings, use_container_width=True)
            with col_act:
                csv_v = st.session_state.venue_bookings.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export CSV",
                    data=csv_v,
                    file_name="venue_bookings_log.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                selected_v_id = st.selectbox("Select ID for Receipt", st.session_state.venue_bookings["Booking ID"].tolist())
                if st.button("📄 Print Receipt", key="btn_prnt_v", use_container_width=True):
                    row = st.session_state.venue_bookings[st.session_state.venue_bookings["Booking ID"] == selected_v_id].iloc[0].to_dict()
                    generate_invoice_dialog(row, "Venue")
        else:
            st.info("No venue reservations recorded yet.")
            
    with tab2:
        if not st.session_state.speaker_bookings.empty:
            col_tbl, col_act = st.columns([4, 1])
            with col_tbl:
                st.dataframe(st.session_state.speaker_bookings, use_container_width=True)
            with col_act:
                csv_s = st.session_state.speaker_bookings.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export CSV",
                    data=csv_s,
                    file_name="speaker_bookings_log.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                selected_s_id = st.selectbox("Select ID for Receipt", st.session_state.speaker_bookings["Booking ID"].tolist())
                if st.button("📄 Print Receipt", key="btn_prnt_s", use_container_width=True):
                    row = st.session_state.speaker_bookings[st.session_state.speaker_bookings["Booking ID"] == selected_s_id].iloc[0].to_dict()
                    generate_invoice_dialog(row, "Speaker")
        else:
            st.info("No speaker engagements recorded yet.")

# -------------------------------------------------------------
# MODULE 6: ADMIN CONTROL PANEL (ADD NEW VENUES / SPEAKERS)
# -------------------------------------------------------------
elif menu == "⚙️ Admin Control Panel":
    st.subheader("⚙️ Resource Management Console")
    st.caption("Add new operational resources directly into the active platform catalog.")

    adm_tab1, adm_tab2 = st.tabs(["🏢 Add New Venue", "🎤 Add New Speaker"])

    with adm_tab1:
        st.markdown("### Register New Venue Listing")
        with st.form("add_venue_form"):
            v_name = st.text_input("Venue Name", placeholder="e.g., Quantum Innovation Hall")
            v_location = st.text_input("Location / Campus Zone", placeholder="e.g., East Block - Floor 3")
            v_cap = st.number_input("Seating Capacity", min_value=10, max_value=5000, value=150)
            v_rate = st.number_input("Hourly Rate (₹)", min_value=500, max_value=100000, value=5000)
            v_tag = st.selectbox("Venue Category Tag", ["Flagship", "Popular", "Interactive", "VIP Space", "Outdoor", "Virtual-Ready", "Collaborative"])
            v_amenities_raw = st.text_input("Amenities (comma-separated)", value="📶 Wi-Fi, 🎥 Projector, ❄️ AC")
            v_image = st.text_input("Image URL (Unsplash or direct image link)", value="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400&q=80")
            v_review = st.text_input("Default Highlight Review", value="Brand new state-of-the-art facilities!")

            if st.form_submit_button("➕ Add Venue to Directory", use_container_width=True):
                if not v_name or not v_location:
                    st.error("Please fill out venue name and location.")
                else:
                    amenity_list = [a.strip() for a in v_amenities_raw.split(",")]
                    new_v = {
                        "ID": f"V{len(st.session_state.venues) + 101}",
                        "Name": v_name,
                        "Capacity": v_cap,
                        "Location": v_location,
                        "Hourly Rate (₹)": v_rate,
                        "Tag": v_tag,
                        "Amenities": amenity_list,
                        "Rating": 5.0,
                        "Top Review": v_review,
                        "Image": v_image
                    }
                    st.session_state.venues = pd.concat([st.session_state.venues, pd.DataFrame([new_v])], ignore_index=True)
                    st.toast(f"✅ {v_name} added to venues!", icon="🎉")
                    st.rerun()

    with adm_tab2:
        st.markdown("### Register New Keynote Speaker")
        with st.form("add_speaker_form"):
            s_name = st.text_input("Speaker Full Name", placeholder="e.g., Dr. Maya Lin")
            s_domain = st.text_input("Primary Domain / Expertise", placeholder="e.g., Quantum Computing")
            s_fee = st.number_input("Hourly Honorarium Fee (₹)", min_value=1000, max_value=200000, value=15000)
            s_slot = st.selectbox("Preferred Time Availability", ["Morning (9 AM - 12 PM)", "Afternoon (1 PM - 5 PM)", "Evening (5 PM - 8 PM)", "Full Day"])
            s_badges_raw = st.text_input("Badges / Distinctions (comma-separated)", value="Domain Specialist, Keynote Speaker")
            s_bio = st.text_area("Short Professional Biography", value="Industry practitioner with expertise in advanced technical topics.")
            s_photo = st.text_input("Photo URL", value="https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=300&q=80")

            if st.form_submit_button("➕ Add Speaker to Directory", use_container_width=True):
                if not s_name or not s_domain:
                    st.error("Please fill out speaker name and domain expertise.")
                else:
                    badge_list = [b.strip() for b in s_badges_raw.split(",")]
                    new_s = {
                        "ID": f"S{len(st.session_state.speakers) + 201}",
                        "Name": s_name,
                        "Expertise": s_domain,
                        "Rating": 5.0,
                        "Fee (₹/hr)": s_fee,
                        "Available Time": s_slot,
                        "Badges": badge_list,
                        "Bio": s_bio,
                        "Photo": s_photo
                    }
                    st.session_state.speakers = pd.concat([st.session_state.speakers, pd.DataFrame([new_s])], ignore_index=True)
                    st.toast(f"✅ {s_name} added to speakers!", icon="🎉")
                    st.rerun()