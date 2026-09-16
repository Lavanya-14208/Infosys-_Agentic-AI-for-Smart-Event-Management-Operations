import streamlit as st
import pandas as pd
import sqlite3
import datetime
import random
import io
import cv2
import numpy as np
import plotly.express as px
from fpdf import FPDF
import qrcode
from PIL import Image

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# =========================================================
# CONFIGURATION & DATABASE INITIALIZATION
# =========================================================
st.set_page_config(
    page_title="Smart Event AI Management Platform",
    page_icon="🎟️",
    layout="wide"
)

DB_FILE = "event_management.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendees (
            attendee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            industry TEXT NOT NULL,
            city TEXT NOT NULL,
            age INTEGER NOT NULL,
            checked_in INTEGER DEFAULT 0,
            checkin_time TEXT DEFAULT 'N/A',
            pin TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM attendees", conn)
    conn.close()
    return df

# =========================================================
# HELPER 1: IN-MEMORY VIP PDF BADGE GENERATOR
# =========================================================
def create_pdf_badge(attendee_id, name, industry, city, pin):
    pdf = FPDF(orientation='P', unit='mm', format=(85, 120))
    pdf.add_page()
    
    # Header Styling
    pdf.set_fill_color(30, 60, 114)
    pdf.rect(0, 0, 85, 25, 'F')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, 8)
    pdf.cell(85, 8, "VIP EVENT PASS", align='C')
    
    # Attendee Details
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(0, 32)
    pdf.cell(85, 8, name, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(0, 40)
    pdf.cell(85, 6, f"{industry} | {city}", align='C')
    
    # Generate QR Code in RAM
    qr_payload = f"VERIFY:{attendee_id}:{name}"
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(qr_payload)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    
    # Render QR Code on PDF
    pdf.image(qr_buffer, x=22, y=48, w=40, h=40, type="PNG")
    
    # Credentials & Security Footers
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(30, 60, 114)
    pdf.set_xy(0, 92)
    pdf.cell(85, 6, f"ID: {attendee_id}  |  PIN: {pin}", align='C')
    
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(120, 120, 120)
    pdf.set_xy(0, 104)
    pdf.cell(85, 5, "Please present this pass at entry terminals.", align='C')
    
    return pdf.output(dest='S').encode('latin1')

# =========================================================
# HELPER 2: AUTOMATED EMAIL SENDER WITH ATTACHMENT
# =========================================================
def send_confirmation_email(to_email, attendee_name, attendee_id, pin, pdf_bytes):
    SENDER_EMAIL = "your_event_email@gmail.com"      # Replace with your email
    SENDER_PASSWORD = "your_app_password_here"       # Replace with your App Password

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = f"🎟️ Registration Confirmed - VIP Pass for {attendee_name}"

    body = f"""Hello {attendee_name},

Thank you for registering for our event! Your registration credentials are below:

--------------------------------------------------
• Attendee ID : {attendee_id}
• Security PIN: {pin}
--------------------------------------------------

Your VIP Entry Pass is attached to this email as a PDF document.
You can present the embedded QR code or use your 4-digit PIN for express entry at the kiosk.

Best regards,
Event Operations Team
"""
    msg.attach(MIMEText(body, 'plain'))

    pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"{attendee_name.replace(' ', '_')}_VIP_Badge.pdf")
    msg.attach(pdf_attachment)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"⚠️ SMTP Email Notice: Could not dispatch email automatically. ({e})")
        return False

# =========================================================
# NAVIGATION SIDEBAR
# =========================================================
st.sidebar.title("🎪 Event Management Console")
page = st.sidebar.radio(
    "Select Module",
    [
        "📊 Organizer Dashboard",
        "🤖 Intelligent Registration Agent",
        "📸 Express Check-In Kiosk",
        "📥 System Integration (CSV Upload)",
        "⏱️ Real-Time Check-In Tracking",
        "💡 AI Registration Intelligence"
    ]
)

