import streamlit as st
import numpy as np
import cv2
from PIL import Image
from backend.FaceRecognition import load_profiles, compute_encodings, match_face, face_confidence

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Recognition Dashboard",
    layout="wide"
)

# =========================
# GLOBAL STYLES (BACKGROUND + UI FIX)
# =========================
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #f5f7fb;
}

/* RTU HEADER */
.rtu-header {
    background-image: url("https://images.candymag.com/candy/images/2022/11/23/applying-to-rizal-technological-university.png");
    background-size: cover;
    background-position: center;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 34px;
    font-weight: bold;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

/* Dark overlay */
.rtu-overlay {
    background-color: rgba(0,0,0,0.55);
    padding: 40px;
    border-radius: 12px;
}

/* Buttons */
.stButton button {
    background-color: #0B4DBA;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    background-color: #083b8a;
    color: white;
}

/* Hide Streamlit default UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (RTU IMAGE TITLE)
# =========================
st.markdown("""
<div class="rtu-header">
    <div class="rtu-overlay">
        RTU Student Face Recognition System
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    font-size:18px;
    font-weight:700;
    color:white;
    text-align:center;
    margin-top:10px;
    background-color:#0B4DBA;
    padding:10px;
    border-radius:8px;
">
    Rizal Technological University Security Monitoring System
</div>
""", unsafe_allow_html=True)

# =========================
# PRIVACY WARNING BANNER
# =========================
st.markdown("""
<div style="
    font-size:14px;
    font-weight:600;
    color:#e74c3c;
    text-align:left;
    margin-top:10px;
    background-color:#fff3cd;
    padding:10px;
    border-radius:10px;
    display:inline-block;
">
    ⚠️ Privacy Notice: This application uses your photo, name, and other personal information solely for face recognition and identity verification purposes. Your data will be handled securely and used only for authorized identification within the system.
</div>
""", unsafe_allow_html=True)
st.divider()

# =========================
# LOAD PROFILES + ENCODINGS
# =========================
profiles = load_profiles()
known_encodings, known_profiles = compute_encodings(profiles)

# =========================
# SESSION STATE
# =========================
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None
if "recognized_profile" not in st.session_state:
    st.session_state.recognized_profile = None
if "match_distance" not in st.session_state:
    st.session_state.match_distance = None

# =========================
# MAIN LAYOUT
# =========================
col1, col2 = st.columns([1, 1])

# ==================================================
# CAMERA SECTION
# ==================================================
with col1:
    st.markdown("""
<div style="background-color:#0B4DBA; padding:10px; border-radius:8px; text-align:center;">
    <h2 style="color:white; margin:0;">📷 Camera</h2>
</div>
""", unsafe_allow_html=True)

    if st.session_state.captured_image is None:
        camera_input = st.camera_input("Take a picture")

        if camera_input:
            file_bytes = np.asarray(bytearray(camera_input.getvalue()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            st.session_state.captured_image = rgb_frame
            profile, distance = match_face(rgb_frame, known_encodings, known_profiles)

            st.session_state.recognized_profile = profile
            st.session_state.match_distance = distance
            st.rerun()

    else:
        st.image(st.session_state.captured_image, channels="RGB", caption="Captured Image", use_container_width=True)
        st.success("✅ Photo Captured")

        if st.button("🗑️ Clear / Take Another Photo", use_container_width=True):
            st.session_state.captured_image = None
            st.session_state.recognized_profile = None
            st.session_state.match_distance = None
            st.rerun()

# ==================================================
# PROFILE SECTION
# ==================================================
with col2:
    st.markdown("""
<div style="background-color:#FFD700;
padding:10px;
border-radius:8px;
text-align:center;
">
    <h2 style="color:#2c3e50;
    margin:0;">👤 Profile Information</h2>
</div>
""", unsafe_allow_html=True)

    if st.session_state.captured_image is not None:

        if st.session_state.recognized_profile == "Unknown":
            st.markdown("""
<div style="
    background:#ffffff;
    border-radius:14px;
    box-shadow:0 8px 22px rgba(0,0,0,0.12);
    overflow:hidden;
    max-width:450px;
    margin:20px auto;
    border:1px solid rgba(0,0,0,0.06);
    text-align:center;
">
    <div style="background:#0B4DBA;
    height:12px;
    "></div>
    <div style="padding:22px 20px 26px 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/bc/Unknown_person.jpg"
             style="
                width:150px;
                height:150px;
                border-radius:50%;
                border:3px solid #ccc;
                margin-bottom:18px;
             ">
        <h2 style="
            margin:0 0 10px 0;
            font-size:24px;
            font-weight:800;
            color:#2c3e50;
        ">
            🚫 Not a student / Not registered
        </h2>
        <p style="
            margin:0;
            font-size:17px;
            color:#e74c3c;
            font-weight:500;
        ">
            ⚠️ Warning: Person not found in the university database.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

        elif st.session_state.recognized_profile:
            profile = st.session_state.recognized_profile

            st.markdown(f"""
<div style="display:flex;
align-items:center;
margin:20px 0;
">
    <span style="font-size:25px;
    font-weight:bold;
    color:#2c3e50;
    ">
        👤 {profile.get('Student_Name','Unknown')}
    </span>
    <span style="background-color:#2ecc71;
    color:white;
    padding:6px 14px;
                 border-radius:8px;
                 font-size:16px;
                 font-weight:bold;
                 margin-left:80px;
                 ">
        ✅ Identity Verified
    </span>
</div>
""", unsafe_allow_html=True)

            if st.session_state.match_distance is not None:
                confidence = face_confidence(st.session_state.match_distance)
                st.progress(int(confidence))
                st.caption(f"🔎 Match Confidence: {confidence}%")

            col_photo, col_info = st.columns([2, 2])

            with col_photo:
                try:
                    img = Image.open(profile["image"])
                    st.image(img, width=250)
                except:
                    st.image(profile["image"], width=250)

            with col_info:
                st.markdown(f"""
<div style="
    text-align:left;
    font-size:27px;
    color:#2c3e50;
    background-color:#f0f0f0;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.1);
">
    <p>🪪 <strong>ID:</strong> {profile.get('Student_Id', 'N/A')}</p>
    <p>💻 <strong>Course:</strong> {profile.get('Course', 'N/A')}</p>
    <p>🎓 <strong>Year Level:</strong> {profile.get('Year_level', 'N/A')}</p>
</div>
""", unsafe_allow_html=True)

            st.divider()

            st.markdown("""
<div style="background-color:#e74c3c;
padding:8px;
border-radius:8px;
text-align:center;
">
    <h3 style="color:white;
    margin:0;">⚠️ Violation Records</h3>
</div>
""", unsafe_allow_html=True)

            records = profile.get("Records", [])
            
            st.write("") 
            
            if isinstance(records, list) and len(records) > 0:
                for item in records:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            st.markdown(f'<div style="color: #2c3e50;">• <b>{k}:</b> {v}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color: #2c3e50;">• {item}</div>', unsafe_allow_html=True)
            elif isinstance(records, dict):
                for k, v in records.items():
                    st.markdown(f'<div style="color: #2c3e50;">• <b>{k}:</b> {v}</div>', unsafe_allow_html=True)
            elif isinstance(records, str) and records.strip():
                st.markdown(f'<div style="color: #2c3e50;">• {records}</div>', unsafe_allow_html=True)
            else:
                st.info("No records found.")