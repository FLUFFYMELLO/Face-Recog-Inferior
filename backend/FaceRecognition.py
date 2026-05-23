import cv2
import face_recognition
import numpy as np
import requests

# =========================
# HELPER FUNCTION
# =========================
def face_confidence(face_distance, threshold=0.6):
    range_val = (1.0 - threshold)
    linear_val = ((1.0 - face_distance) / (range_val * 2.0))
    if face_distance > threshold:
        return round(linear_val * 100, 2)
    else:
        return round(((linear_val + ((1.0 - linear_val) *
            np.power((linear_val - 0.5) * 2, 0.2)))) * 100, 2)

# =========================
# LOAD STUDENT PROFILES
# =========================
def load_profiles(api_url="http://127.0.0.1:8000/students"):
    response = requests.get(api_url, timeout=5)
    return response.json()

# =========================
# PRECOMPUTE ENCODINGS
# =========================
def compute_encodings(profiles):
    known_encodings = []
    known_profiles = []
    for profile in profiles:
        img = face_recognition.load_image_file(profile["image"])
        encoding = face_recognition.face_encodings(img)[0]
        known_encodings.append(encoding)
        known_profiles.append(profile)
    return known_encodings, known_profiles

# =========================
# MATCH FACE
# =========================
def match_face(rgb_frame, known_encodings, known_profiles, threshold=0.47):
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        return "Unknown", None

    distances = face_recognition.face_distance(known_encodings, face_encodings[0])
    best_match_index = np.argmin(distances)
    match_distance = distances[best_match_index]

    if match_distance < threshold:
        return known_profiles[best_match_index], match_distance
    else:
        return "Unknown", match_distance