# =========================================================
# MODULE 1: ORGANIZER DASHBOARD
# =========================================================
if page == "📊 Organizer Dashboard":
    st.title("📊 Registration Intelligence & Executive Dashboard")
    df = get_data()
    
    total = len(df)
    checked_in = len(df[df["checked_in"] == 1])
    pending = total - checked_in
    rate = f"{(checked_in / total * 100):.1f}%" if total > 0 else "0%"
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Registrations", total)
    col2.metric("Checked-In Attendees", checked_in)
    col3.metric("Pending Check-Ins", pending)
    col4.metric("Check-In Rate", rate)
    
    st.markdown("---")
    
    if not df.empty:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Industry Breakdown")
            fig_ind = px.pie(df, names="industry", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_ind, use_container_width=True)
            
        with col_b:
            st.subheader("Demographics by City")
            fig_city = px.bar(df, x="city", color="industry", barmode="group")
            st.plotly_chart(fig_city, use_container_width=True)
    else:
        st.info("No registration records found in the database. Use Module 2 or 4 to add attendees.")

# =========================================================
# MODULE 2: INTELLIGENT REGISTRATION AGENT
# =========================================================
elif page == "🤖 Intelligent Registration Agent":
    st.title("🤖 Intelligent Registration Agent")
    st.write("Register new attendees, generate printable VIP passes, and send automated email confirmations.")

    with st.form("reg_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        industry = st.selectbox("Industry Domain", ["IT & Software", "Finance", "Healthcare", "Education", "VLSI / Embedded Systems", "Other"])
        city = st.text_input("City")
        age = st.number_input("Age", min_value=18, max_value=80, value=22)
        
        submitted = st.form_submit_button("Register Attendee & Dispatch VIP Pass")

    if submitted:
        if not name or not email:
            st.error("Please fill in required fields (Name and Email).")
        else:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            df = get_data()
            new_id = f"ATT-{len(df) + 1:03d}"
            random_pin = str(random.randint(1000, 9999))
            
            try:
                c.execute("INSERT INTO attendees VALUES (?,?,?,?,?,?,?,?,?)", 
                          (new_id, name, email, industry, city, age, 0, "N/A", random_pin))
                conn.commit()
                st.success(f"✅ Attendee {name} registered successfully! Assigned ID: {new_id} | Security PIN: {random_pin}")
                
                # Build in-memory PDF
                badge_pdf = create_pdf_badge(new_id, name, industry, city, random_pin)

                # Send Email
                with st.spinner("📧 Dispatching VIP Badge to email..."):
                    email_sent = send_confirmation_email(email, name, new_id, random_pin, badge_pdf)
                
                if email_sent:
                    st.success(f"📩 Confirmation email sent successfully to {email}!")

                st.session_state['latest_registration'] = {
                    'id': new_id,
                    'name': name,
                    'industry': industry,
                    'city': city,
                    'pin': random_pin,
                    'pdf': badge_pdf
                }
            except sqlite3.IntegrityError:
                st.error("❌ Registration Failed: An attendee with this email address is already registered.")
            finally:
                conn.close()

    if 'latest_registration' in st.session_state:
        reg = st.session_state['latest_registration']
        st.download_button(
            label=f"🎫 Download VIP Pass & Badge for {reg['name']} (PDF)",
            data=reg['pdf'],
            file_name=f"{reg['name'].replace(' ', '_')}_VIP_Badge.pdf",
            mime="application/pdf"
        )

# =========================================================
# MODULE 3: EXPRESS AI KIOSK & VERIFICATION TERMINAL
# =========================================================
elif page == "📸 Express Check-In Kiosk":
    st.title("📸 Express AI Kiosk & Verification Terminal")
    st.write("Verify passes using live camera scanning, badge image upload, or manual PIN entry.")

    tab1, tab2, tab3 = st.tabs(["📷 Scan via Camera", "📁 Upload QR Image", "🔑 Manual PIN Check-In"])

    def process_qr_payload(data):
        if not data:
            st.error("❌ No readable QR code detected. Please ensure high clarity and contrast.")
            return

        st.info(f"🔍 Scanned Payload: {data}")
        parts = data.split(":")
        
        if len(parts) >= 2 and parts[0] == "VERIFY":
            scanned_id = parts[1]
            
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT name, checked_in FROM attendees WHERE attendee_id = ?", (scanned_id,))
            row = c.fetchone()
            
            if row:
                name, checked_in = row
                if checked_in == 1:
                    st.warning(f"⚠️ {name} ({scanned_id}) is ALREADY checked in!")
                else:
                    now_str = datetime.datetime.now().strftime("%I:%M %p")
                    c.execute("UPDATE attendees SET checked_in = 1, checkin_time = ? WHERE attendee_id = ?", (now_str, scanned_id))
                    conn.commit()
                    st.balloons()
                    st.success(f"🎉 ACCESS GRANTED! Welcome, {name} ({scanned_id}). Logged entry at {now_str}.")
            else:
                st.error("❌ Invalid Pass ID! Credentials not found in database.")
            conn.close()
        else:
            st.error("❌ Unrecognized QR code format!")

    with tab1:
        st.subheader("Point Badge QR Code at Camera")
        img_file_buffer = st.camera_input("Snapshot QR Pass")

        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(cv2_img)
            process_qr_payload(data)

    with tab2:
        st.subheader("Upload VIP Badge Image File")
        uploaded_qr = st.file_uploader("Upload saved QR Pass (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

        if uploaded_qr is not None:
            bytes_data = uploaded_qr.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

            st.image(uploaded_qr, caption="Pass Preview", width=250)

            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(cv2_img)
            process_qr_payload(data)

    with tab3:
        st.subheader("Manual Kiosk Keypad")
        col_id, col_pin = st.columns(2)
        
        with col_id:
            input_id = st.text_input("Attendee ID (e.g., ATT-001)")
        with col_pin:
            input_pin = st.text_input("4-Digit Passcode PIN", type="password")

        if st.button("Verify & Grant Entry"):
            if not input_id or not input_pin:
                st.error("Please provide both Attendee ID and PIN passcode.")
            else:
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("SELECT name, pin, checked_in FROM attendees WHERE attendee_id = ?", (input_id.upper(),))
                row = c.fetchone()
                
                if row:
                    name, stored_pin, checked_in = row
                    if str(stored_pin) == str(input_pin):
                        if checked_in == 1:
                            st.warning(f"⚠️ {name} is already checked in.")
                        else:
                            now_str = datetime.datetime.now().strftime("%I:%M %p")
                            c.execute("UPDATE attendees SET checked_in = 1, checkin_time = ? WHERE attendee_id = ?", (now_str, input_id.upper()))
                            conn.commit()
                            st.balloons()
                            st.success(f"✅ ACCESS GRANTED! Welcome, {name}.")
                    else:
                        st.error("❌ Incorrect PIN passcode.")
                else:
                    st.error("❌ Attendee ID not found in database.")
                conn.close()

# =========================================================
# MODULE 4: SYSTEM INTEGRATION (CSV UPLOAD)
# =========================================================
elif page == "📥 System Integration (CSV Upload)":
    st.title("📥 System Integration & Bulk CSV Ingestion")
    st.write("Upload external attendee spreadsheets to onboard participants in bulk.")

    uploaded_file = st.file_uploader("Choose CSV File", type=["csv"])

    if uploaded_file is not None:
        try:
            df_csv = pd.read_csv(uploaded_file)
            st.subheader("📋 Spreadsheet Preview")
            st.dataframe(df_csv.head(), use_container_width=True)

            required_cols = {"Name", "Email", "Industry", "City", "Age"}
            
            if required_cols.issubset(set(df_csv.columns)):
                if st.button("🚀 Process & Ingest Into Database"):
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    
                    df_existing = get_data()
                    current_count = len(df_existing)
                    success_count = 0
                    skip_count = 0

                    for _, row in df_csv.iterrows():
                        current_count += 1
                        new_id = f"ATT-{current_count:03d}"
                        random_pin = str(random.randint(1000, 9999))
                        
                        try:
                            c.execute(
                                "INSERT INTO attendees VALUES (?,?,?,?,?,?,?,?,?)",
                                (
                                    new_id,
                                    row["Name"],
                                    row["Email"],
                                    row["Industry"],
                                    row["City"],
                                    int(row["Age"]),
                                    0,
                                    "N/A",
                                    random_pin
                                )
                            )
                            success_count += 1
                        except sqlite3.IntegrityError:
                            skip_count += 1

                    conn.commit()
                    conn.close()

                    st.success(f"✅ Ingestion Complete! Successfully registered {success_count} new attendees ({skip_count} duplicate emails skipped).")
            else:
                st.error(f"❌ Column Schema Error: CSV must contain headers: {', '.join(required_cols)}")
        
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

# =========================================================
# MODULE 5: REAL-TIME CHECK-IN TRACKING & BADGE RE-ISSUER
# =========================================================
elif page == "⏱️ Real-Time Check-In Tracking":
    st.title("⏱️ Real-Time Attendance Roster & Admin Control Panel")
    st.write("Search attendees, perform manual admin overrides, and re-issue VIP badges.")

    df = get_data()
    search_query = st.text_input("🔍 Search Attendee by Name, Email, or ID", "")
    
    if search_query:
        df_filtered = df[
            df["name"].str.contains(search_query, case=False, na=False) |
            df["email"].str.contains(search_query, case=False, na=False) |
            df["attendee_id"].str.contains(search_query, case=False, na=False)
        ]
    else:
        df_filtered = df

    st.markdown("---")

    if df_filtered.empty:
        st.info("No matching records found.")
    else:
        for idx, row in df_filtered.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                
                col1.write(f"**{row['name']}**")
                col1.caption(f"ID: {row['attendee_id']} | PIN: {row['pin']}")
                
                col2.write(f"🏢 {row['industry']}")
                col2.caption(f"📍 {row['city']}")
                
                if row['checked_in'] == 1:
                    col3.success(f"✅ Checked In\n({row['checkin_time']})")
                else:
                    col3.warning("⏳ Pending Arrival")
                    if col3.button("Manual Check-In", key=f"btn_checkin_{row['attendee_id']}"):
                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        now_str = datetime.datetime.now().strftime("%I:%M %p")
                        c.execute("UPDATE attendees SET checked_in = 1, checkin_time = ? WHERE attendee_id = ?", 
                                  (now_str, row['attendee_id']))
                        conn.commit()
                        conn.close()
                        st.rerun()

                reissue_pdf = create_pdf_badge(
                    row['attendee_id'], row['name'], row['industry'], row['city'], row['pin']
                )
                col4.download_button(
                    label="🎫 Re-issue VIP Badge",
                    data=reissue_pdf,
                    file_name=f"{row['name'].replace(' ', '_')}_VIP_Badge.pdf",
                    mime="application/pdf",
                    key=f"btn_pdf_{row['attendee_id']}"
                )
            st.divider()

# =========================================================
# MODULE 6: AI REGISTRATION INTELLIGENCE ENGINE
# =========================================================
elif page == "💡 AI Registration Intelligence":
    st.title("💡 AI Registration Intelligence & Strategic Insights")
    st.write("Automated demographic evaluations and AI recommendations based on current registrations.")

    df = get_data()

    if df.empty:
        st.warning("No registration data available for evaluation.")
    else:
        top_industry = df["industry"].mode()[0] if not df["industry"].empty else "N/A"
        top_city = df["city"].mode()[0] if not df["city"].empty else "N/A"
        avg_age = round(df["age"].mean(), 1) if not df["age"].empty else 0

        st.subheader("📊 Demographic Highlights")
        col1, col2, col3 = st.columns(3)
        col1.metric("Dominant Industry", top_industry)
        col2.metric("Top Regional Hub", top_city)
        col3.metric("Average Attendee Age", f"{avg_age} Yrs")

        st.markdown("---")
        st.subheader("🤖 Strategic AI Recommendations")

        with st.expander("📍 Venue & Logistics Insights", expanded=True):
            st.write(
                f"• **High Regional Concentration:** A significant portion of attendees are originating from **{top_city}**. "
                f"Consider organizing regional transit passes or satellite networking sessions."
            )

        with st.expander("🎯 Content & Speaker Strategy", expanded=True):
            st.write(
                f"• **Dominant Domain Focus:** **{top_industry}** represents the leading background of registered attendees. "
                f"Prioritize keynotes and technical breakout tracks focused on this sector."
            )

        with st.expander("👥 Audience Engagement Strategy", expanded=True):
            if avg_age < 30:
                st.write(
                    "• **Young Professional & Student Cohort:** The average age indicates a younger audience segment. "
                    "Incorporate interactive Q&A sessions, hackathons, and early-career networking lounges."
                )
            else:
                st.write(
                    "• **Senior & Mid-Career Cohort:** The audience consists primarily of experienced professionals. "
                    "Emphasize executive roundtables and structured B2B networking zones."
                )