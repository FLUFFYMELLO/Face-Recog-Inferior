import cv2
import face_recognition
import numpy as np
import json
import streamlit as st

# Load student profiles JSON
with open("data/studentprofiles.json") as f:
    profiles = json.load(f)

# Precompute encodings
known_encodings = []
known_profiles = []
for profile in profiles:
    img = face_recognition.load_image_file(profile["image"])
    encoding = face_recognition.face_encodings(img)[0]
    known_encodings.append(encoding)
    known_profiles.append(profile)

st.title("📸 Student Face Recognition")

camera_input = st.camera_input("Take a picture")

if camera_input:
    file_bytes = np.asarray(bytearray(camera_input.getvalue()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    st.image(rgb_frame, channels="RGB", caption="Captured Image")

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for encoding in face_encodings:
        # Compute distances
        distances = face_recognition.face_distance(known_encodings, encoding)
        best_match_index = np.argmin(distances)

        # Set stricter threshold (default is 0.6, lower = stricter)
        if distances[best_match_index] < 0.50:
            profile = known_profiles[best_match_index]

            st.image(profile["image"], caption=profile.get("Student_Name", "Unknown"))
            st.write(f"**ID:** {profile.get('Student_Id', 'N/A')}")
            st.write(f"**Course:** {profile.get('Course', 'N/A')}")
            st.write(f"**Year Level:** {profile.get('Year_level', 'N/A')}")
            st.write(f"**Records:** {profile.get('Records', 'N/A')}")
            st.success(f"{profile.get('Student_Name', 'Unknown')} recognized ✅")
        else:
            st.error("❌ Not a student